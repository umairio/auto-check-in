VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
REQS = requirements.txt
DOCKER_COMPOSE = docker compose -f docker-compose.yaml

.PHONY: setup env install clean lint test format up stop down rebuild

setup: env install

env:
	python3 -m venv $(VENV)
	touch .env

install: $(REQS)
	$(PIP) install -r $(REQS)

clean:
	rm -rf $(VENV)
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

lint:
	$(PYTHON) -m flake8 . || $(PYTHON) -m pylint .

test:
	$(PYTHON) -m pytest

format:
	$(PYTHON) -m black .

up:
	$(DOCKER_COMPOSE) up --build

stop:
	$(DOCKER_COMPOSE) stop

down:
	$(DOCKER_COMPOSE) down

rebuild:
	$(DOCKER_COMPOSE) up --build --no-cache
