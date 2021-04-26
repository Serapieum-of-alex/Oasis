# /* Routines for storing population data into files */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"

# /* Function to print the information of a population in a file */
def report_pop(pop, fpt, globalvar):

    # int i, j, k
    for i in range(globalvar.popsize):
        for j in range(globalvar.nobj):

            fpt.write("%e\t",pop['ind'][i].obj[j])

        if globalvar.ncon != 0 :

            for j in range(globalvar.ncon):

                fpt.write("%e\t",pop['ind'][i].constr[j])


        if globalvar.nreal != 0:

            for j in range(globalvar.nreal):

                fpt.write("%e\t",pop['ind'][i].xreal[j])


        if globalvar.nbin != 0:

            for j in range(globalvar.nbin):

                for k in range(globalvar.nbits[j]):

                    fpt.write("%d\t",pop['ind'][i].gene[j][k])

        fpt.write("%e\t",pop['ind'][i].constr_violation)
        fpt.write("%d\t",pop['ind'][i].rank)
        fpt.write("%e\n",pop['ind'][i].crowd_dist)

    return


# /* Function to print the information of feasible and non-dominated population in a file */
def report_feasible (pop, fpt, globalvar):

    # int i, j, k
    for i in range(globalvar.popsize):

        if pop['ind'][i].constr_violation == 0.0 and pop['ind'][i].rank==1:

            for j in range(globalvar.nobj) :

                fpt.write("%e\t",pop['ind'][i].obj[j])

            if globalvar.ncon != 0 :

                for j in range(globalvar.ncon):

                    fpt.write("%e\t",pop['ind'][i].constr[j])


            if globalvar.nreal != 0:

                for j in range(globalvar.nreal):

                    fpt.write("%e\t",pop['ind'][i].xreal[j])


            if globalvar.nbin != 0 :

                for j in range(globalvar.nbin):

                    for k in range(globalvar.nbits[j]):

                        fpt.write("%d\t",pop['ind'][i].gene[j][k])

            fpt.write(fpt,"%e\t",pop['ind'][i].constr_violation)
            fpt.write(fpt,"%d\t",pop['ind'][i].rank)
            fpt.write(fpt,"%e\n",pop['ind'][i].crowd_dist)

    return

