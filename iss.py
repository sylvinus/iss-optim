#!/usr/bin/env python

from math import cos, sin, acos, asin, atan, pi
import math

# Parameters are determined in function of the beta angle.
# There is a fixed list of beta angles so we can over-optimize for that...

"""
other insteresting possible starts:

{"72": {"backpanels_angle": -0.058081170108740809, "frontpanels_angle": 0.096524828897619264, "fast_cycle_2_accel": 0.3131072637717327, "yaw": 0.0, "fast_cycle_1_start": 2.191132510985939, "fast_cycle_1_length": 0.64123387684647237, "fast_cycle_1_accel": 0.13249386279639749, "fast_cycle_2_length": 1.6653094751964459, "fast_cycle_2_start": 4.9912847588147446}
159565.565024 {'72': {'backpanels_angle': -0.0085394627603317379, 'frontpanels_angle': 0.023438086430557007, 'fast_cycle_2_accel': 0.33931555737718289, 'yaw': 0.0, 'fast_cycle_1_start': 3.0859093022032069, 'fast_cycle_1_length': 1.7438042093649595, 'fast_cycle_1_accel': 0.29948464172964662, 'fast_cycle_2_length': 2.077661185972699, 'fast_cycle_2_start': 4.9160996064710663}}
159565.56502 {'72': {'backpanels_angle': -0.0085394777603317387, 'frontpanels_angle': 0.023438086430557007, 'fast_cycle_2_accel': 0.33931555737718289, 'yaw': 0.0, 'fast_cycle_1_start': 3.0859093022032069, 'fast_cycle_1_length': 1.7438042093649595, 'fast_cycle_1_accel': 0.29948464172964662, 'fast_cycle_2_length': 2.077661185972699, 'fast_cycle_2_start': 4.9160996064710663}}

[158538.77428211164, {"-70": {"backpanels_angle": -0.058081170108740809, "frontpanels_angle": 0.096524828897619264, "fast_cycle_2_accel": 0.3131072637717327, "yaw": 0.0, "fast_cycle_1_start": 2.191132510985939, "fast_cycle_1_length": 0.64123387684647237, "fast_cycle_1_accel": 0.13249386279639749, "fast_cycle_2_length": 1.6653094751964459, "fast_cycle_2_start": 4.9912847588147446}}]
159331.610707 {'-70': {'backpanels_angle': -0.0031205354155288837, 'frontpanels_angle': 0.003306896943848182, 'fast_cycle_2_accel': 0.35193894017534844, 'yaw': 0.0, 'fast_cycle_1_start': 3.2064574031683728, 'fast_cycle_1_length': 1.7713782005406706, 'fast_cycle_1_accel': 0.34986622845796067, 'fast_cycle_2_length': 2.1472054569607355, 'fast_cycle_2_start': 4.7932891294498692}}
159293.298401 {'-70': {'backpanels_angle': -0.0055818069530143063, 'frontpanels_angle': 0.018183541522190275, 'fast_cycle_2_accel': 0.36217763626285809, 'yaw': 0.0, 'fast_cycle_1_start': 3.1676050048843378, 'fast_cycle_1_length': 1.7622463711408329, 'fast_cycle_1_accel': 0.31543099452558448, 'fast_cycle_2_length': 2.1718234439542554, 'fast_cycle_2_start': 4.8196411794091372}}

151632.601717 {'-74': {'backpanels_angle': 0.15560119280597581, 'frontpanels_angle': -0.29185396904851968, 'fast_cycle_2_accel': 0.17859680486139437, 'yaw': 0.0, 'fast_cycle_1_start': 3.0605958608245092, 'fast_cycle_1_length': 1.6890880505308581, 'fast_cycle_1_accel': 0.097979098752489641, 'fast_cycle_2_length': 2.2082514016130554, 'fast_cycle_2_start': 4.9291701610333174}}
151809.329981 {'-74': {'backpanels_angle': -0.0016813148769646935, 'frontpanels_angle': -0.31543461601882539, 'fast_cycle_2_accel': 0.18080358853662248, 'yaw': 0.0, 'fast_cycle_1_start': 3.0699925251289315, 'fast_cycle_1_length': 1.7398855546485446, 'fast_cycle_1_accel': 0.14890684738160895, 'fast_cycle_2_length': 2.1793131225704654, 'fast_cycle_2_start': 4.929439382577715}}
151590.422583 {'-74': {'backpanels_angle': 0.16026118345496509, 'frontpanels_angle': -0.29262821941935951, 'fast_cycle_2_accel': 0.17552341280439349, 'yaw': 0.0, 'fast_cycle_1_start': 3.0699906657970368, 'fast_cycle_1_length': 1.7379363465117301, 'fast_cycle_1_accel': 0.14693096502776681, 'fast_cycle_2_length': 2.1762757879598937, 'fast_cycle_2_start': 4.9236244066728592}}
[151488.98261405242, {"-74": {"backpanels_angle": 0.16048406957982925, "frontpanels_angle": -0.28877332900034502, "fast_cycle_2_accel": 0.18080358853662248, "yaw": 0.0, "fast_cycle_1_start": 3.0699925251289315, "fast_cycle_1_length": 1.7398855546485446, "fast_cycle_1_accel": 0.14890684738160895, "fast_cycle_2_length": 2.1793131225704654, "fast_cycle_2_start": 4.9294393825777147}}]


152780.965849 {'74': {'backpanels_angle': -0.12438107495562138, 'frontpanels_angle': 0.30922232597806176, 'fast_cycle_2_accel': 0.19164539576917322, 'yaw': 0.0, 'fast_cycle_1_start': 3.0879538814243546, 'fast_cycle_1_length': 1.7415899237431722, 'fast_cycle_1_accel': 0.19032974616900555, 'fast_cycle_2_length': 2.087375765503332, 'fast_cycle_2_start': 4.9356827680152007}}
152784.716699 {'74': {'backpanels_angle': -0.12436646815374895, 'frontpanels_angle': 0.30757606224507916, 'fast_cycle_2_accel': 0.19165057804193542, 'yaw': 0.0, 'fast_cycle_1_start': 3.087954548826399, 'fast_cycle_1_length': 1.7415902333175564, 'fast_cycle_1_accel': 0.19033233084227863, 'fast_cycle_2_length': 2.0873709020004334, 'fast_cycle_2_start': 4.935683305981026}}
151166.461609 {'74': {'backpanels_angle': 0.10136377074658054, 'frontpanels_angle': 0.32449448958625027, 'fast_cycle_2_accel': 0.13885124872185531, 'yaw': 0.0, 'fast_cycle_1_start': 2.6363927722433815, 'fast_cycle_1_length': 0.54423028147142505, 'fast_cycle_1_accel': 0.013910209552301378, 'fast_cycle_2_length': 2.8941041131297487, 'fast_cycle_2_start': 5.6829097218117823}}
152834.282171 {'74': {'backpanels_angle': -0.10508753931300194, 'frontpanels_angle': 0.30444675953734901, 'fast_cycle_2_accel': 0.19165057804193542, 'yaw': 0.0, 'fast_cycle_1_start': 3.087954548826399, 'fast_cycle_1_length': 1.7415902333175564, 'fast_cycle_1_accel': 0.19033233084227863, 'fast_cycle_2_length': 2.0873709020004334, 'fast_cycle_2_start': 4.935683305981026}}
[152928.60695093052, {"74": {"backpanels_angle": -0.040463658494283905, "backpanels_phase": 5.2036001201666853, "frontpanels_angle": 0.31768531282514034, "fast_cycle_2_accel": 0.2399412725174822, "backpanels_amplitude": 2.8527311385321679, "frontpanels_phase": 5.4109258225195829, "fast_cycle_1_start": 3.0806075316995525, "fast_cycle_1_length": 1.7409493623038732, "fast_cycle_1_accel": 0.23923337055832766, "fast_cycle_2_length": 2.0885153470649493, "frontpanels_amplitude": -0.50776905267858585, "yaw": 0.00029972257465681659, "fast_cycle_2_start": 4.933348883207836}}]
152876.061528 {'74': {'backpanels_angle': -0.10253286101436385, 'frontpanels_angle': 0.30951971118072763, 'fast_cycle_2_accel': 0.19165057804193542, 'yaw': 0.0, 'fast_cycle_1_start': 3.087954548826399, 'fast_cycle_1_length': 1.7415902333175564, 'fast_cycle_1_accel': 0.19033233084227863, 'fast_cycle_2_length': 2.0873709020004334, 'fast_cycle_2_start': 4.935683305981026}}
[152382.1368978579, {"74": {"backpanels_angle": 0.0, "frontpanels_angle": 0.34000000000000002, "fast_cycle_2_accel": 0.31, "yaw": 0.0, "fast_cycle_1_start": 3.0699999999999998, "fast_cycle_1_length": 1.74, "fast_cycle_1_accel": 0.31, "fast_cycle_2_length": 2.0899999999999999, "fast_cycle_2_start": 4.9299999999999997}}]

152928.606951 {'74': {'backpanels_angle': -0.040463658494283905, 'backpanels_phase': 5.2036001201666853, 'frontpanels_angle': 0.31768531282514034, 'fast_cycle_2_accel': 0.2399412725174822, 'backpanels_amplitude': 2.8527311385321679, 'frontpanels_phase': 5.4109258225195829, 'fast_cycle_1_start': 3.0806075316995525, 'fast_cycle_1_length': 1.7409493623038732, 'fast_cycle_1_accel': 0.23923337055832766, 'fast_cycle_2_length': 2.0885153470649493, 'frontpanels_amplitude': -0.50776905267858585, 'yaw': 0.00029972257465681659, 'fast_cycle_2_start': 4.933348883207836}}


"""

PARAMS = {
  "72": {'backpanels_angle': -0.0085394627603317379, 'frontpanels_angle': 0.023438086430557007, 'fast_cycle_2_accel': 0.33931555737718289, 'yaw': 0.0, 'fast_cycle_1_start': 3.0859093022032069, 'fast_cycle_1_length': 1.7438042093649595, 'fast_cycle_1_accel': 0.29948464172964662, 'fast_cycle_2_length': 2.077661185972699, 'fast_cycle_2_start': 4.9160996064710663},
  "74": {'backpanels_angle': -0.040463658494283905, 'backpanels_phase': 5.2036001201666853, 'frontpanels_angle': 0.31768531282514034, 'fast_cycle_2_accel': 0.2399412725174822, 'backpanels_amplitude': 2.8527311385321679, 'frontpanels_phase': 5.4109258225195829, 'fast_cycle_1_start': 3.0806075316995525, 'fast_cycle_1_length': 1.7409493623038732, 'fast_cycle_1_accel': 0.23923337055832766, 'fast_cycle_2_length': 2.0885153470649493, 'frontpanels_amplitude': -0.50776905267858585, 'yaw': 0.00029972257465681659, 'fast_cycle_2_start': 4.933348883207836},
  "-70": {'backpanels_angle': -0.0031205354155288837, 'frontpanels_angle': 0.003306896943848182, 'fast_cycle_2_accel': 0.35193894017534844, 'yaw': 0.0, 'fast_cycle_1_start': 3.2064574031683728, 'fast_cycle_1_length': 1.7713782005406706, 'fast_cycle_1_accel': 0.34986622845796067, 'fast_cycle_2_length': 2.1472054569607355, 'fast_cycle_2_start': 4.7932891294498692},
  "-74": {'backpanels_angle': -0.0016813148769646935, 'frontpanels_angle': -0.31543461601882539, 'fast_cycle_2_accel': 0.18080358853662248, 'yaw': 0.0, 'fast_cycle_1_start': 3.0699925251289315, 'fast_cycle_1_length': 1.7398855546485446, 'fast_cycle_1_accel': 0.14890684738160895, 'fast_cycle_2_length': 2.1793131225704654, 'fast_cycle_2_start': 4.929439382577715},


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
    self.yaw = self.params["yaw"]
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
        self.panels[p] += self.params["frontpanels_angle"]+self.yaw*(self.params.get("frontpanels_amplitude",0)*sin(self.alpha+self.params.get("frontpanels_phase",0)))
      else:
        self.panels[p] += self.params["backpanels_angle"]+self.yaw*(self.params.get("backpanels_amplitude",0)*sin(self.alpha+self.params.get("backpanels_phase",0)))

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
