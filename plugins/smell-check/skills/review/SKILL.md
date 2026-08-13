---
name: review
description: Use at the end of a piece of work, before handing it off or committing - audits what was actually produced against the smell catalogue and cleans up what got through
argument-hint: [path or diff range]
---

Audit the work just produced against the catalogue. Not the codebase, and not the code's
correctness — the specific ways this change may have gone wrong because a language model made
it.

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

## Load the catalogue

The checks come from `${CLAUDE_PLUGIN_ROOT}/references/`. Read the files there and let their
entries be the checklist.

The catalogue is the only source for what counts as a smell. Do not supplement it with
failures you think are worth checking — an invented check is an opinion presented as a
standard, and the whole point of the catalogue is that its entries were observed rather than
imagined.

If `references/` is empty or absent, say so and stop. A review with no catalogue behind it has
nothing to check against.

## Check

Work through every entry that could apply to this change. For each, use the entry's own tell
as the thing you are looking for — the tell is written to be recognizable from the inside, and
it is what makes the check work on your own output.

For every finding, quote the file and line rather than describing it.

## Report

Group findings by catalogue entry, most consequential first. For each: the file and line, what
is wrong in one sentence, and the fix.

State which entries came back clean, briefly. A review that only lists problems gives no signal
about coverage.

If nothing was found, say so plainly. Do not manufacture a finding to justify the review.

## Fix

Present the findings and confirm before changing anything — the user may want only some of
them, and a review that edits unprompted is making its own scope decisions.

On confirmation, apply the fixes and nothing else. Anything you notice along the way that is
outside the findings gets mentioned, not fixed.
