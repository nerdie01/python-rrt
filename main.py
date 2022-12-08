import nav

import numpy as np
import matplotlib.pyplot as plt

grid = nav.generateGrid('rooms.png')
obstacleList = nav.generate_obstacle_list(grid)

nodes = [nav.Node(0, 0)]
for i in range(1000):
    rnd = nav.generate_random_node(grid)
    nind = nav.get_nearest_node(nodes, rnd)
    newNode = nav.steer(nind, rnd)
    if nav.check_collision(newNode, obstacleList):
        nodes.append(newNode)

path = nav.generate_path(nodes[-1])
path.reverse()
path = np.array(path)

#render the path in the grid with matplotlib
plt.imshow(grid, cmap='Greys', origin='lower')
plt.plot(path[:, 0], path[:, 1], 'r')
plt.show()