#!/usr/bin/env python
import rospy, sys, math, tf
import cv2, cv_bridge, numpy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image, LaserScan
from tf.transformations import euler_from_quaternion

class Seeker: 

    def __init__(seeker):
        seeker.img_sub = rospy.Subscriber('/seeker/camera/rgb/image_raw', Image, seeker.img_callback)
        seeker.pub = rospy.Publisher('/seeker/cmd_vel', Twist, queue_size=1)
        seeker.scan_sub = rospy.Subscriber('/seeker/scan', LaserScan, seeker.scan_callback)
        seeker.twist = Twist()
        seeker.cv = cv_bridge.CvBridge()
        seeker.regions_ = {           
            'right':0,
            'left':0,
            'fright':0,
            'front':0,
            'fleft':0
            }
        seeker.found = False
        cv2.namedWindow("Image_Window", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Mask_Window", cv2.WINDOW_NORMAL)
    
    """     def decider():
        global regions_
        regions = seeker.regions_
        d = 0.5
        d2 = 1.5
        if regions['front'] < d: # turn right
              
        elif regions['fleft'] < d or regions['fleft'] == d or regions['left'] < d: # follow wall

        elif regions['front'] > d and regions['fleft'] > d and regions['fright'] > d: # find wall

        elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d: # backup

        elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d : """
   
    # scan callback
    def scan_callback(seeker, msg):
        global ranges, regions_
        ranges = msg.ranges
        regions_ = {
            'right':  min(min(msg.ranges[60:92]), 10),
            'fright': min(min(msg.ranges[10:59]), 10),
            'front':  min(min(msg.ranges[0:10]), 10),
            'fleft':  min(min(msg.ranges[280:339]), 10),
            'left':   min(min(msg.ranges[270:300]), 10),
            }

    # img callback
    def img_callback(seeker, msg):
        # get image from camera(from msg) and encode it to bgr8, then convert this image to hsv
        image = seeker.cv.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_black = numpy.array([0, 0, 0])
        upper_black = numpy.array([180, 255, 30])
        mask = cv2.inRange(hsv, lower_black, upper_black)

        moment = cv2.moments(mask)
        if moment['m00'] > 0:
            seeker.found = True 
            print('I FOUND YOU')
            seeker.twist.linear.x = 0.0
            seeker.twist.angular.z = 0.0
            seeker.pub.publish(seeker.twist)
        else:
            print('hider not found yet')
            #decider()

        #cv2.resizeWindow('Image_Window', 500, 500)
        #cv2.resizeWindow('Mask_Window', 500, 500)
        cv2.imshow("image", image)
        cv2.imshow("mask", mask)
        cv2.waitKey(3)

print('Time to seek!')
rospy.init_node('seeker')
seeker = Seeker()
rospy.spin()