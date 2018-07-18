import sys

from botctl.errors import BotControlError


def command_callback(callback):
    def callback_wrapper(*args, **kwargs):
        try:
            rc = callback(*args, **kwargs)

        except BotControlError as expected_error:
            logger.debug(expected_error)
            rc = -1

        return rc

    return callback_wrapper
