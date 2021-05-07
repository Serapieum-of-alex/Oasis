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
    - nvar
    - pcross_real
    - min_realvar
    - max_realvar
    - eta_c
    - nbin
    - nbits
"""

# from Oasis.ga.rand import random.uniform(0,1), rnd
import numpy as np
import random
from Oasis.ga.datastructure import Population

# define a value for machine precision
eps = 1.0  
while ((eps / 2.0 + 1.0) > 1.0):
    eps = eps / 2.0
eps = 2.0 * eps

class Crossover(Population):
    
    def __init__(self,Population, nrealcross, nbincross, eta_c, pcross_real):
        self.nrealcross = nrealcross
        self.nbincross = nbincross
        self.nvar = Population.nvar
        self.nbin = Population.nbin
        self.min_realvar = Population.min_realvar
        self.max_realvar = Population.max_realvar
        self.eta_c = eta_c
        self.pcross_real = pcross_real
        pass
    
    def Cross(self, parent1, parent2, child1, child2):
        # /* Function to cross two individuals */
    
        if self.nvar != 0 :
            child1, child2 = self.RealCross(parent1, parent2, child1, child2)
    
        if self.nbin != 0 :
            child1, child2 = self.BinCross(parent1, parent2, child1, child2)
    
        return child1, child2, self.nbincross
    
    
    def RealCross(self, parent1, parent2, child1, child2):
        # /* Routine for real variable SBX crossover */
    
        if  random.uniform(0,1) <= self.pcross_real :
            self.nrealcross = self.nrealcross + 1
    
            for i in range(0, self.nvar):
                if  random.uniform(0,1) <= 0.5 :
    
                    if  np.abs(parent1.xreal[i] - parent2.xreal[i]) > eps :
                        if  parent1.xreal[i] < parent2.xreal[i] :
                            y1 = parent1.xreal[i]
                            y2 = parent2.xreal[i]
                        else :
                            y1 = parent2.xreal[i]
                            y2 = parent1.xreal[i]
    
                        yl = self.min_realvar[i]
                        yu = self.max_realvar[i]
                        rand = random.uniform(0,1)
                        beta = 1.0 + (2.0*(y1-yl)/(y2-y1))
                        alpha = 2.0 - pow(beta,-(self.eta_c+1.0))
    
                        if rand <= (1.0/alpha):
                            betaq = pow((rand*alpha),(1.0/(self.eta_c+1.0)))
                        else:
                            betaq = pow ((1.0/(2.0 - rand*alpha)),(1.0/(self.eta_c+1.0)))
    
                        c1 = 0.5*((y1+y2)-betaq*(y2-y1))
                        beta = 1.0 + (2.0*(yu-y2)/(y2-y1))
                        alpha = 2.0 - pow(beta,-(self.eta_c+1.0))
    
                        if rand <= (1.0/alpha) :
                            betaq = pow ((rand*alpha),(1.0/(self.eta_c+1.0)))
                        else:
                            betaq = pow ((1.0/(2.0 - rand*alpha)),(1.0/(self.eta_c+1.0)))
    
                        c2 = 0.5*((y1+y2)+betaq*(y2-y1))
    
                        if c1 < yl :
                            c1 = yl
    
                        if  c2 < yl :
                            c2 = yl
    
                        if  c1 > yu :
                            c1 = yu
    
                        if  c2 > yu :
                            c2 = yu
    
                        if  random.uniform(0,1) <= 0.5 :
                            child1.xreal[i] = c2
                            child2.xreal[i] = c1
                        else :
                            child1.xreal[i] = c1
                            child2.xreal[i] = c2
                    else :
                        child1.xreal[i] = parent1.xreal[i]
                        child2.xreal[i] = parent2.xreal[i]
                else:
                    child1.xreal[i] = parent1.xreal[i]
                    child2.xreal[i] = parent2.xreal[i]
        else :
            for i in range(0, self.nvar):
                child1.xreal[i] = parent1.xreal[i]
                child2.xreal[i] = parent2.xreal[i]
    
        return child1, child2
    
    
    # /* Routine for two point binary crossover */
    def BinCross(self, parent1, parent2, child1, child2):
    
        for i in range(0, self.nbin):
            rand = random.uniform(0,1)
            if  rand <= self.pcross_bin :
                self.nbincross = self.nbincross +1
                site1 = random.uniform(0,self.nbits[i]-1)
                site2 = random.uniform(0,self.nbits[i]-1)
    
                if  site1 > site2 :
                    temp = site1
                    site1 = site2
                    site2 = temp
    
                for j in range(0, site1):
                    child1.gene[i][j] = parent1.gene[i][j]
                    child2.gene[i][j] = parent2.gene[i][j]
    
                for j in range(site1, site2):
                    child1.gene[i][j] = parent2.gene[i][j]
                    child2.gene[i][j] = parent1.gene[i][j]
    
                for j in range(site2, self.nbits[i]):
                    child1.gene[i][j] = parent1.gene[i][j]
                    child2.gene[i][j] = parent2.gene[i][j]
            else:
                for j in range(0, self.nbits[i]):
                    child1.gene[i][j] = parent1.gene[i][j]
                    child2.gene[i][j] = parent2.gene[i][j]
    
        return child1, child2
    
