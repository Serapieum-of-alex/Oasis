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
import time
import numpy as np
import sys
import random #, time
from Oasis.ga.rand import randomize
# from Oasis.ga.eval import evaluate_pop
# from Oasis.ga.decode import decode_pop
from Oasis.ga.rank import assign_rank_and_crowding_distance
from Oasis.ga.report import report_pop, report_feasible
from Oasis.ga.tourselect import selection
from Oasis.ga.mutation import mutation_pop
from Oasis.ga.merge import merge
from Oasis.ga.fillnds import fill_nondominated_sort
# from Oasis.ga.initialize import initialize_pop
from Oasis.ga.rand import randomperc, rndreal

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
                 pmut_real, eta_c, eta_m,pcross_bin,pmut_bin,):
        
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
        
        nbinmut = 0
        nrealmut = 0
        nbincross = 0
        nrealcross = 0
        
        
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
            
        self.ParentPop.CreatePopulation(self.popsize)
        self.ChildPop.CreatePopulation(self.popsize)
        self.OffSprings.CreatePopulation(self.popsize)
        
        # oldrand, jrand = randomize(seed)
        
        self.ParentPop.InitializePop()

        if xinit != 0 :
          i=0
          for j in range(self.nvar) :
              # xreal for the first individual
              self.ParentPop[0][i] = x[j]

        # First Generation
        if printout >= 1 :
            fpt6.writelines("\n\n Initialization done, now performing first generation")

        self.ParentPop.DecodePopulation()
        self.ParentPop.EvaluatePop()
        assign_rank_and_crowding_distance(self.ParentPop, self)

        if printout >= 1 :
            report_pop(self.ParentPop, fpt1, self)
            if printout == 2 :
                fpt4.writelines("# gen = 1\n")
                report_pop(self.ParentPop,fpt4, self)


            fpt6.writelines("\n gen = 1")
            fpt1.flush()
            fpt2.flush()
            fpt3.flush()

            if printout == 2 :
                fpt4.flush()

            fpt5.flush()
            fpt6.flush()

        sys.stdout.flush()

        # Iterate Generations
        for i in range(self.ngen):

            selection(self.ParentPop, self.ChildPop, self, self.nrealcross, self.nbincross)
            mutation_pop(self.ChildPop, self, self.nrealmut, self.nbinmut)
            self.ChildPop.DecodePopulation(self)
            evaluate_pop(self.ChildPop, self)
            merge(self.ParentPop, self.ChildPop, self.OffSprings, self)
            fill_nondominated_sort(self.OffSprings, self.ParentPop, self)

            # Comment following three lines if information for all
            # generations is not desired, it will speed up the execution

            if printout >= 1 :
                if printout == 2 :
                    fpt4.writelines("# gen = %i\n",i)
                    report_pop(self.ParentPop,fpt4, self)
                    fpt4.flush()

                fpt6.writelines("\n gen = %i",i)
                fpt6.flush()


        # Output
        if printout >= 1:
            fpt6.writelines("\n Generations finished")
            report_pop(self.ParentPop,fpt2, self)
            report_feasible(self.ParentPop,fpt3, self)

            if self.nvar != 0 :
                fpt5.writelines("\n Number of crossover of real variable = %i",nrealcross)
                fpt5.writelines("\n Number of mutation of real variable = %i",nrealmut)

            if self.nbin!=0 :
                fpt5.writelines("\n Number of crossover of binary variable = %i",nbincross)
                fpt5.writelines("\n Number of mutation of binary variable = %i",nbinmut)

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
            if self.ParentPop['ind'][i].constr_violation == 0.0  and  self.ParentPop['ind'][i].rank==1 :
                for j in range(self.nobj):
                    f[j] = self.ParentPop['ind'][i].obj[j]

                if self.ncon != 0:
                    for j in range(self.ncon):
                        g[j] = self.ParentPop['ind'][i].constr[j]

                if self.nvar != 0 :
                    for j in range(self.nvar):
                        x[j] = self.ParentPop['ind'][i].xreal[j]

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


class Population():
    
    def __init__(self, nvar, nobj, min_realvar, max_realvar, ncon=0, nbin=0, nbits=0):
        self.nvar = nvar
        self.nbits = nbits
        self.nbin = nbin
        self.nobj = nobj
        self.ncon = ncon
        self.min_realvar = min_realvar
        self.max_realvar = max_realvar
        """
        # 0- rank;
        # 1- constr_violation;
        # 2- *xreal: [array]
                    size = number of variables
        # 3- **gene;
        # 4- *xbin;
        # 5- *obj;
        # 6- *constr;
        # 7- crowd_dist;
        """
        pass
    
    
    def CreateIndividual(self):
        """
        ===============================================
            CreateIndividual(self)
        ===============================================
        CreateIndividual create the individual inside the population
        
        Returns
        -------
        list : [list of arrays]
            [xreal, obj, constraints] list of 3 arrays in case of there is 
            binary variables. [xreal, obj, constraints, gene, xbin] in case  of
            binary variables.
        """
        # xreal = np.zeros(self.nvar, np.float64)
        # # self.rank = np.zeros(nvar, np.float64)
        # # self.constr_violation = np.zeros(nvar, np.float64)
        # if self.nbin != 0:
        #     gene = np.zeros(shape=(self.nbin,self.nbits), dtype=int)
        #     xbin = np.zeros(self.nbin, np.float64)
        # obj = np.zeros(self.nobj, np.float64)
        
        # constr = np.zeros(self.ncon, np.float64)
        # # self.crowd_dist = np.zeros(nvar, np.float64)
        # if self.nbin != 0:
        #     return xreal, obj, constr, gene, xbin
        # else:
        #     return xreal, obj, constr
        return Individual(self.nvar,  self.nobj, self.ncon, nbin=self.nbin, nbits=self.nbits)
    
    
    def CreatePopulation(self, popsize):
        """
        ===============================================
             CreatePopulation(self, popsize)
        ===============================================
        CreatePopulation method creates a population with each individual having 
        a list of properties, each property is either an array or a scalar
        
        Parameters
        ----------
        popsize : [integer]
            size of the population.

        Returns
        -------
        popsize : [integer attribute]
            size of the population.
        Population : [list attribute]
            list of properties [variables, obj, constraints] 3 arrays in case of there is 
            binary variables. [variables, obj, constraints, gene, binary variables] 
            in case  of binary variables.
        """
        self.popsize = popsize
        self.Population = list()
        for i in range(popsize):
            self.Population.append(self.CreateIndividual())
    
    def InitializePop(self):
        """
        =======================================================
            InitializePop(pop, globalvar) 
        =======================================================
         InitializePop method initialize a population randomly
    
        Parameters
        ----------
        pop : TYPE
            DESCRIPTION.
        globalvar : TYPE
            DESCRIPTION.
    
        Returns
        -------
        None.
    
        """        
        for i in range(self.popsize):
            self.Population[i] = self.InitializeInd(self.Population[i])
    
        return


    def InitializeInd(self, Individual):
        """
        =======================================================
            initialize_ind(ind, globalvar)
        =======================================================
        initialize_ind method initialize an individual randomly
        
        
        # 0- rank
        # 1- constr_violation
        # 2- *xreal
        # 3- **gene
        # 4- *xbin
        # 5- *obj
        # 6- *constr
        # 7- crowd_dist
        
        Parameters
        ----------
        ind : TYPE
            DESCRIPTION.
        globalvar : TYPE
            DESCRIPTION.
    
        Returns
        -------
        None.
    
        """

        if self.nvar != 0 :
            for i in range(self.nvar):
                # initialize xreal is the first array in the list of each individual
                Individual.xreal[i] = random.uniform(self.min_realvar[i],self.max_realvar[i]) #rndreal (self.min_realvar[j], self.max_realvar[j])
        
        if self.nbin != 0 :
            for j in range(self.nbin):
                for k in range(self.nbits[j]):
                    if randomperc() <= 0.5 :
                        Individual.gene[j,k] = 0
                    else:
                        Individual.gene[j,k] = 1
                        
        return Individual
    
    
    def DecodePopulation(self):
    # Function to decode a population to find out the binary variable values 
    # based on its bit pattern
        if self.nbin != 0:
            for i in range(self.popsize):
                self.Population[i] = self.DecodeIndividual(self.Population[i])
    
        return
    
    
    def DecodeIndividual(self, indvidual):
    # Function to decode an individual to find out the binary variable values 
    # based on its bit pattern
        if self.nbin != 0 :
            for j in range(self.nbin):
                sumi = 0
                for k in range(self.nbits[j]):
                    if indvidual[3][j,k] == 1:
                        sumi = sumi + np.power(2,self.nbits[j]-1-k);
    
                val1 = sumi*(self.max_binvar[j] - self.min_binvar[j])
                val2 = np.power(2,self.nbits[j])-1
    
                indvidual[4][j] = self.min_binvar[j] + val1 / val2
    
        return
    
    
    def EvaluatePop(self):
    # Routine to evaluate objective function values and constraints for a population
        
        for i in range(self.popsize):
            self.EvaluateIndvidual(self.Population[i])
    
        return
    
    
    def EvaluateIndvidual(self,Individual):
    # Routine to evaluate objective function values and constraints for an individual
      
        # nsga2func(globalvar.nreal, globalvar.nbin, globalvar.nobj, globalvar.ncon,
                   # ind['xreal'], ind['xbin'], ind['gene'], ind['obj'], ind['constr'])
    
        if self.ncon == 0:
            Individual['constr_violation'] = 0.0
        else:
            Individual['constr_violation'] = 0.0;
            for j in range (self.ncon):
                if Individual['constr'][j] < 0.0 :
                    Individual['constr_violation'] = Individual['constr_violation'] + Individual['constr'][j]
    
        return

class Individual():
    
    def __init__(self,nvar,  nobj, ncon, nbin=0, nbits=0):
        self.xreal = np.zeros(nvar, np.float64)
        # self.rank = np.zeros(nvar, np.float64)
        # self.constr_violation = np.zeros(nvar, np.float64)
        if nbin != 0:
            self.gene = np.zeros(shape=(nbin,nbits), dtype=int)
            self.xbin = np.zeros(nbin, np.float64)
        self.obj = np.zeros(nobj, np.float64)
        
        self.constr = np.zeros(ncon, np.float64)
        # self.crowd_dist = np.zeros(nvar, np.float64)
        pass