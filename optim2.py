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
  "72": {'backpanels_angle': -0.0085394627603317379, 'frontpanels_angle': 0.023438086430557007, 'fast_cycle_2_accel': 0.33931555737718289, 'yaw': 0.0, 'fast_cycle_1_start': 3.0859093022032069, 'fast_cycle_1_length': 1.7438042093649595, 'fast_cycle_1_accel': 0.29948464172964662, 'fast_cycle_2_length': 2.077661185972699, 'fast_cycle_2_start': 4.9160996064710663},
  "74": {'backpanels_angle': -0.040463658494283905, 'backpanels_phase': 5.2036001201666853, 'frontpanels_angle': 0.31768531282514034, 'fast_cycle_2_accel': 0.2399412725174822, 'backpanels_amplitude': 2.8527311385321679, 'frontpanels_phase': 5.4109258225195829, 'fast_cycle_1_start': 3.0806075316995525, 'fast_cycle_1_length': 1.7409493623038732, 'fast_cycle_1_accel': 0.23923337055832766, 'fast_cycle_2_length': 2.0885153470649493, 'frontpanels_amplitude': -0.50776905267858585, 'yaw': 0.00029972257465681659, 'fast_cycle_2_start': 4.933348883207836},
  
  "-70": {'backpanels_angle': -0.0031205354155288837, 'frontpanels_angle': 0.003306896943848182, 'fast_cycle_2_accel': 0.35193894017534844, 'yaw': 0.0, 'fast_cycle_1_start': 3.2064574031683728, 'fast_cycle_1_length': 1.7713782005406706, 'fast_cycle_1_accel': 0.34986622845796067, 'fast_cycle_2_length': 2.1472054569607355, 'fast_cycle_2_start': 4.7932891294498692},
  #"-74": {'backpanels_angle': -0.0016813148769646935, 'frontpanels_angle': -0.31543461601882539, 'fast_cycle_2_accel': 0.18080358853662248, 'yaw': 0.0, 'fast_cycle_1_start': 3.0699925251289315, 'fast_cycle_1_length': 1.7398855546485446, 'fast_cycle_1_accel': 0.14890684738160895, 'fast_cycle_2_length': 2.1793131225704654, 'fast_cycle_2_start': 4.929439382577715},
  "-74": {'backpanels_angle': -0.0016813148769646935, 'frontpanels_angle': -0.30243461601882539, 'fast_cycle_2_accel': 0.18080358853662248, 'yaw': 0, 'fast_cycle_1_start': 3.0699925251289315, 'fast_cycle_1_length': 1.7398855546485446, 'fast_cycle_1_accel': 0.14890684738160895, 'fast_cycle_2_length': 2.1793131225704654, 'fast_cycle_2_start': 4.929439382577715},


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

  ["yaw", 0, math.radians(7),True],
  ["frontpanels_angle",-0.5,0.5,True],
  ["backpanels_angle",-0.5,0.5,True],
  ["frontpanels_amplitude",-3,3,True],
  ["backpanels_amplitude",-3,3,True],
  ["frontpanels_phase",0,2 * math.pi,True],
  ["backpanels_phase",0,2 * math.pi,True],

  ["fast_cycle_1_start",2,4,True],
  ["fast_cycle_1_length",0,3,True],
  ["fast_cycle_1_accel",0,0.4,True],
  ["fast_cycle_2_start",4,6,True],
  ["fast_cycle_2_length",0,3,True],
  ["fast_cycle_2_accel",0,0.4,True]

]

var_names = [x[0] for x in VARS if x[3]]
lbs = [x[1] for x in VARS if x[3]]
ubs = [x[2] for x in VARS if x[3]]
startPoint = [PARAMS[str(beta)].get(v, 0) for v in var_names]

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

  for k in VARS:
    if k[0] not in vars[beta]:
      vars[beta][k[0]] = PARAMS[str(beta)].get(k[0], 0)

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



p = GLP(getscore, x0=startPoint, lb=lbs, ub=ubs, maxIter=100, maxFunEvals=100000)
p.fTol = 0.00000001

r = p.maximize('gsubg',iprint=1,plot=0)

print p.xf, p.ff, p.rf