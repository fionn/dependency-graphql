VIRTUAL_ENV ?= venv
SRC = src/

venv: requirements.txt
	@python3 -m venv $@ --prompt $@::dgr
	@source $@/bin/activate && pip install -r $< && pip install pylint mypy types-requests
	@echo "enter virtual environment: source $@/bin/activate"

tags: $(SRC)
	@ctags --languages=python --python-kinds=-i -R $(SRC)

.PHONY: install
install: requirements.txt $(SRC)
	@pip install --user --require-hashes -r $<
	@pip install --user --no-deps .

.PHONY: install_dev
install_dev: venv
	@source $(VIRTUAL_ENV)/bin/activate && pip install -e .[dev]

build: $(SRC)
	@python -m build

.PHONY: outdated
outdated: $(VIRTUAL_ENV)
	@source $(VIRTUAL_ENV)/bin/activate && pip list --outdated

.PHONY: lint
lint:
	@pylint $(SRC)

.PHONY: typecheck
typecheck:
	@mypy $(SRC)
