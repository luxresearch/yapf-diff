init:
	pipenv install --dev
lint: init
	pipenv run flake8
test: lint
	pipenv run python -m unittest tests.unit
