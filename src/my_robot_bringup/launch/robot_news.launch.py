from launch import LaunchDescription
from launch_ros.actions import Node



def generate_launch_description():
    return LaunchDescription([
        Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_giskard",
            output="screen",
        ),
        Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_bb8",
            output="screen",
            ),
        Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_daneel",
            output="screen",
            ),
        Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_jander",
            output="screen",
                ),
        Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_c3po",
            output="screen",
                ),
        Node(
            package="my_py_pkg",
            executable="smartphone",
            name="smartphone",
            output="screen",
        
                ),
        
    ])