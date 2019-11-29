#!/usr/bin/env python

import os,sys

from .Oasis_history import History
from .Oasis_parameter import Parameter
from .Oasis_variable import Variable
from .Oasis_gradient import Gradient
from .Oasis_constraint import Constraint
from .Oasis_objective import Objective
from .Oasis_optimization import Optimization
from .Oasis_optimizer import Optimizer

__all__ = ['History','Parameter','Variable','Gradient','Constraint','Objective','Optimization','Optimizer']

dir = os.path.dirname(os.path.realpath(__file__))
for f in os.listdir(dir):
    if f.startswith('py') and os.path.isdir(os.path.join(dir,f)):
        try:
            exec('from .%s import %s' %(f,f.strip('py')))
            __all__.extend(sys.modules['Oasis.'+f].__all__)
        except Exception as e:
            continue
