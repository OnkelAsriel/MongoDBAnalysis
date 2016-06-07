import urllib2

import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.database_names()
db = client.get_database('exodef')
objects = db.objects

db.collection_names(include_system_collections=False)

from bson.objectid import ObjectId

