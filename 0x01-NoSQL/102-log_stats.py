#!/usr/bin/env python3
""" 12. Log stats """
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx = client.logs.nginx

    count = nginx.count_documents({})
    print(f"{count} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    count = nginx.count_documents({"method": "GET", "path": "/status"})
    print(f"{count} status check")

    print("IPs:")
    top_ips_res = nginx.aggregate([
        {"$group": {"_id": "$ip", "requestCount": {"$count": {}}}},
        {"$sort": {"requestCount": -1}},
        {"$limit": 10}
    ])
    for ip_res in top_ips_res:
        ip = ip_res["_id"]
        reqCount = ip_res["requestCount"]
        print(f"\t{ip}: {reqCount}")
