# WhiteRabbot

Telegram bot for shift rescheduling

## Development

If you want to install the requirements in the virtual environment,
`requirements-freeze.txt` contains a known-good combination of requirement
versions.

    pip install -r requirements-freeze.txt

If you want to pull in updates, use

    pip install -r requirements.txt

instead.

## Roadmap

### The data/ORM layer

This layer limits the data to states that are possible.

First, handle only today, and return a Shift object.

* What shift is now?
* What shift is there at time X today?
* What shift is there at or after time X?

Then extend this to arbitrary days (daily recurrence rules). More complicated
recurrence can wait.

* What shift is there at datetime X?

Then introduce the notion of people, and a shift being covered.

* Who is covering shift X? => regular person
s Who is covering shift X? => nobody
* Who is covering shift X? => Oskar

Next, introduce the notion of Mutations.

* Who is covering shift X? => default person
* Add a mutation to shift X saying it's empty. Now who is covering it?
* Add a mutation to shift X saying Oskar takes it. Now who is covering it?
* Add a mutation to shift X saying it's empty again. Now who?
* Add a mutation to shift Y saying Wimpje takes it. Now who is covering X? Y?


### The API layer

This layer limits the user to operations and queries that are allowed, and that
leave the data in states that are allowed.

At this point we'll probably introduce the notions of a requesting User (who
must match the Person who currently owns the task) and a Schedule (N Users
belong to one Schedule, they can retrieve Shifts from that Schedule,
Modifications must pertain to users and shifts from that Schedule)


### The Telegram interface layer

This layer is a UI for Telegram users, and uses operations from the API layer.

Because of the sequential nature of Telegram interaction, this layer is going
to be a bit of state machine, I expect.

Take Telegram input; do things like

* nothing
* reply to the user
* call one of the API layer operations
* change state
* some combination of the above

This will need tables such as the TelegramUser (distinct from the user), the TelegramGroup.
