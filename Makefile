init:
	pipenv install --dev
lint:
	pipenv run flake8
typecheck:
	MYPYPATH=./stubs pipenv run mypy	yapf_diff
test: lint typecheck
	pipenv run python -m unittest tests.unit
build:
	python setup.py sdist bdist_wheel
deploy: test build
