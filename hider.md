# Table of contents

* [General Overview](overview.md)
  * [Hider](hider.md)
  * [Seeker](seeker.md)
  * [Launch File](launch.md)
  * [Custom World](world.md)
* [Difficulties and Obstacles Overcome](obstacles.md)
  * [Bugs](bugs.md)
  * [Reflection](reflection.md)


## The Hider Bot

Hider starts a meter away from seeker and begins it's quest to find a good hiding place immediately after running the program. First, to make sure the hider did not find the same hiding place every time, the hider turns in one of four directions, which is selected randomly. Once a direction is picked, another method called chooseDirection gives a resepective yaw value to turn to, which was determined based on the general design of the map, so the hider would get to explore all regions of the map quickly. 

``` xml 
        direction = random.randint(1,4)
        print 'Direction: [%s]' % (direction)
        turn = chooseDirection(direction)           #to shorten the turning time, it turns both ways depending on selected direction
        if turn > 0:                
            while yaw < turn:       #turn to the left
                msg.angular.z = 0.3
                cmd_vel_pub.publish(msg)  
        elif turn < 0:      
            while yaw > turn:       #turn to the right
                msg.angular.z = -0.3
                cmd_vel_pub.publish(msg) 
```

It spins until it reaches the designated yaw, then goes forward, now searching for a hiding place. The algorithm is now a wall following one, but there are a few more conditions for the hider. One of the most advanced parts of hider is it's wall following algorithm, which can turn both right and left, and follow walls on both right and left sides, which was one of the most difficult and finicky parts of our project. In order to select a hiding palce, it first uses LIDAR readings to measure proximity in five different regions. 

``` xml
    regions_ = {                #scan regions
        'right':  min(min(msg.ranges[60:92]), 10),
        'fright': min(min(msg.ranges[10:59]), 10),
        'front':  min(min(msg.ranges[0:10]), 10),
        'fleft':  min(min(msg.ranges[280:339]), 10),
        'left':   min(min(msg.ranges[270:300]), 10),
    }
```
Using the front, right, and left scan regions, it determines whether it is in a tight place (on this map, a corner). Once it gets within very close range (under one meter in the front and less than half a meter in right or left), the algorithm moves to the second check, odometry. With it's initial position next to the seeker measured against it's current distance from that point, the hider can tell how far away it is from it's start -- more importantly -- the seeker. Once the hider is over 4 meters away in both x and y directions indicating a likelihood that the hider is out of sight range of the seeker, it is able to hide. There is one exception, however. In the upper right quadrant, direction 4, the design of the map is slightly different, so the hider is able to hide if only the difference in distance on the y plane is greater than 5 instead. This simply made sense for our map to acheive best results, but the hider would also hide fairly effectively without the specific check. 

``` xml
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
```

In the hide state, all turns are stopped, linear speed is decreased to 0.1 to drive it all the way into the corner, and the program ends. 


