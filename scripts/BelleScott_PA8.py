import rospy, cv_bridge, cv2, numpy
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import Twist

def scan_cb(msg):
    #detect if obstacle in the way
    global noObstacle
    noObstacle = min(msg.ranges[0:44]+msg.ranges[310:359]) > 0.3

def cam_cb(msg):
    image = bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')       #from book, we want the second param to be our desired encoding of the image to cv2
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)        #hue saturation value, rbg doesnt work with wrong lighting
    light_yellow = numpy.array([0,0,0], dtype=np.uint8)          #([255,255,250])   #these values are how book defined upper and lower shades of yellow, values are from the book. they worked for me immediately so I'll use them here
    darker_yellow = numpy.array([0,0,255], dtype=np.uint8)       #([10,10,10])
    mask = cv2.inRange(hsv, darker_yellow, light_yellow)
    h,w,d = image.shape    
    top = 3*h/4
    bottom = 3*h/4 + 20
    mask[0:top, 0:w] = 0        #using the book values for masking, it worked for me
    mask[bottom:h, 0:w] = 0
    find_line(mask, w, image)
    smallWindow = cv2.resize(image, (500,350))      #making the open cv image window smaller so it doesnt lag
    cv2.imshow("RobotView",smallWindow)
    cv2.waitKey(3)

def find_line(mask, w, image):
    t = Twist()
    M = cv2.moments(mask)       #this calculates the center of the line via artithmetic, called the centroid 
    if M['m00'] > 0:
        circlex = int(M['m10']/M['m00'])    #defining circle to draw in middle of line, same values as book
        circley = int(M['m01']/M['m00'])
        cv2.circle(image, (circlex,circley),20,(0,0,255), -1)       #draw the red circle, rbg value 0 0. 255 gives red
        follow_line(circlex,w)
    else: 
        t.linear.x = 0.4
        velocity_pub.publish(t)
        print("cant see the line1")
def follow_line(circlex, w):
    #pid controller. i had to chage the one from the book, it was not working for me at all
    global noObstacle
    if noObstacle:
        t = Twist()
        error = circlex-w/2
        t.linear.x = 0.4
        t.angular.z = -float(error)/500
        velocity_pub.publish(t)
        print("i can see the line")
    else:       #if obstacle in path, turn to left. could get my obstacles in gazebo to work but just to test try turning it to a wall. it follows lidar corretly then
        twist.angular.z = 0.3

noObstacle = True
bridge = cv_bridge.CvBridge()
cv2.namedWindow("RobotView", 1)
cam_sub = rospy.Subscriber('camera/rgb/image_raw', Image, cam_cb)
velocity_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
scan_sub = rospy.Subscriber('/scan', LaserScan, scan_cb)
rospy.init_node('linefollower')
rospy.spin()