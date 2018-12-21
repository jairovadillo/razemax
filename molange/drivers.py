import json
import logging
from typing import Union

import boto3

from molange.entities import Message
from molange.exceptions import DriverError
from molange.services import MessageDeduplicationService


class GenericQueueDriver:
    def receive_message(self) -> Union[Message, None]:
        pass

    def delete_message(self, message: Message) -> None:
        pass

    def move_message_to_dead_letter_queue(self, message: Message) -> None:
        pass


class SQSDriver(GenericQueueDriver):
    def __init__(self, sqs_queue, deduplicator=None):
        self._queue = sqs_queue
        self._deduplicator = deduplicator

    def receive_message(self) -> Union[Message, None]:
        message = self._queue.receive_messages()
        if not message:
            return None

        message = message[0]
        message_id, message = self._process_message(message.body)

        if not self._deduplicator:
            return message

        if not self._deduplicator.is_processed(message_id):
            self._deduplicator.add(message_id)
            return message

    def delete_message(self, message_id: str) -> None:
        print("Message {} deleted".format(message_id))

    def move_message_to_dead_letter_queue(self, message_id: Message):
        print("Message {} to DLQ".format(message_id))

    @classmethod
    def _process_message(cls, message_body_str: str) -> Message:
        try:
            message_dict = json.loads(message_body_str)
            message_id = message_dict["MessageId"]
            event_name = message_dict["MessageAttributes"]["event_name"]["Value"]  # TODO: ADD EXCEPTION
            message_content = json.loads(message_dict["Message"])  # TODO: ADD EXCEPTION
        except (KeyError, ) as e:
            raise DriverError(e)

        return Message(id=message_id, event_name=event_name, body=message_content)


def get_sqs_driver(queue_name, aws_settings, redis_connection=None) -> SQSDriver:
    sqs_resource = boto3.resource('sqs', **aws_settings)
    sqs_queue = sqs_resource.get_queue_by_name(QueueName=queue_name)

    deduplicator = None
    if redis_connection:
        deduplicator = MessageDeduplicationService(redis_connection)

    return SQSDriver(sqs_queue, deduplicator)
