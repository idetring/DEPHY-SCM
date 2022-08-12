#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5 February 2022

@author: Igor Detring

"""
import sys
import datetime


## SCMS original case definition
## From Neggers et al 2003
def main(startdate):
  sys.path = ['../utils/',] + sys.path

  import netCDF4 as nc
  import numpy as np
  import xarray as xr

  import constants
  from Case import Case

  ################################################
  # 0. General configuration of the present script
  ################################################

  lplot = False # True # plot all the variables
  lverbose = False # True # print information about variables and case

  ################################################
  # 1. General information about the case
  ################################################
  startDate=startdate.strftime('%Y%m%d%H')

  case = Case('FESSTVaL',
          lat=52.16723,
          lon=-14.12224,
          startDate=startdate.strftime('%Y%m%d%H%M%S'),
          endDate=startdate.strftime('%Y%m%d%H%M%S'),
          surfaceType='land',
          zorog=0.)

  case.set_title("Forcing and initial conditions for FESSTVaL case")
  case.set_reference("FESSTVaL reference Paper...")
  case.set_author("I. Detring")
  case.set_comment("ICON-D2 00 forecast")
  case.set_modifications("Added soil variables tso and wso with dep_tso and dep_wso (depth) dimension")

  ################################################
  # 2. Input netCDF file (init_SCM file) - converting ICON init file to DEPHY
  ################################################
  initdate = startdate.strftime('%Y%m%d%H')
  initfile = f'{initdate}/init_SCM_data_ICOND2_{initdate}_lat52_lon14_dt1.0.nc'
  fin = xr.open_dataset(initfile)

  ################################################
  # 2. Initial state
  ################################################

  # Surface pressure
  ps = fin['psurf'][0].data
  case.add_init_ps(ps)

  #case.add_variable('ps',[ps,])

  z = fin['height'].isel(nt=0).data

  case.add_init_wind(u=fin['uIN'].isel(nt=0).data, v=fin['uIN'].isel(nt=0).data, lev=z, levtype='altitude')

  # Thermodynamical initial profiles
  # Altitude above the ground
  # z = np.genfromtxt('init.txt',dtype=None,skip_header=1,usecols=0)

  # Potential temperature
  # theta = np.genfromtxt('init.txt',dtype=None,skip_header=1,usecols=1)
  theta = fin['thIN'].isel(nt=0).data

  case.add_init_theta(theta, lev=z, levtype='altitude')

  # humidity
  # qv = np.genfromtxt('init.txt',dtype=None,skip_header=1,usecols=2)
  qv = fin['qvIN'].isel(nt=0).data
  case.add_init_qv(qv, lev=z, levtype='altitude')

  qc = fin['qcIN'].isel(nt=0).data
  case.add_init_variable('ql',qc,lev=z,levtype='altitude')

  qi = fin['qiIN'].isel(nt=0).data
  case.add_init_variable('qi',qi,lev=z,levtype='altitude')

  tke = fin['tkeIN'].isel(nt=0).data
  case.add_init_variable('tke',tke,lev=z,levtype='altitude')

  exner = fin['exnerIN'].isel(nt=0).data
  case.add_init_variable('exner',exner,lev=z,levtype='altitude')

  # soil variables
  tso = fin['T_SO'].isel(nt=0).data
  case.add_init_variable('tso',tso,lev=fin['depth_T'].data*-1,levtype='depth',levid='dep_tso')

  wso = fin['W_SO'].isel(nt=0).data
  case.add_init_variable('wso',wso,lev=fin['depth_W'].data*-1,levtype='depth',levid='dep_wso')


  ################################################
  # 3. Forcing
  ################################################

  # Constant Geostrophic wind across the simulation
  ug = fin['uGEO'].data
  vg = fin['vGEO'].data
  time = fin['time'].data
  time = (time - time[0]) / np.timedelta64(1, 's')
  case.add_geostrophic_wind(ug=ug,vg=vg,lev=z,levtype='altitude',time=time)

  u = fin['uIN'].data
  v = fin['vIN'].data
  w = fin['wIN'].data
  case.add_wind_nudging(unudg=u,vnudg=v,ulev=z,vlev=z,time=time,levtype='altitude',timescale=3600,z_nudging=2000)

  case.add_surface_pressure_forcing(fin['psurf'].data,time=time)

  u_adv = fin['dUadv'].data
  v_adv = fin['dVadv'].data
  case.add_forcing_variable('tnua_adv',u_adv,time=time,lev=z,levtype='altitude')
  case.add_forcing_variable('tnva_adv',v_adv,time=time,lev=z,levtype='altitude')


  # Potential temperature and water vapor mixing ratio advectionfin

  theta_adv = fin['dTadv'].data
  qv_adv    = fin['dQVadv'].data

  case.add_theta_advection(theta_adv,lev=z,levtype='altitude',time=time)
  case.add_rv_advection(qv_adv,lev=z,levtype='altitude',time=time)
  case.add_variable('tke',fin['tkeIN'].data,lev=z,levtype='altitude',time=time)


  # Surface Forcing
  # timeSfc = np.genfromtxt('surface_forcing.txt',dtype=None,skip_header=1,usecols=0)
  timeSfc = time
  # shf = np.genfromtxt('surface_forcing.txt',dtype=None,skip_header=1,usecols=1)
  shf = fin['sfc_sens_flx'].data
  # lhf = np.genfromtxt('surface_forcing.txt',dtype=None,skip_header=1,usecols=2)
  lhf = fin['sfc_lat_flx'].data
  ustar = fin['ustar'].data

  case.add_surface_fluxes(sens=shf,lat=lhf,time=timeSfc,forc_wind='ustar',ustar=ustar,time_ustar=time)

  ################################################
  # 4. Writing file
  ################################################

  case.write(f'{startDate}/FESSTVaL_REF_DEF_driver.nc')

  if lverbose:
      case.info()

  ################################################
  # 5. Ploting, if asked
  ################################################

  if lplot:
      case.plot(rep_images=f'./{startDate}/images/driver_DEF/',timeunits='hours')


if __name__ == '__main__':
  initdate = sys.argv[1]
  initdate = datetime.datetime.strptime(initdate, '%Y%m%d%H') # is string -> datetime -> string conversion necessary or helpful?
  main(initdate)