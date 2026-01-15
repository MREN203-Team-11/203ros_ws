# Initial Design Ideas

### Pi 4 (Robot Brain)
- High-level decision making
- runs ros
- processes sensor data
- path planning, mapping, localization
- sends out velocity commands

### Arduino
- motor control
- reads encoders
- runs PID (feedback) loops
- talks to motors

### Motor Driver
- takes PWM + digital direction signals
- supplies current + voltage to motors



## ROS2 Installation guide (Windows)
1) Install WSL2 + Ubuntu 22.04

Open PowerShell as Administrator and run:

wsl --install -d Ubuntu-22.04

Reboot if prompted.

Then open Ubuntu 22.04 from the Start Menu and create your Linux username + password.

Check you’re on WSL2:

wsl -l -v

You should see Ubuntu-22.04 with VERSION 2.

2) Update Ubuntu packages

In the Ubuntu (WSL) terminal:

sudo apt update && sudo apt upgrade -y


Install some common tools:

sudo apt install -y curl gnupg2 lsb-release software-properties-common

3) Add the ROS 2 apt repository (official)

Set locale (avoids weird install issues):

sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8


Add the ROS key + repository:

sudo mkdir -p /etc/apt/keyrings
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  | sudo gpg --dearmor -o /etc/apt/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
| sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null


Update apt:

sudo apt update

4) Install ROS 2 Humble

Recommended full desktop install:

sudo apt install -y ros-humble-desktop


Also install build tools you’ll likely need for a workspace:

sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-vcstool git


Initialize rosdep:

sudo rosdep init
rosdep update

5) Source ROS automatically in new terminals

Add to your ~/.bashrc:

echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

6) Quick verification (ROS tools)

Run:

ros2 --version
ros2 pkg list | head


If that works, ROS is installed.


### ROS2 Humble Docs: https://docs.ros.org/en/humble/index.html https://ros2-tutorial.readthedocs.io 
