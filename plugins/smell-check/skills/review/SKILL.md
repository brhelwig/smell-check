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

## Be hard on it

The user asked for this review because they want the work doubted. Skepticism toward your own
output is the service being requested — it is not rudeness, not pessimism, and not a failure
to be helpful.

Read the change the way someone would who expects to find something wrong with it and is not
invested in the answer. When you are unsure whether something counts, say it and let the user
decide. A finding raised and dismissed costs a sentence. A finding softened into nothing
reaches their codebase.

The pull toward the opposite is strong and it feels like professionalism:

| The thought | What it actually is |
| :-- | :-- |
| "This is fine, it follows the pattern" | You have not checked that the pattern is right here |
| "Close enough" | A judgment you are making on the user's behalf |
| "I would have caught that earlier" | You are the one who wrote it |
| "Mentioning this seems pedantic" | Their standard, not yours, decides what is pedantic |
| "The change works, so it is done" | Working is one entry in the catalogue, not all of them |
| "Flagging my own work looks bad" | Not flagging it is what looks bad, later |

Handing work along as good enough is the failure this skill exists to prevent. Being hard on
it is cheap by comparison.

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

That said, an empty report is the outcome to be most suspicious of. Before giving one, check
that you actually read the diff rather than a summary of it, and that you went through every
catalogue entry that could apply rather than the ones that came to mind.

## Fix

Present the findings and confirm before changing anything — the user may want only some of
them, and a review that edits unprompted is making its own scope decisions.

On confirmation, apply the fixes and nothing else. Anything you notice along the way that is
outside the findings gets mentioned, not fixed.
