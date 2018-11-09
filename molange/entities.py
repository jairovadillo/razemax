class Message(object):
    def __init__(self, event_type_name=None, body=None):
        self.event_type_name = event_type_name
        self.body = body
