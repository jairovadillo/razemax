from unittest.mock import MagicMock

from molange.drivers import SQSDriver


class TestSQSDriver:
    def test_not_message(self):
        queue = MagicMock()
        queue.receive_messages.return_value = None

        result = SQSDriver(queue).receive_message()

        assert result is None

    def test_duplicated_message(self):
        pass

    def test_process_message(self):
        pass

    def test_delete_message(self):
        pass

    def test_process_message(self):
        pass
