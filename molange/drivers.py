import json
import logging
from typing import Union

import boto3

from molange.exceptions import DriverError


class Message:
    def __init__(self, id, event_name, receipt_handle, body):
        self.id = id
        self.event_name = event_name
        self.body = body
        self.receipt_handle = receipt_handle


class GenericQueueDriver:
    def receive_message(self) -> Union[Message, None]:
        pass

    def delete_message(self, message: Message) -> None:
        pass

    def move_message_to_dead_letter_queue(self, message: Message) -> None:
        pass


class SQSDriver(GenericQueueDriver):
    def __init__(self, sqs_queue):
        self._queue = sqs_queue

    def receive_message(self) -> Union[Message, None]:
        message = self._queue.receive_messages(MaxNumberOfMessages=1)
        logging.info(f"Message received: {message}")

        if not message:
            return None

        message = message[0]
        message = self._process_message(message)

        return message

    def delete_message(self, message: Message) -> None:
        self._queue.delete_messages(Entries=[{'Id': 'DummyId', 'ReceiptHandle': message.receipt_handle}])
        logging.info("Message {} deleted".format(message.id))

    def move_message_to_dead_letter_queue(self, message_id: Message):
        print("Message {} to DLQ".format(message_id))

    @classmethod
    def _process_message(cls, message_sqs) -> Message:
        try:
            message_dict = json.loads(message_sqs.body)
            logging.info(f"Message body: {message_sqs.body}")

            message_content = json.loads(message_dict["Message"])
            message_id = message_dict["MessageId"]
            event_name = message_dict["MessageAttributes"]["event_name"]["Value"]
        except (KeyError,) as e:
            raise DriverError(e)
        except json.JSONDecodeError:
            raise DriverError("Message body not JSON encoded.")

        return Message(id=message_id,
                       event_name=event_name,
                       receipt_handle=message_sqs.receipt_handle,
                       body=message_content)


def get_sqs_driver(queue_name, aws_settings) -> SQSDriver:
    sqs_resource = boto3.resource('sqs', **aws_settings)
    sqs_queue = sqs_resource.get_queue_by_name(QueueName=queue_name)

    return SQSDriver(sqs_queue)
