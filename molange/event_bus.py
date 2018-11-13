from collections import defaultdict


class EventBus:
    __subscribers: dict = defaultdict(list)

    @classmethod
    def subscribe(cls, subscriber):
        for event in subscriber.subscribe_to:
            cls.__subscribers[event.name].append(subscriber)

    @classmethod
    def trigger(cls, event):
        for subscriber in cls.__subscribers.get(event.name, []):
            subscriber.run(event)

    @classmethod
    def _reset(cls):
        cls.__subscribers = defaultdict(list)


event_bus = EventBus()
