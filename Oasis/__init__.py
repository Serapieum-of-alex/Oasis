__author__ = 'Mostafa Farrag'
__version__ = '1.0.0'

__docformat__ = 'restructuredtext'

# import os,sys

from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration


# def configuration(parent_package, top_path):

#     config = Configuration('Oasis', parent_package, top_path)

#     # need: auto add_subpackage from source availability
#     config.add_subpackage('NSGA')

#     return config

# setup(**configuration(top_path='').todict())

def configuration(parent_package='',top_path=None):

    from numpy.distutils.misc_util import Configuration

    config = Configuration(None,parent_package,top_path)
    config.set_options(
        ignore_setup_xxx_py=True,
        assume_default_configuration=True,
        delegate_options_to_subpackages=True,
        quiet=True,
    )

    config.add_subpackage('NSGA')
    config.add_subpackage('HS')

    return config

import Oasis.constraint as constraint
import Oasis.objective as objective
import Oasis.variable as variable
import Oasis.parameter as parameter
import Oasis.history as history
import Oasis.gradient as gradient
import Oasis.optimization as optimization
import Oasis.optimizer as optimizer


# import Oasis.hsapi as hsapi
# from Oasis.HS import *
import Oasis.harmonysearch as harmonysearch
import Oasis.ga as ga
# from Oasis.NSGA import *


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