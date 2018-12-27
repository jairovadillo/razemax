import logging

from molange.drivers import GenericQueueDriver
from molange.event_manager import _EventManager

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)


class MessageConsumer:
    def __init__(self, mapper_factory: dict, event_manager: _EventManager, queue_driver: GenericQueueDriver):
        self._mapper_factory = mapper_factory
        self._queue_driver = queue_driver
        self._event_manager = event_manager

    def process_message(self):
        # Receive message
        message = self._queue_driver.receive_message()

        if not message:
            logging.info("No messages to process")
            return None

        logging.info(f"Message type is: {message.event_name}")
        try:
            # Parse message to event
            mapper = self._mapper_factory[message.event_name]
            logging.info(f"Selected mapper is: {mapper}")

            event = mapper(message)
            logging.info(f"Event type is: {event.__class__}")

            # Trigger subscribers
            self._event_manager.trigger(event)
        except Exception as e:  # TODO: specify exceptions...
            logging.error(str(e))
            self._queue_driver.move_message_to_dead_letter_queue(message)
        else:
            self._queue_driver.delete_message(message)
