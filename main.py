from matplotlib import pyplot as plt
from classes import *
from graphs import *
from solver import *
from collections import OrderedDict


def fig_create():
    fig, ax = plt.subplots(1)
    # ax.axvline(x=0, c='black')
    ax.set_xlim([-L * 0.525, L * 0.525])
    ax.set_ylim([-H * 1.05, H * 0.25])
    # show_mesh(elements, ax)
    return fig, ax

def create_mesh(H, L, dy, dx):
    y_step = list(np.arange(-H, dy, dy))
    ly = len(y_step)
    x_step = list(np.arange(0, L+dx, dx) - L / 2)
    nodes = [Node(i, x_step[0], y) for i, y in enumerate(y_step)]
    elements = []
    element_id = 0
    node_id = len(y_step)-1
    for x in x_step[1:]:
        node_id += 1
        nodes.append(Node(node_id, x, y_step[0]))
        for y in y_step[1:]:
            node_id += 1
            nodes.append(Node(node_id, x, y))
            if x <= 0:
                elements.append(Element(element_id, nodes[node_id-1-ly], nodes[node_id-ly], nodes[node_id-1]))
                elements.append(Element(element_id+1, nodes[node_id-1], nodes[node_id-ly], nodes[node_id]))
                element_id += 2
            else:
                elements.append(Element(element_id, nodes[node_id-1], nodes[node_id-1-ly], nodes[node_id]))
                elements.append(Element(element_id+1, nodes[node_id-1-ly], nodes[node_id-ly], nodes[node_id]))
                element_id += 2

    return nodes, elements


def get_napr_from_elems(elems, napr, kind):
    new_napr = {}
    for key in elems:
        new_napr[key]=napr[key][kind][0]
    return new_napr


H = 2
L = 4
puass = 0.3
yung = 200
q = 10

STEPS = [10, 20, 40, 60]

plot_fig2, axs2 = plt.subplots(1, figsize=(17, 12))
plot_fig3, axs3 = plt.subplots(1, figsize=(17, 12))


for step_N in STEPS[:]:
    P = q #-q/(step_N+1)
    step_Nx = 2*step_N
    step_Ny = step_N
    H_step = H / step_Ny
    L_step = L / step_Nx

    nodes, elements = create_mesh(H, L, H_step, L_step)

    U = solve(nodes, elements, yung, puass, P, H, L, step_N)

    get_napryazh_and_deform(nodes, elements, U, puass, yung)
    fig, ax = fig_create()

    # ax.axvline(x=0, c='black')
    # ax[0].set_xlim([-L * 0.525, L * 0.525])
    # ax[0].set_ylim([-H * 1.05, H * 0.25])
    # ax[1].set_xlim([-L * 0.525, L * 0.525])
    # ax[1].set_ylim([-H * 1.05, H * 0.25])
    new_nodes = {}

    for i in range(int(len(U) / 2)):
        nodes[i].x, nodes[i].y = (nodes[i].x + U[i * 2][0], nodes[i].y + U[i * 2 + 1][0])
    for elem in elements:
        ax.add_patch(Polygon(elem.crdnt(),
                             facecolor='lime', edgecolor='blue'
                             ))
    fig.show()
    coloring_elements(elements)
    null_elements = set()
    # for elem in elements:
    #     if step_N % 2 != 0:
    #         for j in range(2 * step_N):
    #             null_elements.add(step_N * step_N + j-step_N)
    #     else:
    #         for j in range(2 * step_N):
    #             null_elements.add(step_N * step_N + j)
    #
    # for elem in elements:
    #     if elem.id not in null_elements:
    #         elem.color = (0, 1.0, 0.0, 1.0)
    #     else:
    #         elem.color = (0.0, 0.0, 0.0, 1.0)


    # for q_ in range(3):
    #     new_napr = get_napr_from_elems(null_elements, napryazh_vs_id, q_)
    #     x = []
    #     y = []
    #     z2 = {}
    #     for element_id in sorted(null_elements):
    #         n_x = (nodes[elements[element_id].ids[0]].x + nodes[elements[element_id].ids[1]].x)/2
    #         if n_x not in z2.keys():
    #             z2[n_x] = new_napr[element_id]
    #         else:
    #             z2[n_x] += new_napr[element_id]
    #             z2[n_x] = z2[n_x]/2
    #
    axs2.plot(np.arange(-H, 0 + H_step / 2, H_step/2).tolist(),
              [(elements[i].napr[1][0] + elements[i + 1].napr[1][0]) / 2
               for i in range(step_Ny ** 2, step_Ny ** 2 + 2 * step_Ny + 1)][::],
              label=step_N)
    axs3.plot(np.arange(-H, 0 + H_step / 2, H_step/2).tolist(),
              [(elements[i].napr[0][0] + elements[i + 1].napr[0][0]) / 2
               for i in range(step_Ny ** 2, step_Ny ** 2 + 2 * step_Ny + 1)][::],
              label=step_N)

    plot_fig2.legend()
    plot_fig2.show()
    axs2.set_xlabel("y")
    axs2.set_ylabel('sigmaYY, x={}'.format(-L/4))
    plot_fig2.savefig('naprYY-x={}.png'.format(-L / 4))
    plot_fig3.legend()
    plot_fig3.show()
    axs3.set_xlabel("y")
    axs3.set_ylabel('sigmaXX, x={}'.format(-L / 4))
    plot_fig3.savefig('naprXX-x={}.png'.format(-L / 4))
    show_color_mesh(elements, ax, 0)
    # show_color_mesh(elements, new_nodes, ax, new_color_elements)
    fig.show()
    fig.savefig(f'steps/step_{step_N}xx.png')
    show_color_mesh(elements, ax, 1)
    # show_color_mesh(elements, new_nodes, ax, new_color_elements)
    fig.show()
    fig.savefig(f'steps/step_{step_N}yy.png')

plot_fig2.legend()
plot_fig2.show()
plot_fig2.savefig(f'napr.png')

