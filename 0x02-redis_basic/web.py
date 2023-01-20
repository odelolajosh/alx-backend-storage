#!/usr/bin/env python3
""" 5. Implementing an expiring web cache and tracker. """
import requests
import redis
from functools import wraps
from typing import Callable


def counter_url(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        url = args[0]
        cache = redis.Redis()
        key = f"result:{url}"
        count_key = f"count:{url}"

        cached = cache.get(key)
        if cached is not None:
            cache.incr(count_key)
            return cached.decode("utf-8")

        result = func(*args, **kwargs)
        cache.setex(key, 10, result)
        return result
    return wrapper


@counter_url
def get_page(url: str) -> str:
    """ obtain content of a URL. """
    return requests.get(url).text
