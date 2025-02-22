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
    #========================================================================
    # all basins calibration parameters for river routing
    f.write('\n# Calibration Parameters')
    f.write('\n:SBGroupPropertyMultiplier     Allsubbasins     MANNINGS_N      n_multi   # Manning`s n')
    f.write('\n:SBGroupPropertyMultiplier     Allsubbasins     Q_REFERENCE     q_multi   # Q_reference')
    # f.write(':SBGroupPropertyMultiplier     Allsubbasins     CELERITY        c_multi   # CELERITY\n')
    # f.write(':SBGroupPropertyMultiplier     Allsubbasins     DIFFUSIVITY     d_multi   # DIFFUSIVITY\n')
    f.write('\n')
    #========================================================================
    # list observed lakes
    if len(finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']==1) & (finalcat_hru_info['HRU_IsLake']==1) & (finalcat_hru_info['Obs_NM']!='02KB001')]['SubId']) > 0:
        print (finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']==1) & (finalcat_hru_info['HRU_IsLake']==1) & (finalcat_hru_info['Obs_NM']!='02KB001')]['SubId'])
        f.write('\n:SubBasinGroup   ObservedLakesubbasins')
        # loop through lake subbasins
        f.write('\n')
        # f.write('')
        if only_lake==1: 
            f.write(str(finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']==1) & (finalcat_hru_info['HRU_IsLake']==1) & (finalcat_hru_info['Obs_SF_IS']!=1)]['SubId'].unique()).replace('[','').replace(']',''))
        else:
            f.write(str(finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']==1) & (finalcat_hru_info['HRU_IsLake']==1)]['SubId'].unique()).replace('[','').replace(']',''))
        # f.write('\n')
        f.write('\n:EndSubBasinGroup')
        f.write('\n')
        f.write('\n:GaugedSubBasinGroup ObservedLakesubbasins')
        f.write('\n')
    #========================================================================
    # calibrate crest width for non observed lakes
    if CalIndCW == 'False': #len(Obs_Types)==1 and Obs_Types[0]=='Obs_SF_IS':
        f.write('\n')
        f.write('\n:SBGroupPropertyMultiplier  Allsubbasins   RESERVOIR_CREST_WIDTH k_multi # Lake crest width multipler')
        f.write('\n')
    else:
        f.write('\n')
        f.write('\n:SubBasinGroup   NonObservedLakesubbasins')
        # loop through lake subbasins
        f.write('\n')
        # f.write('')
        if only_lake==1: 
            f.write(str(finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']!=1) & (finalcat_hru_info['HRU_IsLake']==1) & (finalcat_hru_info['Obs_SF_IS']!=1)]['SubId'].unique()).replace('[','').replace(']',''))
        else:
            f.write(str(finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']!=1) & (finalcat_hru_info['HRU_IsLake']==1)]['SubId'].unique()).replace('[','').replace(']',''))
        # f.write('\n')
        f.write('\n:EndSubBasinGroup')
        f.write('\n:SBGroupPropertyMultiplier  NonObservedLakesubbasins   RESERVOIR_CREST_WIDTH k_multi')
        f.write('\n')
    #========================================================================
    # 921
    f.write('\n:SubBasinGroup   921subbasin')
    f.write('\n921')
    f.write('\n:EndSubBasinGroup')
    f.write('\n:SBGroupPropertyOverride  921subbasin   RESERVOIR_CREST_WIDTH 1.0E+20')