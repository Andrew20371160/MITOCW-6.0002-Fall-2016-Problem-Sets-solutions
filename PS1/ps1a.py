###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
filename1=  'ps1_cow_data.txt'

filename2=  'ps1_cow_data_2.txt'
#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    file =open(filename,'r')
    line = file.readline()
    ret_dict = {}
    while line !='':
        name,weight = line.split(',')
        ret_dict[name] = int(weight)
        line =file.readline()
    return ret_dict
    file.close()
    return ret_dict

# Problem 2

def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    sorted_cows = sorted(cows.keys(),key =lambda x : cows[x],reverse = True)

    ret_trips = []
    while len(sorted_cows)>0:
        ret_trips.append([])

        trip_weight =  0 
        for cow in sorted_cows:
            if cows[cow]+trip_weight <=limit:
                ret_trips[-1].append(cow)
                trip_weight +=cows[cow]


        for cow in ret_trips[-1]:
            sorted_cows.remove(cow)

    return ret_trips


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    min_part_size = len(cows.keys())
    min_part =[]
    for part in get_partitions(cows):
        exceed_limit= False
        for trip in part:
            #for each trip check the cost
            trip_cost = 0
            for cow in trip:
                if cows[cow]+trip_cost >limit:
                    exceed_limit = True
                    break
                else:
                    trip_cost+=cows[cow]
            #for this trip if the limit was exceeded then get out of this partition
            if exceed_limit:
                break
        #after analying the partition if the limit wasn't exceeded then check number of trips
        if not exceed_limit:
            if len(part)<min_part_size:
                min_part_size= len(part)
                min_part= part[:]

    return min_part



# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    #cows_dicts = [{'Jesse':6, 'Maybel': 3, 'Callie': 2, 'Maggie': 5}]
    cows_dicts =[load_cows(filename1),load_cows(filename2)]

    for i in range(len(cows_dicts)):
        start = time.time()
        greed_cows =greedy_cow_transport(cows_dicts[i])
        end =time.time()
        time_taken = end -start
        print('Greed applied on file :',i+1)
        print('number of trips: ',len(greed_cows))
        print('time taken: ',time_taken)

        start = time.time()
        optimal_cows =brute_force_cow_transport(cows_dicts[i])
        end =time.time()
        time_taken = end -start
        print('optimal applied on file :',i+1)
        print('number of trips: ',len(optimal_cows))
        print('time taken: ',time_taken)
        

compare_cow_transport_algorithms()
