import sys
import numpy as np


def load_matrix():

    filename = f'data.txt'
    with open(filename, 'r') as file:
        lines = file.readlines()

    n_tasks = [int(num) for num in lines[0].split()]
    s = (n_tasks[0], n_tasks[0])
    matrix = np.array(np.zeros(s))

    for k in range(1, len(lines)):
        lines[k] = [int(num) for num in lines[k].split()]
    for i in range(0,n_tasks[0]):
        for j in range(0,n_tasks[0]):
            if lines[i+1][j] != '\n':
                matrix[i][j] = lines[i+1][j]

    print(matrix)

    return matrix, n_tasks[0]


def ford():

    matrix, n_tasks = load_matrix()
    distances: list[int] = [1000] * n_tasks
    distances[0] = 0
    print(distances)

    for y in range(0, n_tasks):
        for z in range(0,n_tasks):
            if matrix[y][z] != 0 and distances[z] > distances[y] + matrix[y][z]:
                distances[z] = distances[y] + matrix[y][z]
    print(distances)

def dijkstra():

def main():
    ford()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
