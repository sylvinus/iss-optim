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

PARAMS = {"-73": {"sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.17185025596085413, "sarjp_40": 2.7318196987737333, "sarjp_0": 0.0, "sarjd_24": 0.18690250592679253, "sarjd_20": -0.1976162318357546, "sarjp_48": 3.27818363852848, "sarjd_60": -0.19057760227310092, "sarjd_48": -0.1958366189055746, "sarjd_64": 0.15057077978649744, "sarjd_68": 0.1866701713384736, "sarjd_40": -0.2870706324729989, "sarjd_44": 0.18842004368831164, "backpanels_angle": 0.0, "sarjd_0": 0.18822778646572497, "frontpanels_angle": 0.0, "sarjd_4": 0.12200378052422954, "sarjd_8": -0.19974364348433335, "sarjd_32": -0.16867439625100691, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "blanket_correction": 34.00427082558695, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": 0.05515608848678487, "sarjp_16": 1.0927278795094932, "sarjp_4": 0.2731819698773733, "sarjd_12": 0.16311491218526425, "sarjd_76": -0.21976287568920227, "sarjd_52": -0.10015358589634983, "yaw": 5.291331808269014e-08, "sarjd_72": -0.1854950973341104, "sarjd_56": 0.20957325235776392, "sarjd_84": -0.177324576988608, "sarjp_76": 5.1904574276700925, "sarjd_16": 0.11642061485850469, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.0604248505915738, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.19545131722123746},
 "-71": {"sarjd_12": 0.3625555687902972, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjp_24": 1.63909181926424, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.31063853984504186, "sarjd_20": -0.42534741415808847, "sarjp_48": 3.27818363852848, "sarjd_60": -0.27142432638213504, "sarjd_48": -0.3079313733649128, "sarjd_64": 0.058394142744492644, "sarjd_68": 0.2472940555926893, "sarjd_40": -0.44999116790924165, "sarjd_28": -0.0987479012979564, "backpanels_angle": 0.0, "sarjd_0": 0.35310693699887596, "frontpanels_angle": 0.0, "sarjd_4": -0.08645553340772501, "sarjd_8": -0.44999726637309967, "sarjd_32": -0.3734400472281482, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjd_44": 0.3400569866831709, "sarjp_76": 5.1904574276700925, "blanket_correction": 26.29278589700497, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.08564563803348818, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.4444722996847188, "sarjp_0": 0.0, "sarjd_76": -0.14372854404660168, "sarjd_52": -0.37446065462637546, "yaw": 0.020254186184727817, "sarjd_72": -0.27400117287098935, "sarjd_56": 0.32925971974639917, "sarjd_84": -0.24825384557946314, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.04814166275176679, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.2862759152016461},
 "-75": {"sarjd_12": 0.1325317134811516, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjp_24": 1.63909181926424, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.10266946708818625, "sarjd_20": -0.09798653907949757, "sarjp_48": 3.27818363852848, "sarjd_60": -0.20322905907402808, "sarjd_48": -0.17093482345001101, "sarjd_64": 0.10136631987386141, "sarjd_68": 0.10470389699878081, "sarjd_40": -0.1991413080916789, "sarjd_28": -0.056702913132564585, "backpanels_angle": 0.0, "sarjd_0": 0.15782034112413498, "frontpanels_angle": 0.0, "sarjd_4": 0.08439082388937212, "sarjd_8": -0.1429867630590569, "sarjd_32": -0.13435394771468245, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjd_44": 0.06143314249856582, "sarjp_76": 5.1904574276700925, "sarjp_12": 0.81954590963212, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "blanket_correction": 87.47353685673646, "sarjp_84": 5.73682136742484, "sarjd_36": -0.030011658446713708, "sarjp_16": 1.0927278795094932, "sarjd_16": 0.07482031467302849, "sarjp_0": 0.0, "sarjd_76": -0.2751320492637541, "sarjd_52": -0.26045107510958826, "yaw": 0.03170057493148526, "sarjd_72": -0.2504165071912102, "sarjd_56": 0.13609678544134712, "sarjd_84": -0.25558720932413287, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.013534387502162553, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.14625483314917004},
 "75": {"sarjd_12": 0.1852505190439282, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": 0.12210907299182835, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.19654418235383989, "sarjd_20": -0.1676540092352865, "sarjp_48": 3.27818363852848, "sarjd_60": -0.11692770169618777, "sarjd_48": -0.15420817927350763, "sarjd_64": 0.16099118622742953, "sarjd_68": 0.187854560558365, "sarjd_40": -0.22282058934804577, "sarjd_44": 0.16846516907346967, "backpanels_angle": 0.0, "sarjd_0": 0.19134843988213454, "frontpanels_angle": 0.0, "sarjd_4": 0.15812253594026646, "sarjd_8": -0.16655318122110374, "sarjd_32": -0.10805195957447059, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "blanket_correction": 44.18897582771776, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": 0.1470889425812198, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.16765020994003513, "sarjp_0": 0.0, "sarjd_76": -0.2424379239657828, "sarjd_52": -0.1598120776167237, "yaw": 1.4073793344099197e-10, "sarjd_72": -0.0970864755677601, "sarjd_56": 0.20464880717285722, "sarjd_84": -0.17602761433094005, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.18263283129224078, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.21143267794090922},
 "73": {"sarjd_12": 0.19581661995004238, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjp_24": 1.63909181926424, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.19239173057594983, "sarjd_20": -0.1544493199519403, "sarjp_48": 3.27818363852848, "sarjd_60": -0.14502738900526507, "sarjd_48": -0.12155002853473132, "sarjd_64": 0.16350021192930853, "sarjd_68": 0.1797172298009327, "sarjd_40": -0.2002179010284047, "sarjd_28": -0.16468169330168694, "backpanels_angle": 0.0, "sarjd_0": 0.2030921967433989, "frontpanels_angle": 0.0, "sarjd_4": 0.17190764317943208, "sarjd_8": -0.1295818766503298, "sarjd_32": -0.08546862039974774, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjd_44": 0.10981079720813036, "sarjp_76": 5.1904574276700925, "blanket_correction": -17.828080036680905, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": 0.162192625411122, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.16468713278360814, "sarjp_0": 0.0, "sarjd_76": -0.2180426305798613, "sarjd_52": -0.24487912095448436, "yaw": 3.4361789526957238e-06, "sarjd_72": -0.12694945518417997, "sarjd_56": 0.21158411689751896, "sarjd_84": -0.17513179134521928, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.17668982362118388, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.21009421185459082},
 "71": {"sarjd_12": 0.3822778963979023, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.1511383137283257, "sarjp_40": 2.7318196987737333, "sarjp_28": 1.9122737891416133, "sarjd_20": -0.2883589905259634, "sarjp_48": 3.27818363852848, "sarjd_60": -0.2711709883037301, "sarjd_48": -0.19999408125816642, "sarjd_64": 0.052759702490762936, "sarjd_68": 0.44075022576842504, "sarjd_40": -0.4256157741990103, "sarjd_44": 0.43436666671250185, "backpanels_angle": 0.0, "sarjd_0": 0.4230387693825251, "frontpanels_angle": 0.0, "sarjd_4": 0.25831716090576085, "sarjd_8": -0.21679578185399592, "sarjd_32": -0.17745658607696588, "sarjp_8": 0.5463639397547466, "sarjd_24": 0.41484973764933053, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_12": 0.81954590963212, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "blanket_correction": 0.0, "sarjd_88": 0.17558411972390212, "sarjd_36": 0.14577481333715658, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.17282939146434687, "sarjp_0": 0.0, "sarjd_76": -0.05446729047651863, "sarjd_52": -0.4034684027143485, "yaw": 0.0, "sarjd_72": -0.3004236550628733, "sarjd_56": 0.44994874280227165, "sarjd_84": -0.165887486192706, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjp_84": 5.73682136742484, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.4326484141722389}}
 



def toalpha(minute):
  return math.radians(minute * 360.0 / 92)

beta = sys.argv[1]

VARS = [

  #name, #lower bound, #upper bound

  ["yaw", 0, math.radians(7), False],
  ["blanket_correction",-300,300,False],


  ["backpanels_angle",-0.15,0.15,False],
  ["frontpanels_angle",-0.15,0.15,False],


]

rng = ""
start_range = 0
stop_range = 0

if len(sys.argv)>2:
  rng = sys.argv[2]

  start_range = int(rng.split("-")[0])
  stop_range = min(91,int(rng.split("-")[1]))

for i in range(0,91):
  if i % 4 == 0:
    VARS.append(["sarjp_%s" % i,toalpha(max(0,i-2)),toalpha(min(i+2,91)),False,toalpha(i)])
    VARS.append(["sarjd_%s" % i, -0.45, 0.45, i in range(start_range, stop_range)])


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