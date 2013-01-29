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


"""
  previous records
  -70 159690.936647
72  159563.367508
74  151970.655485
-74 151120.091727
avg : 155586.262842

  {"-70": {"yaw": 0.04170866578798351, "fast_cycle_1_length": 2.209095811369916, "fast_cycle_2_start": 4.8659370866617095, "fast_cycle_2_length": 1.2275974062453887, "fast_cycle_1_start": 2.2478111611667826},
 "72": {"yaw": 0.000814215950018912, "fast_cycle_1_length": 1.48646275448066, "fast_cycle_2_start": 4.917877552930615, "fast_cycle_2_length": 1.3531442319718265, "fast_cycle_1_start": 2.908485444884828},
 "74": {"backpanels_phase": 1.7955624990894643, "backpanels_angle": -0.08011121485432518, "frontpanels_angle": 0.34476690892469347, "fast_cycle_2_accel": 0.2399412725174822, "backpanels_amplitude": -0.03280679613872517, "frontpanels_phase": 2.7945735325886796, "fast_cycle_1_start": 3.0806075316995525, "fast_cycle_1_length": 1.7409493623038732, "fast_cycle_1_accel": 0.23923337055832766, "fast_cycle_2_length": 2.0885153470649493, "frontpanels_amplitude": 2.1312337782269304, "yaw": 2.2663250365290128e-05, "fast_cycle_2_start": 4.933348883207836},
 "-74": {"backpanels_phase": 0.0, "backpanels_angle": 0.06072343146429608, "frontpanels_angle": -0.29801433814516826, "fast_cycle_2_accel": 0.18080358853662248, "backpanels_amplitude": 0.0, "frontpanels_phase": 0.0, "fast_cycle_1_start": 3.0699925251289315, "fast_cycle_1_length": 1.7398855546485446, "fast_cycle_1_accel": 0.14890684738160895, "fast_cycle_2_length": 2.1793131225704654, "frontpanels_amplitude": 0.0, "yaw": 0.0, "fast_cycle_2_start": 4.929439382577715}}
"""


# Parameters are determined in function of the beta angle.
# There is a fixed list of beta angles so we can over-optimize for that...
PARAMS = {"-70": {"fast_cycle_3_start": 2.237929382275514, "fast_cycle_4_prelength": 0.5534151889537027, "fast_cycle_3_prelength": 0.6166746766006286, "fast_cycle_4_length": 0.07166235965547048, "fast_cycle_1_prelength": 0.9344070980381314, "fast_cycle_4_start": 4.285508941497646, "fast_cycle_2_start": 0.6895750308475449, "fast_cycle_2_prelength": 0.06295149295285885, "fast_cycle_1_start": 0.1759508632978138, "fast_cycle_1_length": 0.6935248861025821, "fast_cycle_5_prelength": 0.08173443464544534, "fast_cycle_5_start": 2.832121025678209, "fast_cycle_5_length": 0.5634218448077157, "fast_cycle_6_prelength": 0.17252622656447325, "fast_cycle_2_length": 0.35373380958548906, "fast_cycle_6_start": 4.898824827044014, "yaw": 0.0414804736024119, "fast_cycle_6_length": 0.22315927730537782, "fast_cycle_3_length": 0.7008364263314133},
 "72": {"fast_cycle_3_start": 1.9179132087585402, "fast_cycle_4_prelength": 0.5236651653653963, "fast_cycle_3_prelength": 0.6720849953137594, "fast_cycle_4_length": 0.019490166270924144, "fast_cycle_1_prelength": 0.5863264558380866, "fast_cycle_4_start": 4.370219485764188, "fast_cycle_2_start": 0.8954338239552325, "fast_cycle_2_prelength": 0.28037852347261194, "fast_cycle_1_start": 0.016893475792793506, "fast_cycle_1_length": 0.03993646661426549, "fast_cycle_5_prelength": 0.6163168265418921, "fast_cycle_5_start": 2.903707578725052, "fast_cycle_5_length": 0.3152570215448386, "fast_cycle_6_prelength": 0.40040928196960496, "fast_cycle_2_length": 0.46515020825356856, "fast_cycle_6_start": 4.899632661924799, "yaw": 0.0001777557132575147, "fast_cycle_6_length": 0.24433323024728826, "fast_cycle_3_length": 0.40059491989964013},
 "74": {"fast_cycle_3_start": 2.225200835647714, "fast_cycle_4_prelength": 0.5031835137957196, "fast_cycle_3_prelength": 0.003315289454355025, "fast_cycle_4_length": 0.024308427097226342, "fast_cycle_1_prelength": 0.6951678499746428, "fast_cycle_4_start": 4.615481260894112, "fast_cycle_2_start": 0.820239331043713, "fast_cycle_2_prelength": 0.5649022850943893, "fast_cycle_1_start": 0.0859978840153225, "fast_cycle_1_length": 0.3915483117365642, "fast_cycle_5_prelength": 0.003866266663166723, "fast_cycle_5_start": 2.958118920980893, "fast_cycle_5_length": 0.30318154576694, "fast_cycle_6_prelength": 0.21170048431356975, "fast_cycle_2_length": 0.028139875005793187, "fast_cycle_6_start": 5.0385427983053805, "yaw": 0.0, "fast_cycle_6_length": 0.2178386535284853, "fast_cycle_3_length": 0.02092372384431028},
 "-74": {"fast_cycle_3_start": 1.9983016826923432, "fast_cycle_4_prelength": 0.3199249359758594, "fast_cycle_3_prelength": 0.22044160746709926, "fast_cycle_4_length": 0.361422243194243, "fast_cycle_1_prelength": 0.2784959548493998, "fast_cycle_4_start": 4.745282814110465, "fast_cycle_2_start": 0.40977295481606, "fast_cycle_2_prelength": 0.5383338465664779, "fast_cycle_1_start": 2.7720317689706624, "fast_cycle_1_length": 0.47768584508748724, "fast_cycle_5_prelength": 0.0187932917270459, "fast_cycle_5_start": 2.497828361022921, "fast_cycle_5_length": 0.35909821065937103, "fast_cycle_6_prelength": 0.12824500144311507, "fast_cycle_2_length": 0.023215732759460428, "fast_cycle_6_start": 5.178323186469656, "yaw": 0.020688516408021457, "fast_cycle_6_length": 0.2802575080475719, "fast_cycle_3_length": 0.3126931834589215}}

 


def toalpha(minute):
  return math.radians(minute * 360.0 / 92)

beta = sys.argv[1]

VARS = [

  #name, #lower bound, #upper bound

  ["yaw", 0, math.radians(7), False],

  #["frontpanels_angle",-0.5,0.5, False],
  #["frontpanels_amplitude",-4,4,False],
  #["frontpanels_phase",0,2 * math.pi,False],
  
  #["backpanels_angle",-0.5,0.5,False],
  #["backpanels_amplitude",-4,4,False],
  #["backpanels_phase",0,2 * math.pi,False],

  ["fast_cycle_1_start",toalpha(0),toalpha(10),False],
  ["fast_cycle_1_length",0,1,False],
  ["fast_cycle_1_prelength",0,1,False],

  ["fast_cycle_2_start",toalpha(10),toalpha(20),False],
  ["fast_cycle_2_length",0,1,False],
  ["fast_cycle_2_prelength",0,1,False],

  ["fast_cycle_3_start",toalpha(20),toalpha(35),False],
  ["fast_cycle_3_length",0,1,False],
  ["fast_cycle_3_prelength",0,1,False],

  ["fast_cycle_5_start",toalpha(35),toalpha(50),False],
  ["fast_cycle_5_length",0,1,False],
  ["fast_cycle_5_prelength",0,1,False],

  ["fast_cycle_4_start",toalpha(50),toalpha(70),False],
  ["fast_cycle_4_length",0,1,False],
  ["fast_cycle_4_prelength",0,1,False],

  ["fast_cycle_6_start",toalpha(70),toalpha(91),False],
  ["fast_cycle_6_length",0,1,False],
  ["fast_cycle_6_prelength",0,1,False],

  ["backpanels_angle",-0.4,0.4,True],
  ["frontpanels_angle",-0.4,0.4,True]


]



var_names = [x[0] for x in VARS if x[3]]
lbs = [x[1] for x in VARS if x[3]]
ubs = [x[2] for x in VARS if x[3]]
startPoint = [PARAMS[str(beta)].get(v, 0) for v in var_names]


DB=False
try:
  mongoClient = pymongo.MongoClient("mongodb://iss:station@linus.mongohq.com:10066/iss-results")
  DB = mongoClient["iss-results"]
except Exception, e:
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
      except Exception, e:
        print "MONGO INSERT ERROR:%s" % e

  return ret



p = GLP(getscore, x0=startPoint, lb=lbs, ub=ubs, maxIter=100, maxFunEvals=10000)
p.fOpt = 170000 #Optimal value we could have

r = p.maximize('de', iprint=1, plot=0, population=20) #, searchDirectionStrategy="best")
#r = p.maximize('galileo', iprint=1, plot=0, population=5)
#r = p.maximize('gsubg', iprint=1, plot=0)

print "Solution vector: %s" % p.xf
print "Max value: %s" % p.ff