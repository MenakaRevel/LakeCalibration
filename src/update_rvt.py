'''
update_rvt.py: add calibration observation rvt files
e.g., :RedirectToFile    ./obs/SF_02KB001_921.rvt  
'''
import pandas as pd 
import numpy as np 
import os
import sys
import params as pm
#===================
rvt=pm.RavenDir()+'/'+str(sys.argv[1])+'.rvt'
#===================
# read from params.py
finalcat_hru_info=pm.finalcat_hru_info()
only_lake=pm.only_lake_obs()  # True | False --> only lake observations or any observation
Obs_Types=pm.ObsTypes() #give observation type or types as an array
#===================
# read finalcat_hru_info
finalcat_hru_info=pd.read_csv(finalcat_hru_info)
#===================
#
rvt_string={'SF_IS':'In-situ Stream Flow Observation',
           'WL_IS':'In-situ Lake Water Level Observation',
           'WA_IS':'In-situ Lake Water Area ',
           'SF_RS':'Remotely-sensed In-situ Stream Flow Observation',
           'WL_RS':'Remotely-sensed In-situ Lake Water Level Observation',
           'WA_RS':'Remotely-sensed Lake Water Area ',
           'SF_SY':'Sythetic Stream Flow Observation',
           'WL_SY':'Sythetic Lake Water Level Observation',
           'WA_SY':'Sythetic Lake Water Area ',
}
#===================
valGaugeName={'Little Madawaska Barometer': 'LittleMadawaska',
              'Petawawa River at Narrowbag': 'PetawawaRNarrowbag',
              'Crow River': 'Crow',
              'Nipissing River': 'NippissingCorrected'
}
#===================
counter=0
with open(rvt,'a') as f:
    for ObsType in Obs_Types:
        # get the calibration gauges
        if ObsType=='Obs_SF_IS':
            calGag=finalcat_hru_info.loc[(finalcat_hru_info['Calibration_gauge']==1) & (finalcat_hru_info[ObsType]==1),'Obs_NM'].unique()
        else:
            calGag=finalcat_hru_info.loc[(finalcat_hru_info['Calibration_gauge']==1) & (finalcat_hru_info[ObsType]==1),'HyLakeId'].dropna().unique()
        # suffix for file name
        suffix=ObsType[4:9] # XX_YY
        f.write('\n# '+rvt_string[suffix])
        for gaguge in calGag:
            if ObsType=='Obs_SF_IS':
                subid=finalcat_hru_info[finalcat_hru_info['Obs_NM']==gaguge]['SubId'].dropna().values[0]
                Obs_NM=gaguge
            else:
                # print (gaguge, finalcat_hru_info[finalcat_hru_info['HyLakeId']==gaguge])
                subid=int(finalcat_hru_info[finalcat_hru_info['HyLakeId']==gaguge]['SubId'].dropna().values[0])
                try:
                    Obs_NM=finalcat_hru_info[finalcat_hru_info['HyLakeId']==gaguge]['Obs_NM'].dropna().values[0]
                except:
                    Obs_NM=str(gaguge)
                gaguge=int(gaguge)
            filename='./obs/'+suffix+'_'+str(gaguge)+'_'+str(int(subid))+'.rvt'
            # print ('\n%-19s%-30s #%s'%(':RedirectToFile',filename,str(Obs_NM)))
            f.write('\n%-19s%-30s#%s'%(':RedirectToFile',filename,str(Obs_NM)))
        f.write('\n')
        f.write('\n# Weight to remove winter period [Dec-1 - Apr-1]')
        for gaguge in calGag:
            if ObsType=='Obs_SF_IS':
                subid=finalcat_hru_info[finalcat_hru_info['Obs_NM']==gaguge]['SubId'].dropna().values[0]
                Obs_NM=gaguge
            else:
                # print (gaguge, finalcat_hru_info[finalcat_hru_info['HyLakeId']==gaguge])
                subid=int(finalcat_hru_info[finalcat_hru_info['HyLakeId']==gaguge]['SubId'].dropna().values[0])
                # Obs_NM=finalcat_hru_info[finalcat_hru_info['HyLakeId']==gaguge]['Obs_NM'].dropna().values[0]
                gaguge=int(gaguge)
            filename='./obs/'+suffix+'_'+str(gaguge)+'_'+str(int(subid))+'_weight.rvt'
            # print ('\n%-19s%s'%(':RedirectToFile',filename))
            f.write('\n%-19s%s'%(':RedirectToFile',filename))
        f.write('\n')
        f.write('\n')
    #========================================    
    # write the validation gauges [discharge]
    f.write('\n# Discharge stream [for validation]')
    valGag=finalcat_hru_info.loc[finalcat_hru_info['Validation_Gauge']==1,'Obs_NM'].unique()
    suffix='SF_IS'
    for valObs in valGag:
        # print (valObs)
        subid=finalcat_hru_info[finalcat_hru_info['Obs_NM']==valObs]['SubId'].dropna().values[0]
        filename='./obs/'+suffix+'_'+str(valGaugeName[valObs])+'_'+str(int(subid))+'.rvt'
        f.write('\n%-19s%-40s #%s'%(':RedirectToFile',filename, valObs))
    f.write('\n')
    f.write('\n# Weight to remove winter period [Dec-1 - Apr-1]')
    for valObs in valGag:
        # print (valObs)
        subid=finalcat_hru_info[finalcat_hru_info['Obs_NM']==valObs]['SubId'].dropna().values[0]
        filename='./obs/'+suffix+'_'+str(valGaugeName[valObs])+'_'+str(int(subid))+'_weight.rvt'
        f.write('\n%-19s%s'%(':RedirectToFile',filename))
    #========================================
    # write the validation gauges [water level]
    f.write('\n')
    f.write('\n# Water Level Stream [for validation]')
    valGag=finalcat_hru_info.loc[finalcat_hru_info['Validation_Gauge']==1,'Obs_NM'].unique()
    suffix='WL_IS'
    for valObs in valGag:
        # print (valObs)
        subid=finalcat_hru_info[finalcat_hru_info['Obs_NM']==valObs]['SubId'].dropna().values[0]
        filename='./obs/'+suffix+'_'+str(valGaugeName[valObs])+'_'+str(int(subid))+'.rvt'
        f.write('\n%-19s%-40s #%s'%(':RedirectToFile',filename, valObs))
    f.write('\n')
    f.write('\n# Weight to remove winter period [Dec-1 - Apr-1]')
    for valObs in valGag:
        # print (valObs)
        subid=finalcat_hru_info[finalcat_hru_info['Obs_NM']==valObs]['SubId'].dropna().values[0]
        filename='./obs/'+suffix+'_'+str(valGaugeName[valObs])+'_'+str(int(subid))+'_weight.rvt'
        f.write('\n%-19s%s'%(':RedirectToFile',filename))
