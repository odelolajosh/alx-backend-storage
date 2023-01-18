#!/usr/bin/env python3
""" Cache """
import redis
import uuid
from typing import Union, Callable
from functools import wraps

Data = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """ Decorator. """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs);
    return wrapper


class Cache:
    """ Cache """

    def __init__(self):
        """ Initializes Cache instance. """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Data) -> str:
        """ Stores a value in Redis and returns the key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Data:
        """ Gets the value from Redis using a key. """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """ Gets a string from Redis using a key. """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ Gets an integer from Redis using a key. """
        return self.get(key, int)
