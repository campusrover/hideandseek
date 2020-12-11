## Launch File

Our launch file first designates args for the x,y, and z positions for each robot, as well as their respective yaws. 

``` xml
    <arg name="model" default="burger" doc="model type [burger, waffle, waffle_pi]"/>
    <arg name="seeker_pos_x" default="0"/>
    <arg name="seeker_pos_y" default=" -0.5"/>
    <arg name="seeker_pos_z" default=" 0.0"/>
    <arg name="seeker_yaw" default="0"/>
    <arg name="hider_pos_x" default="0"/>
    <arg name="hider_pos_y" default="0.5"/>
    <arg name="hider_pos_z" default=" 0.0"/>
    <arg name="hider_yaw" default="0" />
```

Afterwords, our custom map, called hideandseek.world, is launched with an initial empty world, with an argument of our world's file, which is shown below.

``` xml 
   <include file="$(find gazebo_ros)/launch/empty_world.launch">
        <arg name="world_name" value="$(find prrexamples)/hideandseek/world/hideandseek.world"/>
        <arg name="paused" value="false"/>
        <arg name="use_sim_time" value="true"/>
        <arg name="gui" value="true"/>
        <arg name="headless" value="false"/>
        <arg name="debug" value="false"/>
    </include>
```

After setting their initial positions, we used grouping for each robot. Here, I put the logic so the launch file knows which python files correspond to which robot. It is also very important to change the all the parameters to match your robots name (ex: $(arg seeker_pos_y)). I had a lot of trouble initially getting two robots to launch, it was one of the project's first blocks. My error was not realizing that absolutely every parameter must be properly named and associated. It was also very helpful to already have example launch files to look at for the many intricate details that I did not understand at first. In our launch file and world, the robots are at the center of the maze like structure, hider on the right, seeker on the left, and starting a meter apart.

``` xml
    <group ns="seeker">
        <param name="robot_description" command="$(find xacro)/xacro.py $(find turtlebot3_description)/urdf/turtlebot3_$(arg model).urdf.xacro" />
        <node pkg="robot_state_publisher" type="robot_state_publisher" name="robot_state_publisher" output="screen">
            <param name="publish_frequency" type="double" value="50.0" />
            <param name="tf_prefix" value="seeker" />
        </node>
        <node name="spawn_urdf" pkg="gazebo_ros" type="spawn_model" args="-urdf -model seeker -x $(arg seeker_pos_x) -y $(arg seeker_pos_y) -z $(arg seeker_pos_z)          -Y $(arg seeker_yaw) -param robot_description" />
    </group>
    <group ns="hider">
        <param name="robot_description" command="$(find xacro)/xacro.py $(find turtlebot3_description)/urdf/turtlebot3_$(arg model).urdf.xacro" />
        <node pkg="robot_state_publisher" type="robot_state_publisher" name="robot_state_publisher" output="screen">
            <param name="publish_frequency" type="double" value="50.0" />
            <param name="tf_prefix" value="hider" />
        </node>
        <node name="spawn_urdf" pkg="gazebo_ros" type="spawn_model" args="-urdf -model hider -x $(arg hider_pos_x) -y $(arg hider_pos_y) -z $(arg hider_pos_z) -Y               $(arg hider_yaw) -param robot_description" />
    </group>
```
