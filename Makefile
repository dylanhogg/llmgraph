run:
	# poetry run llmgraph concepts-general https://en.wikipedia.org/wiki/Large_language_model --levels 2 --llm-model gpt-5-mini --llm-temp 0.0
	# poetry run llmgraph concepts-general https://en.wikipedia.org/wiki/Large_language_model
	# poetry run llmgraph concepts-science https://en.wikipedia.org/wiki/Large_language_model --levels 2 --llm-model gpt-5-mini --llm-temp 0.0
	# poetry run llmgraph machine-learning "https://en.wikipedia.org/wiki/Vision_transformer" --levels 4 --llm-model gpt-5-mini
	poetry run llmgraph machine-learning "https://en.wikipedia.org/wiki/Graph_neural_network" --levels 2 --llm-model gpt-5-mini
	# poetry run llmgraph concepts-science "https://en.wikipedia.org/wiki/Abiogenesis" --levels 4 --llm-model gpt-5-mini
	# poetry run llmgraph concepts-science "https://en.wikipedia.org/wiki/Artificial_life" --levels 4 --llm-model gpt-5-mini
	# poetry run llmgraph concepts-science "https://en.wikipedia.org/wiki/Cellular_automaton" --levels 6 --llm-model gpt-5-mini --max-sum-total-tokens 500000
	# poetry run llmgraph concepts-general "https://en.wikipedia.org/wiki/Free_energy_principle" --levels 4 --llm-model gpt-5-mini
	# poetry run llmgraph concepts-general "https://en.wikipedia.org/wiki/Free_energy_principle" --levels 5 --llm-model gpt-5-mini
	# poetry run llmgraph location-australia https://en.wikipedia.org/wiki/Richmond,_Victoria --levels 5 --llm-model gpt-5-mini --llm-temp 0.0

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

poetry-update:
	# 1. Update pyproject.toml (requires plugin poetry-plugin-up as of March 2024)
	# https://github.com/MousaZeidBaker/poetry-plugin-up
	# One time: poetry self add poetry-plugin-up
	poetry up --latest
	# 2. Update poetry.lock
	poetry update

test:
	poetry run coverage run -m pytest -vvv -s ./tests
	poetry run coverage report

test-selected:
	poetry run coverage run -m pytest -vvv -s ./tests -k test_console
	poetry run coverage report

precommit:
	poetry run ruff check . --fix
	poetry run black llmgraph tests

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
