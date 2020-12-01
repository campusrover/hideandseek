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

# img callback
def img_callback(msg):
    global img
    image = self.bridge.imgmsg_to_cv2(msg)


rospy.init_node('seeker')
img_sub = rospy.Subscriber('/seeker/camera/rgb/image_raw', Image, img_callback)
cmd_vel_pub = rospy.Publisher('/seeker/cmd_vel', Twist, queue_size=10)
last_key_press_time = rospy.Time.now()
rate = rospy.Rate(1)

def check_room():
   msg = Twist()
   msg.angular.z = 0.4
   return msg

while not rospy.is_shutdown():
    t = Twist()
    t = check_room()
    
    cmd_vel_pub.publish(t)
    rate.sleep()