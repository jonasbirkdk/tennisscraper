from pymongo import MongoClient
import dns.resolver
import os
import sys
from holland import holland
from brooks import brooks
from ravens import ravens
from avondale import avondale
from memorial import memorial
from dotenv import load_dotenv

load_dotenv()
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
new_client = MongoClient(os.getenv("mongo_uri"))
new_db = new_client['InterviewCoach']
new_collection = new_db["tennis"]

def not_exists(doc, available):
    for item in available:
        if item['court'] == doc['court'] and item['date'] == doc['date'] and item['time'] == doc['time']:
            return False

    return True


def remove_outdated(court, available):
    cursor = new_collection.find({})

    for doc in cursor:
        if doc['court'] == court and not_exists(doc, available):
            print(available)
            print(doc)
            new_collection.delete_one(doc)


def update_availability(court, res):
    print("Res: ", res)
    available = []
    for key, val in res.items():
        for time in val:
            obj = {"court": court, "date": key, "time": time}
            available.append(obj)
            if not new_collection.find_one(obj):
                new_collection.insert_one(obj)
    remove_outdated(court, available)

holland_res = holland()
update_availability("Holland Park", holland_res)

brooks_res = brooks()
update_availability("Brook Green", brooks_res)

ravens_res = ravens()
update_availability("Ravenscourt", ravens_res)

avondale_res = avondale()
update_availability("Avondale Park", avondale_res)

memorial_res = memorial()
update_availability("Kensington Memorial", memorial_res)
