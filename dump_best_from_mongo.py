#!/usr/bin/env python

import pymongo
import json
import os

mongoClient = pymongo.MongoClient(os.getenv("MONGODB_URI"))
DB = mongoClient["iss-results"]

params = {}

avg = 0
cnt = 0
res = DB.results.find().sort("score", -1)
for r in res:
  if not r["beta"] in params:
    cnt += 1
    avg += r["score"]
    print "%s\t%s" % (r["beta"], r["score"])
    params[r["beta"]] = r["params"]
    
print "avg : %s" % (avg*1.0/cnt)
print

print json.dumps(params).replace("},","},\n")
