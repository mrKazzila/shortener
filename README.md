<h1 align="center">
  Simple Url shortener
</h1>

<div align="center">

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)


</div>
<hr>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech stack</a> •
  <a href="#how-to-use">How To Use</a>
</p>


## Features
- Forms a short url of 5 characters
- Redirects to the main url
- Shows the number of clicks on the url
- Ability to Make short url inactive


## Tech stack
- [Python 3.11](https://www.python.org/downloads/)
- [FastApi](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://pypi.org/project/alembic/)
- [Poetry](https://python-poetry.org/docs/)


## How To Use
<details>

<summary><strong>Use Docker</strong></summary>

1. Firstly clone repo
   ```bash
   git clone git@github.com:mrKazzila/shortener.git
   ```

2. Prepare local env with make
   ```bash
    make prepare_env DB_HOST=your_db_host DB_PORT=your_db_port DB_NAME=your_db_name DB_USER=your_db_user DB_PASSWORD=your_db_pass
   ```

3. Run docker compose with make
   ```bash
   make docker_run
   ```

4. Stop docker compose with make
   ```bash
   make docker_stop
   ```

</details>

<details>
<summary>Local commands</summary>

1. Firstly clone repo
   ```bash
   git clone git@github.com:mrKazzila/shortener.git
   ```

2. Prepare local env with make
   ```bash
    make prepare_env DB_HOST=your_db_host DB_PORT=your_db_port DB_NAME=your_db_name DB_USER=your_db_user DB_PASSWORD=your_db_pass
   ```

3. Settings Poetry with make
   ```bash
   make poetry_setup
   ```

4. Upgrade alembic to head & run fastapi use uvicorn
   ```bash
   make fastapi_run
   ```

5. Run pytest and generate coverage html report
   ```bash
   make tests_coverage
   ```

6. Run linters & formatters
   ```bash
   make run_linters
   ```

</details>


[//]: # (## Documentation)

[//]: # (<details>)

[//]: # (<summary><strong>API Documentation</strong></summary>)

[//]: # (* lorem)

[//]: # (</details>)


<br>
<br>
<p align="center">
  <a href="https://github.com/mrKazzila">GitHub</a> •
  <a href="https://mrkazzila.github.io/resume/">Resume</a> •
  <a href="https://www.linkedin.com/in/i-kazakov/">LinkedIn</a>
</p>
