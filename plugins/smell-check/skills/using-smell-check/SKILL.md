---
name: using-smell-check
description: Use at the start of any software task - loads the full catalogue of recurring ways language models and agents fail at engineering work, and the correction for each
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

Entries live in `${CLAUDE_PLUGIN_ROOT}/references/`. This file is only the index — the
catalogue is those files, and loading this skill is not finished until you have read all of
them. Read every file in that directory now, in parallel, before taking any other action:

- `communication.md`
- `plain-language.md`
- `evidence.md`
- `starting-work.md`
- `comments-and-docs.md`
- `changing-existing-code.md`
- `acting-without-asking.md`
- `sensitive-data.md`
- `external-work.md`
- `twelve-factor.md`

Read the whole directory, not just this list — a file present there but missing here is new,
not optional. Do not sample the ones that seem relevant: a skipped file is a set of smells you
will not notice yourself committing, and deciding relevance before reading is itself the
failure this catalogue exists to name.

Do not narrate the catalogue. Follow the corrections and say what you are doing.

## This pass is the enforcement

The corrections apply while the work happens, at the moment of the action they describe:
before the claim is asserted, before the comment is written, before the reply is sent. There
is no later pass that catches what this one lets through.

`/smell-check:review` exists, but it is the user's tool, invoked by them when they want a second
opinion and not otherwise. Do not run it on yourself, do not offer it at the end of a task, and
do not treat it as the gate that this pass is a draft for. Work as though it will never be run,
because usually it will not be.

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
