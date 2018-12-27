[![Build Status](https://travis-ci.com/21Buttons/molange.svg?branch=master)](https://travis-ci.com/21Buttons/molange)

# Molange

One Paragraph of project description goes here


### Installing


## Running the tests

Simply run `pytest`

### Running end to end tests

To run end to end tests do:
```
cd integration-tests
docker-compose up
```

From another shell do (TODO: Dockerize this):
```
export $(cat integration_tests/local.env )
PYTHONPATH=$(pwd) python integration_tests/sqs_consumer_tests.py
```

## Authors

* **Jairo Vadillo** - *Initial work* - [JairoVadillo](https://github.com/jairovadillo)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
