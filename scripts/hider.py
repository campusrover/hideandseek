#!/usr/bin/env python
#autonomous hider bot

import rospy, cv2, cv_bridge, numpy, math, random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Image
from nav_msgs.msg import Odometry
from geometry_msgs.msg import *
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion

regions_ = {            #initialize regions      
   'right':0,
   'left':0,
   'fright':0,
   'front':0,
   'fleft':0
}
state1 = 0              #initialize all constants
PI = 3.14
distanceX = 0.0
distanceY = 0.0
roll = pitch = yaw = 0
hide = False
turned = False
direction = 0

# scan callback
def scan_callback(msg):
    global ranges, regions_
    ranges = msg.ranges
    regions_ = {                #define scan regions
        'right':  min(min(msg.ranges[60:92]), 10),
        'fright': min(min(msg.ranges[10:59]), 10),
        'front':  min(min(msg.ranges[0:10]), 10),
        'fleft':  min(min(msg.ranges[280:339]), 10),
        'left':   min(min(msg.ranges[270:300]), 10),
    }

def odom_callback(msg):
    global distanceX, distanceY
    global roll, pitch, yaw
    distanceX = msg.pose.pose.position.x
    distanceY = msg.pose.pose.position.y
    orientation = msg.pose.pose.orientation
    orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

# pub/subs
scan_sub = rospy.Subscriber('/hider/scan', LaserScan, scan_callback)
cmd_vel_pub = rospy.Publisher('/hider/cmd_vel', Twist, queue_size=1)
odom_sub = rospy.Subscriber('/hider/odom', Odometry, odom_callback)

# init node 
rospy.init_node('hider')
rate = rospy.Rate(10)
ranges = None; img = None
turned = False

def decider():
    global regions_, hide, turned, direction
    regions = regions_
    d = 0.8
    print(regions_)
    if regions['front'] < d and regions['right'] < 0.4 or regions['left'] < 0.4 and turned == True:  #conditions for corner detection
        if direction == 4:
            if abs(distanceY) > 5:
                change_state(4)
                hide = True
                rospy.loginfo(regions)
        if abs(distanceX) > 4 and abs(distanceY) > 4:     #conditions for odometry readings
            change_state(4)
            hide = True
            rospy.loginfo(regions)
    elif regions['front'] < 1 and regions['left'] < 1:  
        print("here")
        change_state(1)  # turn right
    elif regions['front'] < d and regions['right'] > d:
        print("here2")
        change_state(1)    #wall avoidance
    elif regions['front'] < d and regions['right'] < d:
        print("left")
        change_state(3)     #turn left
    elif regions['fleft'] < d or regions['fleft'] == d or regions['left'] < d or regions['fright'] < d or regions['fright'] == d or regions['right'] < 0.6:
       change_state(2)  # follow wall
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        change_state(0)  # find wall
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
        print("checking")
        change_state(2)     #wall avoidance
        rospy.loginfo(regions)

def change_state(state):
   global state1, distanceX, distanceY
   if state is not state1:
       print 'State: [%s]' % (state)  # prints state and odometry information
       print 'DistanceX: [%s]' % (distanceX)
       print 'DistanceY: [%s]' % (distanceY)
       state1 = state  # changes state

def follow_the_wall():
   global regions_
   msg = Twist()
   msg.linear.x = 0.3       #slower speed following wall for less oscillation
   return msg

def find_wall():
   msg = Twist()
   msg.linear.x = 0.5       #faster speed to find wall
   return msg
 
def turnto(x):      
    msg = Twist()
    msg.linear.x = 0.1
    msg.angular.z = x*PI/6          #turns left or right depending on state 
    return msg
 
def chooseDirection(direction):
    global turned
    turn = 0
    if direction == 1:
        turn = 0.5          #lower right quadrant
    elif direction == 2:
        turn = 2.4          #upper right quadrant
    elif direction == 3:
        turn = -1       #lower left quadrant
    elif direction == 4:
        turn = -2.3         #upper left quadrant
    turned = True 
    return turn

# control loop
while not rospy.is_shutdown():
    global direction
    decider()           #call state decider
    msg = Twist()
    if turned == False:             #if initial heading has not been selected yet 
        direction = random.randint(1,4)
        print 'Direction: [%s]' % (direction)
        direction =4 
        turn = chooseDirection(direction)           #to shorten the turning time, it turns both ways depending on selected direction
        if turn > 0:                
            while yaw < turn:       #turn to the left
                msg.angular.z = 0.3
                cmd_vel_pub.publish(msg)  
        elif turn < 0:      
            while yaw > turn:       #turn to the right
                msg.angular.z = -0.3
                cmd_vel_pub.publish(msg) 
    if state1 == 0:
        msg = find_wall()
    elif state1 == 1:
        msg = turnto(1)      #turns right
    elif state1 == 2:
        msg = follow_the_wall()
        pass
    elif state1 == 3:
        msg = turnto(-1)        #turns left
        pass
    elif state1 == 4:
        msg.linear.x = 0.1
        msg.angular.z = 0
        cmd_vel_pub.publish(msg)        #publish final hiding state
        print(regions_)
        break

    cmd_vel_pub.publish(msg)            #publish all other movements

    # runs at 10hz
    rate.sleep()