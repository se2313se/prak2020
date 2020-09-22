from matplotlib.patches import Rectangle, Polygon
from matplotlib import cm


def get_maximum_minimum(napryazh, kind):
    q = []
    for i in list(napryazh.values()):
        q.append(i[kind][0])
    return max(q), min(q)


def show_color_mesh(elements: dict, nodes: dict, ax, color_elements):
    for key, i in elements.items():
        # print(color_elements[key])
        ax.add_patch(Polygon(
            [nodes[x] for x in i.ids],
            facecolor=color_elements[key]
        ))


def show_mesh(elements: dict, nodes: dict, ax):
    for i in elements.values():
        ax.add_patch(Polygon(
            [nodes[x] for x in i.ids],
            facecolor='yellow', edgecolor='violet'
        ))


def create_colored_elements(napr, kind):
    maximum, minimum = get_maximum_minimum(napr, kind)
    colored_elems = {}
    for key, value in napr.items():
        colored_elems[key] = cm.get_cmap('hot')((value[kind][0] - minimum) / (maximum - minimum)) #heatMapColorforValue(value[kind][0], maximum, minimum)
    return colored_elems