import numpy as np
import matplotlib.pyplot as plt

class FormationControl:
    def __init__(self, length, width, init_poses, init_velocities, goal_pose, dt=0.1, k_pos=1, k_orient=1):
        self.length = length
        self.width = width
        self.init_poses = init_poses
        self.init_velocities = init_velocities
        self.goal_pose = goal_pose
        self.dt = dt
        self.k_pos = k_pos
        self.k_orient = k_orient
        
        self.current_poses = np.copy(init_poses)
        self.current_velocities = np.copy(init_velocities)
        self.prev_error = np.zeros((4, 3))
        self.errors = []
        
    def update(self):
        # Calculate error between current and desired formation
        error_pos = np.zeros((4, 2))
        error_orient = np.zeros((4, 1))
        for i in range(4):
            error_pos[i, :] = self.current_poses[i, :2] - self.goal_pose[i, :2]
            error_orient[i] = self.current_poses[i, 2] - self.goal_pose[i, 2]
        error_pos = error_pos.reshape((-1, 1))
        error_orient = error_orient.reshape((-1, 1))
        error = np.vstack((error_pos, error_orient))
        self.errors.append(error)
        
        # Calculate control inputs using formation control algorithm
        control_inputs = np.zeros((4, 3))
        for i in range(4):
            # Position control
            pos_control = -self.k_pos * error_pos[i]
            # Orientation control
            orient_control = -self.k_orient * error_orient[i]
            # Integral control
            integral_control = self.prev_error[i] * self.dt
            # Derivative control
            derivative_control = (error[i] - self.prev_error[i]) / self.dt
            self.prev_error[i] = error[i]
            # Total control input
            control_inputs[i, :] = pos_control + orient_control + integral_control + derivative_control
        
        # Update velocities using control inputs
        self.current_velocities += control_inputs * self.dt
        
        # Update poses using velocities
        self.current_poses[:, :2] += self.current_velocities[:, :2] * self.dt
        self.current_poses[:, 2] += self.current_velocities[:, 2] * self.dt
        
    def run(self):
        poses_history = [np.copy(self.current_poses)]
        while np.linalg.norm(self.current_poses - self.goal_pose) > 0.1:
            self.update()
            poses_history.append(np.copy(self.current_poses))
        return poses_history, self.errors

# Define virtual rectangle
length = 5
width = 3
corners = np.array([[0, 0, 0], [length, 0, 0], [length, width, 0], [0, width, 0]])

# Define initial poses and velocities
init_poses = corners + np.array([[-0.5, -0.5, 0.1], [0.5, -0.5, -0.1], [0.5, 0.5, 0.1], [-0.5, 0.5, -0.1]])
init_velocities = np.zeros((4, 3))

# Define goal pose
goal_pose = corners + np.array([[2, 2, 0], [6, 2, 0], [8, 6, 0], [4, 6, 0]])

fc = FormationControl(length, width, init_poses, init_velocities, goal_pose, dt=0.01, k_pos=1, k_orient=1)
poses_history, errors = fc.run()

fig, axs = plt.subplots(2, 2, figsize=(10, 10))
for i in range(4):
    axs[i // 2, i % 2].plot([p[i, 0] for p in poses_history], [p[i, 1] for p in poses_history])
    axs[i // 2, i % 2].set_xlabel('X Position')
    axs[i // 2, i % 2].set_ylabel('Y Position')
    axs[i // 2, i % 2].set_title('Robot {}'.format(i+1))
    
axs[1, 1].plot([e[0] for e in errors], label='X Position Error')
axs[1, 1].plot([e[1] for e in errors], label='Y Position Error')
axs[1, 1].plot([e[2] for e in errors], label='Orientation Error')
axs[1, 1].set_xlabel('Time Step')
axs[1, 1].set_ylabel('Error')
axs[1, 1].set_title('Formation Error')
axs[1, 1].legend()
plt.tight_layout()
plt.show()