import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def print_matrix(matrix, type, task):
    with open(f"no_{task}.txt", "a") as file:
        file.write(f"Matrix of {type}:\n")
        file.write(f"{matrix}\n\n")


def draw_graph(x, y, z, type, azim=0, elev=0):
    if type == 1:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot_surface(x, y, z, cmap='viridis')
        ax.view_init(elev=elev, azim=azim)

        plt.savefig(f"graph1(azim={azim})")
    else:
        fig, ax = plt.subplots()
        ax.contour(x, y, z, levels=14, linewidths=0.5, colors='k')
        contour_ = ax.contourf(x, y, z, levels=14, cmap='viridis')
        fig.colorbar(contour_, ax=ax)

        plt.savefig("graph2.png")


if __name__ == "__main__":
    # исходные данные
    H_ROW = 8
    H_COL = 8
    X_ROW = 8
    X_COL = 8
    Y_ROW = (H_ROW + X_ROW - 1)
    Y_COL = (H_COL + X_COL - 1)

    x = np.array([
        [5, 6, 0, 3, 0, 5, 0, 5],
        [5, 4, 0, 4, 0, 5, 0, 3],
        [4, 5, 3, 0, 5, 6, 7, 7],
        [0, 2, 0, 4, 4, 5, 7, 8],
        [5, 0, 6, 5, 7, 8, 7, 9],
        [3, 3, 4, 4, 4, 5, 7, 6],
        [0, 3, 2, 3, 0, 5, 0, 6],
        [4, 4, 5, 7, 0, 9, 8, 4]
    ])
    h = np.array([
        [5, 0, 5, 4, 6, 4, 4, 5],
        [3, 3, 3, 3, 2, 2, 2, 5],
        [4, 5, 7, 8, 8, 5, 7, 6],
        [3, 4, 4, 5, 5, 4, 5, 6],
        [3, 4, 3, 6, 5, 4, 5, 7],
        [0, 3, 4, 4, 0, 4, 6, 4],
        [2, 3, 3, 3, 3, 4, 4, 0],
        [5, 3, 4, 4, 4, 4, 3, 3]
    ])
    y = np.zeros((Y_ROW, Y_COL), dtype=np.int32)


    # дискретная свертка
    y_task1 = y.copy()
    for i in range(y.shape[0]):
        for j in range(y.shape[1]):
            for k1 in range(h.shape[0]):
                for k2 in range(h.shape[1]):
                    if (0 <= i - k1 < x.shape[0]) and (0 <= j - k2 < x.shape[1]):
                        y_task1[i, j] += h[k1, k2] * x[i - k1, j - k2]

    print_matrix(x, 'X', 1)
    print_matrix(h, 'H', 1)
    print_matrix(y_task1, 'Y', 1)


    # суммирование взвешенных и сдвинутых импульсных откликов
    y_task2 = y.copy()
    for k1 in range(x.shape[0]):
        for k2 in range(x.shape[1]):
            temp = np.zeros((y_task2.shape[0], y_task2.shape[1]))
            for m1 in range(h.shape[0]):
                for m2 in range(h.shape[1]):
                    temp[m1 + k1, m2 + k2] = h[m1, m2] * x[k1, k2]
            print_matrix(temp, f"h(n1, n2) * x({k1 + 1}, {k2 + 1})", 2)
            for i in range(y_task2.shape[0]):
                for j in range(y_task2.shape[1]):
                    y_task2[i, j] += temp[i, j]

    print_matrix(y_task2, 'Y', 2)


    # графическое представление
    x = np.arange(Y_ROW)
    y = np.arange(Y_COL)
    z = y_task1.copy()

    x, y = np.meshgrid(x, y)
    draw_graph(x, y, z, type=1, azim=-135, elev=25)
    draw_graph(x, y, z, type=1, azim=45, elev=25)
    draw_graph(x, y, z, type=2)
