# Routines for randomized recursive quick-sort
import random

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

