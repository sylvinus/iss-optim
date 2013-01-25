#!/usr/bin/env python

import pymongo
import json

mongoClient = pymongo.MongoClient("mongodb://iss:station@linus.mongohq.com:10066/iss-results")
DB = mongoClient["iss-results"]

params = {}

res = DB.results.find().sort("score", -1)
for r in res:
  if not r["beta"] in params:
    params[r["beta"]] = r["params"]
    
print json.dumps(params).replace("},","},\n")