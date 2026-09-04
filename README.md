# smell-check

A catalogue of the recurring ways language models and agents fail at software engineering,
and the corrections for them.

A **smell** here is not a defect in the code being written. It is a defect in how the model
approaches the work. These failures do not feel like failures from the inside; they feel like
efficiency, like helpfulness, like getting to the point. Naming them is most of the fix.

The catalogue is a set of rules, one bullet each, grouped by the kind of work they apply to:
the workflow around a change, evidence for a claim, replies to the user, comments and durable
artifacts, and code. Every rule was written from observed behavior, not from guesses about how
models might go wrong.

## Install

```
claude plugin marketplace add brhelwig/smell-check
claude plugin install smell-check@smell-check
```

## Loading the catalogue

The catalogue is about 2,800 words (16,000 characters, roughly 4,000 tokens). A quick question
is usually cheaper answered without it; a longer implementation session is where loading it earns
back its own cost.

The catalogue arrives when a session invokes `using-smell-check`. Two ways to make that happen.

Name it in your project or user `CLAUDE.md`. It survives plugin updates, and it is the way to
say how seriously you want the catalogue taken:

```markdown
## Smell check

Before starting any software task — writing or changing code, debugging, reviewing, planning
work, or answering a question about a codebase — invoke the `smell-check:using-smell-check`
skill and read it in full.

Apply its corrections zealously. Each one works at the moment of the action it names: before
the claim, before the comment, before the reply. Nothing later catches what this pass lets
through, so there is no second gate to leave it for. Where a correction and your own instinct
disagree, the correction wins.

Invoke it again at a stage boundary in a long session, once the catalogue has fallen behind the
work.
```

Zealous means applying every correction that fits, not forcing the work to fit one. The
catalogue's own `When a smell does not apply` still governs: a tell that does not match your
situation is not a smell, and deciding an entry does not apply is a correct outcome rather than
a way out.

Or invoke `/smell-check:using-smell-check` yourself, when a task is big enough to be worth the
context.

Skills also load on demand, so the entry point may pull itself in when a task looks like it
matters. That is unreliable by design and not something to depend on.

Invoking `/smell-check:using-smell-check` again mid-session puts the whole
catalogue back in front of the model. Worth doing at a stage boundary in a long
session, when the catalogue has fallen a long way behind the work.

Earlier versions shipped hooks that nudged every session to load the catalogue and reminded the
model about branches before its first edit. Both are gone. The `SessionStart` hook could not
carry the catalogue itself — Claude Code spills oversized hook output to a file — so it only
asked the session to load the skill, which `CLAUDE.md` does more simply and more durably. The
`PreToolUse` hook was redundant: the catalogue's own entries produce the same branching
behaviour without it, and its command filter matched `2>/dev/null`, so a read-only command
usually spent the one reminder it was allowed to give.

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

Rules live in `plugins/smell-check/skills/using-smell-check/SKILL.md`, one bullet each, under
the section for the kind of work they show up in. Adding one means adding a bullet to that file:
no manifest change, no new skill.

A rule earns its place when a model can notice the moment it applies and the instruction is
specific enough to act on. Write the rule as an imperative sentence, add a trigger clause only
where the rule needs one, and keep the reasoning out unless the rule is counterintuitive. Before
adding a bullet, check whether an existing one already says it; the cost of the catalogue is paid
on every load.

Keep tool names out of it. Where a rule depends on the tracker, the branching model, or how
tests are run, read it from preferences instead. Those genuinely vary per project, which the
opinions do not.

## Benchmark

`evals/` holds a benchmark that runs the catalogue against Opus 5 on four small tasks, in three
arms: the catalogue on `main`, the catalogue in the working tree, and no catalogue. It measures
task completion, files touched outside the task, comment lines added, reply length, filler
phrases, and token cost. See `evals/README.md` to run it. A pull request that changes the
catalogue carries the resulting table.

## License

MIT
