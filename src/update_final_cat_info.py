# #! /usr/bin/python
# #! utf+8
'''
update_final_cat_info.py: add calibration gauge coloumn considering multiple observations.
Obs_Type can be given as a list
'''
import pandas as pd 
import numpy as np 
import os
import sys
import params as pm
#===================
#===================
# read from params.py
finalcat_hru_info_name=pm.finalcat_hru_info()
Obs_Types=pm.ObsTypes() #give observation type or types as an array
#===================
# read finalcat_hru_info
finalcat_hru_info=pd.read_csv(finalcat_hru_info_name,index_col=False)
# finalcat_hru_info.drop(columns='Unnamed: 0',inplace=True)
# update finalcat_hru_info for multiple observations
# The calibration gauges
finalcat_hru_info['Calibration_gauge']=finalcat_hru_info[Obs_Types].eq(1).any(axis=1).astype(int)
# The lake observations
if 'Obs_WA' in Obs_Types[0]:
    finalcat_hru_info['Lake_obs']=finalcat_hru_info[Obs_Types].eq(1).any(axis=1).astype(int)
else:
    finalcat_hru_info['Lake_obs']=finalcat_hru_info[Obs_Types[1::]].eq(1).any(axis=1).astype(int)
# Update the validation gauges if 'Obs_SF_IS' not in Obs_Types:
for obs in Obs_Types:
    if 'Obs_SF' in obs:
        finalcat_hru_info.loc[finalcat_hru_info[obs]==1,['Validation_Gauge']]=1
finalcat_hru_info.to_csv(finalcat_hru_info_name, index=False)