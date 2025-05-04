# AMR_final_project
# Autonomous Mobile Robot - Loader Robot

This repository contains the final project for the **Autonomous Mobile Robots** course. The project implements a loader robot that moves along a predefined line. The system is developed using the **HiWonder TurboPi** platform.

## Project Overview

The primary goal of this project is to build and program an autonomous robot capable of:
- Following a path or line on the ground.
- Performing loading and unloading tasks.

## Features

- **Line Following:** The robot is designed to autonomously follow a predefined line.
- **Loading and Unloading:** The robot performs loading and unloading tasks as part of its functionality.
- **HiWonder TurboPi Platform:** The implementation leverages the features and capabilities of the HiWonder TurboPi.

## Logic Workflow

The robot operates in the following sequence:

1. **System Initialization**:
   - When the program starts, the robot initializes all necessary modules, including sensors, wheel control, and additional motors.
   - The `MecanumChassis` class from `HiwonderSDK.mecanum` is used for wheel control. This class is already included in the robot's firmware.

2. **Line Detection**:
   - The robot uses a **Line Follower Sensor** to detect the line on the ground.
   - The **Line Follower Sensor** analyzes the position of the line relative to the robot and sends data to the control system.

3. **Line Following**:
   - Based on data from the **Line Follower Sensor**, the system adjusts the robot's speed, angle, and angular velocity.
   - The `set_velocity` method is used to control movement:
     ```python
     chassis.set_velocity(speed=50, angle=90, angular_velocity=30)
     ```
   - The robot maintains stable movement, continuously adjusting its parameters to precisely follow the line.

4. **Loading Operation**:
   - When the robot reaches a designated point, it activates the **Ultrasonic Sensor** to determine the exact distance to the object.
   - Once positioned correctly, the robot activates an **additional motor** responsible for the loading task.
   - After completing the loading operation, the robot deactivates both the ultrasonic sensor and the additional motor to optimize resource usage.

5. **Unloading Operation and Completion**:
   - The robot completes its task when the **Line Follower Sensor** detects the line with all its sensors active, indicating that the robot has reached the endpoint.
   - At this point, the **additional motor** performs the unloading operation, delivering the previously loaded items.
   - After completing the unloading operation, the robot deactivates all additional modules and terminates its operation.
