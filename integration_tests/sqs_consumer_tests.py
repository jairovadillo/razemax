import os
import time
from datetime import datetime

from molange.consumers import MessageConsumer
from molange.drivers import get_sqs_driver, Message
from molange.event_manager import event_manager
from molange.publisher import get_sns_message_publisher
from molange.subscribers import Subscriber


# events.py
class FollowCreatedEvent:
    def __init__(self, from_user_id, to_user_id, is_suggested, timestamp):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.is_suggested = is_suggested
        self.timestamp = timestamp


# event_subscribers.py
class FollowCreatedSubscriber(Subscriber):
    # TODO: Subscribe using event + subscriber or subscriber contains event?
    # preferred here because subscriber has to know to which event is subscribing to process it
    subscribe_to = [FollowCreatedEvent]

    @staticmethod
    def execute(event):
        print("Hello from follows! {}: {}".format(event.from_user_id, event.is_suggested))


# apps.py
event_bus = event_manager.subscribe(FollowCreatedSubscriber)


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


# worker.py
def main():
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

    driver = get_sqs_driver(queue_name=queue_name, aws_settings=aws_settings)
    publisher = get_sns_message_publisher(topic_arn=topic_arn, aws_settings=aws_settings)

    publisher.publish("follow_created", {
        'source_user': 'amancioortega',
        'target_user': 'jairo',
        'is_suggested': False,
        'timestamp': datetime.now()
    })

    time.sleep(2)

    consumer = MessageConsumer(mapper_factory=message_factory, event_manager=event_manager, queue_driver=driver)

    consumer.process_message()
    # try:
    # except Exception as e:
    #     logging.error(e)


if __name__ == "__main__":
    main()