""" Decorators.
"""

import time


def one_moment(func):
    """Waits one second before calling function.
    """

    def wrapper(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)
    return wrapper


def slow_down(sec=1):

    def one_moment(func):
        """Waits one second before calling function.
        """

        def wrapper(*args, **kwargs):
            time.sleep(sec)
            return func(*args, **kwargs)
        return wrapper
    return one_moment