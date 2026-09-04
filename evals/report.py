#!/usr/bin/env python3
"""Render results from evals/run.py as markdown tables.

Usage:
    python3 evals/report.py /tmp/smell-bench
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

COLUMNS = [
    ("completed", "Completed", lambda v: f"{v:.0%}"),
    ("skill_loaded", "Skill loaded", lambda v: f"{v:.0%}"),
    ("files_outside_expected", "Extra files", lambda v: f"{v:.1f}"),
    ("comment_lines_added", "Comment lines", lambda v: f"{v:.1f}"),
    ("diff_lines_added", "Lines added", lambda v: f"{v:.0f}"),
    ("reply_chars", "Reply chars", lambda v: f"{v:.0f}"),
    ("headings", "Headings", lambda v: f"{v:.1f}"),
    ("phrase_hits", "Phrase hits", lambda v: f"{v:.1f}"),
    ("em_dashes", "Em dashes", lambda v: f"{v:.1f}"),
    ("turns", "Turns", lambda v: f"{v:.0f}"),
    ("context_tokens", "Context tokens", lambda v: f"{v:,.0f}"),
    ("cost_usd", "Cost USD", lambda v: f"{v:.2f}"),
    ("duration_s", "Seconds", lambda v: f"{v:.0f}"),
]


def numeric(metrics, key):
    value = metrics.get(key)
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, list):
        return float(len(value))
    if value is None:
        return 0.0
    return float(value)


def mean(values):
    return sum(values) / len(values) if values else 0.0


def table(rows_by_arm, arms):
    lines = ["| Metric | " + " | ".join(arms) + " |", "| :-- | " + " | ".join("--:" for _ in arms) + " |"]
    for key, label, fmt in COLUMNS:
        cells = [fmt(mean([numeric(m, key) for m in rows_by_arm[arm]])) for arm in arms]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    out = Path(sys.argv[1])
    results = json.loads((out / "results.json").read_text())
    for m in results:
        for key in ("files_changed", "files_outside_expected"):
            m[key] = [f for f in m[key] if "__pycache__" not in f]
    arms = []
    for m in results:
        if m["arm"] not in arms:
            arms.append(m["arm"])

    by_arm = defaultdict(list)
    by_task_arm = defaultdict(lambda: defaultdict(list))
    for m in results:
        by_arm[m["arm"]].append(m)
        by_task_arm[m["task"]][m["arm"]].append(m)

    runs = max(len(rows[arm]) for rows in by_task_arm.values() for arm in rows)
    print(f"## All tasks (mean over {runs} run(s) per task, model {results[0]['model']})\n")
    print(table(by_arm, arms))
    for task, rows in by_task_arm.items():
        print(f"\n## {task}\n")
        print(table(rows, arms))
        for arm in arms:
            for m in rows[arm]:
                extra = ", ".join(m["files_outside_expected"]) or "none"
                phrases = ", ".join(f"{k} x{v}" for k, v in m["phrases"].items()) or "none"
                print(f"\n- {arm} run-{m['run']}: files changed {m['files_changed']}; extra: {extra}; phrases: {phrases}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
