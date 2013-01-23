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


"""
other insteresting possible starts:
{"72": {"backpanels_angle": -0.058081170108740809, "frontpanels_angle": 0.096524828897619264, "fast_cycle_2_accel": 0.3131072637717327, "yaw": 0.0, "fast_cycle_1_start": 2.191132510985939, "fast_cycle_1_length": 0.64123387684647237, "fast_cycle_1_accel": 0.13249386279639749, "fast_cycle_2_length": 1.6653094751964459, "fast_cycle_2_start": 4.9912847588147446}
[152382.1368978579, {"74": {"backpanels_angle": 0.0, "frontpanels_angle": 0.34000000000000002, "fast_cycle_2_accel": 0.31, "yaw": 0.0, "fast_cycle_1_start": 3.0699999999999998, "fast_cycle_1_length": 1.74, "fast_cycle_1_accel": 0.31, "fast_cycle_2_length": 2.0899999999999999, "fast_cycle_2_start": 4.9299999999999997}}]
[158538.77428211164, {"-70": {"backpanels_angle": -0.058081170108740809, "frontpanels_angle": 0.096524828897619264, "fast_cycle_2_accel": 0.3131072637717327, "yaw": 0.0, "fast_cycle_1_start": 2.191132510985939, "fast_cycle_1_length": 0.64123387684647237, "fast_cycle_1_accel": 0.13249386279639749, "fast_cycle_2_length": 1.6653094751964459, "fast_cycle_2_start": 4.9912847588147446}}]

"""
PARAMS = {
  "72": {"backpanels_angle": 0.0033042337152939865, "frontpanels_angle": -0.01056640892439243, "fast_cycle_2_accel": 0.3428089319992873, "yaw": 0.0, "fast_cycle_1_start": 3.0776485207915103, "fast_cycle_1_length": 1.7427536927878089, "fast_cycle_1_accel": 0.31596510086613522, "fast_cycle_2_length": 2.0889489709868618, "fast_cycle_2_start": 4.926173498557965},
  "74": {"backpanels_angle": 0.0, "frontpanels_angle": 0.33000000000000002, "fast_cycle_2_accel": 0.31, "yaw": 0.0, "fast_cycle_1_start": 3.0699999999999998, "fast_cycle_1_length": 1.74, "fast_cycle_1_accel": 0.31, "fast_cycle_2_length": 2.0899999999999999, "fast_cycle_2_start": 4.9299999999999997},
  "-70": {"backpanels_angle": 0.00077547121336952074, "frontpanels_angle": 0.0080927148776482015, "fast_cycle_2_accel": 0.27364128093748397, "yaw": 0.0, "fast_cycle_1_start": 3.0739091675605743, "fast_cycle_1_length": 1.7409763869535488, "fast_cycle_1_accel": 0.30972196648796291, "fast_cycle_2_length": 2.2001081667798479, "fast_cycle_2_start": 4.8524435650820354},
  "-74": {"backpanels_angle": 0.17224776864608016, "frontpanels_angle": -0.29483245917231549, "fast_cycle_2_accel": 0.20905563634834368, "yaw": 0.0, "fast_cycle_1_start": 3.0699986441940013, "fast_cycle_1_length": 1.7399720037085906, "fast_cycle_1_accel": 0.1497756507810214, "fast_cycle_2_length": 2.0898894192387836, "fast_cycle_2_start": 4.9299050494815209},


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
  "70": {"backpanels_angle": -0.15463899577456608, "frontpanels_angle": -0.031156437841873164, "fast_cycle_2_accel": 0.15097816777464132, "yaw": 0.0, "fast_cycle_1_start": 3.8116338629615298, "fast_cycle_1_length": 2.2348404440689351, "fast_cycle_1_accel": 0.09516664073371689, "fast_cycle_2_length": 2.9033926538153909, "fast_cycle_2_start": 5.6560269696997105},

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

  ["yaw", 0, math.radians(7)],
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



p = GLP(getscore, x0=startPoint, lb=lbs, ub=ubs, maxIter=100, maxFunEvals=1000)
#p.fTol = 0.1

r = p.maximize('gsubg',iprint=1,plot=0)

print p.xf, p.ff, p.rf