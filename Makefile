# Makefile

# Variables
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Default target
all: install run

# Create virtual environment
install:
	@echo "Creating virtual environment..."
	@pipenv install --dev

# Run the program
run:
	@echo "Running program..."
	pipenv run python ruby_finder.py

# Clean up
clean:
	@echo "Removing virtual environment..."
	@rm -rf $(VENV)