#!/usr/bin/env python

# Import PuLP modeler functions
from openopt import NSP

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


 before new sarj algo

 -70  160798.700073
72  159882.296645
-74 152057.208777
74  148647.864878
avg : 155346.517593

{"-70": {"fast_cycle_4_start": 4.285508941497646, "fast_cycle_2_prelength": 0.06295149295285885, "fast_cycle_1_start": 0.17595087829781378, "fast_cycle_5_start": 2.832121025678209, "fast_cycle_7_length": 0.0, "fast_cycle_1_length": 0.6935248861025821, "backpanels_angle": -0.0014026374642177606, "fast_cycle_3_prelength": 0.6166746766006286, "fast_cycle_7_start": 0.0, "frontpanels_angle": -0.0038904449964589625, "yaw": 0.0414804736024119, "fast_cycle_5_prelength": 0.08173443464544534, "fast_cycle_2_length": 0.35373380958548906, "fast_cycle_3_start": 2.237929382275514, "fast_cycle_4_length": 0.07166235965547048, "fast_cycle_1_prelength": 0.9344070980381314, "fast_cycle_6_length": 0.22315927730537782, "fast_cycle_8_start": 0.0, "fast_cycle_6_prelength": 0.17252622656447325, "fast_cycle_3_length": 0.7008364263314133, "fast_cycle_4_prelength": 0.5534151889537027, "fast_cycle_2_start": 0.6895750308475449, "fast_cycle_7_prelength": 0.0, "fast_cycle_5_length": 0.5634218448077157, "fast_cycle_8_length": 0.0, "fast_cycle_6_start": 4.898824827044014, "fast_cycle_8_prelength": 0.0},
 "72": {"backpanels_angle": -0.02032409144504553, "fast_cycle_3_start": 1.9179132087585402, "fast_cycle_3_prelength": 0.6720849953137594, "fast_cycle_4_length": 0.019490166270924144, "fast_cycle_2_start": 0.8954338239552325, "fast_cycle_4_start": 4.370219485764188, "fast_cycle_2_prelength": 0.28037852347261194, "fast_cycle_6_length": 0.24433323024728826, "fast_cycle_1_start": 0.016893475792793506, "fast_cycle_1_length": 0.03993646661426549, "fast_cycle_5_prelength": 0.6163168265418921, "fast_cycle_5_start": 2.903707578725052, "fast_cycle_5_length": 0.3152570215448386, "fast_cycle_6_prelength": 0.40040928196960496, "fast_cycle_2_length": 0.46515020825356856, "fast_cycle_6_start": 4.899632661924799, "fast_cycle_4_prelength": 0.5236651653653963, "frontpanels_angle": 0.011895802947803263, "yaw": 0.0001777557132575147, "fast_cycle_3_length": 0.40059491989964013, "fast_cycle_1_prelength": 0.5863264558380866},
 "74": {"backpanels_angle": -0.06425284635424487, "fast_cycle_3_start": 2.225200835647714, "fast_cycle_3_prelength": 0.003315289454355025, "fast_cycle_4_length": 0.024308427097226342, "fast_cycle_2_start": 0.820239331043713, "fast_cycle_4_start": 4.615481260894112, "fast_cycle_2_prelength": 0.5649022850943893, "fast_cycle_6_length": 0.2178386535284853, "fast_cycle_1_start": 0.0859978840153225, "fast_cycle_1_length": 0.3915483117365642, "fast_cycle_5_prelength": 0.003866266663166723, "fast_cycle_5_start": 2.958118920980893, "fast_cycle_5_length": 0.30318154576694, "fast_cycle_6_prelength": 0.21170048431356975, "fast_cycle_2_length": 0.028139875005793187, "fast_cycle_6_start": 5.0385427983053805, "fast_cycle_4_prelength": 0.5031835137957196, "frontpanels_angle": 0.017089584708456763, "yaw": 0.0, "fast_cycle_3_length": 0.02092372384431028, "fast_cycle_1_prelength": 0.6951678499746428},
 "-74": {"fast_cycle_4_start": 4.745282814110465, "fast_cycle_2_prelength": 0.5383338465664779, "fast_cycle_1_start": 2.7720317689706624, "fast_cycle_5_start": 2.497828361022921, "fast_cycle_7_length": 0.0, "fast_cycle_1_length": 0.47768584508748724, "backpanels_angle": 0.06579061320841215, "fast_cycle_3_prelength": 0.22044160746709926, "fast_cycle_7_start": 0.0, "frontpanels_angle": 0.045345543806413015, "yaw": 0.025378081288875143, "fast_cycle_5_prelength": 0.0187932917270459, "fast_cycle_2_length": 0.023215732759460428, "fast_cycle_3_start": 1.9983016826923432, "fast_cycle_4_length": 0.361422243194243, "fast_cycle_1_prelength": 0.2784959548493998, "fast_cycle_6_length": 0.2802575080475719, "fast_cycle_8_start": 0.0, "fast_cycle_6_prelength": 0.12824500144311507, "fast_cycle_3_length": 0.3126931834589215, "fast_cycle_4_prelength": 0.3199249359758594, "fast_cycle_2_start": 0.40977295481606, "fast_cycle_7_prelength": 0.0, "fast_cycle_5_length": 0.35909821065937103, "fast_cycle_8_length": 0.0, "fast_cycle_6_start": 5.178323186469656, "fast_cycle_8_prelength": 0.0}}

"""


# Parameters are determined in function of the beta angle.
# There is a fixed list of beta angles so we can over-optimize for that...
PARAMS = {"-70": {"sarjd_12": -0.17770814624297943, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.18234192299077615, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.004570466040045529, "sarjd_20": 0.29762632934120725, "sarjp_48": 3.27818363852848, "sarjd_60": 0.21919145588304217, "sarjd_48": -0.010469537582144132, "sarjd_64": 0.23906345239334198, "sarjd_68": -0.15343975917277974, "sarjd_40": 0.2540202420358353, "sarjd_44": -0.29801845972494295, "backpanels_angle": -0.0005626978728677377, "sarjd_0": -0.23870367391881286, "frontpanels_angle": -0.0018021451210250064, "sarjd_4": 0.0797586293245712, "yaw": 0.0416280513684409, "sarjd_32": 0.07867357948820666, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.29518411159183006, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.2674489086140967, "sarjp_0": 0.0, "sarjd_76": -0.1526323389301328, "sarjd_52": -0.26690737194872904, "sarjd_72": 0.024018931931874654, "sarjd_56": -0.06009597614831791, "sarjd_84": 0.2999149298722825, "sarjd_8": -0.21263983948941226, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.2995230580391146, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.22702107145777983},
 "72": {"sarjd_12": 0.04660243952029262, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.18204667247249318, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.04467067367239206, "sarjd_20": 0.2994263532127694, "sarjp_48": 3.27818363852848, "sarjd_60": 0.2662798664139182, "sarjd_48": 0.03642846898929212, "sarjd_64": 0.23619492335427258, "sarjd_68": -0.1609815310219587, "sarjd_40": -0.12313916126853235, "sarjd_44": -0.18987532167448645, "backpanels_angle": -0.014731268451499838, "sarjd_0": 0.033706121881376325, "frontpanels_angle": 0.005921783893742168, "sarjd_4": 0.11436706241711082, "yaw": 0.0004957706763891608, "sarjd_32": -0.1691250271829811, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.14567316748739412, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.1682710649243153, "sarjp_0": 0.0, "sarjd_76": -0.06324744929934911, "sarjd_52": -0.20336694960181267, "sarjd_72": 0.12898535560733598, "sarjd_56": 0.20998818941187436, "sarjd_84": 0.2830994962737556, "sarjd_8": 0.185591296234241, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.261109791732945, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.17855023094124917},
 "74": {"sarjd_12": 0.09614519477998802, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.03447155697763723, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.051031081254910744, "sarjd_20": 0.29681878914596166, "sarjp_48": 3.27818363852848, "sarjd_60": 0.14014930622132693, "sarjd_48": 0.03032968966735536, "sarjd_64": 0.29865609726706777, "sarjd_68": -0.05423205538037699, "sarjd_40": -0.04128281866781282, "sarjd_44": -0.2143889947683093, "backpanels_angle": -0.11105314394448565, "sarjd_0": -0.13598495157710686, "frontpanels_angle": 0.02111383346866192, "sarjd_4": 0.13767633750731653, "yaw": 0.0, "sarjd_32": 0.02651786729399566, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.108437565836883, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.1226370567570091, "sarjp_0": 0.0, "sarjd_76": -0.09483521909243034, "sarjd_52": -0.14663286999684685, "sarjd_72": 0.14292693002490608, "sarjd_56": 0.20358364136321183, "sarjd_84": 0.27900085185021456, "sarjd_8": 0.12371354048387162, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.2813639307840698, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.12327857178581807},
 "-74": {"sarjd_12": -0.11250737650394071, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.1603235144746309, "sarjp_40": 2.7318196987737333, "sarjd_24": -0.021540932246100597, "sarjd_20": 0.2991344606929204, "sarjp_48": 3.27818363852848, "sarjd_60": -0.0002904540082842228, "sarjd_48": -0.07691025079874836, "sarjd_64": 0.29193726297206113, "sarjd_68": -0.29173783024371236, "sarjd_40": -0.2753268252941663, "sarjd_44": -0.26769145134795125, "backpanels_angle": 0.08293409480542584, "sarjd_0": 0.28490838153190784, "frontpanels_angle": 0.038949912370479095, "sarjd_4": 0.0771028304964696, "yaw": 0.02099660013660592, "sarjd_32": -0.0460351553846802, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.17516701888875963, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.1826886480892882, "sarjp_0": 0.0, "sarjd_76": -0.1873847569592944, "sarjd_52": -0.2848656787874202, "sarjd_72": 0.013958834602915726, "sarjd_56": -0.06489327906415357, "sarjd_84": 0.12610682612486412, "sarjd_8": 0.08713961639018108, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.20207489452371433, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.18931981362533032}}
 


def toalpha(minute):
  return math.radians(minute * 360.0 / 92)

beta = sys.argv[1]

VARS = [

  #name, #lower bound, #upper bound

  ["yaw", 0, math.radians(7), False],


  ["backpanels_angle",-0.2,0.2,False],
  ["frontpanels_angle",-0.2,0.2,False],


]
test_cycles = True

rng = "0-91"
if len(sys.argv)>2:
  rng = sys.argv[2]

start_range = int(rng.split("-")[0])
stop_range = min(91,int(rng.split("-")[1]))

for i in range(start_range, stop_range):
  if i % 4 == 0:
    VARS.append(["sarjp_%s" % i,toalpha(max(0,i-2)),toalpha(min(i+2,91)),False,toalpha(i)])
    VARS.append(["sarjd_%s" % i, -0.35, 0.35, test_cycles])


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
      if len(k)>4:
        vars[beta][k[0]] = k[4]
      else:
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
          "range":rng,
          "beta":beta,
          "tested_vars":var_names
        })
      except Exception, e:
        print "MONGO INSERT ERROR:%s" % e

  return ret



p = GLP(getscore, x0=startPoint, lb=lbs, ub=ubs, maxIter=1000, maxFunEvals=10000)
p.fOpt = 170000 #Optimal value we could have

r = p.maximize('de', iprint=1, plot=0) #, population=10) #, searchDirectionStrategy="best")
#r = p.maximize('galileo', iprint=1, plot=1, population=5)
#r = p.maximize('gsubg', iprint=1, plot=0)

#r = p.maximize('asa', iprint=1, plot=1)

print "Solution vector: %s" % p.xf
print "Max value: %s" % p.ff