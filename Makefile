.PHONY: install test test-balance test-support coverage coverage-balance coverage-support run-balance run-support clean

install:
	pip install -r balance/requirements.txt
	pip install -r support/requirements.txt

test: test-balance test-support

test-balance:
	cd balance && python3 -m pytest tests

test-support:
	cd support && python3 -m pytest tests

coverage: coverage-balance coverage-support

coverage-balance:
	cd balance && python3 -m pytest --cov=src --cov-fail-under=90 tests

coverage-support:
	cd support && python3 -m pytest --cov=src --cov-fail-under=60 tests

run-balance:
	cd balance && uvicorn src.main:app --host 0.0.0.0 --port 8081 --reload

run-support:
	cd support && uvicorn app:app --host 0.0.0.0 --port 8082 --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
