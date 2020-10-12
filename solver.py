import numpy as np
from classes import *
EPSILON = 0.0000000002
#в солвер передаем словари {id: Node}, {id: Element}, константы


def B_m(elem):
    a = elem.crdnt()[:, 0]
    b = elem.crdnt()[:, 1]
    return -np.array([
        [b[1] - b[2], 0, b[2] - b[0], 0, b[0] - b[1], 0],
        [0, a[2] - a[1], 0, a[0] - a[2], 0, a[1] - a[0]],
        [a[2] - a[1], b[1] - b[2], a[0] - a[2], b[2] - b[0], a[1] - a[0], b[0] - b[1]],
        ]) / (2 * elem.square())


def D_m(yung, puass):
    return yung * (1 - puass) / ((1 + puass) * (1 - 2 * puass)) * np.array([
        [1, puass / (1 - puass), 0],
        [puass / (1 - puass), 1, 0],
        [0, 0, (1 - 2 * puass) / (2 * (1 - puass))]
    ])


def solve(nodes, elems, yung, puass, P, H, L, step_N):
    def make_zakrep(nodes, k_glob, f_glob):
        nodes_count = len(nodes)
        for node in nodes:
            if node.x == -L/2 or node.x == L/2 or node.y == -H/2:
                key = node.id
                k_glob[key*2:key*2+2, :] = np.zeros((2, nodes_count*2))
                k_glob[:, key*2:key*2+2] = np.zeros((nodes_count*2, 2))
                k_glob[key*2, key*2] = 1
                k_glob[key*2+1, key*2+1] = 1
                f_glob[key*2:key*2+2, :] = np.zeros((2, 1))
                #f_glob[perenumber[key]*2] = 0
                # print(key, val)
        return k_glob, f_glob


    def get_f_loc(elem, P):
        f_loc = np.zeros((6,1))
        for i, point in enumerate(elem.crdnt()):
            if abs(point[1]-H/2)<EPSILON:
                f_loc[i*2+1] = P
        #print(edge)
        # print(np.abs(edge[1] - edge[0]))
        # print(f_loc)

        #print(f_loc.transpose(),a,b)

        return f_loc

    k_glob = np.zeros((2*len(nodes), 2*len(nodes)))
    f_glob = np.zeros((2*len(nodes), 1))

    # i = 0
    for elem in elems:
        a = elem.crdnt()[:, 0]
        b = elem.crdnt()[:, 1]

        B = B_m(elem)
        #print(elem.square(), elem.ids)
        D = D_m(yung, puass)
        k_mini = np.transpose(B).dot(D).dot(B) * elem.square()
        print(elem.id, elem.ids)
        print(B_m(elem))

        col = elem.ids

        #print(elem.id, elem.ids, k_mini[0:2, 4:6], k_glob[col[0]*2:col[0]*2+2, col[2]*2:col[2]*2 + 2])
        for i, col1 in enumerate(col):
            for j, col2 in enumerate(col):
                k_glob[col1 * 2:col1 * 2+2, col2 * 2:col2 * 2+2] += k_mini[i*2:(i+1)*2, j*2:(j+1)*2]

        # f_loc = get_f_loc(elem, P)
        # for i, col1 in enumerate(elem.ids):
        #     f_glob[col1 * 2:col1 * 2+2] += f_loc[i*2:(i+1)*2]
    f_glob[int(((step_N + 1)*(step_N+1)-1)*2-1)] = -P
    k_glob, f_glob = make_zakrep(nodes, k_glob, f_glob)
    # print(f_glob)
    k_glob.tofile('k_glob', sep = ';')
    f_glob.tofile('f_glob', sep = ';')

    return np.linalg.solve(k_glob, f_glob)


def get_napryazh_and_deform(nodes, elems, U, puass, yung):

    deform_vs_id = {}
    napryazh_vs_id = {}
    for elem in elems:
        a = elem.crdnt()[:, 0]
        b = elem.crdnt()[:, 1]

        B = B_m(elem)
        D = D_m(yung, puass)

        u_elem = np.zeros((6, 1))

        for i in range(3):
            for j in range(2):
                u_elem[i*2+j] = U[elem.ids[i] * 2+j]

        elem.deform = B.dot(u_elem).tolist()
        elem.napr = D.dot(elem.deform).tolist()

        #napryazh_vs_id[key] = napryazh
        #deform_vs_id[key] = deform

    return 1




