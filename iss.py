#!/usr/bin/env python

from math import cos, sin, tan, acos, asin, atan, pi
import math

try:
  from pylab import plot, draw, show, hist
except:
  pass

"""
TODO
 - correct for Z offset for SAWs
 - optimal front sarj adjustment
"""

# Parameters are determined in function of the beta angle.
# There is a fixed list of beta angles so we can over-optimize for that...
PARAMS = {"-73": {"sarjd_12": 0.0, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": 0.0, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.0, "sarjd_20": 0.0, "sarjp_48": 3.27818363852848, "sarjd_60": 0.0, "sarjd_48": 0.0, "sarjd_64": 0.0, "sarjd_68": 0.0, "sarjd_40": 0.0, "sarjd_44": 0.0, "backpanels_angle": 0.0, "sarjd_0": 0.0, "frontpanels_angle": 0.0, "sarjd_4": 0.0, "yaw": 0.007175436536597331, "sarjd_32": 0.0, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": 0.0, "sarjp_16": 1.0927278795094932, "sarjd_16": 0.0, "sarjp_0": 0.0, "sarjd_76": 0.0, "sarjd_52": 0.0, "sarjd_72": 0.0, "sarjd_56": 0.0, "sarjd_84": 0.0, "sarjd_8": 0.0, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.0, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.0},
 "-71": {"sarjd_12": 0.0, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": 0.0, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.0, "sarjd_20": 0.0, "sarjp_48": 3.27818363852848, "sarjd_60": 0.0, "sarjd_48": 0.0, "sarjd_64": 0.0, "sarjd_68": 0.0, "sarjd_40": 0.0, "sarjd_44": 0.0, "backpanels_angle": 0.0, "sarjd_0": 0.0, "frontpanels_angle": 0.0, "sarjd_4": 0.0, "yaw": 0.019569839765407493, "sarjd_32": 0.0, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": 0.0, "sarjp_16": 1.0927278795094932, "sarjd_16": 0.0, "sarjp_0": 0.0, "sarjd_76": 0.0, "sarjd_52": 0.0, "sarjd_72": 0.0, "sarjd_56": 0.0, "sarjd_84": 0.0, "sarjd_8": 0.0, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.0, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.0},
 "-70": {"sarjd_12": -0.3712694451224359, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.15414710931785996, "sarjp_40": 2.7318196987737333, "sarjd_24": -0.049314284210064396, "sarjd_20": 0.05671548801733434, "sarjp_48": 3.27818363852848, "sarjd_60": 0.23142296908586663, "sarjd_48": -0.36127431608555444, "sarjd_64": 0.11714755069422614, "sarjd_68": 0.18344074740240193, "sarjd_40": -0.3649725779714389, "sarjp_24": 1.63909181926424, "backpanels_angle": -0.0005626978728677377, "sarjd_0": 0.10361697270681042, "frontpanels_angle": -0.0018021451210250064, "sarjd_4": -0.21803440633021864, "yaw": 0.0416280513684409, "sarjd_32": 0.044505237516302705, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjd_44": -0.10043731825174973, "sarjp_76": 5.1904574276700925, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.35743312891940976, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.29759597041284214, "sarjp_0": 0.0, "sarjd_76": 0.2952121363648696, "sarjd_52": -0.3698538482536094, "sarjd_72": -0.23587505834913702, "sarjd_56": 0.18075278369827202, "sarjd_84": 0.3753205848274733, "sarjd_8": -0.39770193491926414, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.36932587217617624, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.3993286643508178},
 "-75": {"sarjd_12": 0.0, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": 0.0, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.0, "sarjd_20": 0.0, "sarjp_48": 3.27818363852848, "sarjd_60": 0.0, "sarjd_48": 0.0, "sarjd_64": 0.0, "sarjd_68": 0.0, "sarjd_40": 0.0, "sarjd_44": 0.0, "backpanels_angle": 0.0, "sarjd_0": 0.0, "frontpanels_angle": 0.0, "sarjd_4": 0.0, "yaw": 0.018911813515203726, "sarjd_32": 0.0, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": 0.0, "sarjp_16": 1.0927278795094932, "sarjd_16": 0.0, "sarjp_0": 0.0, "sarjd_76": 0.0, "sarjd_52": 0.0, "sarjd_72": 0.0, "sarjd_56": 0.0, "sarjd_84": 0.0, "sarjd_8": 0.0, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.0, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.0},
 "-74": {"sarjd_12": -0.19868169413681036, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.16601505332211963, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.13920843692455181, "sarjd_20": -0.061966115674738004, "sarjp_48": 3.27818363852848, "sarjd_60": 0.23142296908586663, "sarjd_48": -0.3284005424075957, "sarjd_64": 0.18075278369827202, "sarjd_68": 0.23142296908586663, "sarjd_40": -0.17997224632294723, "sarjd_44": -0.16562369655527528, "backpanels_angle": 0.025824642959634138, "sarjd_0": 0.1709959718808408, "frontpanels_angle": 0.03747876646465642, "sarjd_4": 0.1208494498326009, "yaw": 0.02099660013660592, "sarjd_32": -0.18561597969435487, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.16010165325017792, "sarjp_16": 1.0927278795094932, "sarjd_16": 0.06584333588355565, "sarjp_0": 0.0, "sarjd_76": -0.19956046914445771, "sarjd_52": 0.20675155838750187, "sarjd_72": 0.021561789917184437, "sarjd_56": 0.18075278369827202, "sarjd_84": 0.29997348269937946, "sarjd_8": -0.1052816379548429, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.06297208892906464, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.42742412763372123},
 "75": {"sarjd_12": 0.0, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": 0.0, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.0, "sarjd_20": 0.0, "sarjp_48": 3.27818363852848, "sarjd_60": 0.0, "sarjd_48": 0.0, "sarjd_64": 0.0, "sarjd_68": 0.0, "sarjd_40": 0.0, "sarjd_44": 0.0, "backpanels_angle": 0.0, "sarjd_0": 0.0, "frontpanels_angle": 0.0, "sarjd_4": 0.0, "yaw": 0.0, "sarjd_32": 0.0, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": 0.0, "sarjp_16": 1.0927278795094932, "sarjd_16": 0.0, "sarjp_0": 0.0, "sarjd_76": 0.0, "sarjd_52": 0.0, "sarjd_72": 0.0, "sarjd_56": 0.0, "sarjd_84": 0.0, "sarjd_8": 0.0, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.0, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.0},
 "74": {"sarjd_12": 0.05293316463154639, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": 0.04462961067620841, "sarjp_40": 2.7318196987737333, "sarjp_28": 1.9122737891416133, "sarjd_20": 0.1333840357962743, "sarjp_48": 3.27818363852848, "sarjd_60": 0.16294360554977588, "sarjd_48": -0.2029615155189931, "sarjd_64": 0.20421834634503616, "sarjd_68": 0.1448077745703596, "sarjd_40": -0.08685942300598207, "sarjd_44": -0.20265659218767687, "backpanels_angle": -0.09919865680428072, "sarjd_0": 0.14472819729337677, "frontpanels_angle": 0.01890516267244477, "sarjd_4": 0.16294360554977588, "yaw": 0.0, "sarjd_32": -0.16338020498571196, "sarjp_8": 0.5463639397547466, "sarjd_24": 0.06297208892906464, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjd_88": 0.23581902149887712, "sarjd_36": 0.09994337723908381, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.17705761866713504, "sarjp_0": 0.0, "sarjd_76": -0.17720323612048017, "sarjd_52": -0.1827284186337766, "sarjd_72": -0.01785132393001021, "sarjd_56": 0.14472819729337677, "sarjd_84": 0.2952121363648696, "sarjd_8": -0.08535612189734833, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjp_84": 5.73682136742484, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.23587505834913702},
 "73": {"sarjd_12": 0.0, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": 0.0, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.0, "sarjd_20": 0.0, "sarjp_48": 3.27818363852848, "sarjd_60": 0.0, "sarjd_48": 0.0, "sarjd_64": 0.0, "sarjd_68": 0.0, "sarjd_40": 0.0, "sarjd_44": 0.0, "backpanels_angle": 0.0, "sarjd_0": 0.0, "frontpanels_angle": 0.0, "sarjd_4": 0.0, "yaw": 0.0, "sarjd_32": 0.0, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": 0.0, "sarjp_16": 1.0927278795094932, "sarjd_16": 0.0, "sarjp_0": 0.0, "sarjd_76": 0.0, "sarjd_52": 0.0, "sarjd_72": 0.0, "sarjd_56": 0.0, "sarjd_84": 0.0, "sarjd_8": 0.0, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.0, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.0},
 "72": {"sarjd_12": 0.07281422870919477, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": 0.03547021677258176, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.06502644460641806, "sarjd_20": -0.21020796008206055, "sarjp_48": 3.27818363852848, "sarjd_60": 0.24248646594880519, "sarjd_48": -0.25354228353405545, "sarjd_64": 0.21714375848923181, "sarjd_68": 0.25225643259792485, "sarjd_40": -0.08998430151792419, "sarjp_24": 1.63909181926424, "backpanels_angle": -0.014731268451499838, "sarjd_0": 0.22270970545556112, "frontpanels_angle": 0.005921783893742168, "sarjd_4": 0.21218801146237137, "yaw": 0.0004957706763891608, "sarjd_32": -0.11693649248442425, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjd_44": -0.22857060099980125, "sarjp_76": 5.1904574276700925, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.07614177729549036, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.10938184267781229, "sarjp_0": 0.0, "sarjd_76": -0.26686365733285977, "sarjd_52": -0.22637229333011571, "sarjd_72": -0.02572295434206107, "sarjd_56": 0.20246574663226213, "sarjd_84": 0.23588384222635989, "sarjd_8": -0.05759583537478703, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.24043406760009392, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.15690963491279986},
 "71": {"sarjd_12": 0.0, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": 0.0, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.0, "sarjd_20": 0.0, "sarjp_48": 3.27818363852848, "sarjd_60": 0.0, "sarjd_48": 0.0, "sarjd_64": 0.0, "sarjd_68": 0.0, "sarjd_40": 0.0, "sarjd_44": 0.0, "backpanels_angle": 0.0, "sarjd_0": 0.0, "frontpanels_angle": 0.0, "sarjd_4": 0.0, "yaw": 0.0, "sarjd_32": 0.0, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": 0.0, "sarjp_16": 1.0927278795094932, "sarjd_16": 0.0, "sarjp_0": 0.0, "sarjd_76": 0.0, "sarjd_52": 0.0, "sarjd_72": 0.0, "sarjd_56": 0.0, "sarjd_84": 0.0, "sarjd_8": 0.0, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.0, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.0}}
 


DEBUG=False


def smallradians(radians):
  if (radians % (2*pi))<pi:
    return radians % (2*pi)
  else:
    return (radians % (2*pi)) - 2*pi

def anglediff(angle1, angle2):
  if angle1>=angle2:
    return angle1-angle2
  else:
    return angle1-angle2+2*pi

def posdegrees(radians):
  return (math.degrees(radians)) % 360

def smalldegrees(radians):
  if (radians % (2*pi))<pi:
    return (math.degrees(radians)) % 360
  else:
    return ((math.degrees(radians)) % 360) - 360

def addvect(vect1, vect2):
  return [vect1[0]+vect2[0],vect1[1]+vect2[1],vect1[2]+vect2[2]]

# returns alpha, beta
# TODO fix this crap, doesn't work w/ yaw
def vect2angle(vect):
  beta = asin(min(1, max(-1, -vect[1])))

  alpha = acos(min(1, max(-1, -vect[2] / cos(beta))))
  if vect[2]<0 and vect[0]>0:
    alpha = asin(min(1, max(-1, vect[0] / cos(beta))))
  if vect[2]>0 and vect[0] < 0:
    alpha = -acos(min(1, max(-1, -vect[2] / cos(beta))))
  if vect[2]<0 and vect[0] < 0:
    alpha = -acos(min(1, max(-1, -vect[2] / cos(beta))))

  return [alpha, beta]

def angle2vect(angle):
  alpha, beta = angle
  if alpha==0 and beta==0:
    return [0,0,0]
  return [
    cos(beta) * sin(alpha),
    - sin(beta),
    - cos(beta) * cos(alpha)
  ]


"""
def vect2angle2(vect):
  beta = asin(-vect[1])
  if vect[2]==0:
    alpha = pi/2 #cos(vect[0])
  else:
    alpha = atan(vect[0]/-vect[2])+pi

  return [alpha, beta]


print "%s %s" % (vect2angle([0,0,1]), vect2angle2([0,0,1]))
print "%s %s" % (vect2angle([0,0,-1]), vect2angle2([0,0,-1]))
print "%s %s" % (vect2angle([0,1,0]), vect2angle2([0,1,0]))
print "%s %s" % (vect2angle([0,-1,0]), vect2angle2([0,-1,0]))
print "%s %s" % (vect2angle([1,0,0]), vect2angle2([1,0,0]))
print "%s %s" % (vect2angle([-1,0,0]), vect2angle2([-1,0,1]))

sys.exit(0)
"""

class ISS:

  paramsArray = PARAMS
  minutes = []
  angles = []
  speeds = []
  panels = ["4A", "2A", "3B", "1B", "2B", "4B", "1A", "3A"]
  sarjs = ["FRONT", "BACK"]
  panelshades = {}

  # seems to improve the score for beta=74
  invert_front_panel = False


  def setParamsArray(self, params):
    self.paramsArray = params
    

  # Public interface methods
  def getInitialOrientation(self, beta):
    self.params = self.paramsArray[str(int(float(beta)))]
    self.beta = math.radians(float(beta))
    self.yaw = self.params.get("yaw",0)

    if self.beta>0:
      self.panelshades = {
        "2B":"4A",
        "4B":"2A",
        "1A":"3B",
        "3A":"1B"
      }
    else:
      self.panelshades = {
        "4A":"2B",
        "2A":"4B",
        "3B":"1A",
        "1B":"3A"
      }

    self.compute()

    return posdegrees(self.yaw)

  def getStateAtMinute(self, minute):
    return self.minutes[int(minute)]

  def setMinute(self, m):
    self.minute = m
    self.alpha = self.minute * 2 * pi / 92
    self.sun = vect2angle(self.getSunVector())

  def compute(self):

    for m in range(0, 92):
      self.setMinute(m)

      self.angles.append({
        "2B": self.sun[1],
        "4B": self.sun[1],
        "4A": self.sun[1],
        "2A": self.sun[1],
   
        "1A": self.sun[1],
        "3A": self.sun[1],
        "3B": self.sun[1],
        "1B": self.sun[1],

        #SARJS
        "FRONT": self.sun[0],
        "BACK": self.sun[0]
      })

      self.speeds.append({
        "2B": 0,
        "4B": 0,
        "4A": 0,
        "2A": 0,
   
        "1A": 0,
        "3A": 0,
        "3B": 0,
        "1B": 0,

        #SARJS
        "FRONT": 0,
        "BACK": 0
      })

    #self.optimizeSarjAngles()
   #for m in range(0, 92):
    
    #if DEBUG:
      #plot([x["BACK"] for x in self.angles])
      
      #plot([self.angles[i].get("BACK") for i in range(0,92)])
      
    self.optimizeSarjAnglesLinear()





    self.adjustVelocities(sarj=True)

    self.adjustFrontSarj()

    self.adjustVelocities(sarj=True)

  
    #for m in range(0, 92):
    #if DEBUG:
      #plot([x["BACK"] for x in self.angles])
      
      #plot([self.params.get("sarjd_%s"%i,0) for i in range(0,92)])
      #plot([self.angles[i].get("BACK") for i in range(0,92)])
      
      #show()
    
    
      #self.correctPanelsForSarj()

    self.optimizePanelAnglesNew()

    #self.patchPanelAngles()

    #self.zeroBackPanels()

    self.adjustVelocities(saw=True)


    self.setNormals()

  #also converts to degrees
  def setNormals(self):

    for m in range(0, 92):
      d = self.angles[m]
      s = self.speeds[m]

      self.minutes.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

      betabug = 0
      #if self.beta < 0:
      #  betabug = pi

      if self.beta>0:
        self.minutes[m][0] = d["BACK"]
        self.minutes[m][1] = s["BACK"]
        self.minutes[m][2] = - d["FRONT"]
        self.minutes[m][3] = - s["FRONT"]
      else:
        self.minutes[m][0] = d["FRONT"]
        self.minutes[m][1] = s["FRONT"]
        self.minutes[m][2] = - d["BACK"]
        self.minutes[m][3] = - s["BACK"]
      self.minutes[m][4] = - d["1A"] + pi/2 + betabug   # 1A
      self.minutes[m][5] = - s["1A"]
      self.minutes[m][6] = d["2A"] + pi/2 + betabug
      self.minutes[m][7] = s["2A"]
      self.minutes[m][8] = d["3A"] - pi/2 + betabug
      self.minutes[m][9] = s["3A"]
      self.minutes[m][10] = - d["4A"] - pi/2 + betabug
      self.minutes[m][11] = - s["4A"]
      self.minutes[m][12] = d["1B"] - pi/2 + betabug
      self.minutes[m][13] = s["1B"]
      self.minutes[m][14] = - d["2B"] - pi/2 + betabug
      self.minutes[m][15] = - s["2B"]
      self.minutes[m][16] = - d["3B"] + pi/2 + betabug
      self.minutes[m][17] = - s["3B"]
      self.minutes[m][18] = d["4B"] + pi/2 + betabug
      self.minutes[m][19] = s["4B"]


    for i in range(0, 10):
      for m in range(0, 92):
        self.minutes[m][2*i]=posdegrees(self.minutes[m][2*i])
        self.minutes[m][2*i+1]=smalldegrees(self.minutes[m][2*i+1])
              
      
  # Dumb averages
  def setSpeeds(self, sarj=False, saw=False):

    for p in self.angles[0]:

      if p in self.sarjs:
        max_velocity = math.radians(0.15)
        max_accel = math.radians(0.005)
      elif p in self.panels:
        max_velocity = math.radians(0.25)
        max_accel = math.radians(0.01)

      if (sarj and p in self.sarjs) or (saw and p in self.panels):
        for m in range(0, 92):

          speed = smallradians(self.angles[(m + 1) % 92][p] - self.angles[m][p]) / 60

          if speed > max_velocity:
            speed = max_velocity
          elif speed < - max_velocity:
            speed = -max_velocity
          self.speeds[(m + 1) % 92][p] = speed


  def adjustVelocities(self, sarj=False, saw=False):

    # Should only be done once!
    self.setSpeeds(sarj=sarj, saw=saw)

    def path(t, v0, a):
      return v0 * t + a * t * t / 2

    def get_min_possible_angular_shift(speed1, speed2, minSpeed, maxAcc):
      minShift = 0
      t1 = (speed1 - minSpeed) / maxAcc
      t2 = 60 - (speed2 - minSpeed) / maxAcc
      #if DEBUG and m==1 and p=="FRONT":
      #  print minSpeed, speed1, t1, t2
      if (t1 <= t2):
        minShift += path(t1, speed1, -maxAcc)
        minShift += path(t2 - t1, minSpeed, 0)
        minShift += path(60 - t2, minSpeed, maxAcc)
      else:
        t = (speed1 - speed2 + 60 * maxAcc) / 2.0 / maxAcc
        minShift += path(t, speed1, -maxAcc)
        minShift += path(60 - t, speed1 - maxAcc * t, maxAcc)
      return minShift

    def get_max_possible_angular_shift(speed1, speed2, maxSpeed, maxAcc):
      maxShift = 0
      t1 = (maxSpeed - speed1) / maxAcc
      t2 = 60 - (maxSpeed - speed2) / maxAcc

      if (t1 <= t2):
         maxShift += path(t1, speed1, maxAcc)
         maxShift += path(t2 - t1, maxSpeed, 0)
         maxShift += path(60 - t2, maxSpeed, -maxAcc)
      else:
         t = (speed2 - speed1 + 60 * maxAcc) / 2.0 / maxAcc
         maxShift += path(t, speed1, maxAcc)
         maxShift += path(60 - t, speed1 + maxAcc * t, -maxAcc)
      return maxShift

    #auto-compute velocities & adjust if needed.
    for p in self.angles[0]:


      if p in self.sarjs and sarj:
        max_velocity = math.radians(0.15)*0.999999999 # This is to avoid rounding errors
        max_accel = math.radians(0.005)*0.999999999

      elif p in self.panels and saw:
        max_velocity = math.radians(0.25)*0.999999999
        max_accel = math.radians(0.01)*0.999999999
      else:
        continue

      for m in range(0, 92*3):

        PRINTOUT = (DEBUG and p=="BACK" and (m%92)==75)




        if True or (p in self.sarjs):
          nextm = (m + 1) % 92
          cm = m % 92
          sign = 1
        else:
          #go in reverse for saws!
          m = 91 - m
          nextm = (m - 1) % 92
          sign = -1

        if PRINTOUT:
          
          print "angles", self.angles[(m + 1) % 92][p], self.angles[(cm) % 92][p], self.angles[(m + 1) % 92][p] - self.angles[(cm) % 92][p]
          


        diff = smallradians(self.angles[nextm][p] - self.angles[cm][p])

        currentSpeed = self.speeds[cm][p]
        finalSpeed = self.speeds[nextm][p]

        max_diff = get_max_possible_angular_shift(currentSpeed, max_velocity, max_velocity, max_accel)
        min_diff = get_min_possible_angular_shift(currentSpeed, -max_velocity, -max_velocity, max_accel)

        #can the point be atteinted but not at the same speed?
        max_diff_w_speed = max(get_min_possible_angular_shift(currentSpeed, finalSpeed, -max_velocity, max_accel),get_max_possible_angular_shift(currentSpeed, finalSpeed, max_velocity, max_accel))
        min_diff_w_speed = min(get_max_possible_angular_shift(currentSpeed, finalSpeed, max_velocity, max_accel),get_min_possible_angular_shift(currentSpeed, finalSpeed, -max_velocity, max_accel))

        if diff <= (min_diff):
          if PRINTOUT:
            print " - min", diff, min_diff
          self.angles[nextm][p] = sign * (self.angles[cm][p] + min_diff)
          self.speeds[nextm][p] = sign * -max_velocity
        elif diff >= (max_diff):
          if PRINTOUT:
            print " - max"
          self.angles[nextm][p] = sign * (self.angles[cm][p] + max_diff)
          self.speeds[nextm][p] = sign * max_velocity

        elif diff >= max_diff_w_speed:
          if PRINTOUT:
            print " - max-w-speed"
          self.angles[nextm][p] = sign * (self.angles[cm][p] + max_diff_w_speed)

        elif diff <= min_diff_w_speed :
          if PRINTOUT:
            print " - min-w-speed"
          self.angles[nextm][p] = sign * (self.angles[cm][p] + min_diff_w_speed)

        """
        elif (diff > max_diff_w_speed) or (diff < min_diff_w_speed):

          # equal the final speed
          t0 = math.fabs((finalSpeed - currentSpeed) / max_accel) + 1e-8

          diff0 = path(t0, currentSpeed, math.copysign(max_accel, (finalSpeed - currentSpeed)))

          lineardiff = finalSpeed * (60 - t0)
          if lineardiff > (diff-diff0):
            newdiff = path((60 - t0) / 2, finalSpeed, -max_accel) * 2
          else:
            newdiff = path((60 - t0) / 2, finalSpeed, max_accel) * 2


          #angle was modified, not speed
          self.angles[(m + 1) % 92][p] = self.angles[m][p] + diff0 + newdiff
        """

        
        if PRINTOUT:
          
          print "minute", m
          print "diff", diff
          print "max_diffs", max_diff, min_diff
          print "max_diffs_w_speed", max_diff_w_speed, min_diff_w_speed
          
          print "speeds", currentSpeed, finalSpeed
          print "angles", self.angles[(m + 1) % 92][p], self.angles[(cm) % 92][p]
          print "final diff", self.angles[(m + 1) % 92][p] - self.angles[(cm) % 92][p]
          print "max diff", get_max_possible_angular_shift(self.speeds[cm][p], self.speeds[nextm][p], max_velocity, max_accel)
          print
          #print "time to speed",t0, diff0
          #print "resting diff", lineardiff, newdiff
          #print diff0, newdiff, diff0 + newdiff
          #print get_min_possible_angular_shift(currentSpeed,0, max_velocity, -max_accel)
        
        

  def adjustFrontSarj(self):

    if math.fabs(math.degrees(self.beta))>=73.9:
      max_angle = 0.15
    elif math.fabs(math.degrees(self.beta))>=71.9:
      max_angle = 0.20
    else:
      max_angle = 0.27 #optim for -70

    for m in range(0, 92):
      diff = smallradians(self.angles[m]["FRONT"] - self.angles[m]["BACK"])
      if math.fabs(diff) > max_angle:
        self.angles[m]["FRONT"] = self.angles[m]["BACK"] + math.copysign(max_angle, diff)


  # accelerate back panels (ssarj) when passing behind the station
  def optimizeSarjAngles(self):

    def tominute(alpha):
      return alpha * 92 / (2 * pi)

    def set_cycle_velocity_diff(cycle_no):

      start = self.params.get("fast_cycle_%s_start" % cycle_no, 0)
      prelength = self.params.get("fast_cycle_%s_prelength" % cycle_no, 0)
      length = self.params.get("fast_cycle_%s_length" % cycle_no, 0)

      if length == 0:
        return

      minute_start = int(math.ceil(tominute(start) - tominute(prelength)))
      minute_stop = int(math.ceil(tominute(start) + tominute(length)))

      for m in range(minute_start, minute_stop + 1):
        self.angles[m%92]["BACK"] = start

      self.angles[(minute_start-1)%92]["BACK"] = start - (minute_start - (tominute(start) - tominute(prelength)))*60*math.radians(0.10)
      self.angles[(minute_start+1)%92]["BACK"] = start - (minute_stop - (tominute(start) + tominute(length)))*60*math.radians(0.10)

    for i in range(1, 100):
      set_cycle_velocity_diff(i)



  # accelerate back panels (ssarj) when passing behind the station
  def optimizeSarjAnglesLinear(self):

    def tominute(alpha):
      return alpha * 92 / (2 * pi)

    points = []
    for cycle_no in range(0, 130):

      start = self.params.get("sarjp_%s" % cycle_no, 0)
      length = self.params.get("sarjd_%s" % cycle_no, 0)
      
      if length!=0:
        points.append([start, length])

    if len(points) < 2:
      return

    # sort by start point
    points.sort(lambda x, y: cmp(x[0], y[0]))

    # then each minute is between two points w / linear speed between them
    for m in range(0,92):
    
      pointn = 0
      for n in range(0,len(points)):
        if tominute(points[n%len(points)][0])>=m:
          pointn = n
          break

      nextpoint = points[pointn%len(points)]
      lastpoint = points[(pointn-1)%len(points)]

      ratio = ((tominute(nextpoint[0]) - m)%92) / ((tominute(nextpoint[0]) - tominute(lastpoint[0]))%92)
      
      """
      print m, ratio
      print ((tominute(nextpoint[0]) - m)%92), ((tominute(nextpoint[0]) - tominute(lastpoint[0]))%92)
      print tominute(nextpoint[0]), tominute(lastpoint[0])
      print nextpoint[1], lastpoint[1]
      print ratio * (nextpoint[1] - lastpoint[1]) + nextpoint[1]
      print
      """

      self.angles[m]["BACK"] += ratio * (lastpoint[1]-nextpoint[1]) + nextpoint[1]


  def optimizePanelAnglesNew(self):

    if self.beta>0:
      self.invert_front_panel=True

    width_between_blankets = 1927.51
    
    blanket_width = 4752.25

    border_to_blanket = 133.75 + 94

    #TODO wtf

    blanked_corrections = {
      "-70": 60,
      "72": 30,
      "-74": 30, #70,
      "74": 6,
      "75": 35,
      "-75": 102
    }

    border_to_blanket += blanked_corrections.get(str(int(math.degrees(self.beta))), 0)


    for m in range(0, 92):
      self.setMinute(m)

      for p in self.panels:
        if p in self.listFrontSarjPanels():
          sun = self.getSunVectorRelativeToSarj("FRONT")
        else:
          sun = self.getSunVectorRelativeToSarj("BACK")

        if p in self.listFrontPanels():

          axis_z = {"3B":-67, "1A":-67, "2A": -67, "4B":-67, "3A": 5, "1B": 5, "4A": 0, "2B": 0}[p]

          #TODO z
          saw_distance = {"3B":15063, "1A":15063, "2A": 15069, "4B":15069, "3A": 15072, "1B": 15072, "4A": 15070, "2B": 15070}[p]

          sun_angle = pi/2 - vect2angle(sun)[1] #-atan(sun[2] / sun[1])
          shaded_panel = self.panelshades[p]

          shaded_panel_opening_y = sin(self.angles[m][shaded_panel]) * (width_between_blankets / 2 + border_to_blanket)
          shaded_panel_opening_x = cos(self.angles[m][shaded_panel]) * (width_between_blankets / 2 + border_to_blanket)

          remaining_x = shaded_panel_opening_y / tan(sun_angle)

          saw_to_sun_contact = remaining_x + shaded_panel_opening_x + saw_distance

          panel_top_y = tan(sun_angle) * saw_to_sun_contact

          panel_width = (width_between_blankets / 2) + blanket_width

          #Can't optimize the shades (limit case is rect triangle)
          #if pi-asin(panel_width/saw_to_sun_contact)>sun_angle:
          #  continue
          if math.fabs(sin(pi / 2 - sun_angle) * panel_top_y / panel_width)>1:
            continue

          panel_angle = asin(sin(pi / 2 - sun_angle) * panel_top_y / panel_width) - sun_angle

          if self.invert_front_panel:
            panel_angle += pi - 2*sun_angle - 2*panel_angle


          self.angles[m][p] = panel_angle # -74: 0.12 #TODO!!! #(self.angles[m][p]+9*panel_angle)/10


          
          if DEBUG and p == "2B":
            print
            print m
            print sun_angle
            print panel_angle
            """
            print asin(panel_width/saw_to_sun_contact)
            print remaining_x
            print panel_top_y, panel_width
            print shaded_panel_opening_y, shaded_panel_opening_x
            print shaded_panel
            print tan(sun_angle)
            print sin(pi / 2 - sun_angle) * panel_top_y / panel_width
            print math.fabs(sin(pi / 2 - sun_angle) * panel_top_y / panel_width)>1
            #print math.degrees(-(asin(sin(pi / 2 - sun_angle) * panel_top_y / panel_width) - sun_angle) - pi/2)%360
            print self.angles[m][shaded_panel]
            """



  def patchPanelAngles(self):

    for m in range(0, 92):
      for p in self.panels:
        if p in self.listFrontPanels():
          if self.invert_front_panel:
            self.angles[m][p] -= self.params.get("frontpanels_angle", 0)
          else:
            self.angles[m][p] += self.params.get("frontpanels_angle", 0)
        else:
          self.angles[m][p] += self.params.get("backpanels_angle", 0)


  def correctPanelsForSarj(self):

    
    front_vect = self.getSunVectorRelativeToSarj(1 - self.getBackSarj())
    front_optimal_angle = atan(-front_vect[2]/front_vect[1])+pi/2

    back_vect = self.getSunVectorRelativeToSarj(self.getBackSarj())
    back_optimal_angle = atan(-back_vect[2]/back_vect[1])+pi/2
    #print front_optimal_angle
    #print

    # Use this as new base angles
    for p in self.panels:
      if p in self.listFrontSarjPanels():
        #TODO incorrect calculus
        self.panels[p] = front_optimal_angle #front_optimal_angle #sun[0] #sun_front_sarj[1] - anglediff(self.sarjs[1 - self.getBackSarj()], self.sun[0])/10
      else:
        self.panels[p] = back_optimal_angle #sun_back_sarj[1] - anglediff(self.sarjs[self.getBackSarj()], self.sun[0])/10

  # Adds amount to a panel at the last possible time
  def transitionAngleWith(self, panel, amount, target_minute, length=1):

    max_panel_velocity = math.radians(0.15) * 60 #TODO 0.25, polynomial fitting

    # Fix the amount during all the duration
    for m in range(0, length):
      self.angles[(m + target_minute) % 92][panel] += amount

    # Transition towards the ceiling
    m = target_minute
    while True:
      diff = self.angles[m][panel] - self.angles[(m - 1) % 92][panel]
      if math.fabs(diff) < max_panel_velocity:
        break
      self.angles[(m - 1) % 92][panel] = self.angles[m][panel] - math.copysign(max_panel_velocity, diff)
      m = (m - 1) % 92

    m = target_minute + length - 1
    while True:

      diff = self.angles[m][panel] - self.angles[(m + 1) % 92][panel]
      
      if math.fabs(diff) < max_panel_velocity:
        break
      self.angles[(m + 1) % 92][panel] = self.angles[m][panel] - math.copysign(max_panel_velocity, diff)
      m = (m + 1) % 92
         
  def listFrontPanels(self):
    if self.beta < 0:
      return ["4A", "2A", "3B", "1B"]
    else:
      return ["2B", "4B", "1A", "3A"]

  def listFrontSarjPanels(self):
    if self.beta < 0:
      return ["1A", "3A", "3B", "1B"]
    else:
      return ["2B", "4B", "2A", "4A"]

  def zeroBackPanels(self, also_front_sarj=False):
    for m in range(0, 92):
      for p in self.panels:
        if p not in self.listFrontSarjPanels() or (also_front_sarj and p not in self.listFrontPanels()):
          self.angles[m][p] += pi


  # Utilities
  def getSunVector(self):
    alpha = self.alpha

    return [
      cos(self.beta) * sin(alpha) * cos(self.yaw) - sin(self.beta) * sin(self.yaw),
      - cos(self.beta) * sin(alpha) * sin(self.yaw) - sin(self.beta) * cos(self.yaw),
      - cos(self.beta) * cos(alpha)
    ]

  def getSunVectorRelativeToSarj(self, sarj):
    
    sun_vect = self.getSunVector()
    sun_angle = vect2angle(sun_vect)

    sun_angle[0] = anglediff(self.angles[self.minute][sarj], sun_angle[0])

    return angle2vect(sun_angle)
    

if __name__ == "__main__":

  import sys

  DEBUG=True

  obj = ISS()
  if len(sys.argv)>1:
    obj.getInitialOrientation(sys.argv[1])
  else:
    obj.getInitialOrientation(74)
  for i in range(0, 92):
    print "%d %s" % (i, ["%2.14f" % x for x in obj.getStateAtMinute(i)])
