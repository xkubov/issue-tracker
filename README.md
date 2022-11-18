# Issue Tracker

A simple issue tracking app written in Django.

**Features:**

* Issues are managed using [Django Admin](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/) from `/admin` path.
* Issue Tracker uses default Django user model. Permissions are granted based on user's status.
  * Superuser (`is_superuser`) can view/add models, and edit database.
  * Staff (`is_staff`) can only add issues and view them in database.
* Issues admin shows simple statistics for issues (min/max time of resolution, currenly open/closed issues).
* Issue Tracker provides simple REST API written using [Django REST Framework](https://www.django-rest-framework.org).
  * List of issues can be viewed using `/issues` path.
  * Issue details can be viewed using `/issues/<issue_id>/` path.
* Unit testing using `pytest`.
* Production build in `Docker`.
* The project uses `SQLite` database.

## How to develop

This package uses [poetry](https://python-poetry.org). To install Issue Tracker (and its dependencies), use:

```bash
$ poetry install
```

Then, you can start a virutualenv using `poetry shell`:

```bash
$ poetry shell
```

### Running dev server

To be able to run dev server, you need to do following:
1. Run migration (initialize Sqlite server).
2. Create superuser (to access `admin` page).

To run migrations use the following command from `poetry shell`:
```bash
$ ./scripts/manage.py migrate
```

You should see `db.sqlite3` in the root of your repository:
```bash
$ ls ./db.sqlite3
```

To create a superuser us the following command:
```bash
$ ./scripts/manage.py createsuperuser
```

Then, you can start the developemnt server by running:
```bash
$ ./scripts/manage.py runserver
```

You should be able to access admin page by visiting `localhost:8000/admin`.

### Linting & Formatting

You can run linter & formatter from `poetry shell`:

```
$ poe lint
$ poe format
```

### Tests

There are 2 test suites:
* `tests`
* `apps/issues/tests`

You can run tests with the following command from `poetry shell`.

```bash
$ poetry run pytest
```

Apart from tests, linting and formatting is also checked.

### Adding dependencies

To add runtime dependencies use:

```
$ poetry add $PACKAGE_NAME
```

To add development dependencies use:

```
$ poetry add --dev $PACKAGE_NAME
```

## Releasing new version

To create a release commit and tag use from `poetry shell`:

```
$ poe release (major|minor|patch)
```

## Running in Docker

The `issue_tracker` has prepared `Dockerfile` for production deployment.

To run `issue_tracker` using Docker, use:

1. `docker build -t issue_tracker -f ./docker/Dockerfile .`
2. `docker run -p80:80 -e SECRET_KEY=$SECRET_KEY issue_tracker`

** Notes: **

* The `SECRET_KEY` should be randomly generated string.
* The production build will not create `admin` user by default. You can create default `admin` by adding `-eADMIN_PASSORD=$PASSWORD` argument to `docker run`.
* The `SQLite` database is stored in the created container on the following path: `/app/database/db.sqlite3`.
