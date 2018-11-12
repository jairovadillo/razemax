from unittest.mock import MagicMock

from molange.consumers import MessageConsumer
from molange.drivers import GenericDriver
from molange.entities import Message
from molange.event_bus import event_bus


class TestConsumer:
    def test_message_processed(self):
        event_mock = self._get_event_mock('test_event')
        subscriber_mock = self._get_subscriber_mock(event_mock)
        event_factory_mock = self._generate_event_factory(event_mock)
        queue_driver_mock = self._get_queue_driver_mock(event_mock.name)

        event_bus.subscribe(subscriber_mock)

        consumer = MessageConsumer(event_factory=event_factory_mock,
                                   event_bus=event_bus,
                                   queue_driver=queue_driver_mock)
        consumer.process_message()

        subscriber_mock.run.assert_called_once()

    def _get_event_mock(self, event_name):
        event_mock = MagicMock()
        event_mock.name = event_name

        return event_mock

    def _get_subscriber_mock(self, event_to_subscribe):
        subscriber_mock = MagicMock()
        subscriber_mock.subscribe_to = event_to_subscribe

        return subscriber_mock

    def _generate_event_factory(self, event):
        return {
            event.name: event
        }

    def _get_queue_driver_mock(self, event_name) -> GenericDriver:
        queue_driver = MagicMock(spec=GenericDriver)
        queue_driver.receive_message.return_value = Message(event_type_name=event_name, body={'foo': 21})

        return queue_driver
