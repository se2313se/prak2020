import numpy as np


class Node:
    def __init__(self, node_id, node_x, node_y):
        self.id = node_id
        self.x = node_x
        self.y = node_y
        self.xedge = False
        self.yedge = False
        #self.crdnt = np.array([node_x, node_y])

    def crdnt(self):
        return np.array([self.x, self.y])


class Element:
    def __init__(self, id, t_node, l_node, r_node):
        self.id = id
        self.napr = None
        self.deform = None
        self.color = None
        self.t_node = t_node
        self.l_node = l_node
        self.r_node = r_node
        self.ids = np.array([l_node.id, r_node.id, t_node.id])
        self.crdnts = np.array([l_node.crdnt, r_node.crdnt, t_node.crdnt])

    def square(self):
        a = np.array([self.t_node.x-self.l_node.x, self.l_node.x-self.r_node.x, 0])
        b = np.array([self.t_node.y-self.l_node.y, self.l_node.y-self.r_node.y, 0])
        return np.linalg.norm(np.cross(a, b)) / 2

    def crdnt(self):
        return np.array([self.l_node.crdnt(), self.r_node.crdnt(), self.t_node.crdnt()])
