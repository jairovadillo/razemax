from unittest.mock import Mock

from molange.event_manager import EventManager


class TestEvent:
    pass


class TestEvent2:
    pass


class TestEventBus:
    def setup_method(self):
        EventManager._reset()

    def test_call_subscriber_when_event(self):
        subscriber_mock = self._subscribe_to_event(TestEvent)

        event_instance = TestEvent()
        EventManager.trigger(event_instance)

        subscriber_mock.assert_called_once_with(event_instance)

    def test_call_correct_subscriber(self):
        self._subscribe_to_event(TestEvent)
        subscriber_mock2 = self._subscribe_to_event(TestEvent2)

        event_instance = TestEvent()
        EventManager.trigger(event_instance)

        subscriber_mock2.assert_not_called()

    def _subscribe_to_event(self, event_class):
        subscriber_mock = Mock()
        EventManager.subscribe(subscriber_mock, event_class)

        return subscriber_mock
