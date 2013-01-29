#!/usr/bin/env python

from math import cos, sin, tan, acos, asin, atan, pi
import math

"""
TODO
 - correct for Z offset for SAWs
 - optimal front sarj adjustment
 - round corners of backpanel cycles depending on length+prelength
"""


# Parameters are determined in function of the beta angle.
# There is a fixed list of beta angles so we can over-optimize for that...
PARAMS = {"-70": {'fast_cycle_3_start': 1.5781581719959785, 'fast_cycle_4_prelength': 0.5738103536557352, 'fast_cycle_3_prelength': 0.20402276806606734, 'fast_cycle_4_length': 0.5533995345702356, 'fast_cycle_2_start': 0.8717589058059763, 'fast_cycle_4_start': 4.389864585478478, 'fast_cycle_2_prelength': 0.5383338465664779, 'fast_cycle_1_start': 0.1680757991355482, 'fast_cycle_1_length': 0.30226150099755544, 'fast_cycle_2_length': 0.023215732759460428, 'fast_cycle_3_length': 0.17539242588995468, 'yaw': 0.0414804736024119, 'fast_cycle_1_prelength': 0.8996341400498821},
 "72": {"fast_cycle_3_start": 1.6644662062117188, "fast_cycle_4_prelength": 0.1882088293572058, "fast_cycle_3_prelength": 0.6556661559127275, "fast_cycle_4_length": 1.3630347090477684, "fast_cycle_2_start": 0.8627463218613023, "fast_cycle_4_start": 4.715243306618757, "fast_cycle_2_prelength": 0.161266490900138, "fast_cycle_1_start": 0.016893475792793506, "fast_cycle_1_length": 0.4008344812619442, "fast_cycle_2_length": 0.9599593983418363, "fast_cycle_3_length": 0.6632941623306733, "yaw": 0.001777557132575147, "fast_cycle_1_prelength": 0.5863264558380866},
 "74": {'fast_cycle_3_start': 1.5781581719959785, 'fast_cycle_4_prelength': 0.5738103536557352, 'fast_cycle_3_prelength': 0.20402276806606734, 'fast_cycle_4_length': 0.5533995345702356, 'fast_cycle_2_start': 0.8717589058059763, 'fast_cycle_4_start': 4.389864585478478, 'fast_cycle_2_prelength': 0.5383338465664779, 'fast_cycle_1_start': 0.1680757991355482, 'fast_cycle_1_length': 0.30226150099755544, 'fast_cycle_2_length': 0.023215732759460428, 'fast_cycle_3_length': 0.17539242588995468, 'yaw': 2.2663250365290128e-05, 'fast_cycle_1_prelength': 0.8996341400498821},
 "-74": {'fast_cycle_3_start': 1.84397829667227, 'fast_cycle_4_prelength': 1.0738103536557352, 'fast_cycle_3_prelength': 0.20402276806606734, 'fast_cycle_4_length': 0.5533995345702356, 'fast_cycle_2_start': 0.40977295481606, 'fast_cycle_4_start': 4.644093487915346, 'fast_cycle_2_prelength': 0.5383338465664779, 'fast_cycle_1_start': 0.13659098493868665, 'fast_cycle_1_length': 0.30226150099755544, 'fast_cycle_2_length': 0.023215732759460428, 'fast_cycle_3_length': 0.57539242588995468, 'yaw': 0.020688516408021457, 'fast_cycle_1_prelength': 0.8996341400498821}}




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


  def setParamsArray(self, params):
    self.paramsArray = params
    

  # Public interface methods
  def getInitialOrientation(self, beta):
    self.params = self.paramsArray[str(int(float(beta)))]
    self.beta = math.radians(float(beta))
    self.yaw = self.params["yaw"]

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


    self.adjustVelocities(sarj=True)
    
    self.adjustFrontSarj()

    self.adjustVelocities(sarj=True)

      #self.correctPanelsForSarj()

    self.optimizePanelAnglesNew()

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
      #if m==8 and p=="BACK":
      #  print t1, t2
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
      #if m==8 and p=="BACK":
      #  print maxSpeed, speed1, t1, t2
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
        max_velocity = math.radians(0.15)
        max_accel = math.radians(0.005)

      elif p in self.panels and saw:
        max_velocity = math.radians(0.25)
        max_accel = math.radians(0.01)
      else:
        continue

      for m in range(0, 92):

        diff = smallradians(self.angles[(m + 1) % 92][p] - self.angles[m][p])

        currentSpeed = self.speeds[m][p]
        finalSpeed = self.speeds[(m + 1) % 92][p]

        max_diff = get_max_possible_angular_shift(currentSpeed, max_velocity, max_velocity, max_accel)
        min_diff = get_min_possible_angular_shift(currentSpeed, -max_velocity, -max_velocity, -max_accel)

        #can the point be atteinted but not at the same speed?
        max_diff_w_speed = get_max_possible_angular_shift(currentSpeed, finalSpeed, max_velocity, max_accel)
        min_diff_w_speed = get_max_possible_angular_shift(currentSpeed, finalSpeed, -max_velocity, -max_accel)

        if diff <= min_diff + 1e-12:
          self.angles[(m + 1) % 92][p] = self.angles[m][p] + min_diff
          self.speeds[(m + 1) % 92][p] = -max_velocity
        elif diff >= max_diff - 1e-12:
          self.angles[(m + 1) % 92][p] = self.angles[m][p] + max_diff
          self.speeds[(m + 1) % 92][p] = max_velocity

        elif (diff > max_diff_w_speed) or (diff < min_diff_w_speed):

          # equal the final speed
          t0 = math.fabs((finalSpeed - currentSpeed) / max_accel)

          diff0 = path(t0, currentSpeed, math.copysign(max_accel, (finalSpeed - currentSpeed)))

          lineardiff = finalSpeed * (60 - t0)
          if lineardiff > 0:
            newdiff = path((60 - t0) / 2, finalSpeed, -max_accel) * 2
          else:
            newdiff = path((60 - t0) / 2, finalSpeed, max_accel) * 2

          """
          if p=="BACK":
            print "ZANG", m, diff
            print math.copysign(max_accel,(finalSpeed-currentSpeed))
            print currentSpeed, finalSpeed
            print diff0, t0, lineardiff, newdiff
          

          if p=="BACK":
            print 
            print currentSpeed, finalSpeed
            print diff
            print max_diff, min_diff
            print diff >= max_diff - 1e-10
            print max_diff_w_speed, min_diff_w_speed
            print max_velocity, math.degrees(max_velocity)
            print (min_diff-min_diff_w_speed) / 60
            print self.speeds[(m + 1) % 92][p]
            print diff * 2.0 / 60 - currentSpeed
            print math.degrees(self.speeds[(m + 1) % 92][p])
          """

          #angle was modified, not speed
          self.angles[(m + 1) % 92][p] = self.angles[m][p] + diff0 + newdiff

        #elif diff < min_diff_w_speed:
        #  self.speeds[(m + 1) % 92][p] = 2 * diff / 60 - currentSpeed
        
        


  def adjustFrontSarj(self):

    max_angle = 0.23

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

      minute_start = int(math.ceil(tominute(start) - tominute(prelength)))
      minute_stop = int(math.ceil(tominute(start) + tominute(length)))

      for m in range(minute_start, minute_stop + 1):
        self.angles[m%92]["BACK"] = start

      self.angles[(minute_start-1)%92]["BACK"] = start - (minute_start - (tominute(start) - tominute(prelength)))*60*math.radians(0.10)
      self.angles[(minute_start+1)%92]["BACK"] = start - (minute_stop - (tominute(start) + tominute(length)))*60*math.radians(0.10)

    for i in range(1, 5):
      set_cycle_velocity_diff(i)


  def optimizePanelAnglesNew(self):

    width_between_blankets = 1927.51
    
    blanket_width = 4752.25

    border_to_blanket = 133.75 + 94

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
          if pi-asin(panel_width/saw_to_sun_contact)>sun_angle:
            continue

          #print
          #print panel_top_y, panel_width
          #print tan(sun_angle)
          #print sin(pi / 2 - sun_angle) * panel_top_y / panel_width


          panel_angle = asin(sin(pi / 2 - sun_angle) * panel_top_y / panel_width) - sun_angle

          #if p == "1B":
          #  print m, panel_angle

          #

          self.angles[m][p] = panel_angle # -74: 0.12 #TODO!!! #(self.angles[m][p]+9*panel_angle)/10







  def optimizePanelAngles(self):

    for m in range(0, 92):
      for p in self.panels:
        if p in self.listFrontPanels():
          self.angles[m][p] += self.params["frontpanels_angle"]
        else:
          self.angles[m][p] += self.params["backpanels_angle"]


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

  obj = ISS()
  obj.getInitialOrientation(-74)
  for i in range(0, 92):
    print "%d %s" % (i, ["%2.14f" % x for x in obj.getStateAtMinute(i)])
