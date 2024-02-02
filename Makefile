run:
	poetry run llmgraph concepts-general https://en.wikipedia.org/wiki/Large_language_model --levels 2 --llm-model gpt-3.5-turbo --llm-temp 0.0

build:
	poetry build

install:
	poetry install

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
	source venv_install_test/bin/activate ; llmgraph --help
	source venv_install_test/bin/activate ; llmgraph --version
	source venv_install_test/bin/activate ; pip list | grep llmgraph
	rm -rf venv_install_test

poetry-config:
	poetry config --list

poetry-show-tree:
	poetry show --tree

poetry-gen-requirements:
	poetry export --output requirements.txt

test:
	poetry run coverage run -m pytest -vvv -s ./tests
	poetry run coverage report

test-selected:
	poetry run coverage run -m pytest -vvv -s ./tests -k test_console
	poetry run coverage report

black-check:
	poetry run black llmgraph tests --check --verbose

black:
	poetry run black llmgraph tests

ruff-check:
	poetry run ruff check .

ruff:
	poetry run ruff check . --fix

pre-commit:
	poetry run pre-commit run --all-files

pip-audit:
	poetry run pip-audit

.DEFAULT_GOAL := help
.PHONY: help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
