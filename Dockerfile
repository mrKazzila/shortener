FROM python:3.11-slim as base
ENV \
    # python
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    # poetry
    POETRY_VERSION=1.4.2 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app/

RUN \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    # deps for installing poetry
        curl && \
    # install poetry
    curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION && \
    # cleaning cache
    rm -rf /var/cache && \
    rm -rf /var/lib/apt/lists/*


FROM base as venv

COPY ./poetry.lock ./pyproject.toml /app/
RUN poetry export --format requirements.txt --output /app/requirements.txt --without-hashes


FROM python:3.11-slim

RUN groupadd -r docker && \
    useradd -m -g docker unprivilegeduser && \
    mkdir -p /home/unprivilegeduser && \
    chown -R unprivilegeduser /home/unprivilegeduser

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    APP_HOME=/home/unprivilegeduser/shortener

RUN mkdir $APP_HOME

WORKDIR $APP_HOME

COPY --from=venv /app/requirements.txt $APP_HOME/requirements.txt

RUN pip install -r $APP_HOME/requirements.txt && \
    rm $APP_HOME/requirements.txt

COPY . $APP_HOME

RUN chmod +x $APP_HOME/run_app.sh && \
    chown -R unprivilegeduser:docker $APP_HOME

USER unprivilegeduser
