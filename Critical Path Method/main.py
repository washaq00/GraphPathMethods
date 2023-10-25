import sys

import numpy as np

class Node():
    def __init__(self, id = 0, time = 0, ls = 0, lf = 0, es = 0, ef = 0, dpd = 0):
        self.id = id
        self.time = time
        self.ls = ls
        self.lf = lf
        self. es = es
        self.ef = ef
        self.dpd =[]


def critical_path_method(matrix, tasks):

    for k in range(0,len(tasks)):
        for i in range(0, len(tasks)):
            for j in range(0,len(tasks)):
                if matrix[j][i] == 1:
                    tasks[i].es = max(tasks[i].es,tasks[j].ef)
            tasks[i].ef = tasks[i].es + tasks[i].time

    sorted_tasks = sorted(tasks, key=lambda a: -a.ef)
    critical_path = []
    for i in sorted_tasks:
        print(f" o teraz {i.id, i.es, i.ef, i.ls, i.lf}")

    for i in sorted_tasks:
        id = i.id-1
        last_task: bool = True
        for j in range(0,len(tasks)):
            if matrix[id][j] == 1:
                last_task = False
                break
        if last_task:
            tasks[id].lf = sorted_tasks[0].ef
            tasks[id].ls = tasks[id].lf - tasks[id].time
        else:
            tasks[id].lf = sys.maxsize
            tasks[id].ls = sys.maxsize
        for k in range(0,len(tasks)):
            if matrix[id][k] == 1:
                tasks[id].lf = min(tasks[id].lf, tasks[k].ls)
                print(sorted_tasks[id].lf)
        tasks[id].ls = tasks[id].lf - tasks[id].time
    for i in tasks:
        print(f" o teraz {i.id, i.es, i.ef, i.ls, i.lf}")

    # for s in critical_path:
    #     print(s)
    #



def main():

    with open('data80.txt', 'r') as file:
        lines = file.readlines()

    connections = [int(num) for num in lines[0].split()]

    times = [int(num) for num in lines[1].split()]
    tasks = []
    p: int = connections[0]
    s = (p, p)
    matrix = np.array(np.zeros(s))
    dependencies_raw = [int(num) for num in lines[2].split()]
    tks = []
    dpd = []
    tasks = []

    for i in range(0, len(dependencies_raw), 2):
        matrix[dependencies_raw[i]-1][dependencies_raw[i+1]-1] = 1
        dpd.append(dependencies_raw[i])
        tks.append(dependencies_raw[i+1])

    for i in range(0,p):
        tasks.append(Node(id = i+1, time = times[i]))

    for i in range(0,connections[1]):
        for k in range(0,connections[0]):
            if tasks[k].id == tks[i]:
                tasks[k].dpd.append(dpd[i])

    critical_path_method(matrix, tasks)


if __name__ == "__main__":
    main()
