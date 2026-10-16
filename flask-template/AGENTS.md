> **NOTE**: This `AGENTS.md`, and the project's own `README.md` once one is written,
> **must be updated whenever the code changes in a way that affects them** —
> new routes, new env vars, new conventions, new commands, structural changes
> to `src/`. Stale docs are worse than no docs: update this file in the same
> change that makes it inaccurate, don't defer it.

# AGENTS.md

This file provides guidance to AI Agents when working with code in this repository.

## Project state

This directory is a **template**, not a live application. It is copied
as-is into new projects by the `flask-project-template` generator (see the
repository root, one level up) when someone runs the generator's Docker
entrypoint. Nothing here has product-specific
requirements yet: routes, business rules, and data models are placeholders
meant to be filled in per project. Treat any change made here as a change to
the *starting point* every future project inherits, not to a single app.

## Stack

- **Flask** (app-factory pattern) as the web framework.
- **flask-jwt-extended** for JWT authentication.
- **flask-cors** for CORS.
- **SQLAlchemy** (plain engine/session, no ORM models and no
  Flask-SQLAlchemy/Alembic wired in) for relational database access,
  optionally including MSSQL via ODBC (`pyodbc` + the `msodbcsql17` driver).
  MSSQL support is chosen at generation time: the MSSQL-only parts of
  `Dockerfile` and `.env.example` sit between `# >>> mssql` / `# <<< mssql`
  markers, and the generator either strips the markers (opt-in) or deletes
  the whole block (opt-out). Keep any new MSSQL-only lines inside those
  markers.
- **python-dotenv** to load `.env` in development.
- **gunicorn** as the production WSGI server.
- **pytest** for testing.

## Structure

```
flask-template/
├── main.py                 # dev entrypoint: runs src.app:app with the Flask dev server
├── pytest.ini
├── requirements-dev.txt    # test-only deps (pytest); kept out of the prod image
├── .env.example
├── Dockerfile               # production image: installs requirements.txt, runs gunicorn on :8000
├── docker-compose.yml
├── src/
│   ├── app.py               # create_app() factory; module-level `app` for gunicorn (src.app:app)
│   ├── config.py            # Config (env-driven) and TestConfig
│   ├── extensions.py        # shared cors/jwt instances, initialized in create_app()
│   ├── errors.py            # JSON error handlers (HTTPException + generic Exception)
│   ├── routes/               # blueprints (request/response + URL rules only)
│   │   └── health/           # example: GET /health
│   ├── controllers/          # business logic called by routes (currently empty)
│   ├── db/                   # SQLAlchemy engine/session helper (init_engine, get_session)
│   ├── schemas/               # request/response validation and, eventually, ORM models (currently empty)
│   ├── middlewares/           # before/after_request hooks, decorators (currently empty)
│   └── classes/                # shared domain/utility classes (currently empty)
└── tests/                     # mirrors src/ layout (e.g. tests/routes/ for src/routes/)
    └── conftest.py             # app/client fixtures, built via create_app(TestConfig)
```

Every package under `src/` and `tests/` has an `__init__.py` with a
docstring explaining what belongs in that layer — read it before adding a
file to a folder you haven't touched before.

## Coding conventions

- **2-space indentation** throughout (Python included) — this is a hard
  requirement for this repo, not the PEP 8 default.
- **Layering is intentional**: routes stay thin (request/response only) and
  delegate to `controllers/`; data access goes through `db/` or `schemas/`;
  shared cross-cutting code goes in `classes/`. Don't put business logic
  directly in a blueprint handler.
- **Docstrings on `__init__.py`, not inline comments.** Package purpose is
  documented once at the top of the package; avoid restating it in
  individual files.
- `__init__.py` docstrings and all other prose in this template are written
  in **English**.
- No ORM models or migrations are set up. If a project needs them, that's a
  deliberate addition (e.g. Flask-SQLAlchemy + Flask-Migrate), not something
  assumed to already exist.

## Useful commands

Run all commands from inside `flask-template/`.

```sh
# install
pip install -r requirements.txt

# run (dev)
python main.py

# run (prod-like, via Docker)
docker compose up --build

# tests
pip install -r requirements-dev.txt
pytest
pytest tests/routes/test_health.py   # single file
pytest -k test_health_returns_ok     # single test by name
```

`requirements.txt` is not committed in this directory — it is generated at
scaffold time by the generator (`pip freeze > requirements.txt`) based on
what's installed in the generator's container. When adding a new runtime
dependency to the template, it must be added to the generator's own
`Dockerfile` (`pip install ...` line), not to a `requirements.txt` here.

## Environment

Configuration is read from `.env` (see `.env.example`) via `src/config.py`:

| Variable         | Purpose                                                              |
| ---------------- | --------------------------------------------------------------------- |
| `DEBUG_MODE`     | Enables Flask debug mode (`True`/`False`).                            |
| `ALLOWED_HOSTS`  | CORS allowed origins.                                                 |
| `JWT_SECRET_KEY` | Secret key for Flask-JWT-Extended.                                    |
| `DATABASE_URL`   | SQLAlchemy connection string. Leave empty to skip DB initialization.  |

Tests never read `.env` — they use `TestConfig` (empty `DATABASE_URL`, fixed
`JWT_SECRET_KEY`) via the `app`/`client` fixtures in `tests/conftest.py`.

## Pre-production checklist

Before a project generated from this template goes to production:

- [ ] Set a strong, unique `JWT_SECRET_KEY` (the default is `"change-me"`).
- [ ] Set `DEBUG_MODE=False`.
- [ ] Restrict `ALLOWED_HOSTS` to the actual frontend origin(s) instead of `*`.
- [ ] Set a real `DATABASE_URL` if the project uses a database, and confirm
      connectivity/driver setup (ODBC driver version, network access) in the
      target environment.
- [ ] Review `src/errors.py` — the generic exception handler currently
      returns a static message and logs via `app.logger`; confirm logging is
      actually wired to somewhere durable (not just stdout) in production.
- [ ] Fill in real authentication/authorization checks — `flask-jwt-extended`
      is initialized but no route enforces `@jwt_required()` yet.
- [ ] Replace or extend the `GET /health` route if the platform expects a
      specific health-check contract (status codes, payload shape).
- [ ] Pin dependency versions in `requirements.txt` (avoid re-running
      `pip freeze` against an unpinned environment right before deploying).
- [ ] If the project was generated with MSSQL support, confirm it's actually
      needed; if the project doesn't talk to MSSQL, remove the ODBC layer
      from the Dockerfile and `pyodbc` from `requirements.txt` to reduce
      image size and build time.
- [ ] Run `pytest` and make sure test coverage reflects the business logic
      actually added to `controllers/`, `schemas/`, etc.
