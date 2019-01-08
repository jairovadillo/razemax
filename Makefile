.PHONY: tests integration-tests clean-pyc

clean-pyc:
	find . -name \*.pyc -delete
	find . -name \*.pyo -delete
	find . -name \*~ -delete

unit-tests:
	docker-compose run --rm unit-tests

integration-tests:
	docker-compose run --rm integration-tests
