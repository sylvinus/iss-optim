#!/usr/bin/env python

from math import cos, sin, acos, asin, atan, pi
import math

# Parameters are determined in function of the beta angle.
# There is a fixed list of beta angles so we can over-optimize for that...


PARAMS = {"-70": {"backpanels_angle": -0.03661858312156795, "backpanels_phase": 0, "frontpanels_angle": 0.014295270420755898, "fast_cycle_2_accel": 0.35193894017534844, "backpanels_amplitude": 0, "frontpanels_phase": 0, "fast_cycle_1_start": 3.206457403168373, "fast_cycle_1_length": 1.7713782005406706, "fast_cycle_1_accel": 0.34986622845796067, "fast_cycle_2_length": 2.1472054569607355, "frontpanels_amplitude": 0, "yaw": 0.0, "fast_cycle_2_start": 4.793289129449869},
 "72": {"backpanels_angle": -0.02062285024747413, "backpanels_phase": 0, "frontpanels_angle": 0.005393967826593314, "fast_cycle_2_accel": 0.3393155573771829, "backpanels_amplitude": 0, "frontpanels_phase": 0, "fast_cycle_1_start": 3.085909302203207, "fast_cycle_1_length": 1.7438042093649595, "fast_cycle_1_accel": 0.2994846417296466, "fast_cycle_2_length": 2.077661185972699, "frontpanels_amplitude": 0, "yaw": 0, "fast_cycle_2_start": 4.916099606471066},
 "74": {"backpanels_angle": -0.08011121485432518, "backpanels_phase": 5.203600120166685, "frontpanels_angle": 0.34476690892469347, "fast_cycle_2_accel": 0.2399412725174822, "backpanels_amplitude": 2.852731138532168, "frontpanels_phase": 5.410925822519583, "fast_cycle_1_start": 3.0806075316995525, "fast_cycle_1_length": 1.7409493623038732, "fast_cycle_1_accel": 0.23923337055832766, "fast_cycle_2_length": 2.0885153470649493, "frontpanels_amplitude": -0.5077690526785859, "yaw": 0.0002997225746568166, "fast_cycle_2_start": 4.933348883207836},
 "-74": {"backpanels_angle": 0.06072343146429608, "backpanels_phase": 0, "frontpanels_angle": -0.29801433814516826, "fast_cycle_2_accel": 0.18080358853662248, "backpanels_amplitude": 0, "frontpanels_phase": 0, "fast_cycle_1_start": 3.0699925251289315, "fast_cycle_1_length": 1.7398855546485446, "fast_cycle_1_accel": 0.14890684738160895, "fast_cycle_2_length": 2.1793131225704654, "frontpanels_amplitude": 0, "yaw": 0, "fast_cycle_2_start": 4.929439382577715}}




def anglediff(angle1, angle2):
  if angle1>=angle2:
    return angle1-angle2
  else:
    return angle1-angle2+2*pi

def posdegrees(grad):
  return (math.degrees(grad) + 360) % 360

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

  def setParamsArray(self, params):
    self.paramsArray = params
    

  # Public interface methods
  def getInitialOrientation(self, beta):
    self.params = self.paramsArray[str(int(float(beta)))]
    self.beta = math.radians(float(beta))
    self.yaw = self.params["yaw"]
    return posdegrees(self.yaw)

  def getStateAtMinute(self, minute):
    self.minute = int(minute)
    self.alpha = math.radians(self.minute * 360.0 / 92)

    #print [self.alpha, self.beta]
    #print vect2angle(self.getSunVector())
    self.sun = vect2angle(self.getSunVector())

    # normals
    self.panels = {
      "2B": self.sun[1],
      "4B": self.sun[1],
      "4A": self.sun[1],
      "2A": self.sun[1],
 
      "1A": self.sun[1],
      "3A": self.sun[1],
      "3B": self.sun[1],
      "1B": self.sun[1]
    }

    self.sarjs = [
      self.sun[0],    # SSARJ
      self.sun[0]     # PSARJ
    ]


    self.optimizeSarjAngles()

    self.correctPanelsForSarj()

    self.optimizePanelAngles()

    #self.zeroBackPanels(True)

    betabug=0
    if self.beta<0:
      betabug=pi

    return [
      posdegrees(self.sarjs[0]),     # SSARJ
      4.0 / 60,                            # SSARJ velo
      posdegrees(- self.sarjs[1]),   # PSARJ
      -4.0 / 60,                      # PSARJ velo

      posdegrees(- self.panels["1A"] + pi/2 + betabug),   # 1A  #TODO WHY PI/3 ???
      0, #anglediff(self.sarjs[self.getBackSarj()], self.sun[0]),
      posdegrees(self.panels["2A"] + pi/2 + betabug),   # 2A
      0,
      posdegrees(self.panels["3A"] - pi/2 + betabug),   # 3A
      0,
      posdegrees(- self.panels["4A"] - pi/2 + betabug),   # 4A
      0,
      posdegrees(self.panels["1B"] - pi/2 + betabug),     # 1B
      0,
      posdegrees(- self.panels["2B"] - pi/2 + betabug),     # 2B
      0,
      posdegrees(- self.panels["3B"] + pi/2 + betabug),     # 3B
      0,
      posdegrees(self.panels["4B"] + pi/2 + betabug),     # 4B
      0
    ]

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

  def optimizePanelAngles(self):

    for p in self.panels:
      if p in self.listFrontPanels():
        self.panels[p] += self.params["frontpanels_angle"]+self.yaw*(self.params.get("frontpanels_amplitude",0)*sin(self.alpha+self.params.get("frontpanels_phase",0)))
      else:
        self.panels[p] += self.params["backpanels_angle"]+self.yaw*(self.params.get("backpanels_amplitude",0)*sin(self.alpha+self.params.get("backpanels_phase",0)))

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
    for p in self.panels:
      if p not in self.listFrontSarjPanels() or (also_front_sarj and p not in self.listFrontPanels()):
        self.panels[p] += pi


  # Which sarj is on the back of the station?
  def getBackSarj(self):
    if self.beta < 0:
      return 1
    return 0

  # accelerate back panels (ssarj) when passing behind the station
  def optimizeSarjAngles(self):

    def get_cycle_velocity_diff(start, length, accel, angle):
      pos_in_cycle = anglediff(angle, start)

      if length == 0 or pos_in_cycle > length or pos_in_cycle < 0:
        return 0
      elif pos_in_cycle < (length / 2):
        return accel * (2 * pos_in_cycle / length)
      else:
        return accel * (2 - 2 * pos_in_cycle / length)

    ssargp = get_cycle_velocity_diff(self.params["fast_cycle_1_start"], self.params["fast_cycle_1_length"],
        self.params["fast_cycle_1_accel"], self.sarjs[self.getBackSarj()])

    ssargp += get_cycle_velocity_diff(self.params["fast_cycle_2_start"], self.params["fast_cycle_2_length"],
        self.params["fast_cycle_2_accel"], self.sarjs[self.getBackSarj()])
      
    #ssargp = pi / 3


    self.sarjs[self.getBackSarj()] += ssargp

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

    diff_angle = [anglediff(self.sarjs[sarj], sun_angle[0]), self.beta]

    diff_vector = angle2vect(diff_angle)
    return diff_vector
    

if __name__ == "__main__":

  obj = ISS()
  obj.getInitialOrientation(-70)
  for i in range(0, 92):
    print "%d %s" % (i, ["%2.2f" % x for x in obj.getStateAtMinute(i)])
