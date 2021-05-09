# /* Routine for evaluating population members  */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"

# /* Routine to evaluate objective function values and constraints for a population */
def evaluate_pop(pop, globalvar):

    # int i;
    for i in range(globalvar.popsize):

        evaluate_ind(pop['ind'][i],globalvar)

    return;


# /* Routine to evaluate objective function values and constraints for an individual */
def evaluate_ind(ind, globalvar):

    # int j;
    # nsga2func(globalvar.nreal, globalvar.nbin, globalvar.nobj, globalvar.ncon,
               # ind['xreal'], ind['xbin'], ind['gene'], ind['obj'], ind['constr'])

    if globalvar.ncon == 0:

        ind['constr_violation'] = 0.0

    else:

        ind['constr_violation'] = 0.0;
        for j in range (globalvar.ncon):

            if ind['constr'][j] < 0.0 :

                ind['constr_violation'] += ind['constr'][j]



    return;

