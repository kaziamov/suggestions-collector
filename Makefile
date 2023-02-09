app:
	poetry run python predictions_collector/collector.py


full-test:
	poetry run pytest --show-capture=stdout --showlocals -vv
light-test:
	poetry run pytest --no-summary --disable-pytest-warnings
lint:
	poetry run flake8 suggestions_collector tests
check: light-test lint
push: check
	git push


install:
	poetry install
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl --force
test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml