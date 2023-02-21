import random
import math
import colorama
from colorama import Fore, Style
from matplotlib import pyplot as plt

from polygon_edges import PolygonPose


class Formations:
    """
    A class that represents the formation of agents agents with random initial positions and target positions 
    in a 2-D space of size `space_size` and calculates the shortest path between each initial position and 
    target position.

    Attributes:
        agents (int): Number of agents.
        side_length (int): Length of the side of the square target positions.
        space_size (tuple): Size of the 2-D space in the form of (x, y).
        initial_positions (list): List of tuples representing the initial positions of the agents.
        target_positions (list): List of tuples representing the target positions of the agents.
        distances (list): List of tuples representing the distances between each initial and target position.
    """

    def __init__(self, agents, side_length=30, space_size=(200, 200)):
        """
        Initializes the class with the required parameters.

        Args:
            agents (int): Number of agents.
            side_length (int): Length of the side of the square target positions.
            space_size (tuple): Size of the 2-D space in the form of (x, y).
        """
        # number of agents here
        self.agents = agents
        self.side_length = side_length
        self.space_size = space_size
        # initial poses of the agents can  be used here
        self.initial_positions = []
        # generate sides of a polygon
        polygon = PolygonPose(x=100, y=100, theta=math.pi/4,
                          agents=self.agents, side_length=self.side_length)
        self.target_positions = polygon.construct_polygon()

        self.distances = []

    def generate_positions(self):
        """
        Generates random initial and target positions for each robot.

        Returns:
            tuple: A tuple of the form (initial_positions, target_positions) representing the 
            initial and target positions of the agents.
        """
        for i in range(self.agents):
            x = random.randint(*random.choice([(0, 55), (135, self.space_size[0])]))
            y = random.randint(*random.choice([(0, 55), (135, self.space_size[1])]))
            self.initial_positions.append((x, y))
        
        # print("initial poses:", self.initial_positions)
        # print("target poses:", self.target_positions)
        return self.initial_positions, self.target_positions
        

    def get_shortest_path(self, initial_positions, target_positions): 
        """"
        Calculates the shortest path between all the combinations of initial and target poses and 
        find the best combination of initial and tgarget poses for the shortest travel distance combination

        Returns:
            list of tuples which contains the best combination of intial and target poses.
        """
        for i in range(self.agents):
            for j in range(self.agents):
                distance = math.sqrt((self.target_positions[j][0] - self.initial_positions[i][0])**2 +
                                    (self.target_positions[j][1] - self.initial_positions[i][1])**2)
                self.distances.append((distance, i, j))

        self.distances.sort()
        pairs = []
        used_initial = {}
        used_target = {}
        target_dict = {}
        for distance, i, j in self.distances:
            if i not in used_initial and j not in used_target:
                target_dict[i] = self.target_positions[j]
                used_initial[i] = True
                used_target[j] = True
        for i in range(self.agents):
            pairs.append((self.initial_positions[i], target_dict[i]))
        return pairs



def plot_optimized_pairs(pairs):
    x = []
    y = []

    for i, pair in enumerate(initial_positions):
        x.append(pair[0])
        y.append(pair[1])
        plt.annotate(f"[{i + 1}]i_pose", (pair[0], pair[1]))

    a = []
    b = []

    for i, pair in enumerate(target_positions):
        a.append(pair[0])
        b.append(pair[1])
        plt.annotate(f"[{i + 1}]t_pose", (pair[0], pair[1]))

    plt.scatter(x, y, color='red', marker='o', label='Initial Positions')
    plt.scatter(a, b, color='blue', marker='*', label='Target Positions')

    plt.axis([0, 200, 0, 200])
    plt.legend()
    plt.show()


if __name__ == "__main__":
    agents = int(input("Enter the number of agents: "))
    formation = Formations(agents)

    initial_positions, target_positions = formation.generate_positions()
    pairs = formation.get_shortest_path(initial_positions, target_positions)

    for pair in pairs:
        print(Fore.RED+"\nInitial Position:", pair[0],Fore.GREEN+" Target Position:", pair[1])
    
    plot_optimized_pairs(pairs)


