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