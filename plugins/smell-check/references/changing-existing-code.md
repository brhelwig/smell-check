# Changing existing code

Applies when replacing, extending, or migrating something that already exists.

The first three entries are the same reluctance to touch what is already written. The last is
the opposite, and it is worth knowing that both failures live here.

### Leaving behind what the change replaced

**The smell.** Stopping once the new path works.

**The tell.** The old function, branch, config key, or file is still there, because removing
it felt like a separate task.

**The correction.** Finish the change: delete whatever it replaced. A half-migration is worse
than either end state, because both now exist and neither is authoritative.

### Adding a compatibility layer nobody asked for

**The smell.** Keeping the old way working alongside the new one, to be safe.

**The tell.** Preserving an interface because something might still call it, without checking
whether anything does.

**The correction.** Default to the clean break. A compatibility layer commits someone to
maintaining two things, so it has to be asked for rather than assumed.

### Bolting a new variant beside the old one

**The smell.** Writing a second thing that nearly duplicates the first.

**The tell.** Creating a parallel function, class, or file because changing the original would
reach into more places.

**The correction.** Consolidate. Two near-copies is the cost, not the saving.

### Renaming what already had a name

**The smell.** Improving an identifier you were not asked to touch.

**The tell.** A variable, function, or file gets a clearer name while you are in the file for
something else. The new name is genuinely better, which is why it does not feel like a change.

**The correction.** Leave names alone unless renaming is the task, or the code you are adding
cannot work with the old name. A rename touches every call site, buries the real change in the
diff, and breaks the reader's search for a term they knew. Say what you would rename and let
the user decide.
