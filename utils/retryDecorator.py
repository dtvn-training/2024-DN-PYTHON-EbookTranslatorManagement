from functools import wraps
import time
from app.interfaces import Status


def retry_function_decorator(retries=1, timeout=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except:
                    if retries > 0:

                        continue
                    else:
                        raise
            attempts = 0
            while attempts <= retries:
                try:
                    return func(*args, **kwargs)
                except:
                    attempts += 1
                    if attempts > retries:
                        return None, Status.ERROR
                    else:
                        time.sleep(timeout)

        return wrapper
    return decorator
