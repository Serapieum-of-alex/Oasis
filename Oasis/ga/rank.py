# /* Rank assignment routine */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"
INF = 1.0e14

from Oasis.ga.list import insert, delnode
from Oasis.ga.crowddist import assign_crowding_distance_list
from Oasis.ga.dominance import check_dominance
# /* Function to assign rank and crowding distance to a population of size pop_size*/
def assign_rank_and_crowding_distance(new_pop, globalvar):

    # int flag
    # int i
    # int end
    # int front_size
    # int rank=1
    # list *orig
    # list *cur
    # list *temp1, *temp2
    # orig = (list *)malloc(sizeof(list))
    # cur = (list *)malloc(sizeof(list))
    end = 0
    rank = 1
    orig = dict()
    cur = dict()
    front_size = 0
    orig['index'] = -1
    orig['parent'] = None
    orig['child'] = None
    cur['index'] = -1
    cur['parent'] = None
    cur['child'] = None
    temp1 = orig
    for i in range(globalvar.popsize):

        insert(temp1,i)
        temp1 = temp1['child']

    while orig['child'] != None:

        if orig['child']['child'] == None :

            new_pop['ind'][orig['child']['index']].rank = rank
            new_pop['ind'][orig['child']['index']].crowd_dist = INF
            break

        temp1 = orig['child']
        insert(cur, temp1['index'])
        front_size = 1
        temp2 = cur['child']
        temp1 = delnode(temp1)
        temp1 = temp1['child']

        while temp1 != None :
            temp2 = cur['child']

            while end != 1 and temp2 != None :
                end = 0
                flag = check_dominance((new_pop['ind'][temp1['index']]), (new_pop['ind'][temp2['index']]), globalvar)
                if flag == 1 :

                    insert(orig, temp2['index'])
                    temp2 = delnode(temp2)
                    front_size = front_size - 1
                    temp2 = temp2['child']

                if flag == 0 :

                    temp2 = temp2['child']

                if flag == -1 :

                    end = 1


            # while (end!=1 && temp2!=None)
            if flag == 0 or flag == 1 :

                insert (cur, temp1['index'])
                front_size = front_size + 1
                temp1 = delnode (temp1)

            temp1 = temp1['child']

        # while (temp1 != None)
        temp2 = cur['child']
        # do
        while temp2 != None :
            new_pop['ind'][temp2['index']].rank = rank
            temp2 = temp2['child']

        # while (temp2 != None)
        assign_crowding_distance_list(new_pop, cur['child'], front_size, globalvar)
        temp2 = cur['child']

        while cur['child'] != None :
            temp2 = delnode(temp2)
            temp2 = temp2['child']

        # while (cur['child'] !=None)
        rank = rank + 1

    # while (orig['child!=None)
    # free (orig)
    # free (cur)
    return

