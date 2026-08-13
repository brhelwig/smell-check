---
name: using-smell-check
description: Use at the start of any software task - names the recurring ways language models and agents fail at engineering work, and directs you to the skill that corrects each one
---

## What a smell is

A **smell** is a recurring way a language model fails at software work. Not a defect in the
code being written — a defect in how the model approaches the work.

Every smell in this catalogue has the same shape:

- **The smell** — the failure, named.
- **The tell** — what you notice yourself thinking or doing just before you commit it.
- **The correction** — what to do instead.

The tell is the important part. These failures do not feel like failures from the inside.
They feel like efficiency, like helpfulness, like getting to the point. That is why naming
them is worth a skill.

## The rule

Before acting on a request, check the available skills for `smell-check:*` entries and load
any whose description matches what you are about to do. Follow its correction.

When you load one, say which and why in a single short sentence. Do not narrate the catalogue
itself.

One skill load costs a tool call. An unexamined assumption shipped into a user's codebase
costs them a debugging session, and costs more still when it reaches a persistent artifact
that later sessions read as established fact.

## Closing out

Loading a skill up front lowers the odds of a smell; it does not remove them. At the end of a
piece of work, before handing it off or committing, run `/smell-check:review` to audit what
was actually produced against the catalogue.

## When a smell does not apply

This catalogue describes tendencies, not laws. A tell that does not match your actual
situation is not a smell — do not contort the work to fit one. Loading a skill and concluding
it does not apply is a correct outcome, and cheaper than the alternative.

## Preferences

This plugin ships no opinion about which tools an adopter uses. Anything tool-specific — the
issue tracker, the branching model, the review process, the language conventions — lives in a
preferences file that the adopter writes, never in a skill.

Two locations, both optional:

| Scope | Path | Applies to |
| :-- | :-- | :-- |
| Project | `.claude/smell-check/preferences.md` | Everyone working in that repository |
| User | `~/.claude/smell-check/preferences.md` | Every project on that machine |

Read the project file at the start of a task when it exists; it is the one that carries team
conventions. Fall back to the user file when there is no project file. When both exist, the
project file wins on any point where they disagree.

If neither exists and a task turns on a preference you do not have — which tracker to file
against, whether to open a change request — ask rather than guessing, and offer
`/smell-check:setup` to record the answer.

## Precedence

Direct instructions from the user outrank preferences. Preferences outrank this catalogue.
The catalogue outranks your defaults. Follow a smell's correction unless something above it
in that order says otherwise.
