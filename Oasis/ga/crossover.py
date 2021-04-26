# /* Crossover routines */

"""
parent1 :  [struct] >>>> dict
    - xreal : [array]

parent2 :  [struct]
    - xreal : [array]
child1  :  [struct]
    - xreal : [array]
    - gene : [2D array]
globalvar : [global variable struct]
    - nreal
    - pcross_real
    - min_realvar
    - max_realvar
    - eta_c
    - nbin
    - nbits
"""

from Oasis.ga.rand import randomperc, rnd
import numpy as np


eps = 1.0  # define a value for machine precision
while ((eps / 2.0 + 1.0) > 1.0):
    eps = eps / 2.0

eps = 2.0 * eps

# /* Function to cross two individuals */
def crossover(parent1, parent2, child1, child2, globalvar, nrealcross, nbincross):

    if  globalvar.nreal != 0 :

        realcross (parent1, parent2, child1, child2, globalvar, nrealcross)

    if  globalvar.nbin != 0 :

        bincross (parent1, parent2, child1, child2, globalvar, nbincross)

    return


# /* Routine for real variable SBX crossover */
def realcross(parent1, parent2, child1, child2, globalvar, nrealcross):

    if  randomperc() <= globalvar.pcross_real :
        nrealcross = nrealcross + 1

        for i in range(0, globalvar.nreal + 1):

            if  randomperc()<=0.5 :

                if  np.abs(parent1['xreal'][i] - parent2['xreal'][i]) > eps :

                    if  parent1['xreal'][i] < parent2['xreal'][i] :

                        y1 = parent1['xreal'][i]
                        y2 = parent2['xreal'][i]
                    else :
                        y1 = parent2['xreal'][i]
                        y2 = parent1['xreal'][i]

                    yl = globalvar.min_realvar[i]
                    yu = globalvar.max_realvar[i]
                    rand = randomperc()
                    beta = 1.0 + (2.0*(y1-yl)/(y2-y1))
                    alpha = 2.0 - pow(beta,-(globalvar.eta_c+1.0))

                    if rand <= (1.0/alpha):

                        betaq = pow((rand*alpha),(1.0/(globalvar.eta_c+1.0)))

                    else:
                        betaq = pow ((1.0/(2.0 - rand*alpha)),(1.0/(globalvar.eta_c+1.0)))

                    c1 = 0.5*((y1+y2)-betaq*(y2-y1))
                    beta = 1.0 + (2.0*(yu-y2)/(y2-y1))
                    alpha = 2.0 - pow(beta,-(globalvar.eta_c+1.0))

                    if  rand <= (1.0/alpha) :

                        betaq = pow ((rand*alpha),(1.0/(globalvar.eta_c+1.0)))

                    else:

                        betaq = pow ((1.0/(2.0 - rand*alpha)),(1.0/(globalvar.eta_c+1.0)))

                    c2 = 0.5*((y1+y2)+betaq*(y2-y1))

                    if c1 < yl :
                        c1 = yl

                    if  c2 < yl :
                        c2 = yl

                    if  c1 > yu :
                        c1 = yu

                    if  c2 > yu :
                        c2 = yu

                    if  randomperc() <= 0.5 :

                        child1['xreal'][i] = c2
                        child2['xreal'][i] = c1
                    else :
                        child1['xreal'][i] = c1
                        child2['xreal'][i] = c2

                else :

                    child1['xreal'][i] = parent1['xreal'][i]
                    child2['xreal'][i] = parent2['xreal'][i]

            else:
                child1['xreal'][i] = parent1['xreal'][i]
                child2['xreal'][i] = parent2['xreal'][i]
    else :

        for i in range(0, globalvar.nreal+1):

            child1['xreal'][i] = parent1['xreal'][i]
            child2['xreal'][i] = parent2['xreal'][i]

    return


# /* Routine for two point binary crossover */
def bincross (parent1, parent2, child1, child2, globalvar, nbincross):

    for i in range(0, globalvar.nbin+1):

        rand = randomperc()
        if  rand <= globalvar.pcross_bin :
            nbincross = nbincross +1

            site1 = rnd(0,globalvar.nbits[i]-1)
            site2 = rnd(0,globalvar.nbits[i]-1)

            if  site1 > site2 :
                temp = site1
                site1 = site2
                site2 = temp

            for j in range(0, site1+1):

                child1['gene'][i][j] = parent1['gene'][i][j]
                child2['gene'][i][j] = parent2['gene'][i][j]

            for j in range(site1, site2+1):

                child1['gene'][i][j] = parent2['gene'][i][j]
                child2['gene'][i][j] = parent1['gene'][i][j]

            for j in range(site2, globalvar.nbits[i]+1):

                child1['gene'][i][j] = parent1['gene'][i][j]
                child2['gene'][i][j] = parent2['gene'][i][j]

        else:

            for j in range(0, globalvar.nbits[i]+1):

                child1['gene'][i][j] = parent1['gene'][i][j]
                child2['gene'][i][j] = parent2['gene'][i][j]

    return

