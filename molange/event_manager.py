from collections import defaultdict

from .events import Event
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
            self.__subscribers[event.name].append(subscriber)

    def trigger(self, event: Event):
        for subscriber in self.__subscribers.get(event.name, []):
            subscriber.run(event)

    def _reset(self):
        """Never call this outside tests!"""
        self.__subscribers = defaultdict(list)


event_manager = _EventManager()
