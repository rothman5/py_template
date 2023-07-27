# Author      : Rasheed Othman
# Created     : July 26, 2023
# Description : Provides Makefile rules for project navigation.

# Specify the project name here
name := "Template_v1.0.0"

# Use Bash as the default shell
SHELL := bash

# Setting these flags forces an exit when an error occurs
.SHELLFLAGS := -eu -o pipefail -c

# Adding this flag disables any built-in Make rules
MAKEFLAGS += --no-builtin-rules

# This variable is set to run the help message when 'make' is used with no target
.DEFAULT_GOAL := help

# Create an alias for the parent working directory path
pwd := $(realpath $(dir $(abspath $(firstword $(MAKEFILE_LIST)))))

# Run Python packages from the virtual environment if it exists, otherwise use the system's path
# The shell command is run each time the variable is used
.ONESHELL:
py = $(shell if [ -d $(pwd)/env ]; then echo "source $(pwd)/env/Scripts/activate && $(pwd)/env/Scripts/python"; else echo "py"; fi)
pip = $(shell if [ -d $(pwd)/env ]; then echo "source $(pwd)/env/Scripts/activate && $(pwd)/env/Scripts/pip"; else echo "pip"; fi)
black = $(shell if [ -d $(pwd)/env ]; then echo "source $(pwd)/env/Scripts/activate && $(pwd)/env/Scripts/black"; else echo "black"; fi)
pylint = $(shell if [ -d $(pwd)/env ]; then echo "source $(pwd)/env/Scripts/activate && $(pwd)/env/Scripts/pylint"; else echo "pylint"; fi)
pyclean = $(shell if [ -d $(pwd)/env ]; then echo "source $(pwd)/env/Scripts/activate && $(pwd)/env/Scripts/pyclean"; else echo "pyclean"; fi)
pyinst = $(shell if [ -d $(pwd)/env ]; then echo "source $(pwd)/env/Scripts/activate && $(pwd)/env/Scripts/pyinstaller"; else echo "pyinstaller"; fi)

# This variable tells Make that this rule isn't associated with a file.
.PHONY: help
help: ## Display a list of runnable targets
	@echo ------------------------------------------------------------------
	@echo $(name) Application Makefile Usage:
	@echo ------------------------------------------------------------------
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z\$$/]+.*:.*?##\s/ {printf "\033[36m%-12s\033[0m > %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ------------------------------------------------------------------

run: ## Run the application
	$(py) project/main.py

install: requirements.txt ## Install the project Python package requirements
	$(py) -m pip install -U pip
	$(pip) install -U pyinstaller black pylint pyclean
	$(pip) install -U -r requirements.txt

virtualenv: ## Initialize a new Python virtual environment
	py -m pip install -U pip
	pip install -U virtualenv
	py -m venv env
	$(MAKE) install

clean: project ## Remove the Python cache, .spec, and build files
	$(pyclean) project
	@(if [ ! -z $(pwd)/*.spec ]; then rm -rf $(pwd)/*.spec && echo "Cleaned .spec files."; else echo "No .spec files to clean."; fi)
	@(if [ -d $(pwd)/bin/build/ ]; then rm -rf $(pwd)/bin/build/ && echo "Clean build files."; else echo "No build files to clean."; fi)

fullclean: ## Remove the virtual environment
	@(if [ -d $(pwd)/env ]; then $(MAKE) clean && rm -rf $(pwd)/env && echo "Removed the virtual environment."; else echo "No virtual environment to remove."; fi)

lint: ## Use Pylint to check module against PEP8 standards
	@(if [ ! -z $(path) ]; then $(pylint) --max-parents 10 -rn -v $(path); else echo "Usage: make lint path=<path_to_file_or_folder>"; fi)

diff: ## Use Black to show the diff of the reformatted code
	@(if [ ! -z $(path) ]; then $(black) -v --diff $(path); else echo "Usage: make diff path=<path_to_file_or_folder>"; fi)

check: ## Use Black to check the PEP8 code's conformity
	@(if [ ! -z $(path) ]; then $(black) -v --check $(path); else echo "Usage: make check path=<path_to_file_or_folder>"; fi)

format: ## Use Black to reformat the code with PEP8 standards
	@(if [ ! -z $(path) ]; then $(black) -v $(path); else echo "Usage: make format path=<path_to_file_or_folder>"; fi)

one-dir: ## use PyInstaller to compile the binaries into an executable (inside application folder)
	$(pyinst) --distpath bin/ \
			  --workpath bin/build/ \
			  --noconfirm \
			  --onedir \
			  --windowed \
			  --clean \
			  --icon "$(name).ico" \
			  --name $(PROJ) \
			  --add-data "Makefile;." \
			  --add-data "debug.log;." \
			  --add-data "$(name).ico;." \
			  --add-data "requirements.txt;." \
			  "project/main.py"
	rm -rf $(name).spec bin/build/

one-file: ## use PyInstaller to compile the binaries into a portable executable
	$(pyinst) --distpath bin/ \
			  --workpath bin/build/ \
			  --noconfirm \
			  --onefile \
			  --windowed \
			  --clean \
			  --icon "$(name).ico" \
			  --name $(PROJ) \
			  --add-data "Makefile;." \
			  --add-data "console.log;." \
			  --add-data "$(name).ico;." \
			  --add-data "requirements.txt;." \
			  "project/main.py"
	rm -rf $(name).spec bin/build/
