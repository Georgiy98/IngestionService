import logging
import traceback


class RetryException(Exception):
    """Class for gathering all exceptions were happened in case of total fail"""


def retry(amount: int):
    def repeater(func):
        def wrapper(*args, **kwargs):
            error_set = set()
            for _ in range(amount):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_set.add(
                        e.__repr__() + '\n' + '\n'.join(
                            line for line in traceback.StackSummary.from_list(
                                traceback.extract_tb(e.__traceback__)
                            ).format()
                        ))
                    logging.warning(str(e.__repr__()))
            else:
                error_text = '\n'.join(error_set)
                # logging.error(error_text)
                raise RetryException(error_text)

        return wrapper

    return repeater
