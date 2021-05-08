"""
-------------------------------------------------------------------------------
 *
 * NSGA-II (Non-dominated Sorting Genetic Algorithm - II)
 *
 *  current version only works with continous design variables treated as reals
 *  no provisions for binary specification or integer/discrete variable handling
 *
 *  nvar - number of variables
 *  ncon - number of constraints
 *  nobj - number of objectives
 *  f -
 *  x -
 *  g -
 *  nfeval -
 *  xl -
 *  xu -
 *  popsize - population size (a multiple of 4)
 *  ngen    - number of generations
 *  pcross_real - probability of crossover of real variable (0.6-1.0)
 *  pmut_real   - probablity of mutation of real variables (1/nvar)
 *  eta_c - distribution index for crossover (5-20) must be > 0
 *  eta_m - distribution index for mutation (5-50) must be > 0
 *  pcross_bin - probability of crossover of binary variable (0.6-1.0)
 *  pmut_bin - probability of mutation of binary variables (1/nbits)
 *  seed    - seed value must be in (0,1)
 *
 *
 *  Output files
 *
 *  - initial_pop.out: contains initial population data
 *  - final_pop.out: contains final population data
 *  - all_pop.out: containts generation population data
 *  - best_pop.out: contains best solutions
 *  - params.out: contains input parameters information
 *  -   .out: contains runtime information
 *
"""
INF = 1.0e14

import time
import numpy as np
import sys
import random #, time
# from Oasis.ga.rand import randomize
from Oasis.ga.tourselect import Selection
from Oasis.ga.mutation import Mutation
from Oasis.ga.merge import merge
from Oasis.ga.fillnds import NonDominatedSort
from Oasis.ga.datastructure import Population 
# from Oasis.ga.rand import randomperc#, rndreal



class NSGA2():
    """
        

    Parameters
    ----------
    nvar : TYPE
        DESCRIPTION.
    ncon : TYPE
        DESCRIPTION.
    nobj : TYPE
        DESCRIPTION.
    xl : TYPE
        DESCRIPTION.
    xu : TYPE
        DESCRIPTION.
    popsize : TYPE
        DESCRIPTION.
    ngen : TYPE
        DESCRIPTION.
    pcross_real : TYPE
        DESCRIPTION.
    pmut_real : TYPE
        DESCRIPTION.
    eta_c : TYPE
        DESCRIPTION.
    eta_m : TYPE
        DESCRIPTION.
    pcross_bin : TYPE
        DESCRIPTION.
    pmut_bin : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    def __init__(self, nvar, ncon, nobj, xl, xu, popsize, ngen, pcross_real,
                 pmut_real, eta_c, eta_m,pcross_bin,pmut_bin,objconfunc):
        
        # number of real variables
        self.nvar = nvar
        self.nobj = nobj
        self.ncon = ncon
        self.popsize = popsize
        # Probability of crossover of real variable
        self.pcross_real = pcross_real
        # Probability of crossover of binary variable
        self.pcross_bin = pcross_bin
        # Probability of mutation of real variable
        self.pmut_real = pmut_real
        # # Probability of mutation of binary variable
        self.pmut_bin = pmut_bin
        # Distribution index for crossover
        self.eta_c = eta_c
        # Distribution index for mutation
        self.eta_m = eta_m
        self.ngen = ngen
        
        # number of binary variables
        self.nbin = 0
        
        # Lower limit of real variable
        self.min_realvar = np.zeros(nvar, dtype=np.float32)
        # upper limit of real variable
        self.max_realvar = np.zeros(nvar, dtype=np.float32)
        
        for i in range(nvar):
            self.min_realvar[i] = xl[i]
            self.max_realvar[i] = xu[i]
        
        if self.nbin != 0 :            
            # Number of bits for binary variable
            self.nbits = np.zeros(self.nbin, dtype=np.int32)
            # Lower limit of binary variable
            self.min_binvar = np.zeros(self.nbin, dtype=np.float32)
            # upper limit of binary variable
            self.max_binvar = np.zeros(self.nbin, dtype=np.float32)
        
        self.bitlength = 0
        if self.nbin != 0 :
            for i in range(self.nbin):
                self.bitlength = self.bitlength + self.nbits[i]
        
        self.objconfunc = objconfunc
        
        pass


    def nsga2(self, f, x, g, nfeval, printout, seed, xinit):
        """
        

        Parameters
        ----------
        f : TYPE
            DESCRIPTION.
        x : TYPE
            DESCRIPTION.
        g : TYPE
            DESCRIPTION.
        nfeval : TYPE
            DESCRIPTION.
        printout : TYPE
            DESCRIPTION.
        seed : TYPE
            DESCRIPTION.
        xinit : TYPE
            DESCRIPTION.

        Returns
        -------
        int
            DESCRIPTION.

        """
        

        # random numbers seed
        if seed == 0 :
            #use of clock to generate "random" seed
            # time_t seconds
            # seconds = time(NULL)
            rand = random.Random()
            if seed == {} :
                rseed = time.time()
            rand.seed(rseed)

        if printout == 2 :
            fpt1, fpt2, fpt3, fpt4, fpt5, fpt6 = self.Files(printout, seed)
        else:
            fpt1, fpt2, fpt3, fpt5, fpt6 = self.Files(printout, seed)
        
        self.nbinmut = 0
        self.nrealmut = 0
        self.nbincross = 0
        self.nrealcross = 0
        
        
        if self.nbin != 0 :
            self.ParentPop = Population(self.nvar, self.nobj, self.min_realvar, 
                                        self.max_realvar, self.ncon, self.nbin, 
                                        self.nbits)
            self.ChildPop = Population(self.nvar, self.nobj, self.min_realvar, 
                                        self.max_binvar, self.ncon, self.nbin, 
                                        self.nbits)
            self.OffSprings = Population(self.nvar, self.nobj, self.min_realvar, 
                                        self.max_binvar, self.ncon, self.nbin, 
                                        self.nbits)
        else:
            self.ParentPop = Population(self.nvar, self.nobj, self.min_realvar, 
                                        self.max_realvar, self.ncon)
            self.ChildPop = Population(self.nvar, self.nobj, self.min_realvar, 
                                       self.max_realvar, self.ncon)
            self.OffSprings = Population(self.nvar, self.nobj, self.min_realvar, 
                                         self.max_realvar, self.ncon)
            
        self.ParentPop.Create(self.popsize)
        self.ChildPop.Create(self.popsize)
        self.OffSprings.Create(self.popsize)
        
        # oldrand, jrand = randomize(seed)
        
        self.ParentPop.Initialize()

        if xinit != 0 :
          i=0
          for j in range(self.nvar) :
              # xreal for the first individual
              self.ParentPop.Population[i].xreal[j] = x[j]

        # First Generation
        if printout >= 1 :
            fpt6.writelines("\n\n Initialization done, now performing first generation")

        self.ParentPop.Decode()
        res = self.ParentPop.Evaluate(self.objconfunc)
        nfeval = nfeval + 1
        
        # if res :
            # return 1
        
        self.ParentPop.AssignRankCrowdingDistance()

        if printout >= 1 :
            self.ParentPop.Report(fpt1)
            if printout == 2 :
                fpt4.writelines("# gen = 1\n")
                self.ParentPop.Report(fpt4)

            fpt6.writelines("\n gen = 1")
            fpt1.flush()
            fpt2.flush()
            fpt3.flush()

            if printout == 2 :
                fpt4.flush()

            fpt5.flush()
            fpt6.flush()

        sys.stdout.flush()
        
        Select = Selection(self.nrealcross, self.nbincross, self.eta_c, self.pcross_real, 
                  self.popsize, self.nobj)
        Mutate = Mutation(self.nrealmut, self.nbinmut, self.pmut_bin, self.nvar, 
                          self.min_realvar, self.max_realvar, self.eta_m, self.popsize,
                          self.pmut_real, self.nbin)
        
        # Iterate Generations
        for i in range(self.ngen):
            self.ChildPop.Population, self.nbincross = Select.Select(self.ParentPop, self.ChildPop)
            self.ChildPop.Population, self.nrealmut = Mutate.Mutate(self.ChildPop)            
            self.ChildPop.Decode()
            self.ChildPop.Evaluate(self.objconfunc)
            
            self.OffSprings.Population = merge(self.ParentPop, self.ChildPop, self.OffSprings, self)
            NonDominatedSort(self.OffSprings, self.ParentPop, self)

            # Comment following three lines if information for all
            # generations is not desired, it will speed up the execution

            if printout >= 1 :
                if printout == 2 :
                    fpt4.writelines("# gen = %i\n",i)
                    self.ParentPop.Report(fpt4)
                    fpt4.flush()

                fpt6.writelines("\n gen = %i",i)
                fpt6.flush()


        # Output
        if printout >= 1:
            fpt6.writelines("\n Generations finished")
            self.ParentPop.Report(fpt2)
            self.ParentPop.ReportFeasible(fpt3)

            if self.nvar != 0 :
                fpt5.writelines("\n Number of crossover of real variable = %i",self.nrealcross)
                fpt5.writelines("\n Number of mutation of real variable = %i",self.nrealmut)

            if self.nbin!=0 :
                fpt5.writelines("\n Number of crossover of binary variable = %i",self.nbincross)
                fpt5.writelines("\n Number of mutation of binary variable = %i",self.nbinmut)

            sys.sys.stdout.flush()
            fpt1.flush()
            fpt2.flush()
            fpt3.flush()
            if printout == 2:
                fpt4.flush()

            fpt5.flush()
            fpt6.flush()
            fpt1.close()
            fpt2.close()
            fpt3.close()
            
            if printout == 2 :
                fpt4.close()

            fpt5.close()


        for i in range(self.popsize):
            if self.ParentPop.Population[i].constr_violation == 0.0  and  self.ParentPop.Population[i].rank==1 :
                for j in range(self.nobj):
                    f[j] = self.ParentPop.Population[i].obj[j]

                if self.ncon != 0:
                    for j in range(self.ncon):
                        g[j] = self.ParentPop.Population[i].constr[j]

                if self.nvar != 0 :
                    for j in range(self.nvar):
                        x[j] = self.ParentPop.Population[i].xreal[j]
                break


        if printout >= 1 :
            fpt6.writelines("\n Routine successfully exited \n")
            fpt6.flush()
            fpt6.close()


        return 0
    
    
    
    def Files(self, printout, seed):
        
        if printout >= 1:
            fpt1 = open("nsga2_initial_pop.out","w")
            fpt2 = open("nsga2_final_pop.out","w")
            fpt3 = open("nsga2_best_pop.out","w")

            if printout == 2 :
                fpt4 = open("nsga2_all_pop.out","w")

            fpt5 = open("nsga2_params.out","w")
            fpt6 = open("nsga2_run.out","w")
            
            fpt1.writelines("# This file contains the data of initial population\n")
            fpt2.writelines("# This file contains the data of final population\n")
            fpt3.writelines("# This file contains the data of final feasible population (if found)\n")
            
            if printout == 2 :
                fpt4.writelines("# This file contains the data of all generations\n")

            fpt5.writelines("# This file contains information about inputs as read by the program\n")
            fpt6.writelines("# This file contains runtime information\n")



        # Performing Initialization
        if printout >= 1 :
            fpt5.writelines("\n Population size = %d" %self.popsize)
            fpt5.writelines("\n Number of generations = %d" %self.ngen)
            fpt5.writelines("\n Number of objective functions = %d" %self.nobj)
            fpt5.writelines("\n Number of constraints = %d" %self.ncon)
            fpt5.writelines("\n Number of variables = %d" %self.nvar)
            fpt5.writelines("\n Number of real variables = %d" %self.nvar)

            if self.nvar != 0 :
                for i in range(self.nvar):
                    fpt5.writelines("\n Lower limit of real variable %d = %e" %(i+1,self.min_realvar[i]))
                    fpt5.writelines("\n Upper limit of real variable %d = %e" %(i+1,self.max_realvar[i]))

                fpt5.writelines("\n Probability of crossover of real variable = %e" %self.pcross_real)
                fpt5.writelines("\n Probability of mutation of real variable = %e" %self.pmut_real)
                fpt5.writelines("\n Distribution index for crossover = %e" %self.eta_c)
                fpt5.writelines("\n Distribution index for mutation = %e" %self.eta_m)

            fpt5.writelines("\n Number of binary variables = %d" %self.nbin)

            if self.nbin != 0:
                for i in range(self.nbin):
                    fpt5.writelines("\n Number of bits for binary variable %d = %d" %(i+1,self.nbits[i]))
                    fpt5.writelines("\n Lower limit of binary variable %d = %e" %(i+1,self.min_binvar[i]))
                    fpt5.writelines("\n Upper limit of binary variable %d = %e" %(i+1,self.max_binvar[i]))

                fpt5.writelines("\n Probability of crossover of binary variable = %e" %self.pcross_bin)
                fpt5.writelines("\n Probability of mutation of binary variable = %e" %self.pmut_bin)

            fpt5.writelines("\n Seed for random number generator = %e" %seed)

            fpt1.writelines("# of objectives = %d, # of constraints = %d, # of real_var = %d, # of bits of bin_var = %d, constr_violation, rank, crowding_distance\n" %(self.nobj,self.ncon,self.nvar,self.bitlength))
            fpt2.writelines("# of objectives = %d, # of constraints = %d, # of real_var = %d, # of bits of bin_var = %d, constr_violation, rank, crowding_distance\n" %(self.nobj,self.ncon,self.nvar,self.bitlength))
            fpt3.writelines("# of objectives = %d, # of constraints = %d, # of real_var = %d, # of bits of bin_var = %d, constr_violation, rank, crowding_distance\n" %(self.nobj,self.ncon,self.nvar,self.bitlength))

            if printout == 2 :
                fpt4.writelines("# of objectives = %d, # of constraints = %d, # of real_var = %d, # of bits of bin_var = %d, constr_violation, rank, crowding_distance\n"% (self.nobj,self.ncon,self.nvar,self.bitlength))
        
        if printout == 2 :
            return fpt1, fpt2, fpt3, fpt4, fpt5, fpt6
        else:
            return fpt1, fpt2, fpt3, fpt5, fpt6


