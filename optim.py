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
import pymongo
import copy
import datetime

from openopt import GLP
from numpy import *




PARAMS = {
  "72": {"backpanels_angle": -0.011238028948746618, "backpanels_phase": 0, "frontpanels_angle": 0.0047764511116933795, "fast_cycle_2_accel": 0.3393155573771829, "backpanels_amplitude": 0, "frontpanels_phase": 0, "fast_cycle_1_start": 3.085909302203207, "fast_cycle_1_length": 1.7438042093649595, "fast_cycle_1_accel": 0.2994846417296466, "fast_cycle_2_length": 2.077661185972699, "frontpanels_amplitude": 0, "yaw": 0.0, "fast_cycle_2_start": 4.916099606471066},
  "74": {"backpanels_angle": -0.037320679095769964, "backpanels_phase": 5.203600120166685, "frontpanels_angle": 0.31232240374470255, "fast_cycle_2_accel": 0.2399412725174822, "backpanels_amplitude": 2.852731138532168, "frontpanels_phase": 5.410925822519583, "fast_cycle_1_start": 3.0806075316995525, "fast_cycle_1_length": 1.7409493623038732, "fast_cycle_1_accel": 0.23923337055832766, "fast_cycle_2_length": 2.0885153470649493, "frontpanels_amplitude": -0.5077690526785859, "yaw": 0.0002997225746568166, "fast_cycle_2_start": 4.933348883207836},
  
  "-70": {"backpanels_angle": -0.14088013083327708, "backpanels_phase": 0, "frontpanels_angle": 0.002204760114096262, "fast_cycle_2_accel": 0.35193894017534844, "backpanels_amplitude": 0, "frontpanels_phase": 0, "fast_cycle_1_start": 3.206457403168373, "fast_cycle_1_length": 1.7713782005406706, "fast_cycle_1_accel": 0.34986622845796067, "fast_cycle_2_length": 2.1472054569607355, "frontpanels_amplitude": 0, "yaw": 0.0, "fast_cycle_2_start": 4.793289129449869},
  #"-74": {'backpanels_angle': -0.0016813148769646935, 'frontpanels_angle': -0.31543461601882539, 'fast_cycle_2_accel': 0.18080358853662248, 'yaw': 0.0, 'fast_cycle_1_start': 3.0699925251289315, 'fast_cycle_1_length': 1.7398855546485446, 'fast_cycle_1_accel': 0.14890684738160895, 'fast_cycle_2_length': 2.1793131225704654, 'fast_cycle_2_start': 4.929439382577715},
  "-74": {"backpanels_angle": 0.060723431464296082, "backpanels_phase": 0, "frontpanels_angle": -0.29801433814516826, "fast_cycle_2_accel": 0.18080358853662248, "backpanels_amplitude": 0, "frontpanels_phase": 0, "fast_cycle_1_start": 3.0699925251289315, "fast_cycle_1_length": 1.7398855546485446, "fast_cycle_1_accel": 0.14890684738160895, "fast_cycle_2_length": 2.1793131225704654, "frontpanels_amplitude": 0, "yaw": 0, "fast_cycle_2_start": 4.929439382577715},


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

  ["yaw", 0, math.radians(7),False],

  ["frontpanels_angle",-0.5,0.5,True],
  ["frontpanels_amplitude",-3,3,False],
  ["frontpanels_phase",0,2 * math.pi,False],
  
  ["backpanels_angle",-0.5,0.5,True],
  ["backpanels_amplitude",-3,3,False],
  ["backpanels_phase",0,2 * math.pi,False],

  ["fast_cycle_1_start",2,4,False],
  ["fast_cycle_1_length",0,3,False],
  ["fast_cycle_1_accel",0,0.4,False],
  ["fast_cycle_2_start",4,6,False],
  ["fast_cycle_2_length",0,3,False],
  ["fast_cycle_2_accel",0,0.4,False]

]



var_names = [x[0] for x in VARS if x[3]]
lbs = [x[1] for x in VARS if x[3]]
ubs = [x[2] for x in VARS if x[3]]
startPoint = [PARAMS[str(beta)].get(v, 0) for v in var_names]


DB=False
try:
  mongoClient = pymongo.MongoClient("mongodb://iss:station@linus.mongohq.com:10066/iss-results")
  DB = mongoClient["iss-results"]
except e:
  print "No Mongo: %s" % e


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

  tested_vars = copy(vars[beta])

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

    if DB:
      try:
        DB.results.insert({
          "score":best[0],
          "date":datetime.datetime.now(),
          "params":vars[beta],
          "beta":beta,
          "tested_vars":var_names
        })
      except e:
        print "MONGO INSERT ERROR:%s" % e

  return ret



p = GLP(getscore, x0=startPoint, lb=lbs, ub=ubs, maxIter=100, maxFunEvals=10000)
p.fOpt = 170000 #Optimal value we could have

r = p.maximize('de', iprint=1, plot=0, population=10) #, searchDirectionStrategy="best")
#r = p.maximize('galileo', iprint=1, plot=0, population=5)

connection["iss-results"].results.insert({

})


print "Solution vector: %s" % p.xf
print "Max value: %s" % p.ff