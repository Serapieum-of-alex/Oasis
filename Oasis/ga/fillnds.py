# Nond-domination based selection routines
import random
import numpy as np
from Oasis.ga.merge import copy_ind

from Oasis.ga.datastructure import Population
CheckDominance = Population.CheckDominance
AssignCrowdingDistancelist = Population.AssignCrowdingDistancelist
AssignCrowdingDistanceIndices = Population.AssignCrowdingDistanceIndices


def NonDominatedSort(mixed_pop, new_pop, globalvar):
# Routine to perform non-dominated sorting
    
    # int rank=1
    # list *pool
    # list *elite
    # list *temp1, *temp2
    rank = 1
    end = 0
    front_size = 0
    archieve_size = 0
    pool = dict(index = -1, parent=None, child=None) 
    elite = dict(index = -1, parent=None, child=None)    
    temp1 = pool
     
    for i in range(2*globalvar.popsize):
        temp1 = Population.Insert(temp1,i)
        temp1 = temp1['child']

    while archieve_size < globalvar.popsize :
        temp1 = pool['child']
        elite = Population.Insert(elite, temp1['index'])
        front_size = 1
        temp2 = elite['child']
        temp1 = Population.DelNode(temp1)
        temp1 = temp1['child']

        while temp1 != None:
            temp2 = elite['child']
            if temp1 == None :
                break

            while end != 1 and temp2 != None:
                end = 0
                try:
                    flag = CheckDominance(globalvar.nobj, 
                                      mixed_pop.Population[temp1['index']], 
                                      mixed_pop.Population[temp2['index']])
                except:
                    print('xxx')
                    
                if flag == 1 :
                    pool = Population.Insert(pool, temp2['index'])
                    temp2 = Population.DelNode(temp2)
                    front_size = front_size - 1
                    temp2 = temp2['child']

                if flag == 0 :
                    temp2 = temp2['child']

                if flag == -1:
                    end = 1

            if flag == 0 or flag == 1:
                elite = Population.Insert(elite, temp1['index'])
                front_size = front_size + 1
                temp1 = Population.DelNode(temp1)

            temp1 = temp1['child']
        temp2 = elite['child']
        
        j = i
        if archieve_size + front_size <= globalvar.popsize :
            while temp2 != None :
                new_pop.Population[i] = copy_ind(mixed_pop.Population[temp2['index']], 
                                                 new_pop.Population[i], globalvar)
                
                new_pop.Population[i].rank = rank
                archieve_size = archieve_size + 1
                temp2 = temp2['child']
                i = i + 1

            AssignCrowdingDistanceIndices(new_pop, j, i-1, globalvar)
            rank = rank + 1

        else:
            CrowdingFill(mixed_pop, new_pop, i, front_size, elite, globalvar)
            archieve_size = globalvar.popsize
            
            for j in range(globalvar.popsize) :
                new_pop.Population[j].rank = rank

        temp2 = elite['child']

        while elite['child'] !=None:
            temp2 = Population.DelNode(temp2)
            temp2 = temp2['child']

    while pool != None:
        temp1 = pool
        pool = pool['child']

    while elite != None :
        temp1 = elite
        elite = elite['child']

    return


def CrowdingFill(mixed_pop, new_pop, count, front_size, elite, globalvar):
    # Routine to fill a population with individuals in the decreasing order 
    # of crowding distance
  
    # int *dist
    # list *temp
    AssignCrowdingDistancelist(mixed_pop, elite['child'], front_size, globalvar)
    # dist = (int *)malloc(front_size*sizeof(int))
    dist = np.zeros(front_size, dtype=np.int32)
    temp = elite['child']
    
    for j in range(front_size):
        dist[j] = temp['index']
        temp = temp['child']

    quicksort_dist(mixed_pop, dist, front_size)
    for i in range(count, globalvar.popsize) :
        for j in range(front_size-1,0,-1):
            new_pop.Population[i] = copy_ind(mixed_pop.Population[dist[j]], 
                                             new_pop.Population[i], globalvar)

    return


def quicksort_front_obj(pop, objcount, obj_array, obj_array_size):
    # Randomized quick sort routine to sort a population based on a particular 
    # objective chosen
    
    q_sort_front_obj(pop, objcount, obj_array, 0, obj_array_size-1)
    return


def q_sort_front_obj(pop, objcount, obj_array, left, right) :
    # Actual implementation of the randomized quick sort used to sort a 
    # population based on a particular objective chosen
    if left < right:
        index = random.uniform(left, right)
        temp = obj_array[right]
        obj_array[right] = obj_array[index]
        obj_array[index] = temp
        pivot = pop.Population[obj_array[right]].obj[objcount]

        i = left-1
        for j in range(left,right):
            if (pop.Population[obj_array[j]].obj[objcount] <= pivot) :
                i = i + 1
                temp = obj_array[j]
                obj_array[j] = obj_array[i]
                obj_array[i] = temp

        index = i + 1
        temp = obj_array[index]
        obj_array[index] = obj_array[right]
        obj_array[right] = temp
        q_sort_front_obj(pop, objcount, obj_array, left, index-1)
        q_sort_front_obj(pop, objcount, obj_array, index+1, right)

    return


def quicksort_dist(pop, dist, front_size):
    # Randomized quick sort routine to sort a population based on crowding distance
    q_sort_dist (pop, dist, 0, front_size-1)
    return


def q_sort_dist(pop, dist, left, right):
    # Actual implementation of the randomized quick sort used to sort a population 
    # based on crowding distance
    
    if left<right:
        index = random.uniform(left, right)
        temp = dist[right]
        dist[right] = dist[index]
        dist[index] = temp
        pivot = pop.Population[dist[right]].crowd_dist
        i = left-1
        for j in range(left,right):
            if pop.Population[dist[j]].crowd_dist <= pivot:
                i = i + 1
                temp = dist[j]
                dist[j] = dist[i]
                dist[i] = temp

        index = i+1
        temp = dist[index]
        dist[index] = dist[right]
        dist[right] = temp
        q_sort_dist(pop, dist, left, index-1)
        q_sort_dist(pop, dist, index+1, right)

    return


