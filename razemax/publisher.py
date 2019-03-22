import json
import logging
from datetime import datetime

import boto3

from razemax.messages import EventMessage


class SNSMessagePublisher(object):
    def __init__(self, sns_client, topic_arn):
        self._sns_client = sns_client
        self._topic_arn = topic_arn

    def publish(self, event_name: str, event_body: dict, extra_meta: dict = {}):
        meta = {
            "timestamp": datetime.utcnow().isoformat('T'),
            "version": 1
        }
        meta.update(extra_meta)
        message = {
            "type": event_name,
            "meta": meta,
            "body": event_body
        }
        event_message = EventMessage(
            type=event_name,
            body=event_body,
            meta=meta
        )

        event_message_json = event_message.json()
        logging.info(f"event name {event_name}")

        return self._sns_client.publish(TopicArn=self._topic_arn,
                                        Message=event_message_json,
                                        MessageAttributes={
                                            'event_name': {
                                                'DataType': 'String',
                                                'StringValue': event_name
                                            }
                                        })

    @classmethod
    def build(cls, topic_arn: str, aws_settings: dict = {}):
        """ aws_settings is a dict with:
            - region_name
            - aws_access_key_id
            - aws_secret_access_key
            - endpoint_url (optional)
        """
        sns_client = boto3.client('sns', **(aws_settings or {}))

        return cls(sns_client, topic_arn)
