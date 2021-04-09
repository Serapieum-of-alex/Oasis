[![PyPI version](https://badge.fury.io/py/Oasis-Optimization.svg)](https://badge.fury.io/py/Oasis-Optimization)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/oasis/badges/version.svg)](https://anaconda.org/conda-forge/oasis)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/oasis/badges/platforms.svg)](https://anaconda.org/conda-forge/oasis)
[![Python Versions](https://img.shields.io/pypi/pyversions/Oasis-Optimization.png)](https://img.shields.io/pypi/pyversions/Oasis-Optimization)
[![Build Status](https://travis-ci.org/MAfarrag/Oasis.svg?branch=master)](https://travis-ci.org/MAfarrag/Oasis)

[![Documentation Status](https://readthedocs.org/projects/oasis-optimization/badge/?version=latest)](https://oasis-optimization.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MAfarrag/Oasis/master)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/oasis/badges/downloads.svg)](https://anaconda.org/conda-forge/oasis)
[![Downloads](https://pepy.tech/badge/oasis-optimization)](https://pepy.tech/project/oasis-optimization)
[![Downloads](https://pepy.tech/badge/oasis-optimization/month)](https://pepy.tech/project/oasis-optimization)
[![Downloads](https://pepy.tech/badge/oasis-optimization/week)](https://pepy.tech/project/oasis-optimization)

Current build status
====================


<table><tr><td>All platforms:</td>
    <td>
      <a href="https://dev.azure.com/conda-forge/feedstock-builds/_build/latest?definitionId=12400&branchName=master">
        <img src="https://dev.azure.com/conda-forge/feedstock-builds/_apis/build/status/oasis-feedstock?branchName=master">
      </a>
    </td>
  </tr>
</table>


Oasis - Optimization Algorithm for Python 
===================================================================== 


Installation
============
```
Please install Oasis in a Virtual environment so that its requirements don't tamper with your system's python
**Oasis** works with Python 2.7 and 3.7 64Bit on Windows
```
# Install the dependencies
you can check [libraries.io](https://libraries.io/pypi/Oasis-Optimization) to check versions of the libraries
```
conda install Numpy
pip install mpi4py
```
## Install from conda-forge
```
conda install -c conda-forge oasis
```
## Install from Github
to install the last development to time you can install the library from github
```
pip install git+https://github.com/MAfarrag/Oasis.git
```
## Compile 
You can compile the repository after you clone it 
iF python is already added to your system environment variable
```
python setup.py install
```
###### or 
```
pathto_your_env\python setup.py install
```
## pip
to install the last release you can easly use pip
```
pip install Oasis-Optimization
```
## YML file
using the environment.yml file included with hapi you can create a new environment with all the dependencies installed with the latest Hapi version
in the master branch
```
conda env create --name Hapi_env -f environment.yml
```
# Documentation
for step by step Examples and documentation on how to use the algorithm [readthedocs](https://oasis-optimization.readthedocs.io/en/latest/)

