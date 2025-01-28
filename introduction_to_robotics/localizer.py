#!/usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt32, String, UInt32MultiArray, Float64MultiArray
import numpy as np
import colorsys
import time
import datetime

class BayesLoc:

  errors = [0]
  line_idx = -1

  def __init__(self, p0, colour_codes, colour_map):
      self.colour_sub = rospy.Subscriber(
          "mean_img_rgb", Float64MultiArray, self.colour_callback
      )
      self.line_sub = rospy.Subscriber("line_idx", UInt32, self.line_callback)
      self.cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)

      self.num_states = len(p0)
      self.colour_codes = colour_codes
      self.colour_map = colour_map
      self.probability = p0
      self.state_prediction = np.zeros(self.num_states)
      self.cur_colour = None  # most recent measured colour

      self.color_prev = 4
      self.color_state = 4

      self.cur = np.zeros((1,11))
      self.delivery = False
      self.u = 0

      # Initial state table taken from Table 1 in project overview document 	
      self.state_table = [
          [0.85, 0.05, 0.5],
          [0.05, 0.90, 0.05],
          [0.05, 0.05, 0.85]
      ]
      
      self.location = 0
      self.measure_table = [
          []
      ]
 
  def colour_callback(self, msg):
      """
      Callback function that receives the most recent colour measurement from the camera
      """
      self.cur_colour = np.array(msg.data)  # [r, g, b]


  def line_callback(self, msg):
      """
      Callback function that determines how much the robot deviates from the line/path
      """
      self.line_idx = msg.data
      if msg.data < 633:
          self.errors.append(320 - msg.data)


  def follow_path(self):
      """
      Implements PID control to guide the robot along the line/path 
      """
      rate = rospy.Rate(20)

      while not rospy.is_shutdown():
         twist = Twist()
         twist.linear.x = 0.075
         e = 320 - self.line_idx
         integ = np.trapz(self.errors)
         deriv = e - self.errors[-1]

         kp = 0.00149
         ki = 0.00001
         kd = 0.01
         twist.angular.z = e*kp + integ*ki + deriv*kd
         self.cmd_pub.publish(twist)
         self.measurement_model(self.color_state)
     
         self.u = 1
 
         # If the robot was just at an 'office' and is now detects a line,
         # perform a state predict and update
         if self.color_prev != 4 and self.color_state == 4:
             self.state_predict(u)
             self.state_update(u)
             self.location = np.argmax(localizer.probability)

             if self.location not in visited and self.location in tovisit:
                 self.u = 0
                 self.delivery = True
             else:
                 self.u=1
       
             if self.delivery == True:
                 twist.linear.x = 0

                 prev_ang = twist.angular.z
                 twist.angular.z = 0

                 self.cmd_pub.publish(twist)
                 time.sleep(2)

                 twist.linear.x = 0.075
                 twist.angular.z = prev_ang
                 self.delivery = False

         rate.sleep()

      return

  def wait_for_colour(self):
      """
      Loop until a colour is received
      """
      rate = rospy.Rate(100)
      while not rospy.is_shutdown() and self.cur_colour is None:
          rate.sleep()


  def state_model(self, u):
      """
      Determine probability of next office, given current office and movement
      """
      # Close to deterministic, assume u can be used
      probs = [0] * 11 # Probabilities of each office (uniform)

      for x in range(0, len(probs)):
          if x == 0:
              probs[x] += self.probability[x] * self.state_table[1][u + 1]
              probs[x + 1] += self.probability[x] * self.state_table[2][u + 1]
          elif x == len(probs) - 1:
              probs[x - 1] += self.probability[x] * self.state_table[0][u + 1]
              probs[x] += self.probability[x] * self.state_table[1][u + 1]
          else:
              probs[x - 1] += self.probability[x] * self.state_table[0][u + 1]
              probs[x] += self.probability[x] * self.state_table[1][u + 1]
              probs[x + 1] += self.probability[x] * self.state_table[2][u + 1]

      return probs

  def get_euclidean(self, p1, p2):
      return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2)

  def measurement_model(self, x):
      """
      Determine probability of each possible color, given the pixel intensity
      """
      if self.cur_colour is None:
          self.wait_for_colour()

      prob = np.zeros(len(self.colour_codes))

      measure = [0, 0, 0, 0, 0]

      self.wait_for_colour()
      r, g, b = self.cur_colour

      #        [0,      1,       2,        3,       4]
      colors = ["red", "purple", "orange", "brown", "line"]

      for i in range(0, len(measure)):
          dist = self.get_euclidean([r, g, b], colour_codes[i])
          measure[i] = dist

      norm = sum(measure)
      for i in range(0, len(measure)):
          measure[i] = measure[i] / norm
     
      self.color_prev = self.color_state
      prob = min(measure)
      self.color_state = measure.index(prob)

      print(self.probability)
      print(f"{colors[self.color_state]}: {self.location + 2}")

      return measure


  def state_predict(self, u):
      """
      Update state prediction with the predicted probability of being at each
      state (office)
      """
      rospy.loginfo("Predicting state")
    
      state_predictions = [0]*11
      for i in range(len(self.colour_map)):
          state_predictions[i] = float(self.probability[i]) * self.state_model(u)[i]
         
      return state_predictions

  def state_update(self, u):
      """
      Update probabilities with the probability of being at each state
      """
      rospy.loginfo("Updating state")

      state_updates = [0]*11
      for i in range(len(self.colour_map)):
          measure = self.measurement_model(i)
          state_updates[i] = measure[self.colour_map[i-1]] * self.state_predict(u)[i]
      self.probability = state_updates/np.sum(state_updates)
      return self.probability

if __name__ == "__main__":
  # This is the known map of offices by colour
  # 0: red, 1: purple, 2: orange, 3: brown, 4: line
  # current map starting at office #2 and ending at office #12
  colour_map = [1, 2, 3, 0, 1, 2, 0, 1, 2, 3, 3]
  tovisit = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
  visited = []

  colour_codes = [
      [200, 85, 90], # red
      [175, 145, 200], # purple
      [210, 120, 65], # orange
      [180, 165, 145], # brown
      [150, 150, 150] # line
  ]

  # Initial probability of being at a given office is uniform
  p0 = [1/11, 1/11, 1/11, 1/11, 1/11, 1/11, 1/11, 1/11, 1/11, 1/11, 1/11]
  u = 1

  rospy.init_node("final_project")
  localizer = BayesLoc(p0, colour_codes, colour_map)

  rospy.sleep(0.5)
  rate = rospy.Rate(10)

  while not rospy.is_shutdown():
       localizer.measurement_model(0)
       localizer.follow_path()
       rate.sleep()
