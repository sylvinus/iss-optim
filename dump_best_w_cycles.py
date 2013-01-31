#!/usr/bin/env python

import pymongo
import json

mongoClient = pymongo.MongoClient("mongodb://iss:station@linus.mongohq.com:10066/iss-results")
DB = mongoClient["iss-results"]

ranges = {}

avg = 0
cnt = 0
res = DB.results.find().sort("score", -1)
for r in res:
  k = r["beta"]+" "+r["range"]
  if not k in ranges:
    cnt += 1
    avg += r["score"]
    print "%s\t%s" % (k, r["score"])
    ranges[k] = r["params"]
    
params = {}

for p in ranges:
  beta = p.split(" ")[0]
  if not beta in params:
    params[beta] = {}
  params[beta].update(ranges[p])

print "avg : %s" % (avg*1.0/cnt)
print

print json.dumps(params).replace("},","},\n")