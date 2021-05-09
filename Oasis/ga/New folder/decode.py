# /* Routines to decode the population */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"
import numpy as np

# /* Function to decode a population to find out the binary variable values based on its bit pattern */
def decode_pop(pop, globalvar):


    if globalvar.nbin != 0:

        for i in range(globalvar.popsize):
            decode_ind((pop['ind'][i]), globalvar)


    return

# /* Function to decode an individual to find out the binary variable values based on its bit pattern */
def decode_ind (ind, globalvar):

    if globalvar.nbin != 0 :
        for j in range(globalvar.nbin):

            sumi = 0

            for k in range(globalvar.nbits[j]):
                if ind['gene'][j][k] == 1:

                    sumi = sumi + np.power(2,globalvar.nbits[j]-1-k);

            val1 = sumi*(globalvar.max_binvar[j] - globalvar.min_binvar[j])
            val2 = np.power(2,globalvar.nbits[j])-1

            ind['xbin'][j] = globalvar.min_binvar[j] + val1 / val2

    return

