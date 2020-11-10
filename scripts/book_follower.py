#!/usr/bin/env python
import rospy, cv2, cv_bridge, numpy 
from sensor_msgs.msg import Image 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def scan_callback(msg):
    #detect if obstacle in way then turn in way of the line 
    global noObstacle
    noObstacle = min(msg.ranges[0:44] + msg.ranges[310:359]) > 0.3

def image_callback(msg):
    global obstacle
    twist = Twist()
    image = bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = numpy.array([ 10,  10,  10])
    upper_yellow = numpy.array([255, 255, 250])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    h, w, d = image.shape
    search_top = 3*h/4
    search_bot = 3*h/4 + 20
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    M = cv2.moments(mask)
    if M['m00'] > 0:
        if noObstacle:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(image, (cx, cy), 20, (0,0,255), -1) 
            err=cx-w/2
            twist.linear.x = 0.2 
            twist.angular.z = -float(err) / 1000
            cmd_vel_pub.publish(twist)
        else:
            twist.angular.z = 0.3
    smallerImage = cv2.resize(image, (500, 350)) 
    cv2.imshow("RobotView", smallerImage)
    cv2.waitKey(3)

noObstacle = True
bridge = cv_bridge.CvBridge()
cv2.namedWindow("RobotView", 1)
image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, image_callback)
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
scan_sub = rospy.Subscriber('/scan', LaserScan, scan_callback)
rospy.init_node('follower')
rospy.spin()



# #!/usr/bin/env python
# import rospy, cv2, cv_bridge, numpy 
# from sensor_msgs.msg import Image 
# from geometry_msgs.msg import Twist
# class Follower:
#     def __init__(self):
#         self.bridge = cv_bridge.CvBridge()
#         cv2.namedWindow("RobotView", 1)
#         self.image_sub = rospy.Subscriber('camera/rgb/image_raw',
#                                       Image, self.image_callback)
#         self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop',
#                                        Twist, queue_size=1)
#         self.twist = Twist()
#     def image_callback(self, msg):
#         image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
#         hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#         lower_yellow = numpy.array([ 10,  10,  10])
#         upper_yellow = numpy.array([255, 255, 250])
#         mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
#         h, w, d = image.shape
#         search_top = 3*h/4
#         search_bot = 3*h/4 + 20
#         mask[0:search_top, 0:w] = 0
#         mask[search_bot:h, 0:w] = 0
#         M = cv2.moments(mask)
#         if M['m00'] > 0:
#             cx = int(M['m10']/M['m00'])
#             cy = int(M['m01']/M['m00'])
#             cv2.circle(image, (cx, cy), 20, (0,0,255), -1) 
#             err=cx-w/2
#             self.twist.linear.x = 0.2 
#             self.twist.angular.z = -float(err) / 100 
#             self.cmd_vel_pub.publish(self.twist)
#         smallerImage = cv2.resize(image, (500, 350)) 
#         cv2.imshow("RobotView", smallerImage)
#         cv2.waitKey(3)
# if __name__ == "__main__":
#     rospy.init_node('follower')
#     follower = Follower()
#     rospy.spin()
