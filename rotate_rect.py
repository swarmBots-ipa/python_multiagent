import matplotlib.pyplot as plt
import numpy as np

def generate_path(num_points):
    x = np.random.randint(0, 200, num_points)
    y = np.random.randint(0, 200, num_points)
    theta = np.random.uniform(0, 2*np.pi, num_points)
    return x, y, theta

def rotate_point(point, angle):
    c, s = np.cos(angle), np.sin(angle)
    R = np.array([[c, -s], [s, c]])
    return R.dot(point)

def get_rectangle_vertices(center, length, width, theta):
    half_length = length/2
    half_width = width/2

    p1 = np.array([-half_length, -half_width])
    p2 = np.array([half_length, -half_width])
    p3 = np.array([half_length, half_width])
    p4 = np.array([-half_length, half_width])

    vertices = [p1, p2, p3, p4]

    rotated_vertices = []
    for vertex in vertices:
        rotated_vertex = rotate_point(vertex, theta)
        rotated_vertices.append(center + rotated_vertex)

    return rotated_vertices

def plot_rectangle_path(num_points, length, width):
    x, y, theta = generate_path(num_points)
    fig, ax = plt.subplots()
    for i in range(num_points):
        center = np.array([x[i], y[i]])
        vertices = get_rectangle_vertices(center, length, width, theta[i])
        xs = [vertex[0] for vertex in vertices] + [vertices[0][0]]
        ys = [vertex[1] for vertex in vertices] + [vertices[0][1]]
        ax.plot(xs, ys)
    ax.set_xlim([0, 200])
    ax.set_ylim([0, 200])
    plt.show()

plot_rectangle_path(50, 20, 10)