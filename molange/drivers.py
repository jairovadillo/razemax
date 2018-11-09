import json

import boto3

from molange.entities import Message
from molange.serializers import MessageSerializer
from molange.services import MessageDeduplicationService
from typing import Union


class GenericDriver:
    def receive_message(self) -> Union[Message, None]:
        pass

    def delete_message(self, message: Message) -> None:
        pass

    def move_message_to_dead_letter_queue(self, message: Message) -> None:
        pass


class SQSDriver(GenericDriver):
    def __init__(self, sqs_queue, deduplicator=None):
        self._queue = sqs_queue
        self._deduplicator = deduplicator

    def receive_message(self) -> Union[Message, None]:
        message = self._queue.receive_messages()
        if not message:
            return None

        message = message[0]
        message_id, message = self._process_message(message)

        if not self._deduplicator or not self._deduplicator.is_processed(message_id):
            self._deduplicator.add(message_id)
            return message
        else:
            self.delete_message(message_id)
            return None

    def delete_message(self, message: Message) -> None:
        print("Message {} deleted".format(message.event_type_name))

    def move_message_to_dead_letter_queue(self, message: Message):
        print("Message {} to DLQ".format(message.event_type_name))

    def _process_message(self, message):
        message_dict = json.loads(message.body)  # TODO: ADD EXCEPTION
        message_id = message_dict["MessageId"]
        message_content = json.loads(message_dict["Message"])  # TODO: ADD EXCEPTION
        message_content = MessageSerializer(strict=True).load(message_content).data

        return message_id, message_content


def get_sqs_driver(queue_name, aws_settings, redis_connection=None):
    sqs_resource = boto3.resource('sqs', **aws_settings)
    sqs_queue = sqs_resource.get_queue_by_name(QueueName=queue_name)

    deduplicator = None
    if redis_connection:
        deduplicator = MessageDeduplicationService(redis_connection)

    return SQSDriver(sqs_queue, deduplicator)
