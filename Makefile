.PHONY: tests integration-tests

unit-tests:
	docker-compose run --rm --no-deps --entrypoint "pytest -m \"not integration\"" tests

integration-tests:
	docker-compose run --rm tests pytest -m integration