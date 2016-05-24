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


PARAMS = {"-73": {"sarjd_12": -0.17203712476269295, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.17200386170235824, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.14150722011554243, "sarjd_20": 0.15687364407947613, "sarjp_48": 3.27818363852848, "sarjd_60": 0.1652270038628055, "sarjd_48": -0.23697882290831593, "sarjd_64": 0.16988949116834004, "sarjd_68": 0.17402092047115433, "sarjd_40": -0.17193049639973487, "sarjd_44": -0.09303510343725595, "backpanels_angle": 0.0, "sarjd_0": 0.18822828759091625, "frontpanels_angle": 0.0, "sarjd_4": 0.1204269984585837, "sarjd_8": -0.05510347014415693, "sarjd_32": -0.16867439625100691, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "blanket_correction": 34.00427082558695, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.17200870998946005, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.17129943348505303, "sarjp_0": 0.0, "sarjd_76": -0.17198921099375264, "sarjd_52": 0.172217007845566, "yaw": 5.291331808269014e-08, "sarjd_72": -0.12517674189902278, "sarjd_56": 0.17142754318103848, "sarjd_84": 0.3431608617419495, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.13096292531942244, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.04679842648728204},
 "-71": {"sarjd_12": -0.24213880632233462, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjp_24": 1.63909181926424, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.1500894792711388, "sarjd_20": 0.11736976696208923, "sarjp_48": 3.27818363852848, "sarjd_60": 0.2406326227414142, "sarjd_48": -0.4292063755581551, "sarjd_64": 0.12263901360863007, "sarjd_68": 0.2381092638723069, "sarjd_40": -0.44999675566705294, "sarjd_28": -0.07822273203292805, "backpanels_angle": 0.0, "sarjd_0": 0.1523925607021448, "frontpanels_angle": 0.0, "sarjd_4": -0.10353829690951284, "sarjd_8": -0.3677046749188788, "sarjd_32": -0.3754598332467135, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjd_44": -0.15366360776372093, "sarjp_76": 5.1904574276700925, "blanket_correction": 26.29278589700497, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.4128084613088115, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.4488772044314334, "sarjp_0": 0.0, "sarjd_76": -0.28806645682150245, "sarjd_52": -0.36890931741287586, "yaw": 0.020254186184727817, "sarjd_72": -0.12397299754145141, "sarjd_56": 0.4167212975512612, "sarjd_84": 0.3422023329519501, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.40422089792167515, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.44319058622852014},
 "-75": {"sarjd_12": -0.16330267976074136, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjp_24": 1.63909181926424, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.1024735410334406, "sarjd_20": -0.07017363294480795, "sarjp_48": 3.27818363852848, "sarjd_60": 0.038177614399229697, "sarjd_48": -0.2175079304032056, "sarjd_64": 0.10387441108234718, "sarjd_68": 0.09960293755473067, "sarjd_40": -0.17943823127191846, "sarjd_28": -0.11506418975639365, "backpanels_angle": 0.0, "sarjd_0": 0.20531472337135953, "frontpanels_angle": 0.0, "sarjd_4": 0.07710907752461972, "sarjd_8": -0.15338847240475004, "sarjd_32": -0.1362313574431624, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjd_44": -0.1969618124046711, "sarjp_76": 5.1904574276700925, "blanket_correction": 76.57878283864753, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.15846712512725336, "sarjp_16": 1.0927278795094932, "sarjd_16": 0.020050976492879256, "sarjp_0": 0.0, "sarjd_76": -0.2537435328277252, "sarjd_52": -0.22249655965587462, "yaw": 0.031661049579502304, "sarjd_72": 0.10146521082327883, "sarjd_56": 0.2114146606539331, "sarjd_84": 0.29087672366352213, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.03369650418948864, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.05371541564017932},
 "75": {"sarjd_12": 0.008459731698218903, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjp_24": 1.63909181926424, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.07803414944662954, "sarjd_20": 0.09520323885159088, "sarjp_48": 3.27818363852848, "sarjd_60": 0.16294360554977588, "sarjd_48": -0.1997696870427706, "sarjd_64": 0.17790569991334332, "sarjd_68": 0.13683558336597754, "sarjd_40": -0.06813051340894369, "sarjd_28": 0.16659617506461621, "backpanels_angle": 0.0, "sarjd_0": 0.16767746811888262, "frontpanels_angle": 0.0, "sarjd_4": 0.16746966730416166, "sarjd_8": -0.11856387354908639, "sarjd_32": -0.1429117681672872, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjd_44": -0.11793395908943637, "sarjp_76": 5.1904574276700925, "sarjp_12": 0.81954590963212, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "blanket_correction": 44.18897582771776, "sarjp_84": 5.73682136742484, "sarjd_36": -0.167531187512303, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.1676784219993034, "sarjp_0": 0.0, "sarjd_76": -0.15164561550629987, "sarjd_52": 0.1412353581959001, "yaw": 1.4073793344099197e-10, "sarjd_72": -0.1726100861540726, "sarjd_56": 0.1827559467043318, "sarjd_84": 0.41481819343141757, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.18749386108578517, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.23892825545514898},
 "73": {"sarjd_12": 0.07930104370510739, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": 0.026893186446226684, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.09587225747095246, "sarjd_20": 0.13586299165544188, "sarjp_48": 3.27818363852848, "sarjd_60": 0.16505226071850132, "sarjd_48": -0.1886066511344966, "sarjd_64": 0.1667805191913135, "sarjd_68": 0.14404356868097595, "sarjd_40": -0.14439491873484056, "sarjp_24": 1.63909181926424, "backpanels_angle": 0.0, "sarjd_0": 0.1611572658870859, "frontpanels_angle": 0.0, "sarjd_4": 0.17159930736076462, "sarjd_8": -0.0755178590950114, "sarjd_32": -0.16470156033713026, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjd_44": -0.16370534258479646, "sarjp_76": 5.1904574276700925, "sarjp_12": 0.81954590963212, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "blanket_correction": -17.828080036680905, "sarjp_84": 5.73682136742484, "sarjd_36": 0.14689694748739127, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.16471025761461477, "sarjp_0": 0.0, "sarjd_76": -0.19467934156885922, "sarjd_52": -0.16520373657907, "yaw": 3.4361789526957238e-06, "sarjd_72": 0.030058297795181637, "sarjd_56": 0.16347930796963528, "sarjd_84": 0.2822112255345672, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.22590659465262772, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.1476395578792097},
 "71": {"sarjd_12": -0.07956585120120134, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.13703809625506047, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.17926120740252244, "sarjd_20": -0.27806178154609085, "sarjp_48": 3.27818363852848, "sarjd_60": 0.36868418951020016, "sarjd_48": -0.39222011604040413, "sarjd_64": 0.4078022955189135, "sarjd_68": 0.2408999899849302, "sarjd_40": 0.20647430165984187, "sarjd_44": -0.04554659149253241, "backpanels_angle": 0.0, "sarjd_0": 0.4088508578732394, "frontpanels_angle": 0.0, "sarjd_4": 0.25861392110352793, "sarjd_8": -0.029344751090020795, "sarjd_32": 0.03158624169809945, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "blanket_correction": 0.0, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.22813809135379823, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.07691233047256046, "sarjp_0": 0.0, "sarjd_76": -0.3327277517302292, "sarjd_52": -0.40650548113995294, "yaw": 0.0, "sarjd_72": -0.08175551649296676, "sarjd_56": 0.0734220964376234, "sarjd_84": 0.41442981966259906, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.40466595718537324, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.37477849863155666}}

 

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
  mongoClient = pymongo.MongoClient(os.getenv("MONGODB_URI"))
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
