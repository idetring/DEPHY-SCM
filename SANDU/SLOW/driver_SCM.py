#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 09 January 2021

@author: Romain Roehrig
"""

## SANDU/SLOW composite case SCM-enabled definition

import sys
sys.path = ['../../utils/',] + sys.path

import numpy as np

from Case import Case

################################################
# 0. General configuration of the present script
################################################

case_name = 'SANDU'
subcase_name = 'SLOW'
title = "Forcing and initial conditions for SANDU composite slow case - SCM-enabled version"

lplot = True     # plot the new version of the case
lcompare = True  # plot comparisons between original and new versions
lverbose = False # print information on variables and case

################################################
# 1. Get the original version of the case
################################################

# initialize the case structure for the original version
case = Case('{0}/{1}'.format(case_name,subcase_name))

# read case information in file
case.read('{0}_{1}_DEF_driver.nc'.format(case_name,subcase_name))

# display some information about the case
if lverbose:
    case.info()

################################################
# 2. Interpolate onto a new grid, same for all the variables
#    and add new variables if needed
################################################

# grid onto which interpolate the input data

# New vertical grid, 10-m resolution from surface to 50000 m (above the surface)
levout = np.array(range(0,47971,10),dtype=np.float64) 

# New temporal grid, from 18:00 UTC, 15 July 2006 to 18:00 UTC 18 July 2006, 30-minute timestep
timeout = np.arange(0.,(72+1)*3600.,1800.)

# conversion 
# Both temp and thetal are provided for nudging. Use only temp (better for vertical interpolation)
newcase = case.convert2SCM(time=timeout,lev=levout,levtype='altitude',usetemp=True,usetheta=False,usethetal=False)

# update some attributes
newcase.set_title(title)
newcase.set_script("DEPHY-SCM/{0}/{1}/driver_SCM.py".format(case_name,subcase_name))

# display some information about the new version of the case
if lverbose:
    newcase.info()

################################################
# 3. Save new version of the case in netcdf file
################################################

# save the new version of the case in netcdf file 
newcase.write('{0}_{1}_SCM_driver.nc'.format(case_name,subcase_name))

################################################
# 4. Plots if asked
################################################

if lplot:
    newcase.plot(rep_images='./images/driver_SCM/',timeunits='hours')

if lcompare:
    newcase.plot_compare(case,rep_images='./images/compare/',label1="SCM-enabled",label2="Original",timeunits='hours')
