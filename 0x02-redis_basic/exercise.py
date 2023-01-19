#!/usr/bin/env python3
""" Cache """
import redis
import uuid
from typing import Union, Callable
from functools import wraps

Data = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """ counts how many times methods in Cache class are called. """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ decorator wrapper """
        if isinstance(self, Cache):
            key = method.__qualname__
            self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ stores history of inputs and outputs for a function. """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ decorator wrapper. """
        in_key = f"{method.__qualname__}:inputs"
        out_key = f"{method.__qualname__}:outputs"
        output = method(self, *args, **kwargs)
        if isinstance(self, Cache):
            self._redis.rpush(in_key, str(args))
            self._redis.rpush(out_key, output)
        return output
    return wrapper


def replay(fn: Callable):
    """ displays the history of calls of a particular function. """
    if fn is None or not hasattr(fn, "__self__"):
        return
    if not isinstance(fn.__self__, Cache):
        return
    redis_store = getattr(fn.__self__, "_redis", None)
    if redis_store is None:
        return

    key = fn.__qualname__
    in_key = f"{key}:inputs"
    out_key = f"{key}:outputs"

    call_count = 0
    if redis_store.exists(key) != 0:
        call_count = int(redis_store.get(key))
    print(f"{key} was called {call_count} times:")

    call_inputs = redis_store.lrange(in_key, 0, -1)
    call_outputs = redis_store.lrange(out_key, 0, -1)

    for inp, out in zip(call_inputs, call_outputs):
        print(f"{key}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")


class Cache:
    """ Cache """

    def __init__(self):
        """ Initializes Cache instance. """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
