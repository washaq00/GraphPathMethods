<<<<<<< HEAD
#include <iostream>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

// Funkcja obliczająca ścieżkę krytyczną za pomocą macierzy sąsiedztwa
void calculateCriticalPath(const vector<vector<int>>& adjacencyMatrix) {
    int numTasks = adjacencyMatrix.size();

    vector<int> inDegree(numTasks, 0);
    vector<int> earlyStart(numTasks, 0);
    vector<int> earlyFinish(numTasks, 0);

    // Obliczanie stopni wejścia dla każdego zadania
    for (int i = 0; i < numTasks; i++) {
        for (int j = 0; j < numTasks; j++) {
            if (adjacencyMatrix[i][j] == 1) {
                inDegree[j]++;
            }
        }
    }

    // Kolejka do przechowywania zadań o zerowym stopniu wejścia
    queue<int> q;

    // Dodawanie zadań o zerowym stopniu wejścia do kolejki
    for (int i = 0; i < numTasks; i++) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }

    while (!q.empty()) {
        int task = q.front();
        q.pop();

        for (int i = 0; i < numTasks; i++) {
            if (adjacencyMatrix[task][i] == 1) {
                if (earlyFinish[task] + 1 > earlyStart[i]) {
                    earlyStart[i] = earlyFinish[task] + 1;
                }
                inDegree[i]--;
                if (inDegree[i] == 0) {
                    q.push(i);
                }
            }
        }
    }

    // Obliczanie czasu rozpoczęcia i zakończenia zadań
    int projectDuration = 0;
    vector<int> lateStart(numTasks, INT_MAX);
    vector<int> lateFinish(numTasks, INT_MAX);

    for (int i = 0; i < numTasks; i++) {
        lateFinish[i] = earlyStart[i];
        lateStart[i] = lateFinish[i] - 1;
    }

    // Wyszukiwanie zadań na ścieżce krytycznej
    cout << "Critical Path: ";
    for (int i = 0; i < numTasks; i++) {
        if (lateStart[i] == lateFinish[i]) {
            cout << i << " ";
        }
    }
    cout << endl;
}

int main() {
    int numTasks = 6;
    vector<vector<int>> adjacencyMatrix = {
        {0, 1, 1, 0, 0, 0},
        {0, 0, 0, 1, 1, 0},
        {0, 0, 0, 0, 0, 1},
        {0, 1, 0, 1, 0, 1},
        {0, 1, 0, 0, 0, 1},
        {0, 0, 0, 0, 0, 0}
    };

    calculateCriticalPath(adjacencyMatrix);

    return 0;
}
=======
#include<iostream>
#include<fstream>
#include<vector>
#include<unordered_map>
#include<algorithm>

using namespace std;

struct Node {
	int execution_time;
	int ls, lf, es, ef;
	vector<int> dependencies;
};

void load_data_matrix(int*** matrix, unordered_map<int, Node>& tasks) {
	fstream file("data80.txt", ios_base::in);
	int n_tasks, n_connections, execution_time, dependency, count = 0, task_nr = 0;
	file >> n_tasks >> n_connections;
	*matrix = new int* [n_connections];
	for (int i = 0; i < n_connections; i++)
		(*matrix)[i] = new int[n_connections];
	//wiersze skad, kolumny dokad
	for (int i = 0; i < n_connections; i++) {
		for (int j = 0; j < n_connections; j++) {
			(*matrix)[i][j] = 0;
		}
	}
	while (task_nr++ < n_tasks && file >> execution_time)
		tasks[task_nr] = Node{ execution_time };
	while (count++ < n_connections && file >> dependency >> task_nr)
		(*matrix)[dependency - 1][task_nr - 1] = 1;
}

void print_results(unordered_map<int, Node>& tasks, vector<int>& critical_path) {
	for (int i = 1; i < tasks.size() + 1; i++) {
		cout << tasks[i].es << ' ' << tasks[i].ef << ' '
			<< tasks[i].ls << ' ' << tasks[i].lf << endl;
	}
	cout << endl << "Critical Path" << endl; 
	sort(critical_path.begin(), critical_path.end(), [&](int a, int b) { return tasks[a].ef < tasks[b].ef; });
	for (int i = 0; i < critical_path.size(); i++) {
		cout << critical_path[i] << ' ' << tasks[critical_path[i]].es << ' ' << tasks[critical_path[i]].ef << endl;
	}
}

void solve_matrix() {
	int** matrix;
	unordered_map<int, Node> tasks;
	load_data_matrix(&matrix, tasks);
	for (int k = 0; k < tasks.size(); k++) {
		for (int i = 0; i < tasks.size(); i++) {
			for (int j = 0; j < tasks.size(); j++) {
				if (matrix[j][i])
					tasks[i + 1].es = max(tasks[i + 1].es, tasks[j + 1].ef);
			}
			tasks[i + 1].ef = tasks[i + 1].es + tasks[i + 1].execution_time;
		}
	}
	vector<pair<int, Node>> tasks_sorted(tasks.begin(), tasks.end());
	sort(tasks_sorted.begin(), tasks_sorted.end(), [](auto a, auto b) { return a.second.ef > b.second.ef; });
	vector<int> crital_path;
	for (auto&  [nr, task] : tasks_sorted) {
		bool last_task = true;
		for (int i = 0; i < tasks_sorted.size(); i++) {
			if (matrix[nr - 1][i]) {
				last_task = false;
				break;
			}
		}
		if (last_task) {
			tasks[nr].lf = (std::begin(tasks_sorted))->second.ef;
			tasks[nr].ls = tasks[nr].lf - tasks[nr].execution_time;
		}
		else {
			tasks[nr].lf = INT_MAX;
			tasks[nr].ls = INT_MAX;
		}
		for (int j = 0; j < tasks.size(); j++) {
			if (matrix[nr - 1][j])
				tasks[nr].lf = min(tasks[nr].lf, tasks[j + 1].ls);
		}
		tasks[nr].ls = tasks[nr].lf - tasks[nr].execution_time;
		if (tasks[nr].lf - tasks[nr].ef == 0)
			crital_path.push_back(nr);
	}
	print_results(tasks, crital_path);
	for (int i = 0; i < tasks.size(); i++)
		delete[] matrix[i];
	delete matrix;
}

int main(int argc, char** argv) {
	solve_matrix();
	//solve_list();
	return 0;
}
>>>>>>> c01153edeb5e7a607df96d7bb6affa7d722bf6fa
