""" Decorators.
"""

import time


def one_moment(func):
    """ Waits one second before calling function.
    """

    def wrapper(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)
    return wrapper


def slow_down(sec=1):
    """ Slows down a function for an arbitrary number of seconds.
    """

    def one_moment(func):
        """ Waits one second before calling function.
        """

        def wrapper(*args, **kwargs):
            time.sleep(sec)
            return func(*args, **kwargs)
        return wrapper
    return one_moment


def timer(func):
    """ Prints the runtime of the decorated function.
    """

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        run_time = time.perf_counter() - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return result
    return wrapper


def print_arguments(func):
    """ Prints all arguments received by the function before it is executed.
    """

    def wrapper(*args, **kwargs):
        print(args, kwargs)
        res = func(*args, **kwargs)
        return res
    return wrapper


def counted(func):
    """ Counts how many times the function was called.
    """

    def wrapper(*args, **kwargs):
        wrapper.called += 1
        return func(*args, **kwargs)
    wrapper.called = 0
    return wrapper


def func_cache(func):
    """ Caches the result of the function.
    """

    cache = dict()
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper