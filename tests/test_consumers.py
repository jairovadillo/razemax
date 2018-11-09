from unittest.mock import MagicMock

from molange.consumers import MessageConsumer
from molange.entities import Message
from molange.event_bus import EventBus


class TestConsumer:
    def test_message_processed(self):
        event_name = 'event_mock'
        event_mock = MagicMock()
        event_mock.name = event_name

        subscriber_mock = MagicMock()
        subscriber_mock.subscribe_to = event_mock

        event_factory = {
            event_name: event_mock
        }

        EventBus.subscribe(subscriber_mock)

        queue_driver = MagicMock()
        queue_driver.receive_message.return_value = Message(event_type_name=event_name, body={'foo': 21})

        consumer = MessageConsumer(event_factory=event_factory, event_bus=EventBus, queue_driver=queue_driver)
        consumer.process_message()

        subscriber_mock.run.assert_called_once()

