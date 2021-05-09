# /* Routines for storing population data into files */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"


def report_pop(pop, fpt, globalvar):
# /* Function to print the information of a population in a file */
    for i in range(globalvar.popsize):
        for j in range(globalvar.nobj):
            fpt.write("%e\t"%pop.Population[i].obj[j])

        if globalvar.ncon != 0 :
            for j in range(globalvar.ncon):
                fpt.write("%e\t"%pop.Population[i].constr[j])

        if globalvar.nvar != 0:
            for j in range(globalvar.nvar):
                fpt.write("%e\t"%pop.Population[i].xreal[j])

        if globalvar.nbin != 0:
            for j in range(globalvar.nbin):
                for k in range(globalvar.nbits[j]):
                    fpt.write("%d\t"%pop.Population[i].gene[j][k])

        fpt.write("%e\t"%pop.Population[i].constr_violation)
        fpt.write("%d\t"%pop.Population[i].rank)
        fpt.write("%e\n"%pop.Population[i].crowd_dist)

    return


def report_feasible(pop, fpt, globalvar):
# /* Function to print the information of feasible and non-dominated population in a file */

    for i in range(globalvar.popsize):
        if pop.Population[i].constr_violation == 0.0 and pop.Population[i].rank==1:

            for j in range(globalvar.nobj) :
                fpt.write("%e\t"%pop.Population[i].obj[j])

            if globalvar.ncon != 0 :
                for j in range(globalvar.ncon):
                    fpt.write("%e\t"%pop.Population[i].constr[j])


            if globalvar.nvar != 0:
                for j in range(globalvar.nvar):
                    fpt.write("%e\t"%pop.Population[i].xreal[j])

            if globalvar.nbin != 0 :
                for j in range(globalvar.nbin):
                    for k in range(globalvar.nbits[j]):
                        fpt.write("%d\t"%pop.Population[i].gene[j][k])

            fpt.write(fpt,"%e\t"%pop.Population[i].constr_violation)
            fpt.write(fpt,"%d\t"%pop.Population[i].rank)
            fpt.write(fpt,"%e\n"%pop.Population[i].crowd_dist)

    return

