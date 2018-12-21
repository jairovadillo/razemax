from collections import defaultdict

from .subscribers import Subscriber

import logging


logger = logging.getLogger(__name__)


class _EventManager:
    __subscribers: dict = defaultdict(list)

    def subscribe(self, subscriber: Subscriber):
        if not subscriber.subscribe_to:
            logger.warning("{} has empty subscribe_to list".format(type(subscriber).__name__))
            return

        for event in subscriber.subscribe_to:
            self.__subscribers[event].append(subscriber)

    def trigger(self, event):
        for subscriber in self.__subscribers.get(event.__class__, []):
            subscriber.execute(event)

    def _reset(self):
        """Never call this outside tests!"""
        self.__subscribers = defaultdict(list)

    def __str__(self):
        return str(dict(self.__subscribers))

    @property
    def subscribers(self):
        return dict(self.__subscribers)


event_manager = _EventManager()
