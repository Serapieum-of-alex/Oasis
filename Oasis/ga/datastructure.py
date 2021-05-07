# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 21:53:05 2021

@author: mofarrag
"""
INF = 1.0e14

import numpy as np
import random 
import Oasis.ga.sort as sort

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
        # 0- rank
        # 1- constr_violation
        # 2- *xreal: [array]
                    size = number of variables
        # 3- **gene
        # 4- *xbin
        # 5- *obj
        # 6- *constr
        # 7- crowd_dist
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
    
    
    def Create(self, popsize):
        """
        ===============================================
             Create(self, popsize)
        ===============================================
        Create method creates a population with each individual having 
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
    
    def Initialize(self):
        """
        =======================================================
            InitializePop() 
        =======================================================
         InitializePop method initialize a population randomly
    
        Parameters
        ----------
        
    
        Returns
        -------
        None.
    
        """        
        for i in range(self.popsize):
            # self.Population[i] = self.InitializeInd(self.Population[i])
            self.Population[i].Initialize(self.min_realvar, self.max_realvar)
    
        return

    
    def Decode(self):
    # Function to decode a population to find out the binary variable values 
    # based on its bit pattern
        if self.nbin != 0:
            for i in range(self.popsize):
                self.Population[i].Decode()
    
        return
    
    
    def Evaluate(self, objconfunc):
    # Routine to evaluate objective function values and constraints for a population
        for i in range(self.popsize):
            self.Population[i].Evaluate(objconfunc)
    
        return
    
    
    def AssignRankCrowdingDistance(self):

        end = 0
        rank = 1
        orig = LinkedList()
        cur = LinkedList()
        front_size = 0
        temp1 = orig
        for i in range(self.popsize):
            # if i == 0:
            temp1.Append(i)
            # else:
                # temp1.Insert(temp1.head, i)
        
        while orig.head.Child != None:
            if orig.head.Child.Child == None :
                self.Population[orig.head.Child.Index].rank = rank
                self.Population[orig.head.Child.Index].crowd_dist = INF
                break
    
            temp1 = orig.head.Child
            cur.Insert(temp1.Index)
            # cur.Insert(cur.head, temp1.Index)
            front_size = 1
            temp2 = cur.head.Child
            temp1.Remove(temp1)
            temp1 = temp1.head.Child
            
            # update orig with the latest temp1
            # orig = temp1
            
            while temp1 != None :
                temp2 = cur.head.Child
                
                while end != 1 and temp2 != None :
                    end = 0
                    flag = self.CheckDominance(self.nobj, self.Population[temp1.head.Index], self.Population[temp2.head.Index])
                    if flag == 1 :
                        orig = self.Insert(orig, temp2.head.Index)
                        temp2 = self.DelNode(temp2)
                        front_size = front_size - 1
                        temp2 = temp2.head.Child
    
                    if flag == 0 :
                        temp2 = temp2.head.Child
                    if flag == -1 :
                        end = 1
                # update cur.Child dict from temp2
                cur.head.Child = temp2
                # update temp1 from orig ??
                temp1 = orig
                
                if flag == 0 or flag == 1 :
                    cur = self.Insert(cur, temp1.head.Index)
                    front_size = front_size + 1
                    temp1 = self.DelNode(temp1.head)
                # update temp2 from cur.Child dict 
                temp2 = cur.head.Child
                # update orig with the latest temp1
                # orig = temp1
            
                temp1 = temp1.head.Child    
            temp2 = cur.head.Child
            
            while temp2 != None :
                self.Population[temp2.head.Index].rank = rank
                temp2 = temp2.head.Child
            # update cur.Child dict  from temp2
            cur.head.Child = temp2
            
            cur.head.Child = self.AssignCrowdingDistancelist(cur.head.Child, front_size)
            
            temp2 = cur.head.Child
    
            while temp2 != None : #cur.Child temp2 is a pointer to cur.Child
                temp2 = self.DelNode(temp2)
                temp2 = temp2.head.Child
            # new
            cur.head.Child = None
            
            rank = rank + 1
    
        return

    
    def AssignCrowdingDistancelist(self, lst, front_size) :
    # Routine to compute crowding distance based on ojbective function 
    # values when the population in in the form of a list
    
        temp = lst
        if front_size == 1:
            self.Population[lst.Index].crowd_dist = INF
            return
    
        if front_size == 2 :
            self.Population[lst.Index].crowd_dist = INF
            self.Population[lst.Child.Index].crowd_dist = INF
            return
    
        self.obj_array = np.zeros(shap=(self.nobj, front_size), dtype=np.int32)
        dist = np.zeros(front_size, dtype=np.int32)
    
        for j in range(front_size):
            dist[j] = temp.Index
            temp = temp.Child
        
        self.AssignCrowdingDistance(dist, front_size)
        lst = temp
        
        return lst

    @staticmethod    
    def AssignCrowdingDistanceIndices(pop, c1, c2, nobj):
        # Routine to compute crowding distance based on objective function 
        # values when the population in in the form of an array
        
        # int **obj_array
        front_size = c2 - c1 + 1
    
        if front_size == 1:
            pop.Population[c1].crowd_dist = INF
            return
    
        if front_size == 2:
            pop.Population[c1].crowd_dist = INF
            pop.Population[c2].crowd_dist = INF
            return
    
        obj_array = np.zeros(shape=(nobj, front_size), dtype=np.int32)
        dist = np.zeros(shape=(front_size), dtype=np.int32)
    
        for j in range(front_size):
            dist[j] = c1 + 1
    
        Population.AssignCrowdingDistance(dist, obj_array, front_size)
    
        return

    def AssignCrowdingDistance(self, dist, front_size):
        # Routine to compute crowding distances
    
        for i in range(self.nobj):
            for j in range(front_size):
                self.obj_array[i,j] = dist[j]
    
            sort.quicksort_front_obj(self.Population, i, self.obj_array[i], front_size)
    
        for j in range(front_size):
            self.Population[dist[j]].crowd_dist = 0.0
    
        for i in range(self.nobj):
            self.Population[self.obj_array[i,0]].crowd_dist = INF
    
        for i in range(self.nobj):
            for j in range(front_size-1):
                if self.Population[self.obj_array[i,j]].crowd_dist != INF:
    
                    if self.Population[self.obj_array[i,front_size-1]].obj[i] == self.Population[self.obj_array[i,0]].obj[i]:
                        self.Population[self.obj_array[i,j]].crowd_dist += 0.0
                    else:
                        val1 = self.Population[self.obj_array[i,j+1]].obj[i]
                        val2 = self.Population[self.obj_array[i,j-1]].obj[i]
                        val3 = self.Population[self.obj_array[i,front_size-1]].obj[i]
                        val4 = self.Population[self.obj_array[i,0]].obj[i]
                        self.Population[self.obj_array[i,j]].crowd_dist +=  (val1 - val2) /  (val3 - val4)
    
        for j in range(front_size):
            if self.Population[dist[j]].crowd_dist != INF:
                self.Population[dist[j]].crowd_dist = (self.Population[dist[j]].crowd_dist)/self.nobj
    
        return
    
    @staticmethod
    def CheckDominance(nobj, a, b):
        """
        Routine for usual non-domination checking
           It will return the following values
           1 if a dominates b
           -1 if b dominates a
           0 if both a and b are non-dominated
        """
        flag1 = 0
        flag2 = 0
        if a.constr_violation < 0 and b.constr_violation < 0:
            if a.constr_violation > b.constr_violation:
                return 1
            else:
                if a.constr_violation < b.constr_violation:
                    return -1
                else:
                    return 0
        else:
            if a.constr_violation < 0 and b.constr_violation == 0 :
                return -1
            else:
                if a.constr_violation == 0 and b.constr_violation <0:
                    return 1
                else:
                    for i in range(nobj):
                        if a.obj[i] < b.obj[i]:
                            flag1 = 1
                        else:
                            if a.obj[i] > b.obj[i]:
                                flag2 = 1
                    if flag1 == 1 and flag2 == 0 :
                        return 1
                    else:
                        if flag1 == 0 and flag2 == 1:
                            return -1
                        else:
                            return 0
                        
    # @staticmethod
    # def Insert(node, x):
    # # Insert an element X into the list at location specified by NODE
    #     temp = dict()
    #     if node == None:
    #         print("\n Error!! asked to enter after a NULL pointer, hence exiting \n")
    #         return 1
    
    #     temp.Index = x
    #     temp['child'] = node['child']
    #     temp['parent'] = node
    #     if node['child'] != None:
    #         node['child']['parent'] = temp
    
    #     node['child'] = temp
    
    #     return node
    
    # @staticmethod
    # def DelNode(node):
    # # Delete the node NODE from the list 
    #     temp = dict()
    #     if node == None :
    #         print("\n Error!! asked to delete a NULL pointer, hence exiting \n")
    #         return 1
    #     # take the parent 
    #     temp = node['parent']
    #     temp['child'] = node['child']
    #     if temp['child'] != None:
    #         temp['child']['parent'] = temp
    
    #     return temp
    
    
    def Report(self,fpt):
        # /* Function to print the information of a population in a file */
        for i in range(self.popsize):
            for j in range(self.nobj):
                fpt.write("%e\t"%self.Population[i].obj[j])
    
            if self.ncon != 0 :
                for j in range(self.ncon):
                    fpt.write("%e\t"%self.Population[i].constr[j])
    
            if self.nvar != 0:
                for j in range(self.nvar):
                    fpt.write("%e\t"%self.Population[i].xreal[j])
    
            if self.nbin != 0:
                for j in range(self.nbin):
                    for k in range(self.nbits[j]):
                        fpt.write("%d\t"%self.Population[i].gene[j][k])
    
            fpt.write("%e\t"%self.Population[i].constr_violation)
            fpt.write("%d\t"%self.Population[i].rank)
            fpt.write("%e\n"%self.Population[i].crowd_dist)
    
        return


    def ReportFeasible(self, fpt):
    # /* Function to print the information of feasible and non-dominated population in a file */
    
        for i in range(self.popsize):
            if self.Population[i].constr_violation == 0.0 and self.Population[i].rank==1:
    
                for j in range(self.nobj) :
                    fpt.write("%e\t"%self.Population[i].obj[j])
    
                if self.ncon != 0 :
                    for j in range(self.ncon):
                        fpt.write("%e\t"%self.Population[i].constr[j])
    
    
                if self.nvar != 0:
                    for j in range(self.nvar):
                        fpt.write("%e\t"%self.Population[i].xreal[j])
    
                if self.nbin != 0 :
                    for j in range(self.nbin):
                        for k in range(self.nbits[j]):
                            fpt.write("%d\t"%self.Population[i].gene[j][k])
    
                fpt.write(fpt,"%e\t"%self.Population[i].constr_violation)
                fpt.write(fpt,"%d\t"%self.Population[i].rank)
                fpt.write(fpt,"%e\n"%self.Population[i].crowd_dist)
    
        return






class Individual():
    
    def __init__(self,nvar, nobj, ncon, nbin=0, nbits=0):
        self.nvar = nvar
        self.nobj = nobj
        self.ncon = ncon
        self.nbin = nbin
        self.nbits = nbits
        self.xreal = np.zeros(nvar, np.float64)
        self.rank = None
        # self.rank = np.zeros(nvar, np.float64)
        # self.constr_violation = np.zeros(nvar, np.float64)
        if nbin != 0:
            self.gene = np.zeros(shape=(nbin,nbits), dtype=int)
            self.xbin = np.zeros(nbin, np.float64)
        self.obj = np.zeros(nobj, np.float64)
        
        self.constr = np.zeros(ncon, np.float64)
        self.crowd_dist = None# np.zeros(nvar, np.float64)
        pass
    
    
    def Initialize(self, min_realvar, max_realvar):
        """
        =======================================================
            initialize_ind(ind)
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
        
    
        Returns
        -------
        None.
    
        """

        # if self.nvar != 0 :
        for i in range(len(self.xreal)):
            # initialize xreal is the first array in the list of each individual
            self.xreal[i] = random.uniform(min_realvar[i],max_realvar[i]) #rndreal (self.min_realvar[j], self.max_realvar[j])
        
        if self.nbin != 0 :
            for j in range(self.nbin):
                for k in range(self.nbits[j]):
                    if random.uniform(0,1) <= 0.5 :
                        self.gene[j,k] = 0
                    else:
                        self.gene[j,k] = 1
                        
        return 
    
    
    def Decode(self, min_binvar, max_binvar):
    # Function to decode an individual to find out the binary variable values 
    # based on its bit pattern
        if self.nbin != 0 :
            for j in range(self.nbin):
                sumi = 0
                for k in range(self.nbits[j]):
                    if self.gene[j,k] == 1:
                        sumi = sumi + np.power(2,self.nbits[j]-1-k);
    
                val1 = sumi*(max_binvar[j] - min_binvar[j])
                val2 = np.power(2,self.nbits[j])-1
    
                self.xbin[j] = min_binvar[j] + val1 / val2
    
        return
    
    def Evaluate(self, objfunc):
    # Routine to evaluate objective function values and constraints for an individual
      
        # nsga2func(globalvar.nreal, globalvar.nbin, globalvar.nobj, globalvar.ncon,
                    # ind['xreal'], ind['xbin'], ind['gene'], ind['obj'], ind['constr'])
        # Evaluate Ojective Function
        # nreal,nobj,ncon,x,f,g
        [self.obj,self.constr] = objfunc(self.nvar, self.nobj, self.ncon, self.xreal, self.obj, self.constr)
        
        if self.ncon == 0:
            self.constr_violation = 0.0
        else:
            self.constr_violation = 0.0
            for i in range (self.ncon):
                if self.constr[i] < 0.0 :
                    self.constr_violation = self.constr_violation + self.constr[i]
    
        return

#%%
class Node:
    def __init__(self, Index):
        self.Index = Index
        self.Parent = None
        self.Child = None
    
    def __repr__(self):
        return str(self.Index)
    
    
class LinkedList():
    
    def __init__(self, nodes=None):
        self.head = None
        # if given list of nodes take the first node from the top of the list
        # make it a head in the linked list then iterate over the rest of the 
        # list
        
        if nodes is not None:
             node = Node(Index=nodes.pop(0))
             self.head = node
             for elem in nodes:
                 node.Child = Node(Index=elem)
                 node = node.Child
    
    # Define the push method to add elements		
    def Push(self, Index):
    # Define the push method to add elements at the begining
    
        NewNode = Node(Index)
        NewNode.Child = self.head
        if self.head is not None:
           self.head.Parent = NewNode
        self.head = NewNode
     
    # Define the insert method to insert the element		
    def Insert(self, Parent, Index):
        
        if Parent.head is None:
           return
       
        NewNode = Node(Index)
        NewNode.Child = Parent.Child
        Parent.Child = NewNode
        NewNode.Parent = Parent
        
        if NewNode.Child is not None:
           NewNode.Child.Parent = NewNode
         
    
    def Append(self, Index):
        # Define the append method to add elements at the end
        NewNode = Node(Index)
        NewNode.Child = None
        
        if self.head is None:
           NewNode.Parent = None
           self.head = NewNode
           return
        #  get the last node to append the given node after
        last = self.head
        while (last.Child is not None):
           last = last.Child
        last.Child = NewNode
        NewNode.Parent = last
        return
    
    def Remove(self, Index):
        if self.head is None:
            raise Exception("List is empty")
    
        if self.head.Index == Index:
            self.head = self.head.Child
            return
    
        previous_node = self.head
        for node in self:
            if node.Index == Index:
                previous_node.Child = node.Child
                return
            previous_node = node
            
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.Child
            
    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node.Index))
            node = node.Child
        nodes.append("None")
        return " -> ".join(nodes)
    
    # Define the method to print the linked list 
    def listprint(self, node):
      while (node is not None):
         print(node.Index),
         last = node
         node = node.Child

#%%

# dllist = LinkedList()
# print(dllist)
# dllist.Insert(dllist, 13)
# dllist.Push(12)
# print(dllist)
# dllist.Push(8)
# print(dllist)
# dllist.Push(62)
# print(dllist)
# dllist.Insert(dllist.head.Child, 13)
# print(dllist)

# dllist.listprint(dllist.head)    
# #%%
# dllist = LinkedList()
# print(dllist)
# dllist.Push(12)
# print(dllist)
# dllist.Append(9)
# print(dllist)
# dllist.Push(8)
# print(dllist)
# dllist.Push(62)
# print(dllist)
# dllist.Append(45)
# print(dllist)
# # dllist.listprint(dllist.head)
# dllist.Remove(45)
# print(dllist)
# dllist.Remove(8)
# print(dllist)
