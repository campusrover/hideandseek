#!/usr/bin/env python
#autonomous bot

import rospy, cv2, cv_bridge, numpy, math, random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Image
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion

regions_ = {           
   'right':0,
   'left':0,
   'fright':0,
   'front':0,
   'fleft':0
}
state1 = 0
PI = 3.14
distance = 1.5
distanceX = 0.0
distanceY = 0.0
roll = pitch = yaw = 0
hide = False
turned = False


# scan callback
def scan_callback(msg):
    global ranges, regions_
    ranges = msg.ranges
    regions_ = {
        'right':  min(min(msg.ranges[60:92]), 10),
        'fright': min(min(msg.ranges[10:59]), 10),
        'front':  min(min(msg.ranges[0:10]), 10),
        'fleft':  min(min(msg.ranges[280:339]), 10),
        'left':   min(min(msg.ranges[270:300]), 10),
    }

    decider()

def odom_callback(msg):
    global distanceX, distanceY
    global roll, pitch, yaw
    distanceX = msg.pose.pose.position.x
    distanceY = msg.pose.pose.position.y
    orientation = msg.pose.pose.orientation
    orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

# img callback
def img_callback(msg):
    global img
    image = self.bridge.imgmsg_to_cv2(msg)

def key_cb(msg):
   global state; global last_key_press_time
   state = msg.data
   last_key_press_time = rospy.Time.now()

# pub/subs
scan_sub = rospy.Subscriber('/hider/scan', LaserScan, scan_callback)
img_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, img_callback)
cmd_vel_pub = rospy.Publisher('/hider/cmd_vel', Twist, queue_size=1)
odom_sub = rospy.Subscriber('/hider/odom', Odometry, odom_callback)

# init node 
rospy.init_node('hider')
rate = rospy.Rate(10)
ranges = None; img = None
turned = False

def decider():
    global regions_, hide, turned
    regions = regions_
    d = 0.6
    d2 = 1.5
    if abs(distanceX) > 3 and abs(distanceY) > 3 and regions['front'] < 0.4 and regions['right'] < 0.8 and turned == True:  #or regions['left'] < 0.2 
        change_state(4)
        hide = True
        rospy.loginfo(regions)
    elif regions['front'] < 0.8 and regions['left'] < 0.8:  
        change_state(1)  # turn right
    elif regions['front'] < 0.7 and regions['right'] > d and regions['left'] > d:
        change_state(1)     #wont run into wall
    elif regions['fleft'] < d or regions['fleft'] == d or regions['left'] < d or regions['fright'] < d or regions['fright'] == d or regions['right'] < d:
       change_state(2)  # follow wall
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        change_state(0)  # find wall
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
        change_state(3)  # backup
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d :
        change_state(2)
        rospy.loginfo(regions)
def change_state(state):
   global state1, distanceX, distanceY
   if state is not state1:
       print 'State: [%s]' % (state)  # prints state
       print 'DistanceX: [%s]' % (distanceX)
       print 'DistanceY: [%s]' % (distanceY)
       state1 = state  # changes state

def follow_the_wall():
   global regions_
   msg = Twist()
   msg.linear.x = 0.4
   return msg

def find_wall():
   msg = Twist()
   msg.linear.x = 0.4
   return msg
 
def turn():
    msg = Twist()
    msg.linear.x = 0.1
    msg.angular.z = PI/6
    return msg
 
def chooseDirection(direction):
    global turned
    turn = 0
    if direction == 1:
        turn = 0.5
    elif direction == 2:
        turn = 2.5
    elif direction == 3:
        turn = -0.785
    elif direction == 4:
        turn = -2.3
    turned = True 
    return turn

# control loop
while not rospy.is_shutdown():
    global regions_
    decider()
    msg = Twist()
    print(turned)
    if turned == False:
        direction = random.randint(1,4)
        print(direction)
        turn = chooseDirection(direction)
        if turn > 0:
            while yaw < turn:
                msg.angular.z = 0.3
                cmd_vel_pub.publish(msg)            ## might not need second publisher
        elif turn < 0:
            while yaw > turn: 
                msg.angular.z = -0.3
                cmd_vel_pub.publish(msg) 
    if state1 == 0:
        msg = find_wall()
    elif state1 == 1:
        msg = turn()      #turns right
    elif state1 == 2:
        msg = follow_the_wall()
        pass
    elif state1 == 3:
        msg = backup()
        pass
    elif state1 == 4:
        msg.linear.x = 0
        msg.angular.z = 0
        print(regions_)
        break

    cmd_vel_pub.publish(msg)

    # runs at 10hz
    rate.sleep()