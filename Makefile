run:
	poetry run llmgraph-cli

build:
	poetry build

publish:
	# One time: poetry config pypi-token.pypi <your-pypi-token>
	poetry publish --build

publish-test:
	# One time: poetry config repositories.test-pypi https://test.pypi.org/legacy/
	# One time: poetry config pypi-token.test-pypi <your-test-pypi-token>
	poetry publish -r test-pypi

test-install-from-pypi:
	rm -rf venv_install_test
	python3 -m venv venv_install_test
	source venv_install_test/bin/activate ; pip install llmgraph
	source venv_install_test/bin/activate ; pip list | grep llmgraph
	rm -rf venv_install_test

poetry-config:
	poetry config --list

poetry-show-tree:
	poetry show --tree

poetry-gen-requirements:
	poetry export --output requirements.txt

test:
	poetry run pytest -vvv -s ./tests

test-selected:
	poetry run pytest -vvv -s ./tests -k test_console_run

# autoflake removes unused imports and unused variables as reported by pyflakes
autoflake:
	# poetry run autoflake --check --remove-all-unused-imports --recursive .
	poetry run autoflake --in-place --remove-all-unused-imports --recursive llmgraph
	poetry run autoflake --in-place --remove-all-unused-imports --recursive tests

# black code formatter
black:
	poetry run black --line-length 120 .

# flake8 is a python tool that glues together pycodestyle, pyflakes, mccabe
flake8:
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# isort sorts imports
isort:
	poetry run isort --profile black llmgraph tests

.DEFAULT_GOAL := help
.PHONY: help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
