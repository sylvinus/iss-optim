#!/usr/bin/env python

# Import PuLP modeler functions
from openopt import NSP
from FuncDesigner import *

import math
import json
import os
import pipes
import base64
import sys
import random

from openopt import GLP
from numpy import *


PARAMS = {
  "72": {
    "yaw": 0,
    "frontpanels_angle": 0.3,
    "backpanels_angle": 0,
    "fast_cycle_1_start": 3.07,
    "fast_cycle_1_length": 1.74,
    "fast_cycle_1_accel": 0.31,
    "fast_cycle_2_start": 4.93,
    "fast_cycle_2_length": 2.09,
    "fast_cycle_2_accel": 0.31
  },
  "74": {
    "yaw": 0,
    "frontpanels_angle": 0.34,
    "backpanels_angle": 0,
    "fast_cycle_1_start": 3.07,
    "fast_cycle_1_length": 1.74,
    "fast_cycle_1_accel": 0.31,
    "fast_cycle_2_start": 4.93,
    "fast_cycle_2_length": 2.09,
    "fast_cycle_2_accel": 0.31
  },
  "-70": {
    "yaw": 0,
    "frontpanels_angle": 0.4,
    "backpanels_angle": 0,
    "fast_cycle_1_start": 3.07,
    "fast_cycle_1_length": 1.74,
    "fast_cycle_1_accel": 0.31,
    "fast_cycle_2_start": 4.93,
    "fast_cycle_2_length": 2.09,
    "fast_cycle_2_accel": 0.31
  },
  "-74": {
    "yaw": 0,
    "backpanels_angle": 0.17439514350525442, "frontpanels_angle": -0.28738534366121887,
    "fast_cycle_1_start": 3.07,
    "fast_cycle_1_length": 1.74,
    "fast_cycle_1_accel": 0.15,
    "fast_cycle_2_start": 4.93,
    "fast_cycle_2_length": 2.09,
    "fast_cycle_2_accel": 0.21
  },

  #example
  "-72": {
    "yaw": 0,
    "frontpanels_angle": 0.4,
    "backpanels_angle": 0,
    "fast_cycle_1_start": 3.07,
    "fast_cycle_1_length": 1.74,
    "fast_cycle_1_accel": 0.15,
    "fast_cycle_2_start": 4.93,
    "fast_cycle_2_length": 2.09,
    "fast_cycle_2_accel": 0.21
  },
  "70": {
    "yaw": 0,
    "frontpanels_angle": 0.4,
    "backpanels_angle": 0,
    "fast_cycle_1_start": 3.07,
    "fast_cycle_1_length": 1.74,
    "fast_cycle_1_accel": 0.15,
    "fast_cycle_2_start": 4.93,
    "fast_cycle_2_length": 2.09,
    "fast_cycle_2_accel": 0.21
  },

  # competition
  "75": {
    "yaw": 0,
    "frontpanels_angle": 0.4,
    "backpanels_angle": 0,
    "fast_cycle_1_start": 3.07,
    "fast_cycle_1_length": 1.74,
    "fast_cycle_1_accel": 0.31,
    "fast_cycle_2_start": 4.93,
    "fast_cycle_2_length": 2.09,
    "fast_cycle_2_accel": 0.31
  }
}

beta = sys.argv[1]

VARS = [

  #name, #lower bound, #upper bound

  ["yaw", 0, 0], #math.radians(7))
  ["frontpanels_angle",-0.5,0.5],
  ["backpanels_angle",-0.5,0.5],
  ["fast_cycle_1_start",2,4],
  ["fast_cycle_1_length",0,3],
  ["fast_cycle_1_accel",0,0.4],
  ["fast_cycle_2_start",4,6],
  ["fast_cycle_2_length",0,3],
  ["fast_cycle_2_accel",0,0.4]
]

var_names = [x[0] for x in VARS]
lbs = [x[1] for x in VARS]
ubs = [x[2] for x in VARS]
startPoint = [PARAMS[str(beta)][v] for v in var_names]

try:

  fresults = open("bestbeta%s.json" % beta, "r")
  best = json.load(fresults)
  fresults.close()
except:
  best = [0, {}]

def getscore(variables):
  global best

  vars = {}
  vars[beta] = {}
  for i in range(0, len(var_names)):
    vars[beta][var_names[i]] = variables[i]

  #print vars
  arg = "./cli.py %s" % base64.b64encode(json.dumps(vars))
  cmd = "java -jar ISSVis.jar -exec '%s' -beta %s" % (arg, beta)
  #print cmd
  f = os.popen(cmd)
  out = f.read()
  #print out
  if "ERROR" in out:
    #print "ERROR FOR BETA=%s\n\n\n %s" % (beta, out)
    return 0

  ret =  float(out.split("\n")[-2].split(" = ")[1])
  
  if True: #ret>150000:
    print "%s %s" % (ret, vars)

  if ret>best[0]:
    print "NEW BEST!"
    fresults = open("bestbeta%s.json" % beta, "w")
    best = [ret, vars]
    json.dump(best, fresults)
    fresults.close()

  return ret



p = GLP(getscore, x0=startPoint, lb=lbs, ub=ubs, maxIter=3, maxFunEvals=6, maxTime = 100,  maxCPUTime = 300, population=2, searchDirectionStrategy="best", baseVectorStrategy="best")
p.fTol = 0.1

r = p.maximize('de',iprint=1,plot=1,maxIter=3, maxFunEvals=6)

print p.xf, p.ff, p.rf