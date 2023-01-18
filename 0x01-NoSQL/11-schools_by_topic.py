#!/usr/bin/env python3
""" 11. Where can I learn python """


def schools_by_topic(mongo_collection, topic):
    """ Returns the list of school having a specific topic. """
    res = mongo_collection.find({"topics": topic})
    return res
