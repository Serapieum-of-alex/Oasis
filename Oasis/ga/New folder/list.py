# /* A custom doubly linked list implemenation */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"


def insert(node, x):
# Insert an element X into the list at location specified by NODE
    # list *temp
    temp = dict()
    if node == None:
        print("\n Error!! asked to enter after a NULL pointer, hence exiting \n")
        exit(1)

    # temp = (list *)malloc(sizeof(list))
    temp['index'] = x
    temp['child'] = node['child']
    temp['parent'] = node.copy()
    if node['child'] != None:
        node['child']['parent'] = temp.copy()

    node['child'] = temp.copy()

    return node



def delnode(node):
# Delete the node NODE from the list 
    # list *temp
    temp = dict()
    if node == None :

        print("\n Error!! asked to delete a NULL pointer, hence exiting \n")
        exit(1)

    temp = node['parent']
    temp['child'] = node['child']
    if temp['child'] != None:

        temp['child']['parent'] = temp

    # free (node)
    return temp

