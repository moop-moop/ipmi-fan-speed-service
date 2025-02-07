# Project settings
PYTHON = python
VENV = venv
MAIN_SCRIPT = my_project/main.py

# Check if Rye is available
HAVE_RYE = $(shell command -v rye >/dev/null 2>&1 && echo yes || echo no)

.PHONY: setup install run test clean

# Setup virtual environment and install dependencies
setup:
ifeq ($(HAVE_RYE),yes)
	@echo "Using Rye for setup..."
	rye sync
else
	@echo "Using venv + pip for setup..."
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
endif

# Install dependencies (via Rye or pip)
install:
ifeq ($(HAVE_RYE),yes)
	rye sync
else
	$(VENV)/bin/pip install -r requirements.txt
endif

# Run the project
run:
ifeq ($(HAVE_RYE),yes)
	rye run $(PYTHON) $(MAIN_SCRIPT)
else
	$(VENV)/bin/$(PYTHON) $(MAIN_SCRIPT)
endif

# Run tests
test:
ifeq ($(HAVE_RYE),yes)
	rye run python -m unittest discover tests
else
	$(VENV)/bin/python -m unittest discover tests
endif

# Clean up virtual environment and cache
clean:
	rm -rf $(VENV) __pycache__ .pytest_cache *.pyc
ifeq ($(HAVE_RYE),yes)
	rye cache clean
endif
