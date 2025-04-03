import numpy as np
import sys

sys.stdout = open("./output.txt", "w", encoding="utf-8")

def find_max_abs_element(M): # главный элемент
    max_abs = 0
    row_max, col_max = 0, 0

    for i in range(len(M)):
        for j in range(len(M[i]) - 1):
            if abs(M[i][j]) > max_abs:
                max_abs = abs(M[i][j])
                row_max, col_max = i, j
                
    return row_max, col_max


def solve(M):
    major_rows = []

    for _ in range(len(M)):
        row_max, col_max = find_max_abs_element(M)
        m = [-row[col_max] / M[row_max][col_max] for row in M] # множители для обнуления
        major_row = [i / M[row_max][col_max] for i in M[row_max]] # преобразование главной строки
        major_rows.append(major_row)

        # новая матрица с зануленными элементами
        M_new = [
            [M[i][j] + M[row_max][j] * m[i] if j != col_max else 0 for j in range(len(M[i]))] 
            for i in range(len(M)) if i != row_max
        ] 
        M = M_new

    
    major_rows = major_rows[::-1] # в обратном порядке  

    solution = np.zeros(len(major_rows[0]) - 1)

    for row_i in range(len(solution)):
        x_i = None

        for el_i in range(len(major_rows[row_i])):
            if major_rows[row_i][el_i] == 1:
                x_i = el_i
                break

        solution[x_i] = major_rows[row_i][-1]

        for x in range(len(solution)): # для корректного решения
            if x != x_i:
                solution[x_i] -= major_rows[row_i][x] * solution[x]

    return solution

M_example = np.array([
    [2.1, -4.5, -2.0, 19.07],
    [3, 2.5, 4.3, 3.21],
    [-6, 3.5, 2.5, -18.25]]
)


cols = 5
iterations = 3

for _ in range(iterations):
    M = np.random.random((cols, cols + 1))

    solution = solve(np.copy(M))
    solution_np = np.linalg.solve(np.copy(M[:, :-1]), np.copy(M[:, -1]))
    delta = np.abs(solution - solution_np) # разница между рещениями
    delta = M[:, :-1] @ solution - M[:, -1] # насколько решение удовлетворяет системе

    # print_as_table(M, 'M:')
    # print_as_table(solution, 'solution:')
    # print_as_table(solution_np, 'numpy solution:')
    # print_as_table(delta, 'delta:')

    print(f'M: {(M)}')
    print(f'x: {(solution)}')
    print(f'x_np: {(solution_np)}')
    print(f'delta: {(delta)}')
    print()

