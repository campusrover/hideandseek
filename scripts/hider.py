#!/usr/bin/env python
#autonomous bot

import rospy, cv2, cv_bridge, numpy, math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Image

# scan callback
def scan_callback(msg):
    global ranges
    ranges = msg.ranges

# img callback
def img_callback(msg):
    global img
    image = self.bridge.imgmsg_to_cv2(msg)

def key_cb(msg):
   global state; global last_key_press_time
   state = msg.data
   last_key_press_time = rospy.Time.now()

# odom is also not necessary but very useful
def odom_cb(msg):
   return

# pub/subs
scan_sub = rospy.Subscriber('/scan', LaserScan, scan_callback)
img_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, img_callback)
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

# init node 
rospy.init_node('hider')
rate = rospy.Rate(10)
ranges = None; img = None

# control loop
while not rospy.is_shutdown():

    # runs at 10hz
    rate.sleep()