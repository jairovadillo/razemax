.PHONY: tests integration-tests

tests:
	docker-compose run --rm --no-deps --entrypoint "pytest -m \"not integration\"" integration_test

integration-tests:
	docker-compose run --rm integration_test pytest -m integration