#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 03 January 2020

@author: Romain Roehrig

Update all driver files
"""

import os
import shutil

import available_cases as AA

# Current directory
cwd = os.getcwd()

for case in AA.cases:
    for subcase in AA.subcases[case]:
        print("#"*60)
        print("CASE: {0}, SUBCASE: {1}".format(case,subcase))
        tmp = os.path.join(cwd,case,subcase)
        os.chdir(tmp)

        try:
            shutil.rmtree('images')
        except:
            pass

        cmd = "python driver_DEF.py"
        os.system(cmd)
        cmd = "python driver_SCM.py"
        os.system(cmd)

        #try:
        #    os.remove('.DS_Store')
        #except OSError:
        #    pass

        #print os.listdir('./')


