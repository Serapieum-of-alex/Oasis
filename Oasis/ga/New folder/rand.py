"""
/* Definition of random number generation routines */

# include <stdio.h>
# include <stdlib.h>
# include <math.h>

# include "nsga2.h"
# include "rand.h"


oldrand : [array]
    - size is 55,
    - double oldrand[55];

int jrand;
"""

import numpy as np


def randomize(seed):
    """
    Get seed number for random and start it up

    Parameters
    ----------
    seed : [float]
        random number between 0 and 1.

    Returns
    -------
    oldrand : [array]
        array of size  55 random number between 0 and 1.
    jrand : TYPE
        DESCRIPTION.

    """

    oldrand = np.zeros(55)

    jrand = 0

    oldrand, jrand = warmup_random(seed, oldrand, jrand)

    return oldrand, jrand


# /* Get randomize off and running */
def warmup_random(seed, oldrand, jrand):

    oldrand[54] = seed

    new_random = 0.000000001
    prev_random = seed

    for j1 in range(1, 54):

        ii = (21*j1)%54;

        oldrand[ii] = new_random
        new_random = prev_random - new_random

        if new_random < 0.0 :

            new_random = new_random + 1.0

        prev_random = oldrand[ii]

    oldrand = advance_random(oldrand)
    oldrand = advance_random(oldrand)
    oldrand = advance_random(oldrand)
    jrand = 0

    return oldrand, jrand


# /* Create next batch of 55 random numbers */
def advance_random(oldrand):

    for j1 in range(0, 24):
        new_random = oldrand[j1] - oldrand[j1+31]
        if new_random < 0.0:

            new_random = new_random + 1.0

        oldrand[j1] = new_random

    for j1 in range(24, 55):

        new_random = oldrand[j1]-oldrand[j1-24]
        if new_random < 0.0:

            new_random = new_random + 1.0

        oldrand[j1] = new_random

    return oldrand

# /* Fetch a single random number between 0.0 and 1.0 */
def randomperc():
    # replace by random.uniform(0,1)
    jrand = 0
    oldrand = np.zeros(55)

    jrand = jrand + 1
    if jrand >= 55 :

        jrand = 1;
        oldrand = advance_random(oldrand)

    return oldrand[jrand]


# /* Fetch a single random integer between low and high including the bounds */
def rnd(low, high):
    # replace by random.uniform(low, high)

    if low >= high :
        res = low
    else :
        res = low + (randomperc() * (high-low+1))
        if res > high :

            res = high

    return (res)


# /* Fetch a single random real number between low and high including the bounds */
def rndreal(low, high):
    return low + (high-low) * randomperc()

