# /* Crowding distance computation routines */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"

import numpy as np
import Oasis.ga.sort as sort
INF = 1.0e14

# /* Routine to compute crowding distance based on ojbective function values when the population in in the form of a list */
def assign_crowding_distance_list(pop, lst, front_size, globalvar) : #, Global globalvar

    # int **obj_array
    # int *dist
    # int i, j
    # list *temp
    temp = lst

    if front_size==1:
        pop['ind'][lst['index']].crowd_dist = INF
        return

    if front_size==2:
        pop['ind'][lst['index']].crowd_dist = INF
        pop['ind']['lst']['child']['index'].crowd_dist = INF
        return

    obj_array = np.zeros(shap=(globalvar.nobj, front_size), dtype=np.int32)
    dist = np.zeros(shape=(front_size), dtype=np.int32)

    for j in range(front_size):
        dist[j] = temp['index']
        temp = temp['child']

    assign_crowding_distance(pop, dist, obj_array, front_size, globalvar)

    return


# /* Routine to compute crowding distance based on objective function values when the population in in the form of an array */
def assign_crowding_distance_indices(pop, c1, c2, globalvar):

    # int **obj_array


    front_size = c2 - c1 + 1

    if front_size == 1:
        pop['ind'][c1].crowd_dist = INF
        return

    if front_size == 2:

        pop['ind'][c1].crowd_dist = INF
        pop['ind'][c2].crowd_dist = INF
        return

    obj_array = np.zeros(shape=(globalvar.nobj, front_size), dtype=np.int32)
    dist = np.zeros(shape=(front_size), dtype=np.int32)


    for j in range(front_size):

        dist[j] = c1 + 1

    assign_crowding_distance (pop, dist, obj_array, front_size, globalvar)

    return


# /* Routine to compute crowding distances */
def assign_crowding_distance(pop, dist, obj_array, front_size, globalvar):


    for i in range(globalvar.nobj):
        for j in range(front_size):
            obj_array[i,j] = dist[j]

        sort.quicksort_front_obj(pop, i, obj_array[i], front_size)

    for j in range(front_size):
        pop['ind'][dist[j]].crowd_dist = 0.0

    for i in range(globalvar.nobj):
        pop['ind'][obj_array[i][0]].crowd_dist = INF

    for i in range(globalvar.nobj):
        for j in range(front_size-1):
            if pop['ind'][obj_array[i][j]].crowd_dist != INF:

                if pop['ind'][obj_array[i][front_size-1]].obj[i] == pop['ind'][obj_array[i][0]].obj[i]:

                    pop['ind'][obj_array[i][j]].crowd_dist += 0.0

                else:
                    val1 = pop['ind'][obj_array[i,j+1]].obj[i]
                    val2 = pop['ind'][obj_array[i,j-1]].obj[i]
                    val3 = pop['ind'][obj_array[i,front_size-1]].obj[i]
                    val4 = pop['ind'][obj_array[i,0]].obj[i]
                    pop['ind'][obj_array[i][j]].crowd_dist +=  (val1 - val2) /  (val3 - val4)


    for j in range(front_size):
        if pop['ind'][dist[j]].crowd_dist != INF:

            pop['ind'][dist[j]].crowd_dist = (pop['ind'][dist[j]].crowd_dist)/globalvar.nobj

    return

