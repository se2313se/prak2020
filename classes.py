import numpy as np


class Node:
    def __init__(self, node_id, node_x, node_y):
        self.id = node_id
        self.x = node_x
        self.y = node_y
        self.xedge = False
        self.yedge = False
        self.crdnt = np.array([node_x, node_y])


class Element:
    def __init__(self, id, t_node, l_node, r_node):
        self.id = id
        self.t_node = t_node
        self.l_node = l_node
        self.r_node = r_node
        self.ids = np.array([t_node.id, l_node.id, r_node.id])
        self.crdnt = np.array([t_node.crdnt, l_node.crdnt, r_node.crdnt])

    def square(self):
        a = np.array([self.t_node.x, self.l_node.x, self.r_node.x])
        b = np.array([self.t_node.y, self.l_node.y, self.r_node.y])
        return np.linalg.norm(np.cross(a, b)) / 2
