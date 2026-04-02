# PLAN OF ACTION
- gazebo mars sim world
- edit launch_sim.py to launch with a mars world, and run slam mapping on environment
- create rviz launch file to view robot on mars sim, and map being created

- remap, alter map in slam_real_bot.launch.py
- print out images in gmail, finish poster board

- potentially figure out initial pose issue in rviz

- get physical robot ready
- charge battery




# Project Completion:

## Presentation

### Real robot

- make sure joystick, serial, lidar all connected to pi

on pi run `ros2 launch main_pkg teleop_motor.launch.py`

on pc run `ros2 launch main_pkg slam_real_bot.launch.py`

### Sim

- make sure joystick usb is plugged into pc


# SSH

`ssh group11@192.168.50.203`

### IP Address: 192.168.50.203
##### Need to be on MREN203 wifi
##### When closing ssh terminal, run `sudo shutdown now`

## Running SLAM toolbox

run `ros2 launch slam_toolbox online_async_launch.py params_file:=./src/main_pkg/config/mapper_params_online_async.yaml`

in rviz, insert map, select /map topic

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





### ROS2 Humble Docs: https://docs.ros.org/en/humble/index.html https://ros2-tutorial.readthedocs.io 

### Pi Details
host name: group11-pi 

Username: group11

Password: tronisgoated

### NOTES:
slam toolbox library for slam
