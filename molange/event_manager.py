import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class _EventManager:
    __subscribers: dict = defaultdict(set)

    def subscribe(self, subscriber, event):
        self.__subscribers[event].add(subscriber)

    def trigger(self, event):
        for subscriber in self.__subscribers.get(event.__class__, []):
            subscriber(event)

    def _reset(self):
        """Never call this outside tests!"""
        self.__subscribers = defaultdict(set)

    def __str__(self):
        return str(dict(self.__subscribers))

    @property
    def subscribers(self):
        return dict(self.__subscribers)


event_manager = _EventManager()
