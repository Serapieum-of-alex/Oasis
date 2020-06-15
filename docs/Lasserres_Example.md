# Lasserre's Example


You will find the following example in the `02 Lasserre.py` file under the folder `/Examples`. There is no need for copy paste work.

this example tries to find the minimum value of `−(x−1)2−(x−y)2−(y−3)2` where
`1−(x−1)2≥0`, `1−(x−y)2≥0` and `1−(y−3)2≥0`.
It has three minimizers (2,3),(1,2), and (2,2):

	from Oasis.optimization import Optimization                    # Load the Optimization object
	from Oasis.hsapi import HSapi                                  # Load the Harmony search api object

	# define the objective functionand the constraints
	# equality constraint has to come before inequality constraint
	def objfunc(x):
        # Objective function
        f = -(x[0] - 1)**2 - (x[0] - x[1])**2 - (x[1] - 3)**2
        # Equality constraint
        g = [ (x[0] - 1)**2 - 1,
             (x[0] - x[1])**2 - 1,
             (x[1] - 3)**2 - 1]
        # print('Equality Constraint = ' + str(g))
        # print('Obj Fn value = ' + str(f))
        fail = 0
        return f, g, fail

create the Optimization Object:

	opt_prob = Optimization("Lasserre's Example", objfunc)

define the decision variables to the Optimization Object:

	opt_prob.addVar('x1', 'c', lower=-3, upper=3, value=0.0)
	opt_prob.addVar('x2', 'c', lower=-3, upper=3, value=0.0)

define the objective function to the Optimization Object:

	opt_prob.addObj('f')

define the inequality Constraint to the Optimization Object:

	opt_prob.addCon('g1', 'i')
	opt_prob.addCon('g2', 'i')
	opt_prob.addCon('g3', 'i')

create the options dictionary all the optimization parameters should be passed
to the optimization object inside the option dictionary:

	options = dict(hms=50, stopiters=1, fileout = 1, filename ='results/Lasserre.txt',
					prtinniter = 1, prtoutiter = 1, xinit = 1)

Create Optimization solver Object (inhereted from the Optimizer)
check the docs of HSapi:

	opt_engine = HSapi(pll_type = None,options = options)

call the solver to start the optimization process
First the Optimizer object is going to check the order of the constraints
call the optimizer (optimizer.__call__) then hs solver (HSapi.__solve__)
Equality constraints have to come before inequality constraints:

	res = opt_engine(opt_prob, store_sol=True, display_opts=True, store_hst=False,
    	             hot_start=False)

	print(opt_prob.solution(0))
