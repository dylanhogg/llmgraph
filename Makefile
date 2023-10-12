run:
	# poetry run llmgraph
	# poetry run llmgraph food "https://en.wikipedia.org/wiki/Bolognese_sauce" --levels 4
	poetry run llmgraph food "https://en.wikipedia.org/wiki/Burrito" --levels 4

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
	# source venv_install_test/bin/activate ; llmgraph bad_entity "https://en.wikipedia.org/wiki/The_Matrix"
	# source venv_install_test/bin/activate ; llmgraph movie "https://en.wikipedia.org/wiki/The_Matrix"
	# rm -rf venv_install_test

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

black:
	poetry run black llmgraph tests

ruff-check:
	poetry run ruff check .

ruff-fix:
	poetry run ruff check . --fix

.DEFAULT_GOAL := help
.PHONY: help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
