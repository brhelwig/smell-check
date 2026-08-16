# smell-check

A catalogue of the recurring ways language models and agents fail at software engineering,
and the corrections for them.

A **smell** here is not a defect in the code being written. It is a defect in how the model
approaches the work. These failures do not feel like failures from the inside — they feel like
efficiency, like helpfulness, like getting to the point. Naming them is most of the fix.

Every entry in the catalogue has the same three parts:

- **The smell** — the failure, named.
- **The tell** — what the model notices itself thinking just before committing it.
- **The correction** — what to do instead.

Entries are written from observed behavior, not from guesses about how models might go wrong.

One file is not a set of smells. `plain-language.md` carries a writing standard, taken from the
ASD-STE100 Simplified Technical English rules, that several corrections elsewhere assume.

## Install

```
claude plugin marketplace add brhelwig/smell-check
claude plugin install smell-check@smell-check
```

## Loading the catalogue

Installing is all it takes. The plugin ships a `SessionStart` hook that injects the entry point,
`using-smell-check`, into every session, and it is on by default. A catalogue nobody loaded
corrects nothing, and the sessions where it goes unloaded are exactly the ones where nobody
stopped to think about how the work might go wrong.

The cost is context in every session, including the ones where you only wanted to ask a quick
question. To turn it off, clear **Load at session start** in `/plugin`, or set `autoload` to
`false` under this plugin's entry in `pluginConfigs` in `~/.claude/settings.json`.

With autoload off, two things still reach the catalogue. Skills load on demand, so the entry
point may pull itself in when a task looks like it matters, which is unreliable by design. Or
name it in your project or user `CLAUDE.md`, which costs one line and survives plugin updates:

```markdown
At the start of any software task, use the `smell-check:using-smell-check` skill.
```

Either way, invoking `/smell-check:using-smell-check` again mid-session re-reads the reference
files and puts them back in front of the model. Worth doing at a stage boundary in a long
session, when the catalogue has fallen a long way behind the work.

## Checking the work afterwards

Loading the catalogue up front lowers the odds of a smell. It does not remove them — the
failures are called smells precisely because they do not feel like failures while they are
happening.

Following the catalogue while the work happens is the enforcement. `/smell-check:review` is not
a second gate that the first pass can lean on, and the entry point tells the model to work as
though review will never run, because usually it will not.

It is yours to invoke. The skill sets `disable-model-invocation: true`, so the model cannot
decide to run it, cannot offer it at the end of a task, and cannot treat it as a reason to be
loose earlier.

```
/smell-check:review
/smell-check:review src/auth
/smell-check:review main..HEAD
```

The audit runs in a separate agent, `smell-reviewer`. The skill launches it with the diff range
and nothing else: no summary of the work, no account of what was being attempted, no
explanation of why anything was written that way. That distance is the point. Every choice in
the diff already survived its author's judgment once, so re-applying the same judgment returns
the same verdict, and a fresh agent has made no commitments to the code and gains nothing by
defending it.

The agent has no editing tools. Its only checklist is the catalogue, so it stays in step as
entries are added and never invents a check of its own. It reports, and the session that
called it applies whichever findings you pick.

## Preferences

The catalogue ships no opinion about which tools you use. It has to work the same whether you
track work in GitHub, Linear, Jira, or a text file, so anything tool-specific lives in a
preferences file you write — never in a skill.

Run `/smell-check:setup` to create one. It inspects the repository, asks only what it cannot
determine, and writes:

| Scope | Path | Applies to |
| :-- | :-- | :-- |
| Project | `.claude/smell-check/preferences.md` | Everyone working in that repository. Commit it. |
| User | `~/.claude/smell-check/preferences.md` | Every project on that machine. |

Both are optional. When both exist, the project file wins wherever they disagree. Direct
instructions from you outrank both.

Preferences record decisions, not discussion — which tracker, how branches are named, what
command runs the tests, what counts as done, how terse you want the replies.

## Adding a smell

Entries live in `plugins/smell-check/references/`, grouped by the kind of work they show up in.
Adding one means editing a markdown file — no manifest change, no new skill.

An entry earns its place when the tell is something a model can actually notice about itself
and the correction is specific enough to act on. A tell that only a human reviewer could spot
does not work, because the catalogue is read by the thing being corrected.

Keep tool names out of it. Where a correction depends on the tracker, the branching model, or
how tests are run, read it from preferences instead — those genuinely vary per project, which
the opinions do not.

## License

MIT
