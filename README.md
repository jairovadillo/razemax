# Transporter (aka. Molange)
[![Build Status](https://travis-ci.com/21Buttons/molange.svg?branch=master)](https://travis-ci.com/21Buttons/molange)

✉️ Async communications using AWS SNS + SQS for Python services ✨

## Installing dependencies

`pip install -r requirements.txt`

## Running the tests

Simply run `pytest`

### Running end to end tests

To run end to end tests do:
```
cd integration-tests
docker-compose up -d

# Todo dockerize this
export $(cat integration_tests/local.env )
PYTHONPATH=$(pwd) python integration_tests/sqs_consumer_tests.py
```

## Authors

* **Jairo Vadillo** [JairoVadillo](https://github.com/jairovadillo)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
