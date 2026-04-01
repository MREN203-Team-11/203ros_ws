import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory("main_pkg")
    slam_params = os.path.join(pkg_share, "config", "mapper_params_online_async.yaml")
    rviz_config = os.path.join(pkg_share, "config", "real_bot.rviz")

    use_sim_time = LaunchConfiguration("use_sim_time")
    slam_params_file = LaunchConfiguration("slam_params_file")
    rviz_config_file = LaunchConfiguration("rviz_config")

    slam_node = Node(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="slam_toolbox",
        output="screen",
        parameters=[
            slam_params_file,
            {"use_sim_time": use_sim_time},
        ],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
        parameters=[{"use_sim_time": use_sim_time}],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation clock (/clock)",
            ),
            DeclareLaunchArgument(
                "slam_params_file",
                default_value=slam_params,
                description="Path to the slam_toolbox parameter file",
            ),
            DeclareLaunchArgument(
                "rviz_config",
                default_value=rviz_config,
                description="Path to the RViz configuration file",
            ),
            slam_node,
            rviz_node,
        ]
    )
