import sys # used to handle command line arguments

# I figured the first thing that should be done is to store all the information about each task using an object
class Task:
    # stores the number, CPU usage, time, and dependencies (if any) of each task
    def __init__(self, num, cpu, time, rely):
        self.num = num
        self.cpu = cpu
        self.time = time
        self.rely = rely

    # defines a way to print a task in a readable form
    def __str__(self):
        if self.rely == "":
            return f"Task #{self.num} uses {self.cpu} CPUs in {self.time} time and relies on none."
        else:
            return f"Task #{self.num} uses {self.cpu} CPUs in {self.time} time and relies on {self.rely}."

independentTasks = [] # create a list to store the Task objects that do NOT rely on another
dependentTasks = [] # create a list to store the Task objects that do rely on another

# The next task I figured I should work on is reading the information from the input file
# This assumes that a valid file name is the last command line argument entered
with open(sys.argv[len(sys.argv) - 1]) as inFile: # there is no need to close the file when using with/as
    buffer = [] # since the file will be read line by line, this list is used to store information until a Task can be created
    for line in inFile: # loop through every line of inFile
        # check which piece of information the current line has, then add its numerical value into the buffer list
        if "TASK" in line:
            buffer.append("".join(d for d in line if d.isdigit()))
        elif "cpu" in line:
            buffer.append("".join(d for d in line if d.isdigit()))
        elif "time" in line:
            buffer.append("".join(d for d in line if d.isdigit()))
        elif "relies_on" in line:
            buffer.append("".join(d for d in line if d.isdigit()))
        # once the end of a task has been reached, create a Task object using the information in the buffer list
        # then, add the Task into the appropriate list (based on whether it has a dependency or not)
        elif "}" in line:
            # the last line of the file contains a "}" but no Task will be created because the buffer list will be empty
            # (the buffer list will be empty because the second-to-last line of the file also contains a "}")
            if len(buffer) == 3:
                independentTasks.append(Task(int(buffer[0]), int(buffer[1]), int(buffer[2]), ""))
            elif len(buffer) == 4:
                dependentTasks.append(Task(int(buffer[0]), int(buffer[1]), int(buffer[2]), int(buffer[3])))
            buffer.clear() # clear the buffer in order to prepare to read in the next task

# This code outputs the total runtime if all tasks were run in serial -- the total opposite of optimal
'''
serialTime = 0
for task in (independentTasks + dependentTasks):
    serialTime += task.time # accumulate the times of every single task
sys.stdout.write(str(serialTime))
'''

# One optimization that could be made is running any tasks that require 16 or fewer CPUs in parallel
# This is essentially an implementation of the bin packing problem and I will solve it using a greedy approach
# I recognize that other approaches (like branch and bound) may find a better solution, but they can be computationally expensive
# Also, for now I will assume that all tasks that rely on another task will run at the end in serial
BIN_CAPACITY = 16 # I used a constant so that the program can easily be changed if a computer with a different number of CPUs is used to run the tasks
independentTasks.sort(reverse=True, key=lambda task : task.cpu) # sorts the independent tasks by CPU usage from greatest to least
bins = [] # create a list to store the bins of tasks
for task in independentTasks: # loop through every task that has no dependency/-ies
    packed = False
    for i, bin in enumerate(bins): # loop through every bin
        # if the task can fit, add it to the bin
        if bin[0] + task.cpu <= BIN_CAPACITY:
            bins[i] = (bin[0] + task.cpu, bin[1] + [task])
            packed = True
            break
    # if the task can't be packed into an existing bin, create a new bin to pack it into
    if not packed:
        bins.append((task.cpu, [task]))

# A bin consists of a tuple whose first item is an int representing the total CPUs used by its Tasks
# and whose second item is a list containing the Tasks that comprise the bin
# This code prints out the contents of each bin in a readable format
'''
for i, bin in enumerate(bins):
    print(f"bin {i} uses {bin[0]} CPUs and contains:")
    for task in bin[1]:
        print(f"   > {task}")
'''

# This code outputs the total runtime if only independent tasks were packed into bins and all dependent tasks ran in serial

'''
singlyPackedTime = 0
for bin in bins:
    times = []
    for task in bin[1]:
        times.append(task.time)
    singlyPackedTime += max(times)
for dTask in dependentTasks:
    singlyPackedTime += dTask.time
sys.stdout.write(str(singlyPackedTime))
'''

# One additional optimization could be packing the dependent tasks into bins if their dependencies have already been run
# Granted, for the provided input files, the time savings would be minimal because there are few dependent tasks
dTasks = len(dependentTasks)
while dTasks > 1: # execute only when there are multiple dependent tasks that haven't been compared
    # store the task numbers of all dependent tasks
    dependentTaskNums = []
    for dTask in dependentTasks:
        dependentTaskNums.append(dTask.num)
    dependentTasks.sort(key=lambda task : task.cpu) # sorts the dependent tasks by CPU usage from least to greatest
    # create two pointers, one at either end of the dependentTasks list
    leftNum = 0
    rightNum = len(dependentTasks) - 1
    while leftNum < rightNum: # keep going until the two pointers meet
        # assign the pointers and calculate the total CPU usage
        left = dependentTasks[leftNum]
        right = dependentTasks[rightNum]
        sum = left.cpu + right.cpu
        # if the tasks can fit into a bin together and their dependencies have already been run, then...
        if sum <= BIN_CAPACITY and left.rely not in dependentTaskNums and right.rely not in dependentTaskNums:
            # ...pack them into a bin, remove them from the dependentTasks list, and adjust the counter accordingly
            bins.append((sum, [left, right]))
            dependentTasks.remove(left)
            dependentTasks.remove(right)
            dTasks -= 2
            break
        # if the tasks cannot fit into the same bin or a dependency has not been run, then...
        else:
            # ...move the left pointer onto the Task with the next greatest CPU usage and adjust the counter
            leftNum += 1
            dTasks -= 1
            # the dTasks counter prevents an infinite loop by keeping track of how many tasks can still be packed into a bin

# This code ouputs the total runtime after an attempt to pack all tasks into bins is made
binPackedTime = 0
for bin in bins:
    # for each bin, store the runtimes of its constituent tasks
    times = []
    for task in bin[1]:
        times.append(task.time)
    # add only the maximum of the runtimes (all other tasks run in parallel)
    binPackedTime += max(times)
for dTask in dependentTasks:
    # for each dependent task that is run at the end in serial, add onto the time
    binPackedTime += dTask.time
sys.stdout.write(str(binPackedTime)) # output the total time
