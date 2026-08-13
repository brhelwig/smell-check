# Waiting on external work

Applies when something is running outside the session — a build, a deploy, a queued job.

Both entries here come from the same gap: no plan for how long the wait should take. One never
checks again, the other checks constantly.

### Waiting silently on a watch that may never finish

**The smell.** Trusting a completion notice to arrive.

**The tell.** Starting a long-running watch command in the background and then stopping, with
nothing to fall back on. These notices have a habit of never firing, and the turn is left with
no way out.

**The correction.** Bound every backgrounded watch with an explicit timeout, set a little past
the expected duration.

### Polling status in a tight loop

**The smell.** Checking repeatedly because there is nothing else to do.

**The tell.** Re-running a status check every few seconds. Each one costs tokens and none of
them change anything.

**The correction.** When the work has a roughly known duration, schedule a single wakeup near
the expected finish and check once.
