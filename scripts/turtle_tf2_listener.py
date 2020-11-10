#!/usr/bin/env python  
import rospy

import math
import tf2_ros
import geometry_msgs.msg
import turtlesim.srv

# Create a node and allocate a tf buffer and a tf listener.

if __name__ == '__main__':
    rospy.init_node('tf2_turtle_listener')

    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

# Advanced trick to launch a second copy of the turtlesim named after
# the param turtle (default to turtle2)
#need to spawn second turtle this is how to do so
    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(4, 2, 0, 'turtle2')
    spawner(4, 3, 0, 'turtle3')
    spawner(4, 4, 0, 'turtle4')
    spawner(4, 5, 0, 'turtle5')
    turtlename = rospy.get_param('turtle', 'turtle2')
# We are going to steer turtle2. We start by creating a turtle2/cmd_vel publisher
    turtle_vel = rospy.Publisher('%s/cmd_vel' % 'turtle2', geometry_msgs.msg.Twist, queue_size=1)
    turtle2_vel = rospy.Publisher('%s/cmd_vel' % 'turtle3', geometry_msgs.msg.Twist, queue_size=1)
    turtle3_vel = rospy.Publisher('%s/cmd_vel' % 'turtle4', geometry_msgs.msg.Twist, queue_size=1)
    turtle4_vel = rospy.Publisher('%s/cmd_vel' % 'turtle5', geometry_msgs.msg.Twist, queue_size=1)
# And we loop, 10x per second
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
# This is the most important line. Requests the transform between turtle1 and turtle_name
            trans = tfBuffer.lookup_transform('turtle2', 'turtle1', rospy.Time())
            trans_2 = tfBuffer.lookup_transform('turtle3', 'turtle2', rospy.Time())
            trans_3 = tfBuffer.lookup_transform('turtle4', 'turtle3', rospy.Time())
            trans_4 = tfBuffer.lookup_transform('turtle5', 'turtle4', rospy.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException,tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

        msg = geometry_msgs.msg.Twist()
        msg2 = geometry_msgs.msg.Twist()
        msg3 = geometry_msgs.msg.Twist()
        msg4 = geometry_msgs.msg.Twist()
# Some trig to compute the desired motion of turtle2
        msg.angular.z = 4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
        msg.linear.x = 0.5 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2)
        msg2.angular.z = 4 * math.atan2(trans_2.transform.translation.y, trans_2.transform.translation.x)
        msg2.linear.x = 0.5 * math.sqrt(trans_2.transform.translation.x ** 2 + trans_2.transform.translation.y ** 2)
        msg3.angular.z = 4 * math.atan2(trans_3.transform.translation.y, trans_3.transform.translation.x)
        msg3.linear.x = 0.5 * math.sqrt(trans_3.transform.translation.x ** 2 + trans_3.transform.translation.y ** 2)
        msg4.angular.z = 4 * math.atan2(trans_4.transform.translation.y, trans_4.transform.translation.x)
        msg4.linear.x = 0.5 * math.sqrt(trans_4.transform.translation.x ** 2 + trans_4.transform.translation.y ** 2)
# And publish it to drive turtle2
        turtle_vel.publish(msg)
        turtle2_vel.publish(msg2)
        turtle3_vel.publish(msg3)
        turtle4_vel.publish(msg4)
        rate.sleep()