---
name: setup
description: Use when adopting smell-check in a project or on a machine, or when the user asks to change how it works - interviews the user and writes a preferences file
argument-hint: [project|user]
---

Write a preferences file that records how this team or this person works, so no skill in the
catalogue has to assume a particular tool.

## Choose the scope

`$ARGUMENTS` may name the scope. When it does not, ask.

| Scope | Writes to | Choose when |
| :-- | :-- | :-- |
| Project | `.claude/smell-check/preferences.md` | The answers are team conventions and belong in version control |
| User | `~/.claude/smell-check/preferences.md` | The answers are personal and apply across every project |

If a file already exists at the chosen path, read it first and treat this as an edit. Show
what you intend to change and confirm before overwriting. Never discard an existing answer
because the interview did not cover it.

## Interview

Ask only what you cannot already determine, and check before asking. Inspect the repository
first: the remote, the existing branches, a `CONTRIBUTING` file, the test and build
configuration, and any CI definitions. Then confirm what you found rather than asking cold.

Cover these areas. Skip any the user has no opinion on — an absent section is better than a
guessed one.

**Tracking.** Where work is tracked, if anywhere. What a tracked item is called there. Whether
a task should begin by finding or filing one. Where specifications and plans belong. Treat
every tracker as equally valid; do not steer toward one.

**Version control.** Whether work happens on a branch, and how branches are named. Whether
isolated working copies are expected. What the default branch is called. Whether commits are
squashed on merge, which determines whether rationale survives in history or has to live in
the change request.

**Review.** Whether changes go through a change request before merging. Which tool hosts the
review, which is not always where the code lives. How a link to one change's review page is
formed there, so that every reference to a change can carry it. Who reviews. Whether the model
may merge, or must stop and hand off.

**Verification.** How to run the tests, the linter, the type checker, and the build. What
counts as done. Whether a claim of success requires having run something.

**Communication.** Preferred length and directness. Terms to avoid. How much to explain
before acting.

**Model budget.** Whether search and exploration subagents should run on a cheaper model than
the parent. Whether routine work — merge conflicts, log reading, renames — should hand off to a
cheaper tier, and how to offer that.

**Disclosure.** Which org or owner counts as the same team, so work discussed freely inside it
stays generic — no project name, cost, or branch — when written to a repository outside it.

## Write the file

Produce markdown under the headings above, keeping only the sections that got answers. Record
decisions, not discussion:

```markdown
# smell-check preferences

## Tracking

Work is tracked in <tool>. Each item is called a <term>. Start a task by locating the
relevant item; file a new one when none exists. Specifications and plans belong on the item
itself, not in files committed to the repository.

## Review

Changes are reviewed in <tool>. A change's review page is at <link pattern>. Cite that link
whenever you name the change. <who> reviews. Do not merge; hand off after the review passes.

## Verification

Tests: `<command>`. Lint: `<command>`. A change is done when both pass.

## Model budget

Explore and search subagents run on haiku. Plan subagents run on sonnet.
Use the parent's model only for a subagent that must decide something.

## Disclosure

Repositories under `<org>` share context freely. Anything written to a repository under
another owner is generic about what the agent is working on.
```

Write in plain declarative sentences addressed to whoever reads the file next, human or
model. Do not include reasoning, alternatives considered, or dates.

For project scope, tell the user the file should be committed so their team gets the same
behavior.

## After writing

Report the path and summarize what was recorded in two or three lines. If an area was left
out because the user had no preference, say which — a gap the user knows about is a decision,
and a gap they do not know about is a surprise later.
