#!/usr/bin/env python3
""" Cache """
import redis
import uuid
from typing import Union

Data = Union[str, bytes, int, float]


class Cache:
    """ Cache """

    def __init__(self):
        """ Initializes Cache instance. """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Data) -> str:
        """ Stores a value in Redis and returns the key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
