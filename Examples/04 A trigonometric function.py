"""
Created on Sun Feb  2 19:16:18 2020

@author: mofarrag
"""

from IPython import get_ipython
get_ipython().magic("reset -f")
import os
os.chdir("F:/01Algorithms/Oasis/Examples")
from numpy import power
from Oasis.optimization import Optimization
from Oasis.hsapi import HSapi


"""
min −[(sin(x)−1)**3]−[(sin(x)−cos(y))**4]−(cos(y)−3)**2

inequality constraints
    10−(sin(x)−1)2≥0,
    10−(sin(x)−cos(y))2≥0,
    10−(cos(y)−3)2≥0.

"""

def objfunc(x):
    from numpy import sin, cos
    f = -(sin(x[0]) - 1)**3 - (sin(x[0]) - cos(x[1]))**4 - (cos(x[1]) - 3)**2
    g = [(sin(x[0]) - 1)**2 - 10,
        (sin(x[0]) - cos(x[1]))**2 - 10,
        (cos(x[1]) - 3)**2 - 10]
    fail = 0
    return f, g, fail


opt_prob = Optimization('A trigonometric function', objfunc)
opt_prob.addVar('x1', 'c', lower=-10, upper=10, value=0.0)
opt_prob.addVar('x2', 'c', lower=-10, upper=10, value=0.0)
opt_prob.addObj('f')
opt_prob.addCon('g1', 'i')
opt_prob.addCon('g2', 'i')
opt_prob.addCon('g3', 'i')

options = dict(filename ='results/04 A trigonometric function.txt')
opt_engine = HSapi(pll_type = 'POA',options = options)

res = opt_engine(opt_prob, store_sol=True, display_opts=True, store_hst=True,
                 hot_start=False)