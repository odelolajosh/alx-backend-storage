#!/usr/bin/env python3
""" 5. Implementing an expiring web cache and tracker. """
import requests
import redis
from functools import wraps
from typing import Callable


def counter(fn: Callable) -> Callable:
    """ counter decorator. """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        """ wrapper function. """
        cache = redis.Redis()
        res_key = f"result:{args[0]}"
        count_key = f"count:{args[0]}"

        if cache.exists(res_key):
            cache.incr(count_key)
            return cache.get(res_key)

        result = fn(*args, **kwargs)
        cache.setex(res_key, 10, result)
        return result
    return wrapper


@counter
def get_page(url: str) -> str:
    """ obtain content of a URL. """
    r = requests.get(url)
    return r.text
