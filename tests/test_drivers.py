import os
from unittest.mock import MagicMock

import pytest

from molange.drivers import SQSDriver
from molange.exceptions import DriverError


class TestSQSDriver:
    def test_not_message(self):
        queue = MagicMock()
        queue.receive_messages.return_value = None

        result = SQSDriver(queue).receive_message()

        assert result is None

    def test_delete_message(self):
        pass

    def test_process_message(self):
        message_json_str = self._load_message_json_str('./data/sns_sqs_message.json')
        message_sqs = MagicMock()
        message_sqs.body = message_json_str

        message = SQSDriver._process_message(message_sqs)

        assert message.id == "a936a7d0-f63f-5818-b3c4-f345522c5ef6"
        assert message.event_name == "UserCreated"
        assert isinstance(message.body, dict)

    def test_process_message_fails_when_no_name(self):
        message_json_str = self._load_message_json_str('./data/sns_sqs_message_no_name.json')
        message_sqs = MagicMock()
        message_sqs.body = message_json_str

        with pytest.raises(DriverError):
            SQSDriver._process_message(message_sqs)

    def _load_message_json_str(self, path):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        message_file = open(os.path.join(current_dir, path), 'r')
        message_json_str = message_file.read()

        return message_json_str
