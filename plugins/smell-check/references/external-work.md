# Waiting on external work

Applies when something is running outside the session — a build, a deploy, a queued job.

The first two entries come from the same gap: no plan for how long the wait should take. One
never checks again, the other checks constantly.

### Waiting silently on a watch that may never finish

**The smell.** Trusting a completion notice to arrive.

**The tell.** Starting a long-running watch command in the background and then stopping, with
nothing to fall back on. These notices have a habit of never firing, and the turn is left with
no way out.

**The correction.** Bound every backgrounded watch with an explicit timeout, set a little past
the expected duration. The test for any waiting mechanism: it ends on its own on every path —
finished, failed, or stuck. A wait that can only end because the user speaks up is armed
wrong, whatever tool it is built from.

### Polling status in a tight loop

**The smell.** Checking repeatedly because there is nothing else to do.

**The tell.** Re-running a status check every few seconds. Each one costs tokens and none of
them change anything.

**The correction.** When the work has a roughly known duration, schedule a single wakeup near
the expected finish and check once.

### Declaring done while the work can still come back

**The smell.** Measuring "done" against your own finish line instead of the point where
nothing can bounce back to you.

**The tell.** Saying "done" or "handing off" while a check that could fail — CI, a deploy, a
required review — is still pending, especially with "if it fails I can pick it up" in the same
breath. A command still running as you announce nothing is left. Needing to requalify what
"done" meant when the user pushes on it.

**The correction.** There is one useful meaning of done: nothing pending can return the work
to you. If a result could still fail and the fix would be yours, you are not done — you are
waiting; say "waiting on X" and name what happens on each outcome. And once you do say done,
stop. Any command you still feel like running is evidence the claim was early.
