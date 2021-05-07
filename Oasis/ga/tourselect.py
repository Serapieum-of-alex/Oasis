# Tournamenet Selections routines

import random
import numpy as np
from Oasis.ga.crossover import Crossover
from Oasis.ga.datastructure import Population
CheckDominance = Population.CheckDominance

class Selection():
    
    def __init__(self, nrealcross, nbincross, eta_c, pcross_real, popsize, nobj):
        self.nrealcross = nrealcross
        self.nbincross = nbincross
        self.eta_c = eta_c
        self.pcross_real = pcross_real
        self.popsize = popsize
        self.nobj = nobj
        pass
    
    def Select(self, old_pop, new_pop):
        # Routine for tournament selection, it creates a new_pop from old_pop 
        # by performing tournament selection and the crossover
        # int *a1, *a2
        # individual *parent1, *parent2
        
        a1 = np.zeros(self.popsize, dtype=np.int32)
        a2 = np.zeros(self.popsize, dtype=np.int32)
    
        for i in range(self.popsize) :
            a1[i] = a2[i] = i
    
        for i in range(self.popsize):
            rand = random.randint(i, self.popsize-1)
            temp = a1[rand]
            a1[rand] = a1[i]
            a1[i] = temp
            rand = random.randint(i, self.popsize-1)
            temp = a2[rand]
            a2[rand] = a2[i]
            a2[i] = temp
        
        CO = Crossover(old_pop, self.nrealcross, self.nbincross, self.eta_c, self.pcross_real)
        
        for i in range(0, self.popsize, 4):
            parent1 = self.tournament(old_pop.Population[a1[i]], old_pop.Population[a1[i+1]], self.nobj)
            parent2 = self.tournament(old_pop.Population[a1[i+2]], old_pop.Population[a1[i+3]], self.nobj)
            new_pop.Population[i], new_pop.Population[i+1], self.nbincross = CO.Cross(parent1, parent2, 
                                                                      new_pop.Population[i], new_pop.Population[i+1])
            
            parent1 = self.tournament(old_pop.Population[a2[i]], old_pop.Population[a2[i+1]], self.nobj)
            parent2 = self.tournament(old_pop.Population[a2[i+2]], old_pop.Population[a2[i+3]], self.nobj)
            new_pop.Population[i+2], new_pop.Population[i+3], self.nbincross = CO.Cross(parent1, parent2, 
                                                                        new_pop.Population[i+2], new_pop.Population[i+3])
    
        return new_pop.Population, self.nbincross
    
    
    def tournament(self, ind1, ind2, nobj):
        # Routine for binary tournament
    
        flag = CheckDominance(nobj, ind1, ind2)
        if flag == 1:
            return ind1
    
        if flag == -1:
            return ind2
    
        if ind1.crowd_dist > ind2.crowd_dist:
            return ind1
    
        if ind2.crowd_dist > ind1.crowd_dist:
            return ind2
    
        if random.uniform(0,1) <= 0.5:
            return ind1
        else:
            return ind2
    