from collections import defaultdict


class EventBus:
    _subscribers: dict = defaultdict(list)

    @classmethod
    def subscribe(cls, subscriber):
        for event in subscriber.subscribe_to:
            cls._subscribers[event.name].append(subscriber)

    @classmethod
    def trigger(cls, event):
        for subscriber in cls._subscribers.get(event.name, []):
            subscriber.run(event)


event_bus = EventBus()
