# Autonomous Hide and Seek

Picture will go here

A robotics project by Mahima Devanahalli and Belle Scott, autonomous hide and seek features two turtlebot robots in the gazebo similator in a custom map setting. In their environment, the hider will first be given time to hide while the seeker waits, then the seeker can pursue it around the map. Written mostly in python, this program includes techniques of odometry, LIDAR, and computer vision using OpenCV. 

## Instructions to run

Clone repo: https://github.com/campusrover/hideandseek.git

- Launch world with robots of the waffle model (required because they contain cameras) this command: `roslaunch hideandseek project.launch model:=waffle`
  - This is a custom world built by our team, so the world is static
- Open another terminal and `cd` to the scripts folder, and either run hider.py with this command: `python hider.py` or make it executable with `chmod +x hider.py` and then can be run outside of the scripts folder with `rosrun hideandseek hider.py`
- Open another terminal and follow the same steps as with hider to launch seeker with this command: `python seeker.py` or respectively `rosrun hideandseek seeker.py`

Hider will immediately begin moving after running the program, while seeker will be still and print out "waiting"

Seeker's openCV window will be blank initially, as with normal hide and seek your eyes are closed until given permission to seek. Once seeker reaches the time limit (45 sec), two openCV windows will open, one for the camera and one only in black and white for detection of the other black robot. 
