# Razemax
[![Build Status](https://travis-ci.com/21Buttons/razemax.svg?branch=master)](https://travis-ci.com/21Buttons/razemax)

✉️ Async communications using AWS SNS + SQS for Python services ✨

## Documentation

### In-Memory event manager

_Show me the code_

```python
from razemax.event_manager import EventManager


class NorthKoreaThreatCreatedEvent:
    def __init__(self, id, target):
        self.id = id
        self.target = target


def trump_subscriber(event: NorthKoreaThreatCreatedEvent):
    print(f"North korea will attack us or {event.target}!")
    
    
EventManager.subscribe(trump_subscriber, NorthKoreaThreatCreatedEvent)
EventManager.trigger(NorthKoreaThreatCreatedEvent(0, "Mexico"))
```

Result:
```
North korea will attack us or Mexico!
```

### Trigger subscribers from SQS

#### Preconditions

SQS queue has to be subscribed to SNS topic before running the consumer

#### Code

```python
from razemax.consumers import MessageConsumer
from razemax.drivers import SQSDriver
from razemax.event_manager import EventManager
from razemax.publisher import SNSMessagePublisher


def kp_message_to_event(message):
    # Highly recommended to use Marshmallow to validate
    return NorthKoreaThreatCreatedEvent(message.body['id'], message.body['target_name'])

mapper = {
    'KPThreatCreated': kp_message_to_event
}

aws_settings = {
    'region_name': "",
    'aws_access_key_id': "",
    'aws_secret_access_key': "",
    'endpoint_url': ""
}

queue_driver = SQSDriver.build("korea-threats-queue", aws_settings)
MessageConsumer(mapper, EventManager, queue_driver).process_message()

publisher = SNSMessagePublisher.build(aws_settings, 'korea-topic')
publisher.publish('KPThreatCreated', {'id': 21, 'target_name': 'Portugal'})
```

Result:

```
North korea will attack us or Portugal!
```

## Installing (TODO)

`pip install git@github.com/transporter`


## Running the tests

To run end to end tests do:
```
make unit-tests
make integration-tests
```

## Authors

* Jairo Vadillo ([@jairovadillo](https://github.com/jairovadillo))

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
