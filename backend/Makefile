# ===== Setup automation =====
poetry_setup:
	echo "Run poetry setup ..."
	poetry config virtualenvs.in-project true
	poetry shell
	poetry install
	echo "Poetry setup done!"

# ===== Linters & Formatter automation =====
lint:
	echo "Start linters ..."
	-black app/ --quiet
	-ruff check app/ --silent --fix
	-isort app
	echo "Linters done!"
