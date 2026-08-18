# Adaptive Dynamic Multi-Objective Routing (ADMOR)

## Overview

**Adaptive Dynamic Multi-Objective Routing (ADMOR)** is an autonomous navigation framework designed for indoor mobile service robots operating in dynamic, human-centric environments such as hospitals, warehouses, institutional buildings, and service facilities.

ADMOR combines:

* Multi-objective path planning
* Dynamic obstacle prediction
* Adaptive Pareto weighting
* Energy-aware navigation
* Safety-aware routing
* Trajectory smoothness optimization
* ROS 2 Navigation2 (Nav2) integration

The framework continuously balances **path length, energy consumption, safety clearance, and heading smoothness** instead of optimizing only the shortest path.

---

## Key Features

### 1. Multi-Objective Path Planning

ADMOR optimizes four major objectives:

1. **Path Length** – minimizes the distance traveled.
2. **Energy Consumption** – reduces unnecessary acceleration, braking, and rotation.
3. **Safety Clearance** – maintains a safe distance from static and dynamic obstacles.
4. **Heading Smoothness** – reduces sharp turns and rotational jerk.

The combined cost is represented as:

```text
Cost_total =
w_l J_length +
w_e J_energy +
w_c J_clearance +
w_s J_smoothness
```

The weights are dynamically adjusted according to the robot's operating conditions.

---

### 2. Adaptive Pareto Weighting

ADMOR changes the importance of each objective in real time.

Examples:

* High obstacle density → increase safety/clearance priority.
* Battery below 20% → increase energy-efficiency priority.
* High robot speed → increase trajectory smoothness priority.

This allows the robot to adapt its navigation strategy instead of using fixed planning weights.

---

### 3. Dynamic Obstacle Prediction

Moving obstacles such as pedestrians are tracked using an **Extended Kalman Filter (EKF)** with a Constant Velocity (CV) model.

The system predicts obstacle movement over a **3-second horizon**.

This allows ADMOR to avoid locations where a moving pedestrian is expected to be in the near future.

---

### 4. ROS 2 Navigation2 Integration

ADMOR is implemented within the **ROS 2 Humble Hawksbill** ecosystem and integrates with the **Navigation2 (Nav2)** stack.

Main components include:

```text
LiDAR / Depth Camera
        │
        ▼
Dynamic Sensor Processing
        │
        ▼
EKF Multi-Agent Tracking
        │
        ├───────────────┐
        ▼               ▼
ADMOR Global       Dynamic Obstacle
Planner             Information
        │
        ▼
ADMOR Local Controller
        │
        ▼
     /cmd_vel
        │
        ▼
 Differential Drive Robot
```

---

## System Architecture

```text
                ┌──────────────────────┐
                │     2D LiDAR         │
                └──────────┬───────────┘
                           │
                ┌──────────▼───────────┐
                │   Depth Camera       │
                └──────────┬───────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ Dynamic Sensor          │
              │ Processing Layer        │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ EKF Multi-Agent         │
              │ Tracking Node           │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ ADMOR Global Planner    │
              │ Multi-Objective A*      │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ ADMOR Local Controller  │
              │ Trajectory Optimization │
              └────────────┬────────────┘
                           │
                           ▼
                       /cmd_vel
                           │
                           ▼
                ┌──────────────────────┐
                │ Differential Drive   │
                │ Robot                │
                └──────────────────────┘
```

---

## Software Stack

| Component           | Technology                    |
| ------------------- | ----------------------------- |
| Operating Framework | ROS 2 Humble Hawksbill        |
| Navigation          | Navigation2 (Nav2)            |
| Programming         | C++17                         |
| Supporting Scripts  | Python 3.10                   |
| Simulation          | Gazebo Fortress               |
| Sensors             | 2D LiDAR + Depth Camera       |
| Robot Type          | Differential Drive            |
| Tracking            | Extended Kalman Filter        |
| Global Planning     | ADMOR Multi-Objective Planner |
| Local Control       | ADMOR Trajectory Controller   |

The paper specifies a TurtleBot 3 Waffle/custom AGV class platform with 2D LiDAR, depth camera, and STM32 motor controllers.

---

## Main ROS 2 Modules

### Dynamic Sensor Processing

Processes:

```text
/scan
/camera/depth/color/points
```

The sensor-processing layer performs filtering and clustering to identify nearby obstacles.

---

### EKF Multi-Agent Tracking

The tracking node:

* Detects moving objects.
* Assigns tracking IDs.
* Estimates position and velocity.
* Predicts future obstacle locations.
* Generates dynamic safety information.

The tracked state is:

```text
[x, y, vx, vy]
```

---

### ADMOR Global Planner

The global planner:

* Uses multi-objective graph search.
* Considers dynamic obstacle information.
* Uses adaptive weighting.
* Generates global reference paths.

Target planning frequency:

```text
5 Hz
```

---

### ADMOR Local Controller

The local controller:

* Receives the global path.
* Performs local trajectory optimization.
* Considers robot kinematic constraints.
* Generates velocity commands.

Control frequency:

```text
30 Hz
```

Output:

```text
/cmd_vel
```

---

## Mathematical Objectives

### Path Length

```text
J_length(p) = ∫ ||p'(s)|| ds
```

The objective minimizes the total distance traveled.

### Energy

```text
J_energy(p) =
∫ [c1|v| + c2|a|² + c3|ω| + c4|α|²] dt
```

This accounts for velocity, acceleration, angular velocity, and angular acceleration.

### Safety Clearance

```text
J_clearance(p) =
∫ exp(-γ(d_obs(p(s)) - r_robot)) ds
```

If the robot gets too close to an obstacle, the cost increases significantly.

### Smoothness

```text
J_smoothness(p) =
∫ (dκ/ds)² ds
```

This penalizes rapid changes in trajectory curvature and improves motion smoothness.

---

## Default Parameters

| Parameter                   | ROS 2 Key                |   Default |
| --------------------------- | ------------------------ | --------: |
| Maximum Linear Velocity     | `planner.max_vel_x`      |   1.2 m/s |
| Maximum Angular Velocity    | `planner.max_vel_theta`  | 1.8 rad/s |
| Maximum Linear Acceleration | `planner.acc_lim_x`      |  0.8 m/s² |
| Obstacle Decay Rate         | `admor.gamma_decay`      |       4.5 |
| Prediction Horizon          | `ekf.prediction_horizon` |     3.0 s |
| Controller Frequency        | `controller.frequency`   |     30 Hz |

These values are taken from the configuration parameters reported in the paper.

---

## Experimental Setup

ADMOR was evaluated in:

* Gazebo Fortress simulation
* Physical differential-drive mobile robot experiments

The simulation environment was a **40 m × 30 m healthcare facility** containing narrow corridors, doorways, lobby areas, and dynamic pedestrian traffic.

Testing included:

```text
Tier 1 → Static environment
Tier 2 → 2 pedestrians
Tier 3 → 4 pedestrians
Tier 4 → 6 pedestrians
Tier 5 → 8 pedestrians
```

A total of **250 test runs** were conducted.

---

## Benchmark Algorithms

ADMOR was compared against:

### Baseline 1

```text
A* + Dynamic Window Approach (DWA)
```

### Baseline 2

```text
Global A* + Timed Elastic Band (TEB)
```

### Proposed Method

```text
ADMOR
```

---

## Results

| Metric                    | A* + DWA | A* + TEB |       ADMOR |
| ------------------------- | -------: | -------: | ----------: |
| Navigation Success        |    76.0% |    84.0% |   **97.6%** |
| Mean Arrival Time         |   48.5 s |   42.1 s |  **34.8 s** |
| Energy Draw               |  19.8 Wh |  16.9 Wh | **12.8 Wh** |
| Heading Jerk              |     4.82 |     3.15 |    **1.95** |
| Minimum Obstacle Distance |   0.14 m |   0.22 m |  **0.38 m** |
| CPU Load                  |    18.2% |    64.5% |   **26.4%** |

According to the reported experiments, ADMOR achieved a **97.6% navigation success rate**, reduced energy consumption by **24.3%**, improved heading continuity by **38.1%**, and maintained real-time operation above 30 Hz.

---

## Advantages

* Better navigation success in dynamic environments.
* Predictive avoidance of moving pedestrians.
* Reduced energy consumption.
* Smoother robot motion.
* Larger obstacle-clearance margins.
* Adaptive behavior based on battery and environmental conditions.
* Compatible with ROS 2 Navigation2.
* Suitable for embedded mobile robot hardware.

---

## Limitations

### EKF Prediction Limitation

The current prediction model assumes approximately constant velocity.

Sudden pedestrian movements, such as sharp turns, can increase prediction uncertainty and cause conservative braking.

### Ultra-Dense Crowds

If there is insufficient free space for the robot and its safety margin, ADMOR safely stops until sufficient space becomes available.

---

## Future Work

The paper identifies the following future directions:

* Multi-robot collaborative routing
* Multi-floor navigation
* Elevator navigation
* Edge-accelerated deep reinforcement learning
* Improved pedestrian trajectory prediction

---

## Project Structure

A suggested ROS 2 project organization is:

```text
admor_ws/
└── src/
    └── admor/
        ├── admor_global_planner/
        │   ├── include/
        │   ├── src/
        │   ├── plugin.xml
        │   └── CMakeLists.txt
        │
        ├── admor_controller/
        │   ├── include/
        │   ├── src/
        │   └── CMakeLists.txt
        │
        ├── admor_tracking/
        │   ├── admor_tracking/
        │   ├── config/
        │   └── launch/
        │
        ├── admor_bringup/
        │   ├── launch/
        │   ├── config/
        │   └── maps/
        │
        └── README.md
```

---

## Basic ROS 2 Workflow

```bash
# Create workspace
mkdir -p ~/admor_ws/src
cd ~/admor_ws

# Build workspace
colcon build

# Source workspace
source install/setup.bash

# Launch ADMOR system
ros2 launch admor_bringup admor.launch.py
```

---

## Monitoring the Robot

Useful ROS 2 commands:

```bash
ros2 node list
```

```bash
ros2 topic list
```

```bash
ros2 topic echo /cmd_vel
```

```bash
ros2 topic echo /scan
```

```bash
ros2 topic info /cmd_vel
```

---

## Comparison with Traditional Navigation

### Traditional Architecture

```text
Global A*
   ↓
Global Path
   ↓
DWA / TEB
   ↓
Velocity Commands
```

The global and local planners are relatively separated.

### ADMOR

```text
Sensors
   ↓
Dynamic Tracking
   ↓
Dynamic Cost Information
   ↓
Multi-Objective Global Planning
   ↓
Adaptive Local Trajectory Optimization
   ↓
Velocity Commands
```

ADMOR integrates dynamic obstacle prediction and multiple navigation objectives into the planning process.

---

## Applications

ADMOR is intended for indoor autonomous service robots such as:

* Hospital delivery robots
* Warehouse AMRs
* Campus service robots
* Indoor logistics robots
* Elder-care service robots
* Autonomous cleaning/service platforms

---

## Citation

If you use this work in a project or research publication, cite the associated ADMOR paper:

```text
Janupala Venkata Charitha et al.
"Adaptive Dynamic Multi-Objective Routing (ADMOR)
for Autonomous Indoor Service Robots:
Algorithm Design, Architecture, and Empirical Evaluation."
```

---

## License

Add the appropriate open-source license before publishing the repository, for example:

```text
MIT License
```

> Note: The uploaded paper specifies that complete source code, ROS 2 action servers, launch scripts, and experimental datasets are included in a supplementary repository archive, but the actual repository URL is not provided in the paper.
