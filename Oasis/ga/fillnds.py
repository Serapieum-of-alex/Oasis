# /* Nond-domination based selection routines */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"
import numpy as np
import Oasis.ga.list as ls
from Oasis.ga.dominance import check_dominance
from Oasis.ga.crowddist import assign_crowding_distance_indices, assign_crowding_distance_list
from Oasis.ga.merge import copy_ind
from Oasis.ga.sort import quicksort_dist
# /* Routine to perform non-dominated sorting */
def fill_nondominated_sort(mixed_pop, new_pop, globalvar):

    # int flag
    # int i, j
    # int end
    # int front_size
    # int archieve_size
    # int rank=1
    # list *pool
    # list *elite
    # list *temp1, *temp2
    # pool = (list *)malloc(sizeof(list))
    # elite = (list *)malloc(sizeof(list))
    rank = 1
    end = 0
    front_size = 0
    archieve_size = 0
    pool = dict()
    elite = dict()
    pool['index'] = -1
    pool['parent'] = None
    pool['child'] = None
    elite['index'] = -1
    elite['parent'] = None
    elite['child'] = None
    temp1 = pool

    for i in range(2*globalvar.popsize):

        ls.insert(temp1,i)
        temp1 = temp1['child']

    i = 0

    while archieve_size < globalvar.popsize :

        temp1 = pool['child']
        ls.insert(elite, temp1['index'])
        front_size = 1
        temp2 = elite['child']
        temp1 = ls.delnode (temp1)
        temp1 = temp1['child']

        while temp1 != None:

            temp2 = elite['child']
            if temp1==None :

                break

            while end != 1 and temp2 != None:

                end = 0
                flag = check_dominance(mixed_pop['ind'][temp1['index']], mixed_pop['ind'][temp2['index']], globalvar)
                if flag == 1 :
                    ls.insert(pool, temp2['index'])
                    temp2 = ls.delnode(temp2)
                    front_size = front_size - 1
                    temp2 = temp2['child']

                if flag == 0 :

                    temp2 = temp2['child']

                if flag == -1:

                    end = 1


            if flag == 0 or flag == 1:

                ls.insert (elite, temp1['index'])
                front_size = front_size + 1
                temp1 = ls.delnode (temp1)

            temp1 = temp1['child']



        temp2 = elite['child']
        j=i

        if archieve_size + front_size <= globalvar.popsize :

            while temp2 != None :
                copy_ind(mixed_pop['ind'][temp2['index']], new_pop['ind'][i], globalvar)
                new_pop['ind'][i].rank = rank
                archieve_size = archieve_size + 1
                temp2 = temp2['child']
                i = i + 1

            assign_crowding_distance_indices (new_pop, j, i-1, globalvar)

            rank = rank + 1

        else:

            crowding_fill(mixed_pop, new_pop, i, front_size, elite, globalvar)
            archieve_size = globalvar.popsize

            for j in range(globalvar.popsize) :

                new_pop['ind'][j].rank = rank

        temp2 = elite['child']

        while elite['child'] !=None:
            temp2 = ls.delnode(temp2)
            temp2 = temp2['child']



    # while (archieve_size < globalvar.popsize)

    while pool != None:

        temp1 = pool
        pool = pool['child']
        # free (temp1)

    while elite != None :

        temp1 = elite
        elite = elite['child']
        # free (temp1)

    return


# /* Routine to fill a population with individuals in the decreasing order of crowding distance */
def crowding_fill(mixed_pop, new_pop, count, front_size, elite, globalvar):

    # int *dist
    # list *temp
    # int i, j
    assign_crowding_distance_list(mixed_pop, elite['child'], front_size, globalvar)
    # dist = (int *)malloc(front_size*sizeof(int))
    dist = np.zeros(front_size, dtype=np.int32)
    temp = elite['child']
    for j in range(front_size):

        dist[j] = temp['index']
        temp = temp['child']

    quicksort_dist(mixed_pop, dist, front_size)
    for i in range(count, globalvar.popsize) :
        for j in range(front_size-1,0,-1):
            copy_ind(mixed_pop['ind'][dist[j]], new_pop['ind'][i], globalvar)

    # free (dist)
    return

