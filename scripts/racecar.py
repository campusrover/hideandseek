
#!/usr/bin/env python
# Name: Mahima Devanahalli
 
import rospy
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import Twist
import cv2
import cv_bridge
import numpy
 
# This is the LineFollower class which sets a linefollower object to have a subscriber, publisher and twist message as well as a CvBridge


class LineFollower:

 
   def __init__(line_follower):
       line_follower.sub = rospy.Subscriber(
           'camera/rgb/image_raw', Image, line_follower.image_callback)
       line_follower.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
       line_follower.scan_sub = rospy.Subscriber(
           '/scan', LaserScan, line_follower.scan_callback)
       line_follower.twist = Twist()
       line_follower.cv = cv_bridge.CvBridge()
       line_follower.obstacle = 1
       cv2.namedWindow("Image_Window", cv2.WINDOW_NORMAL)
       cv2.namedWindow("band", cv2.WINDOW_NORMAL)
 
   def scan_callback(line_follower, msg):
       line_follower.obstacle = msg.ranges[0]
 
   # This is the callback function for the subscriber
   def image_callback(line_follower, msg):
       # get image from camera(from msg) and encode it to bgr8, then convert this image to hsv
       image = line_follower.cv.imgmsg_to_cv2(msg, desired_encoding='bgr8')
       hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 
       # found these values from trial and error through a colorizer website to find the range of hsv yellow values
       # so that the yellow line can be identified and
       lower_yellow = numpy.array([0, 0, 0])
       upper_yellow = numpy.array([0, 0, 255])
       mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
 
       # get the height and width of the image to be able to find the center of the line/ the centroid
       height = image.shape[0]
       width = image.shape[1]
       top = 3*height/4
       bottom = top + 20
       mask[0:top, 0:width] = 0
       mask[bottom:height, 0:width] = 0
 
       moment = cv2.moments(mask)
       if moment['m00'] > 0:
           # centroid forumula
           cx = int(moment['m10']/moment['m00']) + 100
           cy = int(moment['m01']/moment['m00'])
           error = cx - width/2
 
           # moving the robot by publishing twist messages
           if (line_follower.obstacle < 0.4):
               line_follower.twist.angular.z = 0.2
           else:
               line_follower.twist.angular.z = -float(error) / 1000
           line_follower.twist.linear.x = 0.3
           line_follower.pub.publish(line_follower.twist)
 
       cv2.resizeWindow('Image_Window', 500, 500)
       cv2.resizeWindow('band', 500, 500)
       cv2.imshow('Image_Window', image)
       cv2.imshow("band", mask)
       cv2.waitKey(3)
 
 
print("I will now follow this yellow line")
rospy.init_node('follow_line')
line_follower = LineFollower()
rospy.spin()
