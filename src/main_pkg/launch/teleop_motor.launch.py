from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_name = 'main_pkg'
    pkg_share = get_package_share_directory(package_name)

    robot_params = os.path.join(pkg_share, 'config', 'robot_parameters.yaml')
    teleop_params = os.path.join(pkg_share, 'config', 'teleop_joy.yaml')
    odom_params = os.path.join(pkg_share, 'config', 'odometry_parameters.yaml')

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory(package_name),
                'launch',
                'rsp.launch.py'
            )
        ]),
        launch_arguments={
            'use_sim_time': 'true',
            'use_ros2_control': 'false',
        }.items()
    )

    return LaunchDescription([
        rsp,

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

        Node(
            package='main_pkg',
            executable='odometry_node',
            name='odometry_node',
            output='screen',
            parameters=[odom_params]
        ),
    ])
