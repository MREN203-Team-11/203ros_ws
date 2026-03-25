from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    pkg_share = get_package_share_directory('main_pkg')

    robot_params = os.path.join(pkg_share, 'config', 'robot_parameters.yaml')
    teleop_params = os.path.join(pkg_share, 'config', 'teleop_joy.yaml')

    return LaunchDescription([
        Node(
            package='joy',
            executable='joy_node',
            name='joy_node',
            output='screen',
            parameters=[{
                'device_id': 0,
                'deadzone': 0.1,
                'autorepeat_rate': 20.0,
            }]
        ),

        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            name='teleop_twist_joy_node',
            output='screen',
            parameters=[teleop_params]
        ),

        Node(
            package='main_pkg',
            executable='motor_serial_node',
            name='motor_serial_node',
            output='screen',
            parameters=[robot_params]
        ),
    ])