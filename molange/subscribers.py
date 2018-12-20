from abc import ABC


class Subscriber(ABC):
    @property
    def subscribe_to(self) -> list:
        raise NotImplementedError()

    def execute(self, *args, **kwargs) -> None:
        raise NotImplementedError()
