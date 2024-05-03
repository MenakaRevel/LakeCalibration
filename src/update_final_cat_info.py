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
finalcat_hru_info['Lake_obs']=finalcat_hru_info[Obs_Types[1::]].eq(1).any(axis=1).astype(int)
finalcat_hru_info.to_csv(finalcat_hru_info_name, index=False)