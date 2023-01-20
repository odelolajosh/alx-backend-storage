#!/usr/bin/env python3
""" 12. Log stats """
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx = client.logs.nginx

    count = nginx.count_documents({})
    print("{} logs".format(count))

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    count = nginx.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(count))

    print("IPs:")
    ips = nginx.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in ips:
        print("\t{}: {}".format(ip["_id"], ip["count"]))
