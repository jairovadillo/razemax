from unittest.mock import MagicMock

from molange.consumers import MessageConsumer
from molange.drivers import SQSDriver, Message


class TestConsumer:
    def test_event_triggered(self):
        message_name = 'test_message'
        message = Message(id='id',
                          event_name=message_name,
                          body={'foo': 21},
                          receipt_handle='LKJ358FDH82J')
        queue_driver_mock = self._get_queue_driver_mock(return_value=message)

        event_name = 'test_event'
        event = self._get_event_mock(event_name)
        mapper_factory = {
            message_name: lambda x: event
        }

        event_manager_mock = MagicMock()

        consumer = MessageConsumer(mapper_factory=mapper_factory,
                                   event_manager=event_manager_mock,
                                   queue_driver=queue_driver_mock)
        consumer.process_message()

        event_manager_mock.trigger.assert_called_once_with(event)

    def test_mapper_called(self):
        message_name = 'test_message'
        message = Message(id=2453,
                          event_name=message_name,
                          body={'foo': 21},
                          receipt_handle='aepui2948')
        queue_driver_mock = self._get_queue_driver_mock(return_value=message)

        mapper = MagicMock()
        mapper_factory = {
            message_name: mapper
        }

        event_manager_mock = MagicMock()

        consumer = MessageConsumer(mapper_factory=mapper_factory,
                                   event_manager=event_manager_mock,
                                   queue_driver=queue_driver_mock)
        consumer.process_message()

        mapper.assert_called_once_with(message)

    def test_message_not_received(self):
        mapper_factory = {}
        queue_driver_mock = self._get_queue_driver_mock()
        event_manager_mock = MagicMock()

        consumer = MessageConsumer(mapper_factory=mapper_factory,
                                   event_manager=event_manager_mock,
                                   queue_driver=queue_driver_mock)
        consumer.process_message()

        queue_driver_mock.move_message_to_dead_letter_queue.assert_not_called()
        queue_driver_mock.delete_message.assert_not_called()

    def test_dead_letter_queue_when_missing_mapping(self):
        message = Message(id=2435,
                          event_name='test_message',
                          body={'foo': 21},
                          receipt_handle='24q3w4t')
        queue_driver_mock = self._get_queue_driver_mock(return_value=message)
        event_manager_mock = MagicMock()

        mapper_factory = {}

        consumer = MessageConsumer(mapper_factory=mapper_factory,
                                   event_manager=event_manager_mock,
                                   queue_driver=queue_driver_mock)
        consumer.process_message()

        queue_driver_mock.move_message_to_dead_letter_queue.assert_called_once_with(message)

    def _get_event_mock(self, event_name):
        event_mock = MagicMock()
        event_mock.name = event_name

        return event_mock

    def _get_subscriber_mock(self, event_to_subscribe):
        subscriber_mock = MagicMock()
        subscriber_mock.subscribe_to = event_to_subscribe

        return subscriber_mock

    def _get_queue_driver_mock(self, return_value=None):
        queue_driver = MagicMock(spec=SQSDriver)
        queue_driver.receive_message.return_value = return_value

        return queue_driver
