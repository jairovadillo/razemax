import json
import logging
from datetime import datetime

import boto3


class SNSMessagePublisher(object):
    def __init__(self, sns_client, topic_arn):
        self._sns_client = sns_client
        self._topic_arn = topic_arn

    def publish(self, event_name, event_body):
        message = {
            "type": event_name,
            "meta": {
                "timestamp": datetime.utcnow().isoformat('T'),
                "version": 1
            },
            "body": event_body
        }

        message_json = json.dumps(message)
        logging.info(f"event name {event_name}")

        return self._sns_client.publish(TopicArn=self._topic_arn,
                                        Message=message_json,
                                        MessageAttributes={
                                            'event_name': {
                                                'DataType': 'String',
                                                'StringValue': event_name
                                            }
                                        })

    @classmethod
    def build(cls, aws_settings: dict, topic_arn: str):
        """ aws_settings is a dict with:
            - region_name
            - aws_access_key_id
            - aws_secret_access_key
            - endpoint_url (optional)
        """
        sns_client = boto3.client('sns', **aws_settings)
        return cls(sns_client, topic_arn)
