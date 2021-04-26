# /* Mutation routines */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"
import numpy as np
from Oasis.ga.rand import randomperc
# /* Function to perform mutation in a population */
def mutation_pop(pop, globalvar,nrealmut,nbinmut):

    # int i
    for i in range(globalvar.popsize):

        mutation_ind((pop['ind'][i]),globalvar,nrealmut,nbinmut)

    return


# /* Function to perform mutation of an individual */
def mutation_ind(ind, globalvar,nrealmut,nbinmut):

    if globalvar.nreal != 0 :

        real_mutate_ind(ind, globalvar, nrealmut)

    if globalvar.nbin != 0 :

        bin_mutate_ind(ind, globalvar, nbinmut)

    return


# /* Routine for binary mutation of an individual */
def bin_mutate_ind(ind, globalvar,nbinmut):

    # int j, k
    # double prob
    for j in range(globalvar.nbin) :

        for k in range(globalvar.nbits[j]):

            prob = randomperc()
            if prob['globalvar'].pmut_bin :

                if ind['gene'][j][k] == 0 :

                    ind['gene'][j][k] = 1

                else:

                    ind['gene'][j][k] = 0

                nbinmut = nbinmut + 1

    return


# /* Routine for real polynomial mutation of an individual */
def real_mutate_ind(ind, globalvar,nrealmut):

    # int j
    # double rnd, delta1, delta2, mut_pow, deltaq
    # double y, yl, yu, val, xy
    for j in range(globalvar.nreal) :

        if randomperc() <= globalvar.pmut_real :

            y = ind['xreal'][j]
            yl = globalvar.min_realvar[j]
            yu = globalvar.max_realvar[j]
            delta1 = (y-yl)/(yu-yl)
            delta2 = (yu-y)/(yu-yl)
            rnd = randomperc()
            mut_pow = 1.0/(globalvar.eta_m + 1.0)
            if rnd <= 0.5:

                xy = 1.0 - delta1
                val = 2.0 * rnd + (1.0-2.0*rnd)*(np.power(xy,(globalvar.eta_m + 1.0)))
                deltaq =  np.power(val,mut_pow) - 1.0

            else:
                xy = 1.0 - delta2
                val = 2.0*(1.0-rnd)+2.0*(rnd-0.5)*(pow(xy,(globalvar.eta_m+1.0)))
                deltaq = 1.0 - (pow(val,mut_pow))

            y = y + deltaq*(yu-yl)
            if y<yl:
                y = yl
            if y>yu:
                y = yu
            ind['xreal'][j] = y
            nrealmut+=1


    return

