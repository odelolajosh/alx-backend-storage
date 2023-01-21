#!/usr/bin/env python3
""" 5. Implementing an expiring web cache and tracker. """
import requests
import redis
from functools import wraps
from typing import Callable


def counter_url(func: Callable) -> Callable:
    """ web cache and tracker decorator. """
    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        """ decorator wrapper. """
        url = args[0]
        cache = redis.Redis()
        key = f"result:{url}"
        count_key = f"count:{url}"

        if cache.exists(key):
            cache.incr(count_key)
            return cache.get(key)

        result = func(*args, **kwargs)
        cache.setex(key, 10, result)
        return result
    return wrapper


@counter_url
def get_page(url: str) -> str:
    """ obtain content of a URL. """
    return requests.get(url).content.decode('utf-8')
