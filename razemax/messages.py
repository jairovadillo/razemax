import json


class EventMessage:

    def __init__(self, type, body, meta):
        self.type = type
        self.body = body
        self.meta = meta

    def json(self):
        return json.dumps(self.__dict__)
