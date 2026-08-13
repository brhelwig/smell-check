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

## The catalogue

Entries live in `${CLAUDE_PLUGIN_ROOT}/references/`. Read the file that matches what you are
about to do.

| File | Read it when |
| :-- | :-- |
| `communication.md` | Writing any response. Applies to everything, not only code. |
| `evidence.md` | Stating something as fact, explaining a cause, or finishing a plan. |
| `starting-work.md` | Before the first edit — where the work happens, where the plan is written. |
| `comments-and-docs.md` | Writing or editing a comment or documentation. |
| `changing-existing-code.md` | Replacing, extending, or migrating something that exists. |
| `acting-without-asking.md` | About to spend or change something the user did not authorize. |
| `external-work.md` | Waiting on a build, a deploy, or a queued job. |

`communication.md` and `evidence.md` apply to nearly every task. The rest are situational.

Reading a file costs one tool call. An unexamined assumption shipped into a codebase costs a
debugging session, and costs more still once it reaches somewhere durable that later sessions
read as established fact.

Do not narrate the catalogue. Follow the correction and say what you are doing.

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
