# /* Tournamenet Selections routines */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"
import numpy as np
from Oasis.ga.rand import rnd, randomperc
from Oasis.ga.crossover import crossover
from Oasis.ga.dominance import check_dominance
# /* Routine for tournament selection, it creates a new_pop from old_pop by performing tournament selection and the crossover */
def selection(old_pop, new_pop, globalvar, nrealcross, nbincross):

    # int *a1, *a2
    # int temp
    # int i
    # int rand
    # individual *parent1, *parent2

    # a1 = (int *)malloc(globalvar.popsize*sizeof(int))
    # a2 = (int *)malloc(globalvar.popsize*sizeof(int))
    a1 = np.zeros(shepe=(globalvar.popsize), dtype=np.int32)
    a2 = np.zeros(shepe=(globalvar.popsize), dtype=np.int32)

    for i in range(globalvar.popsize) :

        a1[i] = a2[i] = i

    for i in range(globalvar.popsize):

        rand = rnd(i, globalvar.popsize-1)
        temp = a1[rand]
        a1[rand] = a1[i]
        a1[i] = temp
        rand = rnd(i, globalvar.popsize-1)
        temp = a2[rand]
        a2[rand] = a2[i]
        a2[i] = temp

    for i in range(0, globalvar.popsize, 4):

        parent1 = tournament(old_pop['ind'][a1[i]], old_pop['ind'][a1[i+1]], globalvar)
        parent2 = tournament(old_pop['ind'][a1[i+2]], old_pop['ind'][a1[i+3]], globalvar)
        crossover(parent1, parent2, new_pop['ind'][i], new_pop['ind'][i+1], globalvar, nrealcross, nbincross)
        parent1 = tournament (old_pop['ind'][a2[i]], old_pop['ind'][a2[i+1]], globalvar)
        parent2 = tournament (old_pop['ind'][a2[i+2]], old_pop['ind'][a2[i+3]], globalvar)
        crossover (parent1, parent2, new_pop['ind'][i+2], new_pop['ind'][i+3], globalvar, nrealcross, nbincross)

    # free (a1)
    # free (a2)
    return


# /* Routine for binary tournament */
def tournament(ind1, ind2, globalvar):

    # int flag
    flag = check_dominance(ind1, ind2, globalvar)
    if flag == 1:

        return ind1

    if flag == -1:

        return ind2

    if ind1['crowd_dist'] > ind2['crowd_dist']:

        return ind1

    if ind2['crowd_dist'] > ind1['crowd_dist']:

        return ind2

    if randomperc() <= 0.5:

        return ind1

    else:

        return ind2


