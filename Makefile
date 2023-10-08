run:
	poetry run llmgraph-cli

build:
	poetry build

publish:
	# https://python-poetry.org/docs/repositories/#configuring-credentials
	# One time: poetry config pypi-token.pypi <your-pypi-token>
	poetry publish --build

publish-test:
	# https://python-poetry.org/docs/repositories/#configuring-credentials
	# One time: poetry config repositories.test-pypi https://test.pypi.org/legacy/
	# One time: poetry config pypi-token.test-pypi pypi-mytesttoken
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

black:
	poetry run black  --line-length 120 .

flake8:
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

isort:
	poetry run isort --profile black llmgraph

.DEFAULT_GOAL := help
.PHONY: help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
