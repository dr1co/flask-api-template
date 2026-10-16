# Flask Project Template

A Flask project generator. This repository is not a Flask application itself:
it is a tool (packaged as a Docker image) that creates a new Flask project
from a ready-made template, with a layered structure, JWT authentication,
CORS, relational database support (including MSSQL via ODBC) and
Docker/gunicorn already configured.

## What the template includes

The generated project (the [flask-template/](flask-template/) folder) comes with:

- **App factory** (`create_app()`) in `src/app.py`, with `main.py` as the
  development entrypoint and `src.app:app` as the gunicorn entrypoint.
- **Layered structure** inside `src/`:
  - `routes/` -- blueprints (routes), including an example in `routes/health/`
    (`GET /health`).
  - `controllers/` -- business logic.
  - `db/` -- SQLAlchemy engine and session (`init_engine` / `get_session`).
  - `schemas/` -- payload shape/validation (and models, once an ORM is
    introduced).
  - `middlewares/` -- request/response hooks and decorators.
  - `classes/` -- shared domain/utility classes.
  - `config.py` -- configuration read from environment variables.
  - `extensions.py` -- shared Flask-CORS and Flask-JWT-Extended instances.
  - `errors.py` -- standardized JSON error handlers.
- **Authentication** via `flask-jwt-extended` and **CORS** via `flask-cors`,
  already registered in the app factory.
- **Database** via SQLAlchemy (plain engine/session, no ORM/migrations by
  default), with MSSQL ODBC drivers already installed in the generated
  project's Docker image.
- **Production-ready Docker**: the generated project's `Dockerfile` installs
  dependencies from `requirements.txt`, exposes port `8000` and runs with
  `gunicorn`; `docker-compose.yml` for running it locally.
- **`.env.example`**, `.gitignore` and `.dockerignore` pre-filled with the
  essentials (secrets, caches, virtual environments, IDEs).
- **Tests with pytest**: a `tests/` folder (mirroring `src/`), `app`/`client`
  fixtures in `tests/conftest.py` (using `TestConfig`, isolated from any real
  `.env`) and a working example in `tests/routes/test_health.py`. Test
  dependencies live in `requirements-dev.txt`, separate from the production
  `requirements.txt`.

## Installation

The generator is distributed as a Docker image. On every push to the `main`
branch, the [docker-publish.yml](.github/workflows/docker-publish.yml)
workflow builds and publishes the image to the GitHub Container Registry:

```sh
docker pull ghcr.io/dr1co/flask-project-template:latest
docker run --rm -it \
  -v "$(pwd):/app/output" -w /app/output \
  ghcr.io/dr1co/flask-project-template:latest my-project
```

If the project name is omitted, the container asks for it interactively.

> The `:latest` tag always points to the most recent build of `main` -- there
> are currently no immutable version tags (e.g. per commit). If you need to
> reproduce a specific version, build the image locally from the desired
> commit.

Alternatively, to build the image locally from source:

```sh
git clone https://github.com/dr1co/flask-project-template.git
cd flask-project-template
docker build -t flask-template-generator .
docker run --rm -it -v "$(pwd):/app/output" -w /app/output flask-template-generator my-project
```

In both cases, the container copies the files from
[flask-template/](flask-template/) into `my-project/`, creates an initial
`.env`, runs `pip freeze > requirements.txt` and initializes a git repository
in the generated project.

## After generating the project

```sh
cd my-project

# adjust .env as needed (JWT_SECRET_KEY, DATABASE_URL, etc.)

# local development
python main.py

# or via Docker
docker compose up --build
```

The `GET /health` route can be used to check that the application started
correctly.

### Tests

```sh
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

Tests use `TestConfig` (in `src/config.py`), which forces an empty
`DATABASE_URL` and a fixed `JWT_SECRET_KEY`, so they run isolated from any
local `.env`. New tests should mirror the `src/` structure inside `tests/`
(e.g. `tests/controllers/` for `src/controllers/`).

### Environment variables

Defined in `.env` (see `.env.example` in the generated project):

| Variable         | Description                                                            |
| ---------------- | ---------------------------------------------------------------------- |
| `DEBUG_MODE`     | Enables Flask debug mode (`True`/`False`).                             |
| `ALLOWED_HOSTS`  | Origins allowed by CORS.                                               |
| `JWT_SECRET_KEY` | Secret key used by Flask-JWT-Extended.                                 |
| `DATABASE_URL`   | SQLAlchemy connection string. Leave empty to skip database setup.      |

## CI/CD

The [docker-publish.yml](.github/workflows/docker-publish.yml) workflow runs
on every push to `main`: it builds the generator image (the root
`Dockerfile`) and publishes it to
`ghcr.io/dr1co/flask-project-template:latest` (the image name is derived from
the repository itself, so forks publish under their own owner). There is
currently no manual trigger (`workflow_dispatch`) and no per-commit version
tags -- only `:latest`, always matching the latest commit on `main`.

## Repository structure

```
flask-project-template/
├── Dockerfile              # generator image
├── entrypoint.sh           # script that creates a new project from the template
├── .github/workflows/      # generator image publishing
└── flask-template/         # contents copied into every new project
    ├── Dockerfile
    ├── docker-compose.yml
    ├── main.py
    ├── pytest.ini
    ├── requirements-dev.txt
    ├── .env.example
    ├── src/
    └── tests/
```
