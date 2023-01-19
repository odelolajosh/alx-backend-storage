#!/usr/bin/env python3
""" 5. Implementing an expiring web cache and tracker. """
import requests
import redis
from functools import wraps
from typing import Callable


def get_page(url: str) -> str:
    """ obtain content of a URL. """
    cache = redis.Redis()
    key = f"result:{url}"
    count_key = f"count:{url}"

    if cache.exists(key):
        cache.incr(count_key)
        return cache.get(key)

    result = requests.get(url).text
    cache.incr(count_key)
    cache.setex(key, 10, result)
    return result


if __name__ == "__main__":
    url = "https://www.google.com"
    cache = redis.Redis()
    cache.flushdb()
    print(get_page(url))
    print(get_page(url))
    count_key = f"count:{url}"
    print("get_page is called {} times".format(int(cache.get(count_key))))
