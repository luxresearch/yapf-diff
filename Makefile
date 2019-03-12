init:
	pipenv install --dev
lint:
	pipenv run flake8
typecheck:
	MYPYPATH=./stubs pipenv run mypy	yapf_diff
test: lint typecheck
	pipenv run python -m unittest tests.unit
	pipenv run pip install -q . && pipenv run yapf-diff --help 1> /dev/null
build:
	python setup.py sdist bdist_wheel
