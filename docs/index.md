# Welcome to Oasis 
Optimization Algorithm




## Purpose

Oasis is a Harmony search optimization algorithm which uses stochastic random search based on two factors, harmony memory consideration rate and (HMCR) and pitch adjusting rate (PAR)
The main difference between GA and HS is that GA evaluates many solutions simultaneously which may lead to convergence on a local minimum, whereas HS evaluates only one solution at each iteration which enables the algorithm of broad search and avoids convergence to local minima, HS generates a new offspring after considering all the existing population whereas GA only consider the two parent to generate a new offspring (Lee and Geem 2005).

```
def objfunc(x):
        # Objective function
        f = x[0]**2 + x[1]**2 + x[2]**4
        # Equality constraint
        g = [x[0] + x[1] + x[2] - 4]
        # print('Equality Constraint = ' + str(g))
        # print('Obj Fn value = ' + str(f))
        fail = 0
        return f, g, fail

# create the Optimization Object
opt_prob = Optimization('Testing solutions', objfunc)

# the upper and lower
opt_prob.addVar('x1', 'c', lower=-4, upper=4, value=0.0)
opt_prob.addVar('x2', 'c', lower=-4, upper=4, value=0.0)
opt_prob.addVar('x3', 'c', lower=-4, upper=4, value=0.0)
opt_prob.addObj('f')
opt_prob.addCon('g1', 'e')

options = dict(fileout = 1, filename ='test.txt')
opt_engine = HSapi(options = options)

res = opt_engine(opt_prob)

print(opt_prob.solution(0))
```


## Features


* Available algorithms are (`HS`).
* Nash-Sutcliff (`NSE`), log Nash-Sutcliff (`logNSE`), Root Mean Squared Error (`RMSE`), Mean Absolute Error (`MAE`).
  Kling-Gupta Efficiency (`KGE`).



## Installation

### Dependencies

* [NumPy](http://www.numpy.org/ "Numpy")
* [Scipy](http://www.scipy.org/ "Scipy")

Optional packages are:

* [Matplotlib](http://matplotlib.org/ "Matplotlib")
* [Pandas](http://pandas.pydata.org/ "Pandas")
* [mpi4py](http://mpi4py.scipy.org/ "mpi4py")

### Download

	pip install Hapi


## Project layout



*Above: Overview about functionality of the Hapi package*


	
	__init__.py             # Ensures that all needed files are loaded.
	
    algorithms/
        __init__.py   # Ensures the availability of all algorithms
	
	parallel/
		mpi.py        #Basic Parralel Computing features 

	examples/
		3dplot.py                   # Response surface plot of example files

