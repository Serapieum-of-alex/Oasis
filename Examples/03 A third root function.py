"""
Created on Sun Feb  2 18:39:36 2020

@author: mofarrag
"""
from IPython import get_ipython
get_ipython().magic("reset -f")
import os
os.chdir("F:/01Algorithms/Oasis/Examples")
from numpy import power
from Oasis.optimization import Optimization
from Oasis.hsapi import HSapi


def objfunc(x):
        f = power(x[0]**2 * x[1]**2, 1. / 3.) - x[0] + x[1]**2
		# inequality Constraint: 9 - x**2 - y**2 >= 0
        g = [x[0]**2 + x[1]**2 - 9]
        print('inequality Constraint = ' + str(g))
        print('Obj Fn value = ' + str(f))
        fail = 0
        return f, g, fail

opt_prob = Optimization('A third root function', objfunc)
opt_prob.addVar('x1', 'c', lower=-3, upper=3, value=0.0)
opt_prob.addVar('x2', 'c', lower=-3, upper=3, value=0.0)
opt_prob.addObj('f')
opt_prob.addCon('g1', 'i')


# options = dict(etol=0.0001,atol=0.0001,rtol=0.0001, stopiters=10, hmcr=0.5,
#                par=0.9, hms = 10, dbw = 3000,
#                fileout = 1, filename ='parameters.txt',
#             	seed = 0.5, xinit = 1, scaling = 0,
# 				prtinniter = 1, prtoutiter = 1, stopcriteria = 1,
# 				maxoutiter = 2)
options = dict(filename ='results/03 A third root functions.txt')

opt_engine = HSapi(pll_type = 'POA',options = options)
"""
to use the hot start you have to store the history from a previous run with the
filename parameters in the option dictionary (HSapi) and the store_hst when
calling the optimizer

in the second run to use the history of the previous run just change hot_start
when calling the optimizer to True
"""
res = opt_engine(opt_prob, store_sol=True, display_opts=True, store_hst=True,
                 hot_start=True)

print(opt_prob.solution(0))
