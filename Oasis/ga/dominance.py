# /* Domination checking routines */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"
"""
/* Routine for usual non-domination checking
   It will return the following values
   1 if a dominates b
   -1 if b dominates a
   0 if both a and b are non-dominated */
"""
def check_dominance(a, b, globalvar):

    # int i;
    # int flag1;
    # int flag2;
    flag1 = 0
    flag2 = 0
    if a['constr_violation']<0 and b['constr_violation'] < 0:

        if a['constr_violation'] > b['constr_violation']:

            return 1

        else:

            if a['constr_violation'] < b['constr_violation']:

                return -1

            else:

                return 0

    else:

        if a['constr_violation'] < 0 and b['constr_violation'] == 0 :

            return -1

        else:

            if a['constr_violation'] == 0 and b['constr_violation'] <0:

                return 1

            else:

                for i in range(globalvar.nobj):

                    if a['obj'][i] < b['obj'][i]:

                        flag1 = 1

                    else:

                        if a['obj'][i] > b['obj'][i]:

                            flag2 = 1

                if flag1 == 1 and flag2 == 0 :

                    return 1

                else:

                    if flag1 == 0 and flag2 == 1:

                        return -1

                    else:

                        return 0

