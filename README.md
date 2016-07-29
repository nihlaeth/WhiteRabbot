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

First, handle standalone Shift objects.

- [x]  when does it start?
- [x]  when does it stop?
- [x]  is it active at time X?

Then introduce the notion of people, and a shift being covered.

- [x]  Who is covering shift X? => regular person
- [x]  Who is covering shift X? => nobody
- [x]  Who is covering shift X? => Oskar

Next, introduce the notion of Mutations.

- [ ]  Who is covering shift X? => default person
- [ ]  Add a mutation to shift X saying it's empty. Now who is covering it?
- [ ]  Add a mutation to shift X saying Oskar takes it. Now who is covering it?
- [ ]  Add a mutation to shift X saying it's empty again. Now who?
- [ ]  Add a mutation to shift Y saying Wimpje takes it. Now who is covering X? Y?

Now, let's introduce recurrence rules.

- [ ]  Return None if there isn't a shift at time T
- [ ]  Return a shift if there is one
- [ ]  What is the next shift at or after time T?
- [ ]  What is the next shift at or before time T?
- [ ]  May I have a list of shifts between T1 and T2?

A bunch of recurrence rules together form a Schedule.

- [ ]  What shift is now?
- [ ]  What shift is there at time X today?
- [ ]  What shift is there at or after time X?


### The API layer

This layer limits the user to operations and queries that are allowed, and that
leave the data in states that are allowed.

At this point we'll probably introduce the notions of a requesting User (who
must match the Person who currently owns the task) and link the Schedule to the
Shifts. (N Users belong to one Schedule, they can retrieve Shifts from that
Schedule, Modifications must pertain to users and shifts from that Schedule.)


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


## Some sketches

### The real life situation

    zorggroep 1<--->1 Telegram groep N<--->N Telegram users
        1
        |
        1
    Schedule  1<---> Potential shifts (weekday, name)
        1
        |
        N
    Mutation N<--->1/0 Telegram user

### The database table

    Schedule          N<--->N Telegram users
    - Telegram group          - name
        1                     - telegram_user_id
        |                  /
        N           ______/
    Mutation N     /     |
    - mutator     1      /
    - new cover null or 1
    - shift (somehow, data model to be determined)
