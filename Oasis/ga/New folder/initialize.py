
from Oasis.ga.rand import randomperc, rndreal



def initialize_pop(pop, globalvar) :
    """
    =======================================================
        initialize_pop(pop, globalvar) 
    =======================================================
     initialize_pop method initialize a population randomly

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
    
    for i in range(globalvar.popsize):
        initialize_ind((pop['ind'][i]),globalvar)

    return



def initialize_ind(ind, globalvar):
    """
    =======================================================
        initialize_ind(ind, globalvar)
    =======================================================
    initialize_ind method initialize an individual randomly
    
    
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

    # int j, k
    if globalvar.nreal != 0 :
        for j in range(globalvar.nreal):
            ind['xreal'][j] = rndreal (globalvar.min_realvar[j], globalvar.max_realvar[j])


    if globalvar.nbin != 0 :
        for j in range(globalvar.nbin):
            for k in range(globalvar.nbits[j]):
                if randomperc() <= 0.5 :
                    ind['gene'][j][k] = 0
                else:
                    ind['gene'][j][k] = 1
    return

