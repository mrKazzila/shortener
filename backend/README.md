<h1 align="center">
  shortener api
</h1>

<div align="center">

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

2. Setup poetry
   ```bash
   make poetry_setup
   ```

3. Copy env example settings to env and fill them in
   ```bash
   cp env/.env.example env/.env
   ```

4. Run docker compose with make
   ```bash
   make docker_run
   ```

5. Stop docker compose with make
   ```bash
   make docker_stop
   ```

</details>

<details>
<summary>Other useful commands</summary>

1. Run pytest and generate coverage html report
   ```bash
   make test_coverage
   ```

2. Run linters & formatters
   ```bash
   make lint
   ```

</details>

## Documentation
<details>
<summary><strong>API Documentation</strong></summary>

**`POST` | Create short url: [`http://localhost:8000/`](http://localhost:8000/)**

Example:
   - Request

       ```
        {
          "target_url": "https://example.com/"
        }
       ```

   - Response

      ```
        {
          "id": 0,
          "url": "http://localhost:8000/L0pFi",
          "target_url": "https://example.com/"
        }
      ```

**`GET` | Redirect to target url: [`http://localhost:8000/<url_key>`](http://localhost:8000/<url_key>)**

Example:
   - Request

     ```
        {
            "url_key": "1236"
        }
     ```

</details>


<br>
<br>
<p align="center">
  <a href="https://github.com/mrKazzila">GitHub</a> •
  <a href="https://mrkazzila.github.io/resume/">Resume</a> •
  <a href="https://www.linkedin.com/in/i-kazakov/">LinkedIn</a>
</p>
