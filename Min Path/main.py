import sys
import numpy as np
import heapq


def load_matrix()-> tuple:

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

    # print(matrix)

    return matrix, n_tasks[0]


def ford()-> None:

    matrix, n_tasks = load_matrix()
    distances: list[int] = [1000] * n_tasks
    distances[0] = 0

    for y in range(0, n_tasks):
        for z in range(0,n_tasks):
            if matrix[y][z] != 0 and distances[z] > distances[y] + matrix[y][z]:
                distances[z] = distances[y] + matrix[y][z]

    print(distances)


def next_to_visit(i: int, matrix) -> list:
    visit = []
    for y in range(0,len(matrix)):
            if matrix[i][y] != 0:
                temp = [y,matrix[i][y]]
                visit.append(temp)

    return visit


class Node:
    def __init__(self, id = 0, distance = sys.maxsize):
        self.visited = False
        self.distance = distance
        self.id = id


# def find_min(graphs: list[Node]):
#     temp = 0
#     temp_id = 0
#     for i in range(0,len(graphs)):
#         if graphs[i].visited and graphs[i].distance < temp:
#             temp = graphs[i].distance
#             temp_id = graphs[i].id
#     return temp_id
#
#
# def find_next(graph: list[Node]) -> int:
#     minimal = find_min(graph)
#     min_id = graph[0].id - minimal
#
#     return min_id
#
#
# def dijkstra() -> None:
#     graph: list[Node] = []
#     matrix: list
#     n_tasks: int
#     ds:int
#
#     matrix, n_tasks = load_matrix()
#     for i in range(0,n_tasks):
#         graph.append(Node(id = i))
#     graph[0].distance = 0
#
#     for i in range(0,n_tasks):
#         minimal = find_next(graph)
#         graph[minimal].visited = True
#
#         for neighbor in range(0,n_tasks):
#             if not graph[neighbor].visited and matrix[minimal][neighbor] != 0 and graph[minimal].distance != sys.maxsize:
#                 ds = graph[minimal].distance + matrix[minimal][neighbor]
#                 if ds < graph[neighbor].distance:
#                     graph[neighbor].distance = graph[minimal].distance + matrix[minimal][neighbor]
#
#     for i in range(0,len(graph)):


def dijkstra_heap():
    matrix, n_tasks = load_matrix()
    adj = {}
    graph: list[Node] = []

    for i in range(0,n_tasks):
        graph.append(Node(id = i))
    graph[0].distance = 0
    minHeap:list[Node] = []
    minHeap.append((graph[0]))

    while minHeap:
        current = minHeap.pop().id
        if graph[current].visited:
            continue
        graph[current].visited = True

        for neighbor in range(0,n_tasks):
            if not graph[neighbor].visited and matrix[current][neighbor] != 0 and graph[current].distance != sys.maxsize:
                ds = graph[current].distance + matrix[current][neighbor]
                if ds < graph[neighbor].distance:
                    graph[neighbor].distance = ds
                    minHeap.append(Node(id =neighbor, distance = ds))

    for i in range(0,len(graph)):
        print(graph[i].distance)






def main():
    # ford()
    dijkstra_heap()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


