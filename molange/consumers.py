from molange.drivers import GenericDriver
from molange.event_manager import _EventManager

import logging


class MessageConsumer:
    def __init__(self, mapper_factory: dict, event_manager: _EventManager, queue_driver: GenericDriver):
        self._mapper_factory = mapper_factory
        self._queue_driver = queue_driver
        self._event_manager = event_manager

    def process_message(self):
        message = self._queue_driver.receive_message()

        if not message:
            return None

        try:
            mapper = self._mapper_factory[message.event_type_name]
            event = mapper(message)

            self._event_manager.trigger(event)
        except Exception as e:  # TODO: specify exceptions...
            logging.error(str(e))
            self._queue_driver.move_message_to_dead_letter_queue(message)
        else:
            self._queue_driver.delete_message(message)
