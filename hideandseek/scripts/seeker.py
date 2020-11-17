#!/usr/bin/env python
#teleop bot
import rospy
import sys
import math
import tf
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion
def key_cb(msg):
   global state; global last_key_press_time
   state = msg.data
   last_key_press_time = rospy.Time.now()
rospy.init_node('seeker')
key_sub = rospy.Subscriber('keys', String, key_cb)
state = "H"
last_key_press_time = rospy.Time.now()
# set rate
rate = rospy.Rate(1)
velocity_vector = [0, 0]
PI = math.pi
LINEAR_SPEED = 0.2
ANGULAR_SPEED = PI/4
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
while not rospy.is_shutdown():
    # print out the current state and time since last key press
    t = Twist()
    current_time = rospy.Time.now()
    lapse = current_time - last_key_press_time
    # rotate left
    if state == "l":
        velocity_vector = [0, 1]
    # rotate right
    elif state == "r":
        velocity_vector = [0, -1]
    # move forward
    elif state == "f":
        velocity_vector = [1, 0]
    # move backward
    elif state == "b":
        velocity_vector = [-1, 0]

    t.linear.x = LINEAR_SPEED * velocity_vector[0]
    t.angular.z = ANGULAR_SPEED * velocity_vector[1]
    
    cmd_vel_pub.publish(t)
    rate.sleep()