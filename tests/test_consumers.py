from unittest.mock import MagicMock

from molange.consumers import MessageConsumer
from molange.drivers import GenericDriver
from molange.entities import Message
from molange.event_bus import event_bus


class TestConsumer:
    def test_message_processed(self):
        message_name = 'test_message'
        event_name = 'test_event'
        event = self._get_event_mock(event_name)
        mapper_factory = {
            message_name: lambda x: event
        }

        message = Message(event_type_name=message_name, body={'foo': 21})
        queue_driver_mock = self._get_queue_driver_mock(return_value=message)

        subscriber_mock = self._get_subscriber_mock(event)
        event_bus.subscribe(subscriber_mock)

        consumer = MessageConsumer(mapper_factory=mapper_factory,
                                   event_bus=event_bus,
                                   queue_driver=queue_driver_mock)
        consumer.process_message()

        subscriber_mock.run.assert_called_once()

    def test_message_not_received(self):
        mapper_factory = {}
        queue_driver_mock = self._get_queue_driver_mock()

        consumer = MessageConsumer(mapper_factory=mapper_factory,
                                   event_bus=event_bus,
                                   queue_driver=queue_driver_mock)

        consumer.process_message()

        queue_driver_mock.move_message_to_dead_letter_queue.assert_not_called()
        queue_driver_mock.delete_message.assert_not_called()

    def _get_event_mock(self, event_name):
        event_mock = MagicMock()
        event_mock.name = event_name

        return event_mock

    def _get_subscriber_mock(self, event_to_subscribe):
        subscriber_mock = MagicMock()
        subscriber_mock.subscribe_to = event_to_subscribe

        return subscriber_mock

    def _get_queue_driver_mock(self, return_value=None):
        queue_driver = MagicMock(spec=GenericDriver)
        queue_driver.receive_message.return_value = return_value

        return queue_driver
