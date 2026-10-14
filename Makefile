.PHONY: install
install:
	venv/bin/pip install -r requirements-dev.txt
	venv/bin/pip install -e .

.PHONY: test
test:
	venv/bin/py.test -vv --cov-report term-missing:skip-covered --cov=linkpreview
