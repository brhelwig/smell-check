#!/usr/bin/env python3
"""Run the catalogue benchmark: each task under each arm, one headless Claude Code session per run.

Usage:
    python3 evals/run.py --arms old,new,none --runs 1 --model claude-opus-5 --out /tmp/smell-bench

Arms:
    old   the catalogue at --old-ref (default origin/main), loaded with --plugin-dir
    new   the catalogue in this working tree, loaded with --plugin-dir
    none  no catalogue and no instruction to load one
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EVALS = Path(__file__).resolve().parent
PLUGIN_SUBDIR = Path("plugins/smell-check")

LOAD_INSTRUCTION = """## Smell check

Before starting any software task - writing or changing code, debugging, reviewing, planning
work, or answering a question about a codebase - invoke the `smell-check:using-smell-check`
skill and read it in full.

Apply its corrections zealously. Each one works at the moment of the action it names: before
the claim, before the comment, before the reply. Nothing later catches what this pass lets
through, so there is no second gate to leave it for. Where a correction and your own instinct
disagree, the correction wins.
"""

PHRASES = [
    "great question",
    "honestly",
    "you're absolutely right",
    "you are absolutely right",
    "good catch",
    "fair point",
    "want me to",
    "say the word",
    "if you'd like",
    "if you want",
    "i can also",
    "happy to",
    "let me know",
    "worth noting",
    "worth mentioning",
    "keep in mind",
    "under the hood",
    "leverage",
    "robust",
    "spike",
    "unlock",
    "surface",
    "delve",
    "seamless",
    "note:",
]


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--arms", default="old,new,none")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--model", default="claude-opus-5")
    parser.add_argument("--out", required=True)
    parser.add_argument("--tasks", default="", help="comma-separated task names; default all")
    parser.add_argument("--old-ref", default="origin/main")
    parser.add_argument("--max-turns", type=int, default=30)
    parser.add_argument("--max-budget-usd", default="3")
    parser.add_argument("--timeout", type=int, default=900, help="seconds per run")
    parser.add_argument("--workers", type=int, default=3)
    return parser.parse_args()


def export_old_plugin(ref, out):
    target = out / "old-plugin"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    archive = subprocess.run(
        ["git", "archive", ref, str(PLUGIN_SUBDIR)],
        cwd=REPO, check=True, capture_output=True,
    ).stdout
    tar_path = target / "plugin.tar"
    tar_path.write_bytes(archive)
    with tarfile.open(tar_path) as tar:
        tar.extractall(target, filter="data")
    tar_path.unlink()
    return target / PLUGIN_SUBDIR


def plugin_dir_for(arm, old_ref, out):
    if arm == "old":
        return export_old_plugin(old_ref, out)
    if arm == "new":
        return REPO / PLUGIN_SUBDIR
    return None


def git(cwd, *args):
    return subprocess.run(
        ["git", "-c", "user.name=Fixture Author", "-c", "user.email=fixture@example.com", *args],
        cwd=cwd, check=True, capture_output=True, text=True,
    ).stdout


def prepare_fixture(fixture, workdir):
    shutil.copytree(EVALS / "fixtures" / fixture, workdir, dirs_exist_ok=True)
    git(workdir, "init", "-q")
    git(workdir, "add", "-A")
    git(workdir, "commit", "-q", "-m", "Fixture")
    return git(workdir, "rev-parse", "HEAD").strip()


def claude_command(prompt, model, plugin_dir, max_turns, max_budget):
    cmd = [
        "claude", "-p", prompt,
        "--model", model,
        "--output-format", "stream-json",
        "--verbose",
        "--permission-mode", "acceptEdits",
        "--setting-sources", "project",
        "--no-session-persistence",
        "--max-turns", str(max_turns),
        "--max-budget-usd", str(max_budget),
        "--allowedTools", "Bash(python3 *)", "Bash(python *)", "Bash(git *)",
    ]
    if plugin_dir is not None:
        cmd += ["--plugin-dir", str(plugin_dir), "--append-system-prompt", LOAD_INSTRUCTION]
    return cmd


def parse_stream(lines):
    result = None
    tool_calls = {}
    skill_loaded = False
    assistant_text = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = event.get("type")
        if kind == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    name = block.get("name", "")
                    tool_calls[name] = tool_calls.get(name, 0) + 1
                    target = json.dumps(block.get("input", {}))
                    if "using-smell-check" in target:
                        skill_loaded = True
                elif block.get("type") == "text":
                    assistant_text.append(block.get("text", ""))
        elif kind == "result":
            result = event
    return result, tool_calls, skill_loaded, assistant_text


def comment_lines_added(diff_text):
    count = 0
    for line in diff_text.splitlines():
        if line.startswith("+++") or not line.startswith("+"):
            continue
        body = line[1:].strip()
        if body.startswith("#") and not body.startswith("#!"):
            count += 1
    return count


def untracked_diff(workdir, untracked):
    chunks = []
    for rel in untracked:
        path = workdir / rel
        if path.is_file():
            text = path.read_text(errors="replace")
            chunks.append("+++ " + rel + "\n" + "\n".join("+" + l for l in text.splitlines()) + "\n")
    return "".join(chunks)


def measure_reply(reply):
    lower = reply.lower()
    hits = {p: lower.count(p) for p in PHRASES if lower.count(p)}
    return {
        "reply_chars": len(reply),
        "reply_words": len(reply.split()),
        "headings": len(re.findall(r"^#+ ", reply, flags=re.M)),
        "bullets": len(re.findall(r"^\s*[-*] ", reply, flags=re.M)),
        "em_dashes": reply.count("—"),
        "phrase_hits": sum(hits.values()),
        "phrases": hits,
    }


def run_check(task, workdir, reply):
    if "check" in task:
        proc = subprocess.run(["bash", "-c", task["check"]], cwd=workdir, capture_output=True, text=True)
        return proc.returncode == 0
    if "reply_contains_all" in task:
        lower = reply.lower()
        return all(term.lower() in lower for term in task["reply_contains_all"])
    return None


def run_once(task, arm, run_number, args, plugin_dir, out):
    run_dir = out / task["name"] / arm / f"run-{run_number}"
    run_dir.mkdir(parents=True, exist_ok=True)
    workdir = Path(tempfile.mkdtemp(prefix=f"smell-{task['name']}-{arm}-"))
    base = prepare_fixture(TASKS["fixture"], workdir)

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    cmd = claude_command(task["prompt"], args.model, plugin_dir, args.max_turns, args.max_budget_usd)
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=workdir, env=env, capture_output=True, text=True, timeout=args.timeout)
        stdout, stderr, timed_out = proc.stdout, proc.stderr, False
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        timed_out = True
    wall = time.time() - started

    (run_dir / "stream.jsonl").write_text(stdout)
    if stderr:
        (run_dir / "stderr.txt").write_text(stderr)

    result, tool_calls, skill_loaded, assistant_text = parse_stream(stdout.splitlines())
    reply = (result or {}).get("result") or (assistant_text[-1] if assistant_text else "")
    (run_dir / "reply.md").write_text(reply)

    status = git(workdir, "status", "--porcelain")
    untracked = [line[3:].strip() for line in status.splitlines() if line.startswith("??")]
    tracked = git(workdir, "diff", "--name-only", base).splitlines()
    changed = sorted(f for f in set(tracked) | set(untracked) if "__pycache__" not in f)
    diff = git(workdir, "diff", base) + untracked_diff(workdir, untracked)
    (run_dir / "diff.patch").write_text(diff)

    expected = set(task["expected_files"])
    usage = (result or {}).get("usage", {})
    metrics = {
        "task": task["name"],
        "arm": arm,
        "run": run_number,
        "model": args.model,
        "skill_loaded": skill_loaded,
        "completed": run_check(task, workdir, reply),
        "files_changed": changed,
        "files_outside_expected": sorted(set(changed) - expected),
        "diff_lines_added": sum(1 for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")),
        "comment_lines_added": comment_lines_added(diff),
        "tool_calls": tool_calls,
        "edit_calls": tool_calls.get("Edit", 0) + tool_calls.get("Write", 0) + tool_calls.get("MultiEdit", 0),
        "turns": (result or {}).get("num_turns"),
        "context_tokens": sum(usage.get(k, 0) or 0 for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")),
        "output_tokens": usage.get("output_tokens"),
        "cost_usd": (result or {}).get("total_cost_usd"),
        "duration_s": round(((result or {}).get("duration_ms") or wall * 1000) / 1000, 1),
        "timed_out": timed_out,
        "is_error": (result or {}).get("is_error", result is None),
        **measure_reply(reply),
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    shutil.rmtree(workdir, ignore_errors=True)
    flag = "ok" if metrics["completed"] else "incomplete"
    print(f"{task['name']:18} {arm:5} run-{run_number}: {flag}, skill_loaded={skill_loaded}, "
          f"files={len(changed)}, reply={metrics['reply_chars']}c, cost=${metrics['cost_usd']}", flush=True)
    return metrics


def main():
    args = parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    wanted = {t.strip() for t in args.tasks.split(",") if t.strip()}
    tasks = [t for t in TASKS["tasks"] if not wanted or t["name"] in wanted]
    plugin_dirs = {arm: plugin_dir_for(arm, args.old_ref, out) for arm in arms}

    jobs = [(task, arm, n) for task in tasks for arm in arms for n in range(1, args.runs + 1)]
    print(f"{len(jobs)} runs on {args.model}, {args.workers} at a time, output in {out}", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_once, task, arm, n, args, plugin_dirs[arm], out) for task, arm, n in jobs]
        results = [f.result() for f in futures]
    (out / "results.json").write_text(json.dumps(results, indent=2))
    print(f"wrote {out / 'results.json'}")


TASKS = json.loads((EVALS / "tasks.json").read_text())

if __name__ == "__main__":
    sys.exit(main())
