# Mutation routines


import random
import numpy as np

class Mutation():
    
    def __init__(self, nrealmut, nbinmut, pmut_bin, nvar, min_realvar, 
                 max_realvar, eta_m, popsize, pmut_real, nbin):
        self.nrealmut = nrealmut
        self.nbinmut = nbinmut
        self.pmut_bin = pmut_bin
        self.nvar = nvar 
        self.min_realvar = min_realvar
        self.max_realvar = max_realvar
        self.eta_m = eta_m
        self.popsize = popsize
        self.pmut_real = pmut_real
        self.nbin = nbin
        pass
        
    def Mutate(self, pop):
        # /* Function to perform mutation in a population */
        for i in range(self.popsize):
            pop.Population[i] = self.MutationInd(pop.Population[i])
    
        return pop.Population, self.nrealmut
    
    
    def MutationInd(self, ind):
        # /* Function to perform mutation of an individual */
        if self.nvar != 0 :
            ind = self.MutateReal(ind)
    
        if self.nbin != 0 :
            ind = self.MutateBin(ind)
    
        return ind
    
    
    def MutateBin(self, ind):
    # /* Routine for binary mutation of an individual */
        
        for j in range(self.nbin) :
            for k in range(self.nbits[j]):
    
                prob = random.uniform(0,1)
                
                if prob <= self.pmut_bin :
                    if ind.gene[j,k] == 0 :
                        ind.gene[j,k] = 1
                    else:
                        ind.gene[j,k] = 0
                        
                    self.nbinmut = self.nbinmut + 1
    
        return ind
    
    
    # /* Routine for real polynomial mutation of an individual */
    def MutateReal(self, ind):
        
        for j in range(self.nvar) :
            if random.uniform(0,1) <= self.pmut_real :
                y = ind.xreal[j]
                yl = self.min_realvar[j]
                yu = self.max_realvar[j]
                delta1 = (y-yl)/(yu-yl)
                delta2 = (yu-y)/(yu-yl)
                rnd = random.uniform(0,1)
                mut_pow = 1.0/(self.eta_m + 1.0)
                
                if rnd <= 0.5:
                    xy = 1.0 - delta1
                    val = 2.0 * rnd + (1.0-2.0*rnd)*(np.power(xy,(self.eta_m + 1.0)))
                    deltaq =  np.power(val,mut_pow) - 1.0
                else:
                    xy = 1.0 - delta2
                    val = 2.0*(1.0-rnd) + 2.0*(rnd-0.5)*(pow(xy,(self.eta_m+1.0)))
                    deltaq = 1.0 - (pow(val,mut_pow))
    
                y = y + deltaq*(yu-yl)
                if y<yl:
                    y = yl
                if y>yu:
                    y = yu
                ind.xreal[j] = y
                self.nrealmut = self.nrealmut + 1
        
        return ind
    
