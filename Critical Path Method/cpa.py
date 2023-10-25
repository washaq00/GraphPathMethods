import time

start_time = time.time()

with open('data70.txt', 'r') as file:
    lines = file.readlines()

# Extract times from 2 line
times = [int(num) for num in lines[1].split()]
times.append(0) #extra task with 0 duration

# Separate the pairs and the rest of the data and  transcrypt
dependencies_raw = [int(num) for num in lines[2].split()]
pairs_int = [(dependencies_raw[i], dependencies_raw[i + 1]) for i in range(0, len(dependencies_raw), 2)]
pairs = [[str(obj) for obj in pair] for pair in pairs_int]

tasks = dict()
number = 0

#initialization of tasks
for element in times:
    number += 1
    tasks['task'+ str(number)]= dict()
    tasks['task'+ str(number)]['id'] = number
    tasks['task'+ str(number)]['duration'] = element
    tasks['task'+ str(number)]['dependencies'] = ['-1']
    tasks['task'+ str(number)]['ES'] = 0
    tasks['task'+ str(number)]['EF'] = 0
    tasks['task'+ str(number)]['LS'] = 0
    tasks['task'+ str(number)]['LF'] = 0
    tasks['task'+ str(number)]['float'] = 0

#adding dependencies
for pair in pairs:
    tasks['task'+ str(pair[1])]['dependencies'].append(str(pair[0]))
    if '-1' in tasks['task'+ str(pair[1])]['dependencies']:
        del tasks['task'+ str(pair[1])]['dependencies'][0]

#Check where are no further depencies, write them to last task
del tasks['task'+ str(len(tasks.keys()))]['dependencies'][0] #delete '-1' from last task
for element in list(tasks.keys())[:-1]: #without last element
    check = False
    for element2 in tasks.keys():
        for dipendenza in tasks[element2]['dependencies']:
            if(int(dipendenza) == int(tasks[element]['id'])):
                check = True
    if(check==False):
        tasks['task'+ str(len(tasks.keys()))]['dependencies'].append(str(tasks[element]['id']))


for taskFW in tasks: #slides all the tasks
    if('-1' in tasks[taskFW]['dependencies']): #checks if it's the first task
        tasks[taskFW]['ES'] = 0
        tasks[taskFW]['EF'] = (tasks[taskFW]['duration'])
    else: #not the first task
        for k in tasks.keys():
            for dipendenza in tasks[k]['dependencies']: #slides all the dependency in a single task
                if(dipendenza != '-1' and len(tasks[k]['dependencies']) == 1): #if the task k has only one dependency
                    tasks[k]['ES'] = int(tasks['task'+ dipendenza]['EF'])
                    tasks[k]['EF'] = int(tasks[k]['ES']) + int(tasks[k]['duration'])
                elif(dipendenza !='-1'): #if the task k has more dependency
                    if(int(tasks['task'+dipendenza]['EF']) > int(tasks[k]['ES'])):
                        tasks[k]['ES'] = int(tasks['task'+ dipendenza]['EF'])
                        tasks[k]['EF'] = int(tasks[k]['ES']) + int(tasks[k]['duration'])

#sort by rising EF
sorted_tasks = sorted(tasks.items(), key=lambda x: x[1]['EF'])
#reverse list
bList = [task_name for task_name, _ in sorted_tasks[::-1]]

for taskBW in bList:
    if(bList.index(taskBW) == 0): #check if it's the last task (so no more task)
        tasks[taskBW]['LF']=tasks[taskBW]['EF'] 
        tasks[taskBW]['LS']=tasks[taskBW]['ES']
    for dipendenza in tasks[taskBW]['dependencies']: #slides all the dependency in a single task
        if(dipendenza != '-1'): #check if it's NOT the last task
            if(tasks['task'+ dipendenza]['LF'] == 0): #check if the the dependency is already analyzed
                tasks['task'+ dipendenza]['LF'] = int(tasks[taskBW]['LS'])
                tasks['task'+ dipendenza]['LS'] = int(tasks['task'+ dipendenza]['LF']) - int(tasks['task'+ dipendenza]['duration'])
                tasks['task'+ dipendenza]['float'] = int(tasks['task'+ dipendenza]['LF']) - int(tasks['task'+ dipendenza]['EF'])
            if(int(tasks['task'+ dipendenza]['LF']) >int(tasks[taskBW]['LS']) ): #put the minimun value of LF for the dependencies of a task
                tasks['task'+ dipendenza]['LF'] = int(tasks[taskBW]['LS'])
                tasks['task'+ dipendenza]['LS'] = int(tasks['task'+ dipendenza]['LF']) - int(tasks['task'+ dipendenza]['duration'])
                tasks['task'+ dipendenza]['float'] = int(tasks['task'+ dipendenza]['LF']) - int(tasks['task'+ dipendenza]['EF'])

end_time = time.time()
print("process time:")
print(tasks['task'+str(len(tasks))]['EF'])
print('\nES, EF, LS, LF, float')
for task in list(tasks.keys())[:-1]:
    print(str(tasks[task]['ES']) +', '+str(tasks[task]['EF']) +', '+str(tasks[task]['LS']) +', '+str(tasks[task]['LF']))
print("\nCritical path:")
for task_name, task_info in sorted_tasks[:-1]:
    if task_info['float'] == 0:
        print(f"{task_info['id']}, {task_info['LS']}, {task_info['LF']}")

elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time) 