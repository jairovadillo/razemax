from collections import defaultdict


class EventBus:
    _subscribers = defaultdict(list)

    @classmethod
    def subscribe(cls, subscriber):
        cls._subscribers[subscriber.subscribe_to.name].append(subscriber)

    @classmethod
    def trigger(cls, event):
        for subscriber in cls._subscribers.get(event.name, []):
            subscriber.run(event)
