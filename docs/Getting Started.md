# Getting started

To start your experience with Oasis you need to have Oasis installed. Please see the [Installation chapter](Installation.md) for further details.

You will find the following example in the `01 Equality Constraint.py` file under the folder `/Examples`. There is no need for copy paste work.

To use Oasis we have to import it and use one of the pre-build examples:

	from Oasis.optimization import Optimization                    # Load the Optimization object
	from Oasis.hsapi import HSapi                                  # Load the Harmony search api object


this example tries to find the minimum value of `x**2+y**2+z**4` where `x+y+z=4`

first define the general function that conains the objective function and the constraints
Equality constraint has to come before inequality constraint:

	def objfunc(x):
		# Objective function
		f = x[0]**2 + x[1]**2 + x[2]**4
		# Equality constraint
		g = [x[0] + x[1] + x[2] - 4]
		# print('Equality Constraint = ' + str(g))
		# print('Obj Fn value = ' + str(f))
		fail = 0
		return f, g, fail


create the Optimization Object:

	opt_prob = Optimization('Testing solutions', objfunc)

define the decision variables to the Optimization Object

addVar method takes 4 parameters

Parameters:
    - name:
        [String]: Variable Name
    - Vartype:
        [String]: Variable Type ('c'-continuous, 'i'-integer,
                'd'-discrete), *Default* = 'c'
    - value:
        [numeric]: Variable Value, Default = 0.0
    - lower:
        [numeric]: Variable Lower Value, for continuous and integer variables
    - upper:
        [numeric]: Variable Upper Value, for continuous and integer variables
    - choices:
        [List]: Variable Choices, for discrete valiables

addVar method of the optimization object calls the Variable Object

to use the values of the variables as initial values in the search for the optimal
set of values set the "xinit" in the Optimization options to 1
options = dict(xinit = 1) :

	opt_prob.addVar('x1', 'c', lower=-4, upper=4, value=0.0)
	opt_prob.addVar('x2', 'c', lower=-4, upper=4, value=0.0)
	opt_prob.addVar('x3', 'c', lower=-4, upper=4, value=0.0)

define the objective function to the Optimization Object
f is the name of the function inside the objfunc defined above:

	opt_prob.addObj('f')

define the Equality Constraint to the Optimization Object:

	opt_prob.addCon('g1', 'e')

create the options dictionary all the optimization parameters should be passed
to the optimization object inside the option dictionary:

	options = dict(hms=50, stopiters=1, fileout = 1, filename ='results/EqualityConstraint.txt',
					prtinniter = 1, prtoutiter = 1, xinit = 1)

Create Optimization solver Object (inhereted from the Optimizer)
check the docs of HSapi:

	opt_engine = HSapi(pll_type = None,options = options)

call the solver to start the optimization process
First the Optimizer object is going to check the order of the constraints
call the optimizer (optimizer.__call__) then hs solver (HSapi.__solve__)
Equality constraints have to come before inequality constraints:

	res = opt_engine(opt_prob, store_sol=True, display_opts=True, store_hst=False,
    	             hot_start=False) # filename="EqualityConstraint1.txt"

	print(opt_prob.solution(0))
