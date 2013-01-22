#!/usr/bin/env python

import sys

from iss import ISS

beta = sys.stdin.readline().strip()

obj = ISS()
print obj.getInitialOrientation(beta)

sys.stdout.flush()

for minute in range(0, 92):
  print "1"
  print "\n".join([str(f) for f in obj.getStateAtMinute(minute)])
  sys.stdout.flush()
