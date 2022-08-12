#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 5 February 2022

@author: Igor Detring
"""
import sys
import datetime

## FESSTVaL SCM-enabled case definition
def main(startdate):
    import sys
    sys.path = ['../utils/',] + sys.path
    import numpy as np
    from Case import Case

    startDate=startdate.strftime('%Y%m%d%H')

    ################################################
    # 0. General configuration of the present script
    ################################################

    lplot = True    # plot the new version of the case
    lcompare = True  # plot comparisons between original and new versions
    lverbose = True # print information on variables and case

    ################################################
    # 1. Get the original version of the case
    ################################################

    # initialize the case structure for the original version
    case = Case('FESSTVaL')

    # read case information in file
    case.read(f'{startDate}/FESSTVaL_REF_DEF_driver.nc')

    # display some information about the case
    if lverbose:
        case.info()

    ################################################
    # 2. Interpolate onto a new grid, same for all the variables
    #    and add new variables if needed
    ################################################

    # grid onto which interpolate the input data

    # New vertical grid, 10-m resolution from surface to 6000 m (above the surface)
    levout = np.array(range(0,6001,10),dtype=np.float64) 
    # New temporal grid, from 11:30 UTC, 21 June 1997 to 02:00 UTC, 22 June 1997, 30-min timestep
    timeout = np.array(range(0,86400+1,3600),dtype=np.float64) 
    # conversion
    newcase = case.convert2SCM(time=timeout,lev=levout,levtype='altitude')
    depout = np.array(range(-20,0,1),dtype=np.float64)
    depout = np.array(np.unique(list(newcase.variables['tso'].height.data[0]) + list(newcase.variables['wso'].height.data[0])))
    newcase = newcase.interpolate(time=timeout,lev=depout,levtype='depth')
    # add a surface temperature. To be improved...
    ts = timeout*0. + 310 # same shape as timeout
    newcase.add_variable('ts',ts,time=timeout,timeid='time')
    # update some attributes
    newcase.set_title("Forcing and initial conditions for FESSTVaL REAL - SCM-enabled version")
    newcase.set_script("DEPHY-SCM/FESSTVaL/driver_SCM.py")
    # display some information about the new version of the case
    if lverbose:
        newcase.info()
    ################################################
    # 3. Save new version of the case in netcdf file
    ################################################
    # save the new version of the case in netcdf file 
    newcase.write('/hpc/uwork/idetring/routscm/DEPHY-SCM/FESSTVaL/%s/FESSTVaL_REF_SCM_driver.nc' % startDate)

    ################################################
    # 4. Plots if asked
    ################################################

    if lplot:
        newcase.plot(rep_images='./images/driver_SCM/',timeunits='hours')

    if lcompare:
        newcase.plot_compare(case,rep_images='./images/compare/',label1="SCM-enabled",label2="Original",timeunits='hours')


if __name__ == '__main__':
    initdate = sys.argv[1]
    initdate = datetime.datetime.strptime(initdate, '%Y%m%d%H') # is string -> datetime -> string conversion necessary or helpful?
    main(initdate)