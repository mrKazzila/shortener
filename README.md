<h1 align="center">
  Simple Url shortener
</h1>

<div align="center">

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

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
- [Backend](backend/README.md)
- [Frontend](https://github.com/facebook/create-react-app)
- [Postman for API testing](https://www.postman.com/)


## How To Use
<details>

<summary><strong>Use Make & Docker</strong></summary>

1. Firstly clone repo
   ```bash
   git clone git@github.com:mrKazzila/shortener.git
   ```

2. SetUp env for [Backend](https://github.com/mrKazzila/shortener/blob/main/backend/README.md) and [Frontend](https://github.com/mrKazzila/shortener/blob/main/frontend/README.md) parts

3. Run all services
   ```bash
   make docker_setup_all
   ```

4. Run only frontend
   ```bash
   make docker_run_front
   ```

5. Run only backend
   ```bash
   make docker_run_back
   ```

6. Run backend tests
   ```bash
   make docker_run_tests_back
   ```

</details>


## Over-engineering note
<details>

<summary><strong>Click me</strong></summary>
I understand that many technologies/constructions in code for such a simple project is over-engineering,
but just wanted to practice advanced technologies on a simple project. Don't scold ;)

</details>


<br>
<br>
<p align="center">
  <a href="https://github.com/mrKazzila">GitHub</a> •
  <a href="https://mrkazzila.github.io/resume/">Resume</a> •
  <a href="https://www.linkedin.com/in/i-kazakov/">LinkedIn</a>
</p>
