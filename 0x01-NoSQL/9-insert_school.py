#!/usr/bin/env python3
""" 9. Insert a document in Python """


def insert_school(mongo_collection, **kwargs):
    """ Inserts a new document in a collection based on kwargs. """
    new = mongo_collection.insert_one(kwargs)
    return new.inserted_id

