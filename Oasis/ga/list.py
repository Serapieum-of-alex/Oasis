# /* A custom doubly linked list implemenation */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"

# /* Insert an element X into the list at location specified by NODE */
def insert(node, x):

    # list *temp
    temp = dict()
    if node == None:

        print("\n Error!! asked to enter after a NULL pointer, hence exiting \n")
        exit(1)

    # temp = (list *)malloc(sizeof(list))
    temp['index'] = x
    temp['child'] = node['child']
    temp['parent'] = node
    if node['child'] != None:

        node['child']['parent'] = temp

    node['child'] = temp

    return


# /* Delete the node NODE from the list */
def delnode(node):

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

