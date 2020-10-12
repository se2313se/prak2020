from matplotlib.patches import Rectangle, Polygon
from matplotlib import cm
import numpy as np


def get_maximum_minimum(elements):
    q = []
    for i in elements:
        q.append(i.napr)
    q = np.array(q)
    max_ = [max(q[:, i].tolist()) for i in range(3)]
    min_ = [min(q[:, i].tolist()) for i in range(3)]
    return max_, min_


def show_color_mesh(elems, ax, k):
    for elem in elems:
        # print(color_elements[key])
        ax.add_patch(Polygon(
            elem.crdnt(),
            facecolor=elem.color[k]
        ))


def show_mesh(elements, ax):
    for elem in elements:
        ax.add_patch(Polygon(elem.crdnt(),
                        facecolor='lime', edgecolor='blue'
        ))


def coloring_elements(elems):
    maximum, minimum = get_maximum_minimum(elems)
    for elem in elems:
        elem.color = [cm.get_cmap('hot')((elem.napr[i][0] - minimum[i][0]) / (maximum[i][0] - minimum[i][0])) for i in range(3)]
        #heatMapColorforValue(value[kind][0], maximum, minimum)
