import os

import pytest
from asynctest import CoroutineMock, Mock

from aiorazemax.drivers import SQSDriver
from aiorazemax.exceptions import DriverError


class TestSQSDriver:

    @pytest.mark.asyncio
    async def test_not_message(self):
        client = Mock()
        client.receive_message = CoroutineMock(return_value=None)

        queue_url = 'some_queue_url'

        sqs_driver = SQSDriver(client, queue_url)
        result = await sqs_driver.receive_message()

        assert result is None

    def test_delete_message(self):
        pass

    def test_process_message(self):
        message_json_str = self._load_message_json_str('./data/sns_sqs_message.json')
        message_sqs = {}
        message_sqs['Body'] = message_json_str
        message_sqs['ReceiptHandle'] = 'ef5c2897-1197-4398-b34a-32508dd5db70'

        message = SQSDriver._process_message(message_sqs)

        assert message.id == "a936a7d0-f-b3c4-"
        assert message.event_name == "UserCreated"
        assert isinstance(message.body, dict)

    def test_process_message_fails_when_no_name(self):
        message_json_str = self._load_message_json_str('./data/sns_sqs_message_no_name.json')
        message_sqs = {}
        message_sqs['Body'] = message_json_str

        with pytest.raises(DriverError):
            SQSDriver._process_message(message_sqs)

    def _load_message_json_str(self, path):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        message_file = open(os.path.join(current_dir, path), 'r')
        message_json_str = message_file.read()

        return message_json_str
