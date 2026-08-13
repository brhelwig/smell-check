# Changing existing code

Applies when replacing, extending, or migrating something that already exists.

All three entries here are the same reluctance to touch what is already written.

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
