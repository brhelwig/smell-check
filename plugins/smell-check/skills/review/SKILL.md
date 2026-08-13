---
name: review
description: Use at the end of a piece of work, before handing it off or committing - audits what was actually produced against the smell catalogue and cleans up what got through
argument-hint: [path or diff range]
---

Audit the work just produced. Not the codebase, and not the code's correctness — the specific
ways this change may have gone wrong because a language model made it.

You are reviewing your own output. That is the difficulty: every choice here already survived
your judgment once, so re-applying the same judgment returns the same verdict. The way through
is to stop consulting your memory of what you did and read what is actually on disk.

## Establish ground truth first

Before evaluating anything, get the real change in front of you.

1. Get the diff. Use `$ARGUMENTS` when given; otherwise diff the working tree against the last
   commit, and include untracked files — new files are where unrequested work hides.
2. List every file touched, and note any you cannot explain by pointing to something the user
   asked for.
3. Read the preferences file if one exists, project scope first. It defines what done means
   here.

Do not skip to the checks with a summary of the diff in mind. Read it.

## Checks

Work through each. For every finding, quote the file and line rather than describing it.

**Claims with nothing behind them.** Find every assertion made about this work — that tests
pass, that a command succeeds, that a bug is fixed. For each, identify the command that
produced that evidence. If no command ran, the claim is unsupported. Either run it now or
withdraw the claim. This is the highest-value check on the list; do it first.

**Invented surfaces.** Every function, method, flag, config key, environment variable, and
import introduced or referenced. Confirm each exists — in the codebase, or in the dependency's
actual documentation. Plausible is not the same as real, and a name that follows the local
convention perfectly is exactly the kind that gets fabricated.

**Scope drift.** Anything in the diff nobody asked for: an extra feature, a refactor taken in
passing, reformatting of untouched lines, a dependency added for convenience. Each one is
either the user's decision to make or noise in their review.

**Scope shortfall.** The opposite, and the one more likely to be missed. Re-read the original
request and enumerate its parts. Which were completed, which were partially done, which were
quietly dropped because they were harder than the rest? A dropped part the user does not know
about is the failure; a dropped part you name is a decision.

**Half-migrations.** Where something was replaced, confirm the thing it replaced is gone —
old function, old branch of a conditional, old config key, old file. A compatibility shim left
behind without being asked for is the same finding.

**Rewrites in place of edits.** Files replaced wholesale where a targeted change was called
for, and unrelated churn riding along in the diff.

**Leftover scaffolding.** Debug output, commented-out code, temporary files, placeholder
values, `TODO` markers added during this work.

**Comments that carry no information.** Comments restating what the line does, comments
narrating the change rather than the end state — anything phrased as "now uses", "changed
to", "previously". Whoever reads the file later has no idea there was a before.

**Speculation written as fact.** Statements committed to durable places — commit messages,
change request descriptions, issue comments, documentation — that assert a cause or a
capability nobody verified. These are the most expensive findings, because later sessions read
them as established.

## Report

Group findings by check, most consequential first. For each: the file and line, what is wrong
in one sentence, and the fix.

State the checks that came back clean, briefly. A review that only lists problems gives no
signal about coverage.

If nothing was found, say so plainly. Do not manufacture a finding to justify the review.

## Fix

Present the findings and confirm before changing anything — the user may want some of it, and
a review that edits unprompted commits the scope-drift smell it was checking for.

On confirmation, apply the fixes and nothing else. Anything you notice along the way that is
outside the findings gets mentioned, not fixed.
