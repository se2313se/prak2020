from matplotlib import pyplot as plt
from helper import *
from classes import *
from graphs import *
from solver import *
from collections import OrderedDict


def create_mesh(H, L, dy, dx):
    y_step = list(np.arange(0, H, dy))
    ly = len(y_step)
    x_step = list(np.arange(0, L, dx)) #- L / 2)
    nodes = {i: Node(i, x_step[0], y) for i, y in enumerate(y_step)}
    elements = {}
    element_id = 0
    node_id = len(y_step)-1
    for x in x_step[1:]:
        node_id += 1
        nodes[node_id] = Node(node_id, x, 0)
        for y in y_step[1:]:
            node_id += 1
            nodes[node_id] = Node(node_id, x, y)
            if x > 0:
                elements[element_id] = Element(element_id, nodes[node_id-1-ly], nodes[node_id-ly], nodes[node_id-1])
                elements[element_id+1] = Element(element_id+1, nodes[node_id-1], nodes[node_id-ly], nodes[node_id])
                element_id += 2
            else:
                elements[element_id] = Element(element_id, nodes[node_id-1], nodes[node_id-1-ly], nodes[node_id])
                elements[element_id+1] = Element(element_id+1, nodes[node_id-1-ly], nodes[node_id-ly], nodes[node_id])
                element_id += 2

    return nodes, elements



#zamenil v tele main
#def heatMapColorforValue(value, maximum, minimum): #zamenil
#    h = (value - minimum) / (maximum - minimum)
#    return cm.get_cmap('hot')((value - minimum) / (maximum - minimum))



def get_napr_from_elems(elems, napr, kind):
    new_napr = {}
    for key in elems:
        new_napr[key]=napr[key][kind][0]
    return new_napr


H = 2
L = 10
puass = 0.3
yung = 200
q = 3.2


fig, ax = plt.subplots(1)
ax.axvline(x=0, c='black')
ax.set_xlim([-L*0.05, L * 1.05])
ax.set_ylim([-H, H])

# стриоим балкуdefshow_balk(H, L, ax, fig) = show_balk(height, length, ax, fig):
#                                                   ax.add_patch(Rectangle((0, -height / 2), length, height))
#                                                   fig.show()
ax.add_patch(Rectangle((0, -H / 2), L, H))
fig.show()

STEPS = np.arange(1, 100, 1)[2:32:2][10:13]

plot_fig2, axs2 = plt.subplots(1, figsize=(17, 12))


for step_N in STEPS[:]:
    P = -q/(step_N+1)
    H_step = H / step_N
    L_step = L / step_N

    # строим узлы и элементы
    nodes, elements = create_mesh(H, L, H_step, L_step)
    fig, ax = plt.subplots(1)
    ax.axvline(x=0, c='black')
    ax.set_xlim([-L * 0.05, L * 1.05])
    ax.set_ylim([-H, H])


    # Строим перемещения
    U = solve(nodes, elements, yung, puass, P, H)

    napryazh_vs_id, deform_vs_id = get_napryazh_and_deform(nodes, elements, U, puass, yung)
    fig, ax = plt.subplots(1)
    ax.axvline(x=0, c='black')
    ax.set_xlim([-L * 0.05, L * 1.05])
    ax.set_ylim([-H, H])
    new_nodes = {}

    for i in range(int(len(U) / 2)):
        new_nodes[i] = (nodes[i].x + U[i * 2][0], nodes[i].y + U[i * 2 + 1][0])
    show_mesh(elements, new_nodes, ax)
    fig.show()
    color_elements = create_colored_elements(napryazh_vs_id, 1)
    new_color_elements = {}
    null_elements = set()
    for key in color_elements.keys():
        if step_N % 2 != 0:
            for j in range(2 * step_N):
                null_elements.add(step_N * step_N + j-step_N)
        else:
            for j in range(2 * step_N):
                null_elements.add(step_N * step_N + j)

    for key, value in color_elements.items():
        if key not in null_elements:
            new_color_elements[key] = (1.0, 0.0, 0.0, 1.0)
        else:
            new_color_elements[key] = (0.0, 0.0, 0.0, 1.0)


    for q_ in range(3):
        new_napr = get_napr_from_elems(null_elements, napryazh_vs_id, q_)
        x = []
        y = []
        z2 = {}
        for element_id in sorted(null_elements):
            n_x = (nodes[elements[element_id].ids[0]].x + nodes[elements[element_id].ids[1]].x)/2
            if n_x not in z2.keys():
                z2[n_x]=new_napr[element_id]
            else:
                z2[n_x]+=new_napr[element_id]
                z2[n_x]=z2[n_x]/2

        axs2.plot(list(z2.keys()), list(z2.values()))

    show_color_mesh(elements, new_nodes, ax, color_elements)
    # show_color_mesh(elements, new_nodes, ax, new_color_elements)
    fig.show()
    fig.savefig(f'steps/step_{step_N}.png')




plot_fig2.show()
plot_fig2.savefig(f'napr.png')

