import urllib2

import pymongo

client = pymongo.MongoClient()

user = ""
password = ""

if user != "" and password != "":
    client.the_database.authenticate(user, password, mechanism='SCRAM-SHA-1')

db = client.database_names()
db = client.get_database('exodef')
objects = db.objects

db.collection_names(include_system_collections=False)

from bson.objectid import ObjectId

