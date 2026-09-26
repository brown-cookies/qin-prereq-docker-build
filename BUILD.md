# Section 7 — the build

A short brief, not a tutorial. Once your prediction sheet is filled in and section 7 is
ticked, this is what closes it.

## What you are building

A small program that stores short notes and lists them back, split into two Compose services:
your program, and a PostgreSQL database it talks to. You containerise both yourself, from an
empty directory, in a repository of your own.

## The interface

This much is fixed, and it is fixed so your submission can be checked by running it rather than
by reading it:

- The Compose file declares two services, named `app` and `db`.
- `db` is `postgres:18`.
- The app answers on host port `8080`.
- `POST /events` with a JSON body `{"note": "<text>"}` stores one event and returns `201` with
  a JSON body `{"id": <integer>, "note": "<text>"}`.
- `GET /events` returns `200` with a JSON array of every stored event, in the order they were
  stored, each one `{"id": <integer>, "note": "<text>"}`; an empty array `[]` when there are
  none yet.
- A `POST` whose body is not JSON, or has no `note` key, or whose `note` is empty, not a
  string, or longer than 200 characters, returns `400`.
- In PostgreSQL, the role, the database, and the table are all named `events`. The table has at
  least an integer `id` assigned by the database itself, and a text `note`.
- The database's data lives on a named volume.
- The repository holds `app.py`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`,
  `.dockerignore`, and `NOTES.md` at its root. Nothing else is required.

## The domain rules

A note is text and is never empty; the longest one allowed is 200 characters. An id, once
assigned, is never reused, and the database is the thing assigning it — your program does not
invent one. Events are never edited or deleted once stored; the only operations are adding one
and listing all of them. Whatever is stored before you run `docker compose down` is still
there, unchanged, the next time you run `docker compose up`.

## What you need

`psycopg`, pinned to a specific version in `requirements.txt`, and the standard library's
`http.server`. Nothing else is needed to meet the interface above.

## What you are not doing

No tests. No web framework — `http.server` is sufficient and the point of the exercise is what
sits underneath it, not on top of it. Nothing from this programme's later sections belongs
here either: no orchestration beyond what Compose itself gives you, and nothing you would only
reach for at a scale this build does not have.

## How this is marked

You are told this up front because it is not a trick: your submission is marked by cloning it
and running it. Four things are looked at.

- After a one-line change to `app.py`, the rebuild is timed, and the step that installs your
  dependencies has to come from the build cache rather than run again.
- The app has to answer a request made to the host on port `8080`.
- The rows your app stores have to actually be found inside the `db` service's own database.
- The rows have to still be there after `docker compose down` followed by `docker compose up`.

That is everything that is looked at. There is no fifth thing, no hidden threshold, and no
partial credit for effort that does not show up in one of the four. Aim at the brief above, not
at this list.

## The two conditions

The same two conditions as every build in this programme:

- Build it from an empty directory.
- Do not follow any single tutorial end to end.

## How long this should take

A weekend at most. If it is taking longer, cut back to the interface above and say so on
Discord rather than pushing on quietly.

## Delivery

A new repository of your own — not this material repository — with the build on a feature
branch, delivered as a pull request. Put the pull request link in your section 7 completion
update on Discord, and bring it to your session. The repository's root holds exactly the
layout given in the interface above.

## `NOTES.md`

Three short paragraphs, one each on: your Dockerfile (what gets copied when, and why you
ordered it that way); your Compose file (how your app finds the database, and what waits for
what before either starts serving); and anything you could not get working. Treat this file as
the fourth column of your prediction sheet, written in prose instead of a table — an honest
account of what you did and did not manage, not a sales pitch for the code.

One more thing belongs in it, or in your Compose file's comments: the database password you
use here is a local, throwaway one, invented for this build alone. Do not reuse a password
from anywhere else, in this file or any other you commit.

## What to submit

A pull request, from a feature branch, in a new repository of your own, the same way as
earlier sections. Put the link in your section 7 completion update on Discord, and bring it to
your session.

## This is not the capstone

The capstone at the end of your checklist is also called "the build." It is a separate, larger
project, built later, using more of what this programme covers than this section does.
Finishing this does not shorten the capstone, and the capstone does not depend on anything here
beyond the habit of containerising something real from an empty directory.
