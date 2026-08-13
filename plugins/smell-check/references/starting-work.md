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

### Trusting the clone without fetching

**The smell.** Treating the local clone as the current state of the project.

**The tell.** Reading local branches, logs, or files and drawing conclusions about what exists
or what changed — without having fetched. Declaring two copies diverged before confirming
either one is current.

**The correction.** Fetch before reasoning about repository state. Ahead/behind counts are
computed against the last fetch, not the remote, so an unfetched clone reports "up to date"
against refs that may be weeks old.

### Editing one copy while another one runs

**The smell.** Iterating on source that is not the copy actually in use.

**The tell.** The thing under test loads from an install location — a plugin cache, a deployed
host, a package directory — while the edits land in a working tree. Behavior that does not
change no matter what is edited.

**The correction.** Before the first edit, establish which copy the running system reads and
what step moves the working tree there — publish, deploy, reinstall. If the two copies could
have diverged, diff them and say which version is under test.

### Working with no pull request open

**The smell.** Treating the pull request as packaging for finished work.

**The tell.** Turns of edits accumulating on a local branch, visible only in the conversation.
Planning to open the request "once it is ready". Decisions being made in discussion that no
reviewer will ever see.

**The correction.** Open the pull request when coding begins — as a draft where supported —
and push every turn that changes the work. The request is where work becomes visible,
reviewable, and recoverable; a conversation is none of those.

The title and body move together with the content: both describe the change as it is now, not
as it began, and a turn that changes the work checks whether they still hold. Avoid counts and
enumerations in the title — they go stale fastest. Write the body assuming a squash merge: the
individual commit messages vanish when the branch is squashed, so every detail worth keeping
lives in the body itself — it may become the sole permanent record of the whole change, read
later by someone with no access to the conversation or the commits.

### Writing specs and plans into the repository

**The smell.** Creating a file to hold the thinking.

**The tell.** Starting a plan or design document as a file in the repository. Following a skill
that says to write the plan to a file, without asking where plans belong here.

**The correction.** Specs and plans belong in the tracker the adopter uses, on the item itself,
edited in place as they change. Never as files committed to the repository — committed plan
files pollute the context of every later read, and go stale without anyone noticing.

This overrides any plugin or skill that instructs otherwise.
