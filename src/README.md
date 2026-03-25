# SSH

`ssh group11@192.168.50.203`

### IP Address: 192.168.50.203
##### Need to be on MREN203 wifi
##### When closing ssh terminal, run `sudo shutdown now`

## Driving the robot with the gamepad

run `ros2 lauch main_pkg teleop_motor.launch.py`

Make sure the gamepad is plugged into the pi, the pi and arduino are connected

## Running Motors through ROS

1) Run in Pi terminal `ros2 run main_pkg motor_serial_node --ros-args --params-file src/main_pkg/config/robot_parameters.yaml`

2) On computer run `ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 0.0}}" -r 5`

Note:
Viewing topic messages
`ros2 topic echo /topic_name`

## Viewing Lidar data

1) ON THE PI Run `ros2 launch main_pkg rplidar.launch.py`

2) ON YOUR PC Open rviz

run `rviz2`

3) Click add -> laser scan, set the topic to /scan

4) Type "laser_frame" in the fixed frame box

Note:

Stop lidar `ros2 service call /stop_motor std_srvs/srv/Empty {}`

Start lidar `ros2 service call /start_motor std_srvs/srv/Empty {}`

If the node is being weird run `killall rplidar_composition` to kill the lidar node

## Running Gazebo + Driving Robot

1) Open Gazebo
Run `ros2 launch main_pkg launch_sim.launch.py`

optional: add `world:=./src/main_pkg/worlds/obstacles.world` to end of command if you want to run in a obstacles.world, replace this with any other world you want to run the sim in.

2) Plug the gamepad into your pc

## Visualizing robot

Run `ros2 launch main_pkg view_robot.launch.py`


## Where Do I write Code? How do I run it?

This may look overly complex with a bunch of random files, but to write/run code, follow these steps:

### 1) Write all code in files in 203ROS_WS/main_pkg/main_pkg
ex. Make a file(node) called mynode.py in this directory

### 2) Make sure all dependencies for you code are in package.xml in the directory 203ROS_WS/main_pkg/package.xml
ex. adding rclpy, std_msgs dependencies to package.xml\

```
<exec_depend>rclpy</exec_depend>\
<exec_depend>std_msgs</exec_depend>
```

### 3) Add entry point for you written code to setup.py in the directory 203ROS_WS/main_pkg/setup.py
ex. adding entry point called liam_node for the mynode.py

```
file\
entry_points={\
        'console_scripts': [\
                'liam_node = main_pkg.mynode:main',\
        ],\
},
```

This set sthe main function, found in the mynode file in the main_pkg directory as the code to run when the now named 'liam_node' is called

### 4) Check for missing dependencies
Go to 203ROS_WS,

In the terminal:\
`rosdep install -i --from-path src --rosdistro humble -y`

This ensures all dependencies your code required are present

### 5) Build the package
While in 203ROS_WS,

In terminal:\
`colcon build --packages-select main_pkg`

### 6) Source the setup files
Open new terminal and write:\
`source install/setup.bash`

### 7) run nodes
In the same new terminal run:\
`ros2 run main_pkg <nodeName>`

ex. running liam_node\
`ros2 run main_pkg liam_node`



### ROS2 Humble Docs: https://docs.ros.org/en/humble/index.html https://ros2-tutorial.readthedocs.io 

### Pi Details
host name: group11-pi 

Username: group11

Password: tronisgoated

### NOTES:
slam toolbox library for slam
