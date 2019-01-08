.PHONY: tests integration-tests

unit-tests:
	docker-compose run --rm unit-tests

integration-tests:
	docker-compose run --rm integration-tests
