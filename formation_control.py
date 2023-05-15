import numpy as np

class RectangularFormationControl:
    def __init__(self, length, width, robot_poses, robot_velocities, kp=1, ki=0, kd=0):
        """Initializes the class with the dimensions of the virtual rectangle, the poses and velocities of the robots, and the PID control gains.

        Args:
            length (_type_): _description_
            width (_type_): _description_
            robot_poses (_type_): _description_
            robot_velocities (_type_): _description_
            kp (int, optional): _description_. Defaults to 1.
            ki (int, optional): _description_. Defaults to 0.
            kd (int, optional): _description_. Defaults to 0.
        """
        self.length = length
        self.width = width
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.robot_poses = robot_poses
        self.robot_velocities = robot_velocities
        self.desired_poses = self.get_desired_poses()
        
        self.prev_error = np.zeros((4, 3))
        self.integral_error = np.zeros((4, 3))

    def get_desired_poses(self):
        """Calculates the desired poses of the robots to maintain the rectangular shape.

        Returns:
            _type_: _description_
        """
        x, y, theta = self.robot_poses.T
        xc, yc = (x.mean(), y.mean())
        return np.array([
            [xc - self.length / 2, yc + self.width / 2, theta[0]],
            [xc + self.length / 2, yc + self.width / 2, theta[1]],
            [xc + self.length / 2, yc - self.width / 2, theta[2]],
            [xc - self.length / 2, yc - self.width / 2, theta[3]]
        ])

    def get_error(self):
        """Calculates the error between the current robot poses and the desired poses.

        Returns:
            _type_: _description_
        """
        return self.desired_poses - self.robot_poses

    def get_control_input(self):
        """Calculates the control inputs using a PID controller based on the error and the control gains.

        Returns:
            _type_: _description_
        """
        error = self.get_error()
        derivative_error = error - self.prev_error
        self.integral_error += error
        
        control_input = np.zeros((4, 3))
        for i in range(4):
            for j in range(3):
                control_input[i, j] = (
                    self.kp * error[i, j] +
                    self.ki * self.integral_error[i, j] +
                    self.kd * derivative_error[i, j]
                )
        
        self.prev_error = error
        return control_input

    def update_robot_velocities(self):
        """Updates the velocities of the robots using the control inputs.
        """
        control_input = self.get_control_input()
        self.robot_velocities += control_input

    def navigate_to_goal_pose(self, goal_pose):
        """Navigates the robots to the goal pose while maintaining

        Args:
            goal_pose (_type_): _description_
        """
        while np.linalg.norm(self.robot_poses - goal_pose) > 0.1:
            self.update_robot_velocities()
            self.robot_poses += self.robot_velocities
            self.desired_poses = self.get_desired_poses()

    def stop_at_goal_pose(self, goal_pose):
        self.robot_poses = goal_pose
        self.robot_velocities = np.zeros((4, 3))
        self.desired_poses = self.get_desired_poses()