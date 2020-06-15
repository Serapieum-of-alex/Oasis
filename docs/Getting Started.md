# Getting started

To start your experience with Oasis you need to have Oasis installed. Please see the [Installation chapter](Installation.md) for further details.

You will find the following example in the `01 Equality Constraint.py` file under the folder `/Examples`. There is no need for copy paste work.

To use Oasis we have to import it and use one of the pre-build examples:

	from Oasis.optimization import Optimization                    # Load the Optimization object
	from Oasis.hsapi import HSapi                                  # Load the Harmony search api object

this example tries to find the minimum value of x**2+y**2+z**4 where x+y+z=4
# first define the general function that conains the objective function and the constraints