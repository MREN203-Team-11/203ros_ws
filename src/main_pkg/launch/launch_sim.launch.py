import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    package_name = 'main_pkg'
    pkg_share = get_package_share_directory(package_name)
    teleop_params = os.path.join(pkg_share, 'config', 'teleop_joy.yaml')
    slam_params = os.path.join(pkg_share, "config", "sim_slam_params.yaml")
    rviz_config = os.path.join(pkg_share, "config", "mars_sim.rviz")


    slam_params_file = LaunchConfiguration("slam_params_file")
    rviz_config_file = LaunchConfiguration("rviz_config")
    use_sim_time = LaunchConfiguration("use_sim_time")

    # Publish robot_description using the non-ros2_control xacro branch
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(package_name),
                'launch',
                'rsp.launch.py'
            )
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'use_ros2_control': 'false',
        }.items()
    )

    world = os.path.join(
        get_package_share_directory('main_pkg'),
        'worlds',
        'mars.world'
    )

    gazebo_params_file = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'gazebo_params.yaml'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ),
        launch_arguments={
            'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file,
            'world': world
            }.items()
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_bot',
                   '-x', '18.0',
                   '-y', '0.0',
                   '-z', '5.0',
                ],
        output='screen'
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        output='screen',
        parameters=[{
            'device_id': 0,
            'deadzone': 0.1,
            'autorepeat_rate': 20.0,
        }]
    )

    teleop_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        output='screen',
        parameters=[teleop_params]
    )

    slam_node = Node(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="slam_toolbox",
        output="screen",
        parameters=[slam_params_file],  
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
        parameters=[{"use_sim_time": use_sim_time}],
    )



    return LaunchDescription([

        DeclareLaunchArgument(
            "rviz_config",
            default_value=rviz_config,
            description="Path to the RViz configuration file",
        ),

        DeclareLaunchArgument(
            "slam_params_file",
            default_value=slam_params,
            description="Path to the slam_toolbox parameter file",
        ),

        DeclareLaunchArgument(
            "use_sim_time",
            default_value="true",
            description="Use simulation clock (/clock)",
        ),

        rsp,
        gazebo,
        spawn_entity,
        joy_node,
        teleop_node,
        slam_node,
        rviz_node
    ])
