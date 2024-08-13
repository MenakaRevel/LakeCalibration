# #! /usr/bin/python
# #! utf+8
'''
create_cw_para_tpl.py: create crest_width_par.csv.tpl file using the observed lakes

create csv.tpl file with Hylakid and w_{Hylakid}
'''
import pandas as pd 
import numpy as np 
import os
import sys
import params as pm
#===================
csv_tpl=sys.argv[1]
#===================
# read from params.py
finalcat_hru_info=pm.finalcat_hru_info()
only_lake=pm.only_lake_obs()  # True | False --> only lake observations or any observation
Obs_Types=pm.ObsTypes()
#===================
# read finalcat_hru_info
finalcat_hru_info=pd.read_csv(finalcat_hru_info)
# CW_list=['w_%d'%(HyLakeId) for HyLakeId in finalcat_hru_info[(finalcat_hru_info[Obs_Type]==1) & (finalcat_hru_info['HRU_IsLake']==1)]['HyLakeId'].unique()]
# colnames=['%d'%(HyLakeId) for HyLakeId in finalcat_hru_info[(finalcat_hru_info[Obs_Type]==1) & (finalcat_hru_info['HRU_IsLake']==1)]['HyLakeId'].unique()]

if only_lake==1: 
    CW_dict=dict([('%d'%(HyLakeId),'w_%d'%(HyLakeId)) for HyLakeId in finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']==1) & (finalcat_hru_info['HRU_IsLake']==1) & (finalcat_hru_info['Lake_obs']==1)]['HyLakeId'].unique()])
else:
    CW_dict=dict([('%d'%(HyLakeId),'w_%d'%(HyLakeId)) for HyLakeId in finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']==1) & (finalcat_hru_info['HRU_IsLake']==1)]['HyLakeId'].unique()])
# print (CW_dict)
# print (CW_list)
# df_cw_para=pd.DataFrame(data=np.transpose(np.array(CW_list)), columns=colnames)
df_cw_para=pd.DataFrame(CW_dict,index=[0])
print (df_cw_para)

df_cw_para.to_csv(csv_tpl,index=False)