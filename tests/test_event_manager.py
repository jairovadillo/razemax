from unittest.mock import Mock

from molange.event_manager import event_manager


class TestEvent:
    pass


class TestEvent2:
    pass


class TestEventBus:
    def setup_method(self):
        event_manager._reset()

    def test_call_subscriber_when_event(self):
        subscriber_mock = self._subscribe_to_event(TestEvent)

        event_instance = TestEvent()
        event_manager.trigger(event_instance)

        subscriber_mock.execute.assert_called_once_with(event_instance)

    def test_call_correct_subscriber(self):
        self._subscribe_to_event(TestEvent)
        subscriber_mock2 = self._subscribe_to_event(TestEvent2)

        event_instance = TestEvent()
        event_manager.trigger(event_instance)

        subscriber_mock2.execute.assert_not_called()

    def _subscribe_to_event(self, event_class):
        subscriber_mock = Mock()
        subscriber_mock.subscribe_to = [event_class]
        event_manager.subscribe(subscriber_mock)

        return subscriber_mock
