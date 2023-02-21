import matplotlib.pyplot as plt
import numpy as np
import random

class Rectangle:

    def __init__(self, width, height, center):
        self.width = width
        self.height = height
        self.center = center
        self.vertices = self.compute_vertices()

    def compute_vertices(self):
        x, y = self.center
        half_width = self.width / 2
        half_height = self.height / 2
        vertices = [(x - half_width, y - half_height),
                    (x + half_width, y - half_height),
                    (x + half_width, y + half_height),
                    (x - half_width, y + half_height)]
        return vertices

    def translate(self, delta):
        dx, dy = delta
        self.center = (self.center[0] + dx, self.center[1] + dy)
        self.vertices = self.compute_vertices()

    def plot(self):
        x, y = zip(*self.vertices)
        plt.plot(x, y)

def generate_path(n_points, x_range, y_range):
    x_points = random.sample(range(x_range), n_points)
    y_points = random.sample(range(y_range), n_points)
    return list(zip(x_points, y_points))

def plot_path(path):
    x, y = zip(*path)
    plt.plot(x, y, marker='o')

# Define the size of the 2D space and the size of the rectangle
x_range, y_range = 200, 200
width, height = 20, 40

# Define the number of points in the random path
n_points = 10

# Generate the random path
path = generate_path(n_points, x_range, y_range)

# Create a rectangle with the initial center
center = path[0]
rectangle = Rectangle(width, height, center)

# Plot the initial rectangle and the path
rectangle.plot()
plot_path(path)

# Move the rectangle along the path and plot the updated rectangle
for i in range(1, n_points):
    delta = (path[i][0] - path[i-1][0], path[i][1] - path[i-1][1])
    rectangle.translate(delta)
    rectangle.plot()

# Add axis labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Path traced by a rectangle')
plt.show()