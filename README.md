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

## Install

```
claude plugin marketplace add brhelwig/smell-check
claude plugin install smell-check@smell-check
```

## Loading the catalogue

Skills load on demand: Claude pulls one in when its description matches the work. That is the
default and it costs nothing until it fires.

The entry point, `using-smell-check`, is different — it is what tells the model the catalogue
exists and when to reach for it. There are three ways to get it in front of the model, in
increasing order of cost.

**Do nothing.** The entry point may still load on its own when a task looks like it matters.
Unreliable by design; fine if you want to try the skills individually first.

**Reference it from `CLAUDE.md`** — recommended. Add one line to your project or user
`CLAUDE.md`:

```markdown
At the start of any software task, use the `smell-check:using-smell-check` skill.
```

This survives plugin updates, works in every project you add it to, and costs one line of
context.

**Turn on autoload.** The plugin ships a `SessionStart` hook, off by default. Enable it in
`/plugin` by setting **Load at session start**, or set `autoload` to `true` under this
plugin's entry in `pluginConfigs` in `~/.claude/settings.json`. The hook then injects the
entry point into every session — including sessions where you only wanted to ask a quick
question, which is the cost to weigh.

You do not need more than one of these.

## Checking the work afterwards

Loading the catalogue up front lowers the odds of a smell. It does not remove them — the
failures are called smells precisely because they do not feel like failures while they are
happening.

`/smell-check:review` is the backstop. Run it at the end of a piece of work, before you commit
or hand it off, and it audits what was actually produced:

```
/smell-check:review
/smell-check:review src/auth
/smell-check:review main..HEAD
```

It reads the diff rather than trusting its own account of what it did, which is the whole
point — the context that produced the slop is the same one that already judged it acceptable.
Its checklist is the catalogue itself, so it stays in step as entries are added and never
invents a check of its own. It reports first and asks before changing anything.

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
