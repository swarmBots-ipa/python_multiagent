import math
import matplotlib.pyplot as plt

class PolygonPose:
    def __init__(self, x, y, theta, agents, side_length):
        """
        Initializes a new PolygonPose object with a center point (x, y), an orientation angle theta (in radians),
        a number of edges agents, and a side length.
        """
        self.x = x
        self.y = y
        self.theta = theta
        self.agents = agents
        self.side_length = side_length
        self.vertices = self.construct_polygon()

    def construct_polygon(self):
        """
        Constructs the polygon and returns a list of its vertices.
        """
        # Compute the coordinates of the first vertex
        first_vertex_x = self.x + self.side_length * math.cos(self.theta)
        first_vertex_y = self.y + self.side_length * math.sin(self.theta)

        # Compute the angle between subsequent vertices
        angle_between_vertices = 2 * math.pi / self.agents

        # Initialize a list to store the polygon vertices
        vertices = [(first_vertex_x, first_vertex_y)]

        # Compute the remaining vertices and add them to the list
        for i in range(1, self.agents):
            # Compute the angle of the current vertex
            vertex_angle = self.theta + i * angle_between_vertices

            # Compute the coordinates of the current vertex
            vertex_x = self.x + self.side_length * math.cos(vertex_angle)
            vertex_y = self.y + self.side_length * math.sin(vertex_angle)

            # Add the current vertex to the list
            vertices.append((vertex_x, vertex_y))

        # Add the first vertex again to close the polygon
        vertices.append((first_vertex_x, first_vertex_y))
        return vertices[0:self.agents+1]

    def plot_vertices(self):
        """
        Plots the vertices of the polygon using Matplotlib.
        """
        # Extract the x and y coordinates of the vertices
        x = [vertex[0] for vertex in self.vertices]
        y = [vertex[1] for vertex in self.vertices]

        # Plot the vertices
        plt.plot(x, y, '-o')

        # Add labels and title
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('PolygonPose')

        # Show the plot
        plt.show()


def main():
    # Create a new polygon object
    x = 0
    y = 0
    theta = math.pi/4  # 45 degrees in radians
    agents = int(input("Enter the number of agents: "))
    side_length = 2
    polygon = PolygonPose(x, y, theta, agents, side_length)

    # Plot the vertices of the polygon
    polygon.plot_vertices()


if __name__ == '__main__':
    main()



