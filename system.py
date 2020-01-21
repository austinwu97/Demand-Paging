import sys

#Class for each process
class Process():

    def __init__(self, A, B, C, num_references, size, reference):
        self.finished = False
        self.A = A
        self.B = B
        self.C = C
        self.D = float((1-A-B-C)) / float(size)
        self.num_faults = 0
        self.residency_time = 0.0
        self.num_eviction = 0
        self.references_left = num_references
        self.reference = (111 * reference) % size

#function used to run LRU, FIFO, and RANDOM
def run(processes, size, page_size, random_nums, frame_table, R):

    processes = processes #keep track of all the processes
    method = R #LRU, FIFO, RANDOM
    size = size
    page_size = page_size
    random_nums = random_nums
    frame_table = frame_table
    completed_processes_counter = 0
    num_faults = 0
    num_evictions = 0
    residency = 0.0
    in_table = False
    temp_counter = -1
    current_time = 0
    index = 0

    while(completed_processes_counter != len(processes)):
        for i in range(3):
            current_time += 1
            processes[index].references_left -= 1

            # Check if the process is in the frame table
            temp_page = processes[index].reference/page_size
            for k in range(len(frame_table) - 1, -1, -1):
                # Page is found in the frame table
                if (frame_table[k][1] == index and frame_table[k][0] == temp_page):
                    in_table = True
                    frame_table[k][3] = current_time
                    break #no need to continue

                elif (frame_table[k][1] == -1):
                    if (temp_counter < 0):
                        temp_counter = k

            #page not in the table
            if (in_table == False):
                processes[index].num_faults += 1

                if (temp_counter >= 0):
                    fixed = []
                    fixed.append(processes[index].reference / page_size)
                    fixed.append(index)
                    fixed.append(current_time)
                    fixed.append(current_time)
                    del frame_table[temp_counter]
                    frame_table.insert(temp_counter, fixed)
                    temp_counter = -1

                else:
                    # Determine which method to use
                    if (method == "lru"):
                        lru = frame_table[len(frame_table)-1][3]
                        temp_index = len(frame_table)-1
                        for j in range(len(frame_table)-1, -1, -1):
                            if(frame_table[j][3] < lru):
                                lru = frame_table[j][3]
                                temp_index = j

                        # calculating residency time
                        evicted_process_index = frame_table[temp_index][1]
                        processes[evicted_process_index].residency_time += current_time - frame_table[temp_index][2]
                        processes[evicted_process_index].num_eviction += 1

                        # put into frame
                        temp = []
                        temp.append(processes[index].reference / page_size)
                        temp.append(index)
                        temp.append(current_time)
                        temp.append(current_time)
                        del frame_table[temp_index]
                        frame_table.insert(temp_index, temp)

                    elif (method == "fifo"):
                        fifo = frame_table[len(frame_table)-1][2]
                        temp_index = len(frame_table) - 1
                        for j in range(len(frame_table) - 1, -1, -1):
                            if (frame_table[j][2] < fifo):
                                fifo = frame_table[j][2]
                                temp_index = j

                        # calculating residency time
                        evicted_process_index = frame_table[temp_index][1]
                        processes[evicted_process_index].residency_time += current_time - frame_table[temp_index][2]
                        processes[evicted_process_index].num_eviction += 1

                        # put into frame
                        temp = []
                        temp.append(processes[index].reference / page_size)
                        temp.append(index)
                        temp.append(current_time)
                        temp.append(current_time)
                        del frame_table[temp_index]
                        frame_table.insert(temp_index, temp)

                    else: #random
                        #select random frame to evict
                        random_index = int(random_nums.next())
                        temp_index = random_index % len(frame_table)
                        evicted_process_index = frame_table[temp_index][1]

                        #calculating residency time
                        processes[evicted_process_index].residency_time += current_time - frame_table[temp_index][2]
                        processes[evicted_process_index].num_eviction += 1

                        #put into frame
                        temp = []
                        temp.append(processes[index].reference / page_size)
                        temp.append(index)
                        temp.append(current_time)
                        temp.append(current_time)
                        del frame_table[temp_index]
                        frame_table.insert(temp_index, temp)





            in_table = False #reset

            #calculate next reference
            randomNum = float(random_nums.next())
            y = (randomNum / float(2147483648))

            if (y < processes[index].A):
                processes[index].reference = (processes[index].reference + 1) % size

            elif (y < processes[index].A + processes[index].B):
                processes[index].reference = (processes[index].reference - 5) % size

            elif(y < processes[index].A + processes[index].B + processes[index].C):
                processes[index].reference = (processes[index].reference + 4) % size

            else:
                randomNum = float(random_nums.next())
                processes[index].reference = randomNum % size

            #Check if process is finished simulating
            if (processes[index].references_left == 0):
                processes[index].finished = True
                completed_processes_counter += 1
                break

        if (index == len(processes) - 1):
            index = 0 #reset back to the first process
        else:
            index += 1

    #print the results
    for i in range (len(processes)):
        num_faults += processes[i].num_faults

        if (processes[i].num_eviction == 0):
            print("Process " + str((i+1)) + " had " + str(processes[i].num_faults) + " faults")
            print("No average residence applicable")

        else:
            num_evictions += processes[i].num_eviction
            residency += processes[i].residency_time
            average_residency = float(processes[i].residency_time)/float(processes[i].num_eviction)
            print("Process " + str((i+1)) + " had " + str(processes[i].num_faults) + " faults and " + str(average_residency) + " average residency")

    if (num_evictions > 0):
        print("The total number of faults is " + str(num_faults) + " and the overall average residency is " + str(residency/num_evictions))

    else:
        print("The total number of faults is " + str(num_faults))
        print("No evictions, no overall average residency is applicable")


#function used to make the frame table
def makeTable(table_size):

    frame_table = []
    for i in range(table_size):
        frame_table.append(None)

    columns = []
    for j in range(4):
        columns.append(-1)

    for i in range (len(frame_table)):
        frame_table[i] = columns

    return frame_table

if __name__ == "__main__":

    #take in the user input, make sure there are 7 parameters
    if (len(sys.argv) != 7):
        print("Incorrect input, please try again (do not input the last 0 as extra last argument)")
        exit()

    M = int(sys.argv[1]) # machine size
    P = int(sys.argv[2]) # page size
    S = int(sys.argv[3]) # size of each process
    J = int(sys.argv[4]) # job mix
    N = int(sys.argv[5]) # number of references
    R = str(sys.argv[6]) # replacement algorithm

    random_num_file = open("random-numbers.txt", "r")
    table_size = M/P
    processes = [] #list to keep track of all the processes


    print("The machine size is: " + str(M))
    print("The page size is : " + str(P))
    print("The process size is: " + str(S))
    print("The job mix number is " + str(J))
    print("The number of references per process is: " + str(N))
    print("The replacement algorithm is: " + R)
    print("\n")

    #Make processes and add to the list of processes depending on the job mix
    if (J == 1):
        processes.append(Process(1,0,0,N,S,1))

    elif (J == 2):
        processes.append(Process(1,0,0,N,S,1))
        processes.append(Process(1,0,0,N,S,2))
        processes.append(Process(1,0,0,N,S,3))
        processes.append(Process(1,0,0,N,S,4))

    elif (J == 3):
        processes.append(Process(0, 0, 0, N, S, 1))
        processes.append(Process(0, 0, 0, N, S, 2))
        processes.append(Process(0, 0, 0, N, S, 3))
        processes.append(Process(0, 0, 0, N, S, 4))

    else:
        processes.append(Process(0.75, 0.25, 0, N, S, 1))
        processes.append(Process(0.75, 0, 0.25, N, S, 2))
        processes.append(Process(0.75, 0.125, 0.125, N, S, 3))
        processes.append(Process(0.5, 0.125, 0.125, N, S, 4))

    #Run the process and pass which algorithm should be used
    frame_table = makeTable(table_size)
    if (R != "lru" and R != "fifo" and R != "random"):
        print("Incorrect specified algorithm")
        exit()
    else:
        run(processes, S, P, random_num_file, frame_table, R)

