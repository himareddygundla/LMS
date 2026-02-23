import time
from functools import wraps

def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        elapsed = round(end - start, 4)
        print(f"⏱ {func.__name__} took {elapsed} seconds")

        return result, elapsed
    return wrapper