import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from formation_control import RectangularFormationControl

# Define the initial robot poses and velocities
robot_poses = np.array([
    [0, 0, 0],
    [0, 1, np.pi/2],
    [1, 1, np.pi],
    [1, 0, -np.pi/2]
])
robot_velocities = np.zeros((4, 3))

# Define the dimensions of the virtual rectangle
length = 1.5
width = 1

# Create an instance of the RectangularFormationControl class
controller = RectangularFormationControl(length, width, robot_poses, robot_velocities, kp=1, ki=0, kd=0)

# Define the goal pose
goal_pose = np.array([
    [2, 2, 0],
    [2, 3, np.pi/2],
    [3, 3, np.pi],
    [3, 2, -np.pi/2]
])

# Define the figure and axis for the plot
fig, ax = plt.subplots()
ax.set_xlim([-0.5, 3.5])
ax.set_ylim([-0.5, 3.5])
ax.set_aspect('equal')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Rectangular Formation Control')

# Define the robot markers
markers = []
for i in range(4):
    marker, = ax.plot([], [], 'o', markersize=10)
    markers.append(marker)

# Define the function to update the plot in each frame of the animation
def update(frame):
    # Navigate the robots to the goal pose
    controller.navigate_to_goal_pose(goal_pose)
    
    # Update the robot markers with the current poses
    for i, marker in enumerate(markers):
        x, y, theta = controller.robot_poses[i]
        marker.set_data([x], [y])
        marker.set_markerfacecolor((1, 0, 0, 0.5))
        marker.set_markeredgecolor((0, 0, 0, 1))
        marker.set_marker("$ {} $".format(i+1))

    # Update the plot limits to include all the robot positions
    x_min = min(controller.robot_poses[:, 0]) - 1
    x_max = max(controller.robot_poses[:, 0]) + 1
    y_min = min(controller.robot_poses[:, 1]) - 1
    y_max = max(controller.robot_poses[:, 1]) + 1
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    return markers

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(100), blit=True)

# Show the plot
plt.show()