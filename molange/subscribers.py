from abc import ABC


class Subscriber(ABC):
    subscribe_to: list = []

    def execute(self, *args, **kwargs) -> None:
        raise NotImplementedError()
