FROM ubuntu:jammy

# Install pinned poetry version.
RUN pip install 'poetry==1.2.1'

# Copying this first will improve caching and re-runs.
COPY poetry.lock pyproject.toml /app/

WORKDIR /app

# Project initialization:
# Disable using virtualenvs. Docker is already isolated environment.
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY . /app
