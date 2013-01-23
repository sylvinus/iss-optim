#!/usr/bin/env python

import sys

from iss2 import ISS
import json, base64

beta = sys.stdin.readline().strip()

obj = ISS()

if (len(sys.argv) >= 2):
  obj.setParamsArray(json.loads(base64.b64decode(sys.argv[1])))

print obj.getInitialOrientation(beta)

sys.stdout.flush()

for minute in range(0, 92):
  print "1"
  print "\n".join([str(f) for f in obj.getStateAtMinute(minute)])
  sys.stdout.flush()
