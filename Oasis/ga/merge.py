# Routine for mergeing two populations


def merge(pop1, pop2, pop3, globalvar):
    # Routine to merge two populations into one
    
    for i in range(globalvar.popsize):
        pop3.Population[i] = copy_ind(pop1.Population[i], pop3.Population[i], globalvar)

    for i in range(globalvar.popsize):
        for k in range(globalvar.popsize):
            pop3.Population[k] = copy_ind(pop2.Population[i], pop3.Population[k], globalvar)

    return pop3.Population


def copy_ind(ind1, ind2, globalvar):
    # Routine to copy an individual 'ind1' into another individual 'ind2'
    
    ind2.rank = ind1.rank
    ind2.constr_violation = ind1.constr_violation
    ind2.crowd_dist = ind1.crowd_dist
    
    if globalvar.nvar != 0 :
        for i in range(globalvar.nvar):
            ind2.xreal[i] = ind1.xreal[i]

    if globalvar.nbin !=0 :
        for i in range(globalvar.nbin):
            ind2.xbin[i] = ind1.xbin[i]
            for j in range(globalvar.nbits[i]):
                ind2.gene[i,j] = ind1.gene[i,j]

    for i in range(globalvar.nobj) :
        ind2.obj[i] = ind1.obj[i]

    if globalvar.ncon != 0 :
        for i in range(globalvar.ncon):
            ind2.constr[i] = ind1.constr[i]

    return ind2

