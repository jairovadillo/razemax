from marshmallow import Schema, fields, post_load

from .entities import Message


class MessageSerializer(Schema):
    event_type_name = fields.Str(required=True)
    body = fields.Dict(required=True)

    @post_load
    def create_object(self, data):
        return Message(**data)
