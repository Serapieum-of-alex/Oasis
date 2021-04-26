# /* Routine for mergeing two populations */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"

# /* Routine to merge two populations into one */
def merge(pop1, pop2, pop3, globalvar):

    # int i, k
    for i in range(globalvar.popsize):

        copy_ind((pop1['ind'][i]), (pop3['ind'][i]), globalvar)

    for i in range(globalvar.popsize):
        for k in range(globalvar.popsize):
            copy_ind((pop2['ind'][i]), (pop3['ind'][k]), globalvar)

    return


# /* Routine to copy an individual 'ind1' into another individual 'ind2' */
def copy_ind(ind1, ind2, globalvar):

    # int i, j
    ind2['rank'] = ind1['rank']
    ind2['constr_violation'] = ind1['constr_violation']
    ind2['crowd_dist'] = ind1['crowd_dist']
    if globalvar.nreal != 0 :

        for i in range(globalvar.nreal):

            ind2['xreal'][i] = ind1['xreal'][i]


    if globalvar.nbin !=0 :

        for i in range(globalvar.nbin):

            ind2['xbin'][i] = ind1['xbin'][i]

            for j in range(globalvar.nbits[i]):

                ind2['gene'][i][j] = ind1['gene'][i][j]



    for i in range(globalvar.nobj) :

        ind2['obj'][i] = ind1['obj'][i]

    if globalvar.ncon != 0 :

        for i in range(globalvar.ncon):

            ind2['constr'][i] = ind1['constr'][i]

    return

