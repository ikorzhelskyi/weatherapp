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


def timer(func):
    """Prints the runtime of the decorated function.
    """

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        run_time = time.perf_counter() - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return result
    return wrapper