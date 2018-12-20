from datetime import datetime


class Event:
    def __init__(self, body, timestamp: datetime = datetime.utcnow()):
        self._body = body
        self._timestamp = timestamp

    @property
    def name(self) -> str:
        return type(self).__name__

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def body(self) -> dict:
        return self._body
