# A third root functions


You will find the following example in the `03 A third root functions.py` file under the folder `/Examples`. There is no need for copy paste work.

this example tries to find the minimum value of `\sqrt[3]{(xy)^2}-x+y^2` where
`9 - x**2 - y**2 >= 0`.
It has three minimizers (2,3),(1,2), and (2,2):

	from Oasis.optimization import Optimization                    # Load the Optimization object
	from Oasis.hsapi import HSapi                                  # Load the Harmony search api object

	# define the objective functionand the constraints
    def objfunc(x):
        f = power(x[0]**2 * x[1]**2, 1. / 3.) - x[0] + x[1]**2
		# inequality Constraint: 9 - x**2 - y**2 >= 0
        g = [x[0]**2 + x[1]**2 - 9]
        print('inequality Constraint = ' + str(g))
        print('Obj Fn value = ' + str(f))
        fail = 0
        return f, g, fail

create the Optimization Object, add variables and Constraint:

	opt_prob = Optimization('A third root function', objfunc)
	opt_prob.addVar('x1', 'c', lower=-3, upper=3, value=0.0)
	opt_prob.addVar('x2', 'c', lower=-3, upper=3, value=0.0)
	opt_prob.addObj('f')
	opt_prob.addCon('g1', 'i')

	options = dict(filename ='results/03 A third root functions.txt')

Create Optimization solver Object (inhereted from the Optimizer)
check the docs of HSapi:

	opt_engine = HSapi(pll_type = "POA",options = options)

to use the hot start you have to store the history from a previous run with the
filename parameters in the option dictionary (HSapi) and the store_hst when
calling the optimizer

in the second run to use the history of the previous run just change hot_start
when calling the optimizer to True

	res = opt_engine(opt_prob, store_sol=True, display_opts=True, store_hst=True,
                 hot_start=True)

	print(opt_prob.solution(0))
