import logging
import traceback
from exceptions import RetryException


def _get_error_msg(error):
    return error.__repr__() + '\n' + '\n'.join(
        line for line in traceback.StackSummary.from_list(
            traceback.extract_tb(error.__traceback__)
        ).format()
    )


def retry(amount: int, include=(BaseException,), exclude=(BaseException,)):
    if type(include) == type and issubclass(include, BaseException):
        include = (include,)
    if type(exclude) == type and issubclass(exclude, BaseException):
        exclude = (exclude,)

    def repeater(func):
        def wrapper(*args, **kwargs):
            error_set = set()
            for _ in range(amount):
                try:
                    return func(*args, **kwargs)
                except include as e:
                    error_set.add(_get_error_msg(e))
                    if exclude != (BaseException,) and any(map(lambda error: isinstance(e, error), exclude)):
                        raise RetryException('\n'.join(error_set))

                    logging.warning(str(e.__repr__()))
                except exclude as e:
                    error_set.add(_get_error_msg(e))
                    raise RetryException('\n'.join(error_set))

            else:
                error_text = '\n'.join(error_set)
                raise RetryException(error_text)

        return wrapper

    return repeater
