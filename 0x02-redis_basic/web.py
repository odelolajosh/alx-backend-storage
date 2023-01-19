#!/usr/bin/env python3
""" 5. Implementing an expiring web cache and tracker. """
import requests
import redis
from functools import wraps
from typing import Callable


def counter_url(fn: Callable) -> Callable:
    """ counter decorator. """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        """ wrapper function. """
        if not args:
            return fn(*args, **kwargs)

        cache = redis.Redis()
        key = f"result:{args[0]}"
        count_key = f"count:{args[0]}"

        if cache.exists(key):
            cache.incr(count_key)
            return cache.get(key)

        result = fn(*args, **kwargs)
        cache.incr(count_key)
        cache.setex(key, 10, result)
        return result
    return wrapper


@counter_url
def get_page(url: str) -> str:
    """ obtain content of a URL. """
    r = requests.get(url)
    return r.text


if __name__ == "__main__":
    url = "https://www.google.com"
    cache = redis.Redis()
    cache.flushdb()
    print(get_page(url))
    print(get_page(url))
    count_key = f"count:{url}"
    print("get_page is called {} times".format(int(cache.get(count_key))))
