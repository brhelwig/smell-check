# Comments and documentation

Applies whenever writing or editing a comment, a documentation file, or any explanatory text
that lives alongside code.

A comment is the last resort, reached only after naming and structure have failed. Well-named
variables, functions, and types carry the meaning; a comment is what you write when the meaning
genuinely cannot be expressed in code, which is rare. Write none by default, and treat every
one you do write as needing a case.

### Commenting what the code already says

**The smell.** Writing a comment because the code looks bare.

**The tell.** The comment restates the line beneath it. You added it to be helpful rather than
because something was unclear. Nothing would be lost by deleting it.

**The correction.** Delete it. Bare code is the goal, not a gap to fill.

### Commenting instead of naming

**The smell.** Explaining in prose what a name could have carried.

**The tell.** The comment defines the thing under it — what a variable holds, what a block is
for, what a magic number means. Writing it feels like clarifying, and the sentence usually
contains the better name.

**The correction.** Spend the comment on the identifier instead. Rename the variable, extract
the block into a named function, promote the constant. Reach for a comment only once naming
and structure have both been tried and the meaning still will not fit in code.

### Explaining what rather than why

**The smell.** The comment narrates mechanics that the code already shows.

**The tell.** The comment could be reconstructed by reading the line under it. It describes
the steps rather than the reason the steps are that way.

**The correction.** A comment explains why. If it restates the code, delete it — do not reword
it.

### Writing the comment as a record of the change

**The smell.** Commenting for the reviewer of this diff instead of the next reader of the file.

**The tell.** "Now uses." "Changed to." "Previously." "This used to." Any phrasing that implies
a before.

**The correction.** Write for the merged end state. Whoever opens the file later has no idea
there was a change. History lives in version control, which is where it should stay.

### Fixing only the lines you touched

**The smell.** Leaving a violation alone because it was not in scope.

**The tell.** Noticing a comment two lines up that breaks these rules and stepping over it,
because fixing it would widen the change.

**The correction.** When editing a file, fix comment violations across the whole file, not only
the lines being touched.

### Flagging stale documentation instead of resolving it

**The smell.** Marking a problem and treating that as handling it.

**The tell.** Adding "this may be out of date" or "note: possibly stale" next to something you
know is wrong.

**The correction.** Revise it or delete it. Never merely flag it.

### The same explanation in more than one place

**The smell.** Repeating an explanation because it is relevant in two spots.

**The tell.** Copying a comment or a paragraph rather than moving it, because extracting it
would mean touching more files.

**The correction.** Duplication is evidence the explanation sits in the wrong place. Extract it
to one place, even when that makes the change reach further. Not repeating yourself applies
continuously, not only when it is convenient.
