import asyncio
import os

import pytest

from aiorazemax.consumers import MessageConsumer
from aiorazemax.drivers import SQSDriver, Message
from aiorazemax.event_manager import EventManager
from aiorazemax.publisher import SNSMessagePublisher


# events.py
class FollowCreatedEvent:
    def __init__(self, from_user_id, to_user_id, is_suggested, timestamp):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.is_suggested = is_suggested
        self.timestamp = timestamp


def follow_created_subscriber(event: FollowCreatedEvent):
    assert event.from_user_id == "amancioortega"
    assert event.is_suggested is False


# apps.py
event_bus = EventManager.subscribe(follow_created_subscriber, FollowCreatedEvent)


# mappers.py
def follow_created_mapper(message: Message):
    body = message.body.get('body')
    event_dict = {
        'from_user_id': body.get('source_user'),
        'to_user_id': body.get('target_user'),
        'is_suggested': body.get('is_suggested'),
        'timestamp': body.get('timestamp')
    }
    return FollowCreatedEvent(**event_dict)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_integration_sqs():
    message_factory = {
        'follow_created': follow_created_mapper
    }

    aws_settings = {
        'region_name': os.environ['AWS_REGION'],
        'aws_access_key_id': os.environ['AWS_ACCESS_KEY_ID'],
        'aws_secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY'],
        'endpoint_url': os.environ.get('AWS_ENDPOINT_URL')
    }

    queue_name = os.environ['SQS_QUEUE_NAME']
    topic_arn = os.environ['SNS_TOPIC_ARN']

    driver = await SQSDriver.build(queue_name=queue_name, aws_settings=aws_settings)
    publisher = await SNSMessagePublisher.build(topic_arn=topic_arn, aws_settings=aws_settings)
    consumer = MessageConsumer(mapper_factory=message_factory, event_manager=EventManager(), queue_driver=driver)

    assert await consumer.process_message() is False

    await publisher.publish("follow_created", {
        'source_user': 'amancioortega',
        'target_user': 'jairo',
        'is_suggested': False,
        'timestamp': "2018-12-01T11:23:23.0000"
    })

    await asyncio.sleep(1)   # Wait for deliver
    assert await consumer.process_message() is True
    assert await consumer.process_message() is False

    await driver.close()
    await publisher.close()
