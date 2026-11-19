# ROS 2 Turtlesim — Catch Them All

A ROS 2 Jazzy project where a turtle autonomously moves toward
other turtles and catches them in the Turtlesim simulator.

Built as the final project of Edouard Renard's
ROS 2 for Beginners course.

## Features

- Spawns turtles at random positions.
- Selects the nearest turtle or the first available target.
- Uses proportional control for linear and angular velocity.
- Removes caught turtles through ROS 2 services.
- Configures behavior through YAML parameters.
- Starts the system using an XML launch file.

## Architecture

| Node | Responsibility |
|---|---|
| turtlesim_node | Runs the simulation |
| turtle_controller | Selects targets and controls turtle1 |
| TurtleSpwner | Spawns turtles and handles catch requests |

The spawner publishes targets on `/alive_turtle`.
The controller reads `/turtle1/pose`, publishes velocity commands
to `/turtle1/cmd_vel`, and calls `/catch_turtle`.
The spawner uses Turtlesim's `/spawn` and `/kill` services.

## Requirements

- Ubuntu 24.04 with ROS 2 Jazzy
- Turtlesim
- colcon and rosdep

## Build and Run

In a new terminal:

```bash
source /opt/ros/jazzy/setup.bash
git clone https://github.com/yuvalzisk/ros2-turtlesim-catch-them-all.git
cd ros2-turtlesim-catch-them-all
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
ros2 launch my_robot_bringup turtlesim_catch_them_all.launch.xml
```

## Configuration

Edit `src/my_robot_bringup/config/catch_them_all_config.yaml`:

| Parameter | Description |
|---|---|
| catch_closest_turtle_first | Select the nearest target when true |
| turtle_name_prefix | Prefix for newly spawned turtles |
| spwan_freq | Spawn frequency in turtles per second |

Parameter names match the current implementation.

## Repository Contents

The workspace also includes earlier ROS 2 course exercises.
The final project uses `turtlesim_catch_them_all`,
`my_robot_interfaces`, and `my_robot_bringup`.

## Demo


https://github.com/user-attachments/assets/840a4330-a92f-4f59-8f97-b0205cc9b568


