import numpy as np
import matplotlib.pyplot as plt
import random
import math
import copy

def generateGrid(filename='rooms.png'):
    map = plt.imread(filename)
    map = np.mean(map, axis=2)
    map = np.where(map < 0.5, 0, 1)
    return map

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

    def __repr__(self):
        return str((self.x, self.y))

def distance(n1, n2):
    return np.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)

def generate_random_node(map):
    x = random.randint(0, map.shape[0]-1)
    y = random.randint(0, map.shape[1]-1)
    return Node(x, y)

def get_nearest_node(nodes, rnd):
    dlist = [(distance(node, rnd), node) for node in nodes]
    dlist.sort()
    return dlist[0][1]

def steer(fromNode, toNode, extendLength=1.0):
    d, theta = distance(fromNode, toNode), math.atan2(toNode.y - fromNode.y, toNode.x - fromNode.x)
    if d > extendLength:
        toNode = Node(fromNode.x + extendLength * math.cos(theta), fromNode.y + extendLength * math.sin(theta))
    toNode.parent = fromNode
    return toNode

def check_collision(node, obstacleList):
    if node is None:
        return False
    for (ox, oy, size) in obstacleList:
        dx_list = [node.x - ox, node.x - ox - size, node.x - ox + size]
        dy_list = [node.y - oy, node.y - oy - size, node.y - oy + size]
        d_list = [dx * dx + dy * dy for (dx, dy) in zip(dx_list, dy_list)]
        if min(d_list) <= size * size:
            return False  # collision
    return True  # safe

def generate_path(node):
    path = [[node.x, node.y]]
    while node.parent is not None:
        node = node.parent
        path.append([node.x, node.y])
    return path

def generate_obstacle_list(grid):
    obstacleList = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 0:
                obstacleList.append((i, j, 1))
    return obstacleList

grid = generateGrid('rooms.png')
obstacleList = generate_obstacle_list(grid)

nodes = [Node(0, 0)]
for i in range(1000):
    rnd = generate_random_node(grid)
    nind = get_nearest_node(nodes, rnd)
    newNode = steer(nind, rnd)
    if check_collision(newNode, obstacleList):
        nodes.append(newNode)

path = generate_path(nodes[-1])
path.reverse()
path = np.array(path)