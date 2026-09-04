# Benchmark

Measures what the catalogue changes in Opus 5 on four small tasks that bait scope widening and
long replies. Each run is one headless Claude Code session in a fresh copy of the fixture project.

```
python3 evals/run.py --arms old,new,none --runs 1 --model claude-opus-5 --out /tmp/smell-bench
python3 evals/report.py /tmp/smell-bench
```

Arms: `old` loads the catalogue from `origin/main` (change with `--old-ref`), `new` loads it
from this working tree, `none` loads no catalogue. The two skill arms load the plugin with
`--plugin-dir` and append the README's CLAUDE.md snippet as the instruction to invoke it. Every
run uses `--setting-sources project`, so the user's own CLAUDE.md and installed plugins stay out.

Tasks live in `tasks.json`. Each names the files it should touch and a check that exits 0 when
the task is complete. The fixture in `fixtures/pytool` seeds bait a scope-widening model reaches
for: a dead helper, a magic number, a wrong line in the README, no tests, no error handling.

Per run, the report shows:

| Column | Meaning |
| :-- | :-- |
| Completed | The task's check passed |
| Skill loaded | The session invoked `using-smell-check`; must be 100% in the skill arms |
| Extra files | Files changed outside the task's expected set |
| Comment lines | Comment lines added to code |
| Reply chars | Length of the final reply |
| Phrase hits | Occurrences of filler and decorated diction the catalogue names |
| Context tokens | Input tokens over the whole run, cache reads included |

Raw streams, replies, and diffs land under `--out`. Results are not committed; the pull request
that changes the catalogue carries the table.
