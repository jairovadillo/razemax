# Transporter (aka. Molange)
[![Build Status](https://travis-ci.com/21Buttons/molange.svg?branch=master)](https://travis-ci.com/21Buttons/molange)

✉️ Async communications using AWS SNS + SQS for Python services ✨

## Documentation

### In-Memory event manager

_Show me the code_

```python
from molange.event_manager import event_manager


class NorthKoreaThreatCreatedEvent:
    def __init__(self, id, target):
        self.id = id
        self.target = target


def trump_subscriber(event: NorthKoreaThreatCreatedEvent):
    print(f"North korea will attack us or {event.target}!")
    
    
event_manager.subscribe(trump_subscriber, NorthKoreaThreatCreatedEvent)
event_manager.trigger(NorthKoreaThreatCreatedEvent(0, "Mexico"))
```

Result:
```
North korea will attack us or Mexico!
```

### Trigger subscribers from SQS

```python
from molange.consumers import MessageConsumer
from molange.drivers import get_sqs_driver
from molange.event_manager import event_manager


def kp_message_to_event(message):
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

queue_driver = get_sqs_driver(aws_settings, "korea-threats-queue")
MessageConsumer(mapper, event_manager, queue_driver).process_message()
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
