# Twelve-factor services

Applies when writing or changing something that runs as a long-lived service: anything
deployed, scaled, or restarted by something other than a person at a terminal.

It does not apply to scripts, command-line tools, notebooks, build steps, or anything that runs
once and exits on a machine someone is sitting at. Reaching for these corrections there
produces ceremony, not portability.

Each entry below is a shortcut that makes the immediate task work and costs the service
somewhere it cannot be seen yet: on the second instance, the next deploy, the first restart.
That is what makes them smells rather than mistakes. Every one of them is locally reasonable.

### Hardcoding what varies between deploys

**The smell.** Writing the value in, because you have it and the code needs to run.

**The tell.** A host name, port, bucket, queue name, credential, feature flag, or timeout
written as a literal. "I'll put the default here and it can be overridden later." Naming a
constant `DEFAULT_` and treating that as the override story.

**The correction.** Anything that differs between one deploy and another comes from the
environment, with no default that silently works in production. A missing required value should
stop the process at startup and name what is missing, rather than falling back to the
developer's machine.

### Keeping state where the process can see it

**The smell.** Storing something in memory or on local disk because that is the shortest path
to persistence.

**The tell.** A module-level dictionary, a cache written to a temp directory, an uploaded file
saved next to the code, a counter that increments across requests. "This only needs to survive
between requests."

**The correction.** Treat the filesystem and process memory as a scratchpad that vanishes
without warning, because it does. Anything that must outlive a single request goes to a backing
service. Two instances of the process must be able to serve the same user without either
knowing the other exists.

### Special-casing a backing service instead of attaching it

**The smell.** Writing the local database, cache, or queue in as a fixture of the code.

**The tell.** A connection helper that knows it is talking to localhost. Branching on whether
this is "the real" service. A distinction in code between a service you run and a third-party
one.

**The correction.** Every backing service is an attached resource reached through a URL from
config. Swapping a local instance for a managed one is a config change, never a code change,
and the code should not be able to tell which it got.

### Using what happens to be installed

**The smell.** Calling something available on the machine you are on.

**The tell.** Shelling out to a tool that was not declared. Importing a library that is present
because something else pulled it in. Assuming a system package, a language runtime already on
the path, or a global that was installed by hand.

**The correction.** Declare every dependency explicitly, and isolate them so the declaration is
the only source. If the code needs it, the manifest says so and the version is pinned. If it is
not in the manifest, assume it is not there.

### Substituting a lighter backing service in development

**The smell.** Swapping in something simpler so the setup stays easy.

**The tell.** SQLite standing in for Postgres, an in-memory queue for the real broker, a local
directory for object storage. "It is the same interface." The differences that matter are the
ones the interface hides.

**The correction.** Run the same backing services in development as in production. Where the
gap is unavoidable, say which behaviors are not covered locally, such as transaction semantics,
concurrency, ordering, and failure modes, rather than letting the substitution imply a parity it
does not have.

### Writing logs to files

**The smell.** Treating logs as something the application manages.

**The tell.** A log file path in config. Rotation, retention, or cleanup logic. A directory that
has to exist before startup. Deciding where logs live at all.

**The correction.** Write to standard output as an unbuffered stream of events and stop there.
Routing, retention, and search belong to whatever runs the process. An application that manages
its own log files has taken on a job that does not survive being run twice on one host.

### Running one-off work inside the running application

**The smell.** Putting a migration, backfill, or repair where the code already runs.

**The tell.** Schema changes at startup. An admin endpoint that triggers a data fix. A flag that
makes the service do something else this once. It is where the database connection already is,
so it is the shortest path.

**The correction.** One-off work runs as a one-off process against the same code and the same
config, invoked separately. Startup does not mutate anything the service depends on being
correct. With several instances starting at once that is a race, and the one that loses
corrupts what the others are reading.

### Startup with no shutdown

**The smell.** Writing the path in and not the path out.

**The tell.** Connections opened, threads spawned, work claimed from a queue, with no handling
of a termination signal. Restarting is something you do by killing it. "It will be fine, the
work is quick."

**The correction.** Shut down cleanly on the signal the platform sends: stop accepting new work,
finish or return what is in flight, release what was claimed. Processes are killed constantly
and without notice, by deploys, by autoscaling, by the host going away, so a clean exit is a
normal path and not an error path.
