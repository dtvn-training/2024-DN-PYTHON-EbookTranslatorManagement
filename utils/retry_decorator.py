from functools import wraps
import time
import sqlalchemy.exc
from app.interfaces import Status


def retry_function_decorator(retries=1, timeout=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts <= retries:
                try:
                    return func(*args, **kwargs)
                except sqlalchemy.exc.SQLAlchemyError:
                    attempts += 1
                    if attempts > retries:
                        return None, Status.ERROR
                    else:
                        time.sleep(timeout)
                except Exception:
                    return None, Status.ERROR
        return wrapper
    return decorator
