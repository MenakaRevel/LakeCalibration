# #! /usr/bin/python
# #! utf+8
'''
update_rvh_tpl.py: update the rvh.tpl file for NonObservedLakesubbasins

add 
:SubBasinGroup   NonObservedLakesubbasins
xxx
:EndSubBasinGroup 
:SBGroupPropertyMultiplier  NonObservedLakesubbasins   RESERVOIR_CREST_WIDTH k_multi
'''
import pandas as pd 
import numpy as np 
import os
import sys
import params as pm
#===================
rvh_tpl=sys.argv[1]
#===================
# read from params.py
finalcat_hru_info=pm.finalcat_hru_info()
only_lake=pm.only_lake_obs()  # True | False --> only lake observations or any observation
Obs_Types=pm.ObsTypes()
CalIndCW=pm.CaliCW()
# print (len(Obs_Types), Obs_Types[0])
#===================
# read finalcat_hru_info
finalcat_hru_info=pd.read_csv(finalcat_hru_info)
#===================
with open(rvh_tpl,'a') as f:
    if CalIndCW == 'False': #len(Obs_Types)==1 and Obs_Types[0]=='Obs_SF_IS':
        f.write('\n')
        f.write(':SBGroupPropertyMultiplier  Allsubbasins   RESERVOIR_CREST_WIDTH k_multi\n')
        f.write('\n')
    else:
        f.write('\n')
        f.write(':SubBasinGroup   NonObservedLakesubbasins\n')
        # loop through lake subbasins
        f.write(' ')
        if only_lake==1: 
            f.write(str(finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']!=1) & (finalcat_hru_info['HRU_IsLake']==1) & (finalcat_hru_info['Obs_SF_IS']!=1)]['SubId'].unique()).replace('[','').replace(']',''))
        else:
            f.write(str(finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']!=1) & (finalcat_hru_info['HRU_IsLake']==1)]['SubId'].unique()).replace('[','').replace(']',''))
        f.write('\n')
        f.write(':EndSubBasinGroup\n')
        f.write(':SBGroupPropertyMultiplier  NonObservedLakesubbasins   RESERVOIR_CREST_WIDTH k_multi\n')
        f.write('\n')
    f.write(':SubBasinGroup   921subbasin\n')
    f.write('\t921\n')
    f.write(':EndSubBasinGroup\n')
    f.write(':SBGroupPropertyOverride  921subbasin   RESERVOIR_CREST_WIDTH 1.0E+20\n')