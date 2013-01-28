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





PARAMS = {"-70": {"backpanels_phase": 3.103508118113964, "backpanels_angle": -0.03661858312156795, "frontpanels_angle": 0.014295270420755898, "fast_cycle_2_accel": 0.35193894017534844, "backpanels_amplitude": -1.080347834250686, "frontpanels_phase": 2.9160227413940065, "fast_cycle_1_start": 3.206457403168373, "fast_cycle_1_length": 0.7713782005406706, "fast_cycle_1_accel": 0.34986622845796067, "fast_cycle_2_length": 0.6472054569607355, "frontpanels_amplitude": -0.8803043042143972, "yaw": 0.041480473602411905, "fast_cycle_2_start": 4.793289129449869},
 "72": {"backpanels_angle": -0.003316651371834394, "backpanels_phase": 0.0, "frontpanels_angle": -0.003659480987842902, "fast_cycle_2_accel": 0.3393155573771829, "backpanels_amplitude": 0.0, "frontpanels_phase": 0.0, "fast_cycle_1_start": 3.085909302203207, "fast_cycle_1_length": 0.7438042093649595, "fast_cycle_1_accel": 0.2994846417296466, "fast_cycle_2_length": 1.077661185972699, "frontpanels_amplitude": 0.0, "yaw": 0.04, "fast_cycle_2_start": 4.916099606471066},
 "74": {"backpanels_phase": 1.7955624990894643, "backpanels_angle": -0.08011121485432518, "frontpanels_angle": 0.34476690892469347, "fast_cycle_2_accel": 0.2399412725174822, "backpanels_amplitude": -0.03280679613872517, "frontpanels_phase": 2.7945735325886796, "fast_cycle_1_start": 3.0806075316995525, "fast_cycle_1_length": 1.7409493623038732, "fast_cycle_1_accel": 0.23923337055832766, "fast_cycle_2_length": 1.0885153470649493, "frontpanels_amplitude": 2.1312337782269304, "yaw": 2.2663250365290128e-05, "fast_cycle_2_start": 4.933348883207836},
 "-74": {'backpanels_phase': 1.1791692397657714, 'backpanels_angle': 0.06072343146429608, 'frontpanels_angle': -0.29801433814516826, 'fast_cycle_2_accel': 0.18080358853662248, 'backpanels_amplitude': -2.9927468158713895, 'frontpanels_phase': 5.966603964825565, 'fast_cycle_1_start': 3.0699925251289315, 'fast_cycle_1_length': 0.0, 'fast_cycle_1_accel': 0.14890684738160895, 'fast_cycle_2_length': 0.0, 'frontpanels_amplitude': -1.6956530978562752, 'yaw': 0.03, 'fast_cycle_2_start': 4.929439382577715}}




beta = sys.argv[1]

VARS = [

  #name, #lower bound, #upper bound

  ["yaw", 0, math.radians(7), True],

  #["frontpanels_angle",-0.5,0.5, False],
  #["frontpanels_amplitude",-4,4,False],
  #["frontpanels_phase",0,2 * math.pi,False],
  
  #["backpanels_angle",-0.5,0.5,False],
  #["backpanels_amplitude",-4,4,False],
  #["backpanels_phase",0,2 * math.pi,False],

  ["fast_cycle_1_start",2,4,True],
  ["fast_cycle_1_length",0,3,True],
  #["fast_cycle_1_accel",0,0.4,False],
  ["fast_cycle_2_start",4,6,True],
  ["fast_cycle_2_length",0,3,True],

  ["fast_cycle_3_start",0,2,True],
  ["fast_cycle_2_length",0,2,True],
  #["fast_cycle_2_accel",0,0.4,False]

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
    vars[beta][var_names[i]] = float(variables[i])

  tested_vars = copy(vars[beta])

  for k in VARS:
    if k[0] not in vars[beta]:
      vars[beta][k[0]] = float(PARAMS[str(beta)].get(k[0], 0))

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
      except e: #TODO not working?
        print "MONGO INSERT ERROR:%s" % e

  return ret



p = GLP(getscore, x0=startPoint, lb=lbs, ub=ubs, maxIter=100, maxFunEvals=10000)
p.fOpt = 170000 #Optimal value we could have

r = p.maximize('de', iprint=1, plot=0, population=40) #, searchDirectionStrategy="best")
#r = p.maximize('galileo', iprint=1, plot=0, population=5)
#r = p.maximize('gsubg', iprint=1, plot=0)

print "Solution vector: %s" % p.xf
print "Max value: %s" % p.ff