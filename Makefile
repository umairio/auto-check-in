VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
REQS = requirements.txt

# Targets
.PHONY: all setup install

all: 

setup:
    python3 -m venv $(VENV)

install: $(REQS)
    $(PIP) install -r $(REQS)

