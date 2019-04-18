import json
import logging
from datetime import datetime

import boto3


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
        message_json = json.dumps(message)

        # https://docs.python.org/3/howto/logging.html#optimization
        logging.debug('event_name %s, topic_arn %s, message_json %s', event_name, self._topic_arn, message_json)

        return self._sns_client.publish(TopicArn=self._topic_arn,
                                        Message=message_json,
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
