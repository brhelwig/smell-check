---
name: review
description: Audits a finished change against the smell catalogue in a separate agent. Invoke this only when the user asks for it by name.
argument-hint: [path or diff range]
disable-model-invocation: true
---

Hand the change to the `smell-reviewer` agent and relay what it finds.

This runs when the user asks for it and at no other time. It is not a step in your workflow,
not a gate before committing, and not something to offer at the end of a task. The catalogue
is meant to be followed while the work happens; this is the user's second opinion on whether it
was, taken when they want one.

## Scope the review

`$ARGUMENTS` may name a path or a diff range. When it does not, the scope is the working tree
against the last commit, including untracked files.

Resolve the scope before launching — the agent starts with no knowledge of this session, so it
needs to be told what to look at rather than left to infer it.

## Launch the agent

Launch `smell-reviewer` with the scope you resolved. Pass what it cannot see for itself: the
diff range or paths, and the repository root.

Pass no summary of the work, no account of what you were trying to do, and no explanation of
why anything was written the way it was. Its distance from that reasoning is the reason the
review happens in a separate agent, and briefing it away is the one thing that would waste the
call.

Do not review the change yourself while waiting, and do not pre-filter what you send. Deciding
in advance which parts are worth looking at is the same judgment that produced the work.

## Relay the findings

Report what the agent returned. Do not soften a finding because you disagree with it, and do
not drop one because you remember a reason it is fine — the user asked for the audit, and an
edited audit is not one. Where you think a finding is wrong, say so alongside it and let them
decide.

## Fix on request

Present the findings and stop. Apply fixes only when the user says which ones, and apply
nothing else — anything you notice along the way gets mentioned, not fixed.
