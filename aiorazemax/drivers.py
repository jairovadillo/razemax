import asyncio
import json
import logging
from typing import Union

import aiobotocore

from aiorazemax.exceptions import DriverError


class Message:
    def __init__(self, id, event_name, receipt_handle, body):
        self.id = id
        self.event_name = event_name
        self.body = body
        self.receipt_handle = receipt_handle


class SQSDriver:
    def __init__(self, sqs_client, sqs_queue_url):
        self._client = sqs_client
        self._queue_url = sqs_queue_url

    async def receive_message(self) -> Union[Message, None]:
        messages = await self._client.receive_message(
            QueueUrl=self._queue_url,
            MaxNumberOfMessages=1
        )

        logging.debug(f"Message received: {messages}")

        if not messages or not messages['Messages']:
            return None

        messages = messages['Messages']
        message = messages[0]
        message = self._process_message(message)

        return message

    async def mark_message_processed(self, message: Message) -> None:
        await self._client.delete_message(
            QueueUrl=self._queue_url,
            ReceiptHandle=message.receipt_handle
        )
        logging.debug("Message {} deleted".format(message.id))

    def mark_message_unprocessed(self, message_id: Message, exception: Exception):
        # TODO: Add dead letter queue implementation
        pass

    @classmethod
    def _process_message(cls, message_sqs) -> Message:
        try:
            message_dict = json.loads(message_sqs["Body"])
            logging.debug(f"Message body: {message_sqs['Body']}")

            message_content = json.loads(message_dict["Message"])
            message_id = message_dict["MessageId"]
            event_name = message_dict["MessageAttributes"]["event_name"]["Value"]
        except (KeyError,) as e:
            raise DriverError(e)
        except json.JSONDecodeError:
            raise DriverError("Message body not JSON encoded.")

        return Message(id=message_id,
                       event_name=event_name,
                       receipt_handle=message_sqs['ReceiptHandle'],
                       body=message_content)

    @classmethod
    async def build(cls, queue_name: str, aws_settings: dict):
        loop = asyncio.get_running_loop()
        session = aiobotocore.get_session(loop=loop)
        sqs_client = session.create_client('sqs', **aws_settings)

        sqs_queue_info = await sqs_client.get_queue_url(QueueName=queue_name)

        return cls(sqs_client, sqs_queue_info['QueueUrl'])
