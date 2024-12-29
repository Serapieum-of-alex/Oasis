__author__ = 'Mostafa Farrag'
__version__ = '1.0.2'

__docformat__ = 'restructuredtext'

import Oasis.constraint as constraint
import Oasis.objective as objective
import Oasis.variable as variable
import Oasis.parameter as parameter
import Oasis.history as history
import Oasis.gradient as gradient
import Oasis.optimization as optimization
import Oasis.optimizer as optimizer



import Oasis.harmonysearch as harmonysearch

# module level doc-string
__doc__ = """

Oasis is a Harmony search optimization algorithm which uses stochastic random
search based on two factors, harmony memory consideration rate and (HMCR) and
pitch adjusting rate (PAR). The main difference between GA and HS is that GA
evaluates many solutions simultaneously which may lead to convergence on a
local minimum, whereas HS evaluates only one solution at each iteration which
enables the algorithm of broad search and avoids convergence to local minima,
HS generates a new offspring after considering all the existing population
whereas GA only consider the two parent to generate a new offspring
(Lee and Geem 2005).
"""