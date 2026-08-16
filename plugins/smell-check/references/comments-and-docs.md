# Comments and documentation

Applies whenever writing or editing a comment, a documentation file, or any explanatory text
that lives alongside code.

### Commenting what the code already says

**The smell.** Writing a comment because the code looks bare.

**The tell.** The comment restates the line beneath it. You added it to be helpful rather than
because something was unclear. Nothing would be lost by deleting it.

**The correction.** Default to no comments. Comment only what cannot be derived from the code
itself.

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

### Treating your own output as the house style

**The smell.** Matching the surrounding code when the surrounding code is yours.

**The tell.** "I should follow the existing style of this file." Reading a convention off code
you wrote last week and treating it as a project decision. Telling a subagent to match the
style of the codebase, which hands your own habit to something that cannot tell the difference.
This one feels like diligence, because matching the surrounding code is normally correct.

**The correction.** Check who wrote what you are matching. Where a convention traces back to
your own earlier output, it is not a convention: it is your default, and copying it again
doubles it. This compounds fastest with comments, which is why a codebase can reach three lines
of comment for every line of code without anyone choosing that. Follow conventions that came
from a person, and take the rules in this file from the file rather than from the neighbors.

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
