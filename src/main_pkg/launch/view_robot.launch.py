from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory
import os
import xacro


def generate_launch_description():
    pkg_share = get_package_share_directory("main_pkg")
    xacro_file = os.path.join(pkg_share, "description", "robot.urdf.xacro")

    robot_description = xacro.process_file(xacro_file).toxml()

    use_joint_state_publisher_gui = LaunchConfiguration("use_joint_state_publisher_gui")
    use_rviz = LaunchConfiguration("use_rviz")

    declare_jsp_gui = DeclareLaunchArgument(
        "use_joint_state_publisher_gui",
        default_value="true",
        description="Start joint_state_publisher_gui",
    )

    declare_use_rviz = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Start RViz2",
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
        condition=IfCondition(use_joint_state_publisher_gui),
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription(
        [
            declare_jsp_gui,
            declare_use_rviz,
            robot_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz_node,
        ]
    )
