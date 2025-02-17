# Метод прогонки
def metod_progonki(matrix: list, vector: list) -> list:
    matrix_size = len(matrix)
    alpha_i = [0.0 for i in range(matrix_size)]
    beta_i = [0.0 for i in range(matrix_size)]

    """1. Вычисляем нулевые коэффициенты прогонки: alpha_0, beta_0"""
    b_0 = matrix[0][1]
    c_0 = matrix[0][0]
    g_0 = vector[0]

    alpha_i[1] = -b_0 / c_0
    beta_i[1] = g_0 / c_0

    """2. Итерационно вычисляем остальные коэффициенты прогонки: alpha_i, beta_i """
    for i in range(1, matrix_size - 1):
        a_i = matrix[i][i - 1]
        c_i = matrix[i][i]
        b_i = matrix[i][i + 1]
        g_i = vector[i]
        alpha_i[i + 1] = -b_i / (alpha_i[i] * a_i + c_i)
        beta_i[i + 1] = (g_i - a_i * beta_i[i]) / (alpha_i[i] * a_i + c_i)

    """3. Вычисляем последнюю компоненту вектора решений: v_i[n]"""
    v_i = [0 for i in range(matrix_size)]
    a_N = matrix[matrix_size - 1][matrix_size - 2]
    c_N = matrix[matrix_size - 1][matrix_size - 1]
    g_N = vector[matrix_size - 1]
    v_i[matrix_size - 1] = (g_N - a_N * beta_i[matrix_size - 1]) / (alpha_i[matrix_size - 1] * a_N + c_N)

    """4. Вычисляем оставшиеся компоненты: v_i"""
    for i in range(2, matrix_size + 1):
        v_i[matrix_size - i] = alpha_i[matrix_size - i + 1] * v_i[matrix_size- i + 1] + beta_i[matrix_size - i + 1]
    return v_i

# Вспомогательная сетка
def make_grid():
    r[0] = R_left
    for i in range(1, N + 1):
        r[i] = R_left + i * ((R_right - R_left) / N)
        h[i - 1] = r[i] - r[i - 1]
    r_half[0] = (r[1] + r[0]) / 2
    hi[0] = h[0] / 2
    for i in range(1, N - 1):
        r_half[i] = (r[i] + r[i + 1]) / 2
        hi[i] = (h[i] + h[i - 1]) / 2
    hi[N - 1] = (h[N - 2] + h[N - 1]) / 2
    hi[N] = h[N - 1] / 2
    r_half[N - 1] = (r[N] + r[N - 1]) / 2

# Заполняем вектора
def fill_vectors(test_type: int):
    global v, xi
    if test_type == 0: # Для константного теста
        v = 1
        xi = 1
        for i in range(N + 1):
            k[i] = 1
            f[i] = 1
            u[i] = 1
            q[i] = 1
    elif test_type == 1: # Для линейного теста
        v = 28
        xi = 2
        for i in range(N + 1):
            if i < N:
                k[i] = 2 * r_half[i] + 1
            f[i] = -4 - 12 * r[i] + r[i]**3
            u[i] = r[i]**2
            q[i] = r[i]
    elif test_type == 2: # Для 3 теста
        v = 72
        xi = 24
        for i in range(N + 1):
            if i < N:
                k[i] = 2 * r_half[i]
            f[i] = 3 * r[i]
            u[i] = 3
            q[i] = r[i]

# Вычисляем коэффициенты a, b, c и заполняем ими матрицу
def evaluate_ratio():
    ratio_matrix[0][1] = -r_half[0] * k[0] / h[0]
    ratio_matrix[0][0] = r_half[0] * k[0] / h[0] + hi[0] * r_half[0] * q[0] / 2

    g[0] = hi[0] * r_half[0] * f[0] / 2
    for i in range(1, N):
        ratio_matrix[i][i - 1] = -r_half[i - 1] * k[i - 1] / h[i - 1]
        ratio_matrix[i][i + 1] = -r_half[i] * k[i] / h[i]
        ratio_matrix[i][i] = r_half[i] * k[i] / h[i] + r_half[i - 1] * k[i -1] / h[i - 1] + hi[i] * r[i] * q[i]
        g[i] = hi[i] * r[i] * f[i]

    ratio_matrix[N][N - 1] = -r_half[N - 1] * k[N - 1] / h[N - 1]
    ratio_matrix[N][N] = r_half[N - 1] * k[N - 1] / h[N - 1] + r[N] * xi +hi[N] * r[N] * q[N]
    g[N] = hi[N] * r[N] * f[N] + r[N] * v


# Константный тест
def model_test(test_type: int):
    make_grid()
    fill_vectors(test_type)
    evaluate_ratio()

    """Находим максимум погрешности"""
    result = metod_progonki(ratio_matrix, g)

    maximum = abs(result[0] - u[0])
    for i in range(N + 1):
        temp = abs(result[i] - u[i])
        #print(f"{result[i]:e}\t\t{result[i] - u[i]:e}")
        if maximum < temp:
            maximum = temp
    print(f"Max delta: {maximum:e}")


N = 1024 # Число разбиений
R_left = 0 # Левая граница интервала
R_right = 2 # Правая граница интервала
v = 0
xi = 1

r = [0.0 for i in range(N + 1)]
r_half = [0.0 for i in range(N)]

h = [0.0 for i in range(N + 1)]
hi = [0.0 for i in range(N + 1)]

a = [0.0 for i in range(N + 1)]
b = [0.0 for i in range(N + 1)]
c = [0.0 for i in range(N + 1)]
g = [0.0 for i in range(N + 1)]

k = [0.0 for i in range(N + 1)]
q = [0.0 for i in range(N + 1)]
f = [0.0 for i in range(N + 1)]
u = [0.0 for i in range(N + 1)]

ratio_matrix = [[0 for i in range(N + 1)] for j in range(N + 1)]

if __name__ == '__main__':
    #result = metod_progonki(matrix_A, vector_g)
    #print("Результат работы метода прогонки:\n")
    # for i in range(N):
    # print(f'Radius: {r[i]:.2f}, Temperature: {result[i]:.2f}')

    print(f"\nN = {N:d}")
    print("----------Константный тест----------")
    model_test(0)
    print("\n----------Линейный тест----------")
    model_test(1)
    print("\n----------Нелинейный тест----------")
    model_test(2)