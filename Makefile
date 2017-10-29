test:
	py.test tests

clean:
	rm -rf **/*.pyc **/__pycache__ .mypy_cache/

deps:
	pip3 install .

lint:
	prospector

type_check:
	mypy **/*.py --ignore-missing-imports

check: lint type_check


