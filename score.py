#!/usr/bin/env python

import os, sys

totest = [74, 72, -70, -74]
totest = [75,-75,73,-73,71,-71]

def getscore(beta):
  os.system("rm -rf *.pyc")
  f = os.popen("java -Xmx1000M -jar ISSVis.jar -exec './cli.py' -beta %s" % beta)
  out = f.read()
  #print out
  if "ERROR" in out:
    print "ERROR FOR BETA=%s\n\n\n %s" % (beta, out)
    sys.exit(1)

  return float(out.split("\n")[-2].split(" = ")[1])

total = 0
for beta in totest:
  s = getscore(beta)
  print "%s\t%s" % (beta, s)
  total += s

print
print "Avg : %s" % (total/len(totest))
