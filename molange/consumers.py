from molange.drivers import GenericDriver
from molange.event_bus import EventBus

import logging


class MessageConsumer:
    def __init__(self, event_factory: dict, event_bus: EventBus, queue_driver: GenericDriver):
        self._event_factory = event_factory
        self._queue_driver = queue_driver
        self._event_bus = event_bus

    def process_message(self):
        message = self._queue_driver.receive_message()

        if not message:
            return None

        event = self._event_factory.get(message.event_type_name)
        if not event:
            # TODO: report unimplemented event
            return None

        event.load(message.body)

        try:
            self._event_bus.trigger(event)
        except Exception as e:
            logging.error(str(e))
            self._queue_driver.move_message_to_dead_letter_queue(message)
        else:
            self._queue_driver.delete_message(message)
