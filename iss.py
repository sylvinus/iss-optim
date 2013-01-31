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
PARAMS = {"-70": {"sarjd_12": -0.17770814624297943, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.18234192299077615, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.004570466040045529, "sarjd_20": 0.29762632934120725, "sarjp_48": 3.27818363852848, "sarjd_60": 0.21919145588304217, "sarjd_48": -0.010469537582144132, "sarjd_64": 0.23906345239334198, "sarjd_68": -0.15343975917277974, "sarjd_40": 0.2540202420358353, "sarjd_44": -0.29801845972494295, "backpanels_angle": -0.0005626978728677377, "sarjd_0": -0.23870367391881286, "frontpanels_angle": -0.0018021451210250064, "sarjd_4": 0.0797586293245712, "yaw": 0.0416280513684409, "sarjd_32": 0.07867357948820666, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.29518411159183006, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.2674489086140967, "sarjp_0": 0.0, "sarjd_76": -0.1526323389301328, "sarjd_52": -0.26690737194872904, "sarjd_72": 0.024018931931874654, "sarjd_56": -0.06009597614831791, "sarjd_84": 0.2999149298722825, "sarjd_8": -0.21263983948941226, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.2995230580391146, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": 0.22702107145777983},
 "72": {"sarjd_12": 0.04660243952029262, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.18204667247249318, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.04467067367239206, "sarjd_20": 0.2994263532127694, "sarjp_48": 3.27818363852848, "sarjd_60": 0.2662798664139182, "sarjd_48": 0.03642846898929212, "sarjd_64": 0.23619492335427258, "sarjd_68": -0.1609815310219587, "sarjd_40": -0.12313916126853235, "sarjd_44": -0.18987532167448645, "backpanels_angle": -0.014731268451499838, "sarjd_0": 0.033706121881376325, "frontpanels_angle": 0.005921783893742168, "sarjd_4": 0.11436706241711082, "yaw": 0.0004957706763891608, "sarjd_32": -0.1691250271829811, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.14567316748739412, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.1682710649243153, "sarjp_0": 0.0, "sarjd_76": -0.06324744929934911, "sarjd_52": -0.20336694960181267, "sarjd_72": 0.12898535560733598, "sarjd_56": 0.20998818941187436, "sarjd_84": 0.2830994962737556, "sarjd_8": 0.185591296234241, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.261109791732945, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.17855023094124917},
 "74": {"sarjd_12": 0.09614519477998802, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.03447155697763723, "sarjp_40": 2.7318196987737333, "sarjd_24": 0.051031081254910744, "sarjd_20": 0.29681878914596166, "sarjp_48": 3.27818363852848, "sarjd_60": 0.14014930622132693, "sarjd_48": 0.03032968966735536, "sarjd_64": 0.29865609726706777, "sarjd_68": -0.05423205538037699, "sarjd_40": -0.04128281866781282, "sarjd_44": -0.2143889947683093, "backpanels_angle": -0.11105314394448565, "sarjd_0": -0.13598495157710686, "frontpanels_angle": 0.02111383346866192, "sarjd_4": 0.13767633750731653, "yaw": 0.0, "sarjd_32": 0.02651786729399566, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.108437565836883, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.1226370567570091, "sarjp_0": 0.0, "sarjd_76": -0.09483521909243034, "sarjd_52": -0.14663286999684685, "sarjd_72": 0.14292693002490608, "sarjd_56": 0.20358364136321183, "sarjd_84": 0.27900085185021456, "sarjd_8": 0.12371354048387162, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.2813639307840698, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.12327857178581807},
 "-74": {"sarjd_12": -0.11250737650394071, "sarjp_20": 1.3659098493868667, "sarjp_44": 3.0050016686511065, "sarjd_28": -0.1603235144746309, "sarjp_40": 2.7318196987737333, "sarjd_24": -0.021540932246100597, "sarjd_20": 0.2991344606929204, "sarjp_48": 3.27818363852848, "sarjd_60": -0.0002904540082842228, "sarjd_48": -0.07691025079874836, "sarjd_64": 0.29193726297206113, "sarjd_68": -0.29173783024371236, "sarjd_40": -0.2753268252941663, "sarjd_44": -0.26769145134795125, "backpanels_angle": 0.08293409480542584, "sarjd_0": 0.28490838153190784, "frontpanels_angle": 0.038949912370479095, "sarjd_4": 0.0771028304964696, "yaw": 0.02099660013660592, "sarjd_32": -0.0460351553846802, "sarjp_8": 0.5463639397547466, "sarjp_28": 1.9122737891416133, "sarjp_72": 4.91727545779272, "sarjp_24": 1.63909181926424, "sarjp_56": 3.8245475782832266, "sarjp_52": 3.5513656084058534, "sarjp_36": 2.45863772889636, "sarjp_32": 2.1854557590189865, "sarjp_12": 0.81954590963212, "sarjp_84": 5.73682136742484, "sarjd_36": -0.17516701888875963, "sarjp_16": 1.0927278795094932, "sarjd_16": -0.1826886480892882, "sarjp_0": 0.0, "sarjd_76": -0.1873847569592944, "sarjd_52": -0.2848656787874202, "sarjd_72": 0.013958834602915726, "sarjd_56": -0.06489327906415357, "sarjd_84": 0.12610682612486412, "sarjd_8": 0.08713961639018108, "sarjp_76": 5.1904574276700925, "sarjp_4": 0.2731819698773733, "sarjp_80": 5.463639397547467, "sarjp_68": 4.644093487915346, "sarjd_88": 0.20207489452371433, "sarjp_64": 4.370911518037973, "sarjp_88": 6.010003337302213, "sarjp_60": 4.0977295481606, "sarjd_80": -0.18931981362533032}}
 

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

    self.optimizeSarjAnglesLinear()


    #for m in range(0, 92):


    self.adjustVelocities(sarj=True)

    self.adjustFrontSarj()

    self.adjustVelocities(sarj=True)

    if DEBUG:
      #plot([x["BACK"] for x in self.angles])
      
      plot([self.params.get("sarjd_%s"%i,0) for i in range(0,92) if i%4==0])
      show()
    


      #self.correctPanelsForSarj()

    self.optimizePanelAnglesNew()

    self.patchPanelAngles()

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
    for cycle_no in range(1, 100):

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
        if tominute(points[n%len(points)][0])>m:
          pointn = n
          break

      nextpoint = points[pointn%len(points)]
      lastpoint = points[(pointn-1)%len(points)]

      ratio = ((tominute(nextpoint[0]) - m)%92) / ((tominute(nextpoint[0]) - tominute(lastpoint[0]))%92)
      #print m, ratio
      #print tominute(nextpoint[0]), tominute(lastpoint[0])
      #print nextpoint[1], lastpoint[1]
      #print ratio * (nextpoint[1] - lastpoint[1]) + nextpoint[1]
      #print
      self.angles[m]["BACK"] += ratio * (nextpoint[1] - lastpoint[1]) + nextpoint[1]




  def optimizePanelAnglesNew(self):

    width_between_blankets = 1927.51
    
    blanket_width = 4752.25

    border_to_blanket = 133.75 + 94

    #TODO wtf
    if self.beta>math.radians(73.9):
      border_to_blanket = 0

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

          """
          if p == "2B":
            print
            print m
            print sun_angle
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

          #Can't optimize the shades (limit case is rect triangle)
          #if pi-asin(panel_width/saw_to_sun_contact)>sun_angle:
          #  continue
          if math.fabs(sin(pi / 2 - sun_angle) * panel_top_y / panel_width)>1:
            continue

          panel_angle = asin(sin(pi / 2 - sun_angle) * panel_top_y / panel_width) - sun_angle


          self.angles[m][p] = panel_angle # -74: 0.12 #TODO!!! #(self.angles[m][p]+9*panel_angle)/10




  def patchPanelAngles(self):

    for m in range(0, 92):
      for p in self.panels:
        if p in self.listFrontPanels():
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
