#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 01 October 2020

@author: Etienne Vignon
"""

## MPACE SCM-enabled case definition

import sys
sys.path = ['../../utils/',] + sys.path

import numpy as np

from Case import Case

################################################
# 0. General configuration of the present script
################################################

lplot = True     # plot the new version of the case
lcompare = True  # plot comparisons between original and new versions
lverbose = False # print information on variables and case

################################################
# 1. Get the original version of the case
################################################

# initialize the case structure for the original version
case = Case('MPACE/REF')

# read case information in file
case.read('MPACE_REF_DEF_driver.nc')

# display some information about the case
if lverbose:
    case.info()

################################################
# 2. Interpolate onto a new grid, same for all the variables
#    and add new variables if needed
################################################

# grid onto which interpolate the input data

# New vertical grid, 10-m resolution from surface to 6000 m (above the surface)
#levout = np.array(range(0,6001,10),dtype=np.float64) 

# New temporal grid, from 17:00 UTC, 09 October 2004 to 05:00 UTC, 10 October 2004, 1-hour timestep
#timeout = np.array(range(0,43201,3600),dtype=np.float64) 

# conversion
newcase = case.convert2SCM()


# update some attributes
newcase.set_title("Forcing and initial conditions for MPACE/REF case - SCM-enabled version")
newcase.set_script("driver_SCM.py")

# display some information about the new version of the case
if lverbose:
    newcase.info()

################################################
# 3. Save new version of the case in netcdf file
################################################

# save the new version of the case in netcdf file 
newcase.write('MPACE_REF_SCM_driver.nc')

################################################
# 4. Plots if asked
################################################

if lplot:
    newcase.plot(rep_images='./images/driver_SCM/',timeunits='hours')

if lcompare:
    newcase.plot_compare(case,rep_images='./images/compare/',label1="SCM-enabled",label2="Original",timeunits='hours')
