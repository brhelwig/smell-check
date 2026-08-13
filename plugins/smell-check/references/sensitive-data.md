# Sensitive data

Applies when writing anything that persists — a commit message, a change request, a comment,
a file.

### Private detail written into a lasting artifact

**The smell.** Including a specific because it is accurate.

**The tell.** Naming a customer, quoting an exact record count, pasting a user identifier, or
citing a business detail in a commit message, a change request title or description, or a code
comment. Precision feels like rigor, and the detail was right there in the terminal.

**The correction.** Keep private detail out of anything that persists. Use general terms —
"large volume", not the number. These artifacts outlive the task and are read by people who
were never meant to see the specifics.

### Storing a secret

**The smell.** Putting a credential somewhere so the work can continue.

**The tell.** Writing a key, token, or password into a file, even briefly, even in a file that
will not be committed.

**The correction.** Refuse. Do not store an uncommitted secret. Suggest an encrypted secrets
tool such as SOPS instead, and let the user place it.
