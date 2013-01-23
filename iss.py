#!/usr/bin/env python

from math import cos, sin, acos, asin, atan, pi
import math

# Parameters are determined in function of the beta angle.
# There is a fixed list of beta angles so we can over-optimize for that...

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


def anglediff(angle1, angle2):
  if angle1>=angle2:
    return angle1-angle2
  else:
    return angle1-angle2+2*pi

def posdegrees(grad):
  return (math.degrees(grad) + 360) % 360


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
    #f = open("lastparams.json","w")
    #json.dump(params, f)
    #f.close()

  # Public interface methods
  def getInitialOrientation(self, beta):
    self.params = self.paramsArray[str(int(float(beta)))]
    self.beta = math.radians(float(beta))
    self.yaw = 0 #self.params["yaw"]
    return posdegrees(self.yaw)

  def getStateAtMinute(self, minute):
    self.minute = int(minute)
    self.alpha = math.radians(self.minute * 360.0 / 92)

    #print self.getSunVector(minute)
    #print [math.degrees(x) for x in vect2angle(self.getSunVector(minute))]
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

    #self.zeroBackPanels()

    return [
      posdegrees(self.sarjs[0]),     # SSARJ
      4.0 / 60,                            # SSARJ velo
      posdegrees(- self.sarjs[1]),   # PSARJ
      -4.0 / 60,                      # PSARJ velo

      posdegrees(- self.panels["1A"] + pi/2),   # 1A  #TODO WHY PI/3 ???
      0, #anglediff(self.sarjs[self.getBackSarj()], self.sun[0]),
      posdegrees(self.panels["2A"] + pi/2),   # 2A
      0,
      posdegrees(self.panels["3A"] - pi/2),   # 3A
      0,
      posdegrees(- self.panels["4A"] - pi/2),   # 4A
      0,
      posdegrees(self.panels["1B"] - pi/2),     # 1B
      0,
      posdegrees(- self.panels["2B"] - pi/2),     # 2B
      0,
      posdegrees(- self.panels["3B"] + pi/2),     # 3B
      0,
      posdegrees(self.panels["4B"] + pi/2),     # 4B
      0
    ]

  def correctPanelsForSarj(self):

    sun_back_sarj = vect2angle(self.getSunVectorRelativeToSarj(self.getBackSarj()))
    sun_front_sarj = vect2angle(self.getSunVectorRelativeToSarj(1 - self.getBackSarj()))

    # Use this as new base angles
    for p in self.panels:
      if p in self.listFrontSarjPanels():
        #TODO incorrect calculus
        self.panels[p] = sun_front_sarj[1] - anglediff(self.sarjs[1 - self.getBackSarj()], self.sun[0])/10
      else:
        self.panels[p] = sun_back_sarj[1] - anglediff(self.sarjs[self.getBackSarj()], self.sun[0])/10

  def optimizePanelAngles(self):

    for p in self.panels:
      if p in self.listFrontPanels():
        self.panels[p] += self.params["frontpanels_angle"]
      else:
        self.panels[p] += self.params["backpanels_angle"]

  def listFrontPanels(self):
    if self.beta < 0:
      return ["4A", "2A", "3B", "1B"]
    else:
      return ["2B", "4B", "1A", "3A"]

  def listFrontSarjPanels(self):
    if self.beta > 0:
      return ["1A", "3A", "3B", "1B"]
    else:
      return ["2B", "4B", "2A", "4A"]

  def zeroBackPanels(self):
    for p in self.panels:
      if p in self.listFrontSarjPanels():
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
    alpha = self.sarjs[sarj]
    
    return [
      cos(self.beta) * sin(alpha) * cos(self.yaw) - sin(self.beta) * sin(self.yaw),
      - cos(self.beta) * sin(alpha) * sin(self.yaw) - sin(self.beta) * cos(self.yaw),
      - cos(self.beta) * cos(alpha)
    ]



if __name__ == "__main__":

  obj = ISS()
  obj.getInitialOrientation(-74)
  for i in range(0, 92):
    print "%d %s" % (i, ["%2.2f" % x for x in obj.getStateAtMinute(i)])
