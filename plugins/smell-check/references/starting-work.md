# Starting work

Applies before the first edit, when establishing where the work happens and where the thinking
is written down.

### Working in the main checkout, or on the default branch

**The smell.** Editing where the session happened to open.

**The tell.** Starting to change files before establishing where you are. Assuming the current
directory is the right place because nothing said otherwise.

**The correction.** Code work happens in a separate working copy, never the main checkout and
never on the default branch. Confirm you are actually in one before doing anything else —
check, do not assume. Prefer a tool that creates and cleans up the working copy over doing it
by hand, since it handles placement and removal.

### Writing specs and plans into the repository

**The smell.** Creating a file to hold the thinking.

**The tell.** Starting a plan or design document as a file in the repository. Following a skill
that says to write the plan to a file, without asking where plans belong here.

**The correction.** Specs and plans belong in the tracker the adopter uses, on the item itself,
edited in place as they change. Never as files committed to the repository — committed plan
files pollute the context of every later read, and go stale without anyone noticing.

This overrides any plugin or skill that instructs otherwise.
