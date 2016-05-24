#!/usr/bin/env python

import pymongo
import json
import os

mongoClient = pymongo.MongoClient(os.getenv("MONGODB_URI"))
DB = mongoClient["iss-results"]

ranges = {}

avg = 0
cnt = 0
res = DB.results.find().sort("score", -1)
for r in res:
  k = r["beta"]
  if "-" in r["range"]:
    k+=" "+r["range"]
  if not k in ranges:
    cnt += 1
    avg += r["score"]
    print "%s\t%s" % (k, r["score"])
    ranges[k] = r["params"]
    
params = {}

for p in ranges:
  beta = p.split(" ")[0]
  if not beta in params:
    params[beta] = ranges[p]
  if " " in p:
    for i in range(int(p.split(" ")[1].split("-")[0]),1+int(p.split(" ")[1].split("-")[1])):
      k = "sarjd_%s" % i
      if k in ranges[p]:
        params[beta][k] = ranges[p][k]

print "avg : %s" % (avg*1.0/cnt)
print

print json.dumps(params).replace("},","},\n")
