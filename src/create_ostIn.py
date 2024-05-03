'''
create_ostIn.py    : create the ostIn.txt file
input: 
    outname    : 'ostIn.txt'
    final_cat  : final_cat_info 
    RavenDir   : RavenInput folder
    progType   : 'DDS' #ShuffledComplexEvolution
    objFunc    : 'GCOP'
    RandomSeed : Random number
    MaxIter    : number of trials
    only_lake  : only lake observations used lake CW calibration
    ObsTypes   : observation types
output:
    create the ostIn.txt file
'''
import pandas as pd 
import numpy as np 
import os
import sys
import re
import params as pm
#====================
def read_cal_gagues(RavenDir):
    # Define a regular expression pattern to match the desired lines
    pattern = r'^:RedirectToFile\s+\.\/obs\/(.*?)(?<!_weight)\.rvt'

    # Open the file and read its lines
    with open(RavenDir+"/Petawawa.rvt", 'r') as file:
        lines = file.readlines()

    # Extract values matching the pattern starting from line 39
    values = []
    skip_lines = False
    for line in lines[38:]:
        if 'validation' in line:
            skip_lines = True
            continue
        elif skip_lines:
            break
        
        match = re.match(pattern, line)
        if match:
            values.append(match.group(1))
    return values
#====================
def read_evaluation_met(RavenDir):
    # Define a regular expression pattern to match the desired line
    pattern = r'^:EvaluationMetrics\s+(.*)$'

    # Open the file and read its lines
    with open(RavenDir+"/Petawawa.rvi", 'r') as file:
        lines = file.readlines()

    # Extract the list of evaluation metrics
    evaluation_metrics = []
    for line in lines:
        match = re.match(pattern, line)
        if match:
            evaluation_metrics = match.group(1).split()

    # return list of evaluation metrics
    return evaluation_metrics
#====================
def divide_chunks(l, n): 
    # Yield successive n-sized 
    # chunks from l. 
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
#====================
ostin=sys.argv[1]
RandomSeed=sys.argv[2]
MaxIter=sys.argv[3]
#===================
# read from params.py
Obs_Types=pm.ObsTypes() #give observation type or types as an array
RavenDir=pm.RavenDir()
progType=pm.ProgramType()
objFunc=pm.ObjectiveFunction()
only_lake=pm.only_lake_obs() # 1 --> only lake | 0     observations or any    observation
costFunc=pm.CostFunction()
#====================
# read finalcat_hru_info
finalcat_hru_info=pd.read_csv(pm.finalcat_hru_info())
# get the lake observation list
if only_lake==1:    
    CW_para_list=finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']==1) & (finalcat_hru_info['HRU_IsLake']==1) &    (finalcat_hru_info['Lake_obs']==1)]['HyLakeId'].unique()
else:
    CW_para_list=finalcat_hru_info[(finalcat_hru_info['Calibration_gauge']==1) & (finalcat_hru_info['HRU_IsLake']==1)]['HyLakeId'].unique()
#====================
# coefficient lower    and    upper bounds for the CW
lowCW=0.1
upCW=1.6
#====================
with open(ostin, 'w') as f:
    f.write(     'ProgramType          '+str(progType)              )
    f.write('\n'+'ObjectiveFunction    '+str(objFunc)              )
    f.write('\n'+'ModelExecutable      ./Ost-RAVEN.sh'              )
    f.write('\n'+'PreserveBestModel    ./save_best.sh'              )
    f.write('\n'+'#OstrichWarmStart      yes'                          )
    f.write('\n'+''                                                  )
    f.write('\n'+'BeginExtraDirs'                                  )
    f.write('\n'+'RavenInput'                                      )
    f.write('\n'+'#best'                                          )
    f.write('\n'+'EndExtraDirs'                                      )
    f.write('\n'+''                                                  )
    f.write('\n'+'BeginFilePairs'                                  )
    f.write('\n'+'Petawawa.rvp.tpl;              Petawawa.rvp'          )
    f.write('\n'+'Petawawa.rvh.tpl;              Petawawa.rvh'          )
    f.write('\n'+'crest_width_par.csv.tpl;      crest_width_par.csv')
    f.write('\n'+'Petawawa.rvc.tpl;              Petawawa.rvc'          )
    f.write('\n'+''                                                  )
    f.write('\n'+'#can be multiple (.rvh, .rvi)'                  )
    f.write('\n'+'EndFilePairs'                                      )
    #==============================================================
    # parameters
    #==============================================================
    # 1.1 Soil Parameters
    f.write('\n')
    f.write('\n')
    f.write('#Parameter    Specification')
    f.write('\n'+'BeginParams')
    f.write('\n'+'#parameter                init.        low        high         tx_in    tx_ost    tx_out    format')
    f.write('\n')
    f.write('\n'+'## SOIL')    
    f.write('\n'+'%D_FF%                    0.1          0.01       0.2          none    none    none # high')
    f.write('\n'+'%D_AT%                    0.1          0.01       2            none    none    none')
    f.write('\n'+'%MLT_F_Add%               random       0          6            none    none    none')
    f.write('\n'+'%MIN_MLT_F%               random       1          3            none    none    none')
    f.write('\n'+'#%HBV_MLT_A_C%            random       0.1        1            none    none    none')
    f.write('\n'+'%Rfrez_F%                 random       0          4            none    none    none')
    f.write('\n'+'%WFPS%                    random       0.9        27           none    none    none')
    f.write('\n'+'%HydCond_FF%              random       10         1000         none    none    none')
    f.write('\n'+'%FC_FF%                   random       0.1        0.7          none    none    none')
    f.write('\n'+'%FC_AT%                   random       0.1        0.7          none    none    none')
    f.write('\n'+'%FC_BT%                   random       0.5        0.99         none    none    none')
    f.write('\n'+'%MAX_BASEFLOW_RATE_FF%    random       10         1000         none    none    none')
    f.write('\n'+'%MAX_BASEFLOW_RATE_AT%    random       10         1000         none    none    none')
    f.write('\n'+'%MAX_BASEFLOW_RATE_BT%    random       10         1000         none    none    none')
    f.write('\n'+'%BASEFLOW_N_FF%           random       1.00E-01   4.00E+00     none    none    none')
    f.write('\n'+'%BASEFLOW_N_AT%           random       1.00E-01   4.00E+00     none    none    none')
    f.write('\n'+'%BASEFLOW_N_BT%           random       1.00E-01   8.00E+00     none    none    none')
    f.write('\n'+'%Rain_Snow_T%             random       -2         2            none    none    none')
    f.write('\n'+'%Rain_Snow_Delta%         random       0          6            none    none    none')
    f.write('\n'+'%MAX_PERC_RATE_FF%        random       10         1000         none    none    none')
    f.write('\n'+'%MAX_PERC_RATE_AT%        random       10         1000         none    none    none')
    f.write('\n'+'%MAX_CAP_RISE_RATE%       random       10         1000         none    none    none')
    f.write('\n')
    f.write('\n'+'%MAX_CAPACITY%            random       0          5            none    none    none')
    f.write('\n'+'%MAX_SNOW_CAPACITY%       random       0          5            none    none    none')
    f.write('\n'+'%RAIN_ICEPT_PCT%          random       0.01       0.2          none    none    none')
    f.write('\n'+'%SNOW_ICEPT_PCT%          random       0.01       0.3          none    none    none')
    f.write('\n') 
    f.write('\n'+'%LAKE_PET_CORR%           random       0.5        1.5          none    none    none')
    f.write('\n'+'%PET_CORRECTION%          random       0.5        1.5          none    none    none')
    #-----------------------------------------------------------------------------------------
    ## 1.2 Routing parameters
    f.write('\n')
    f.write('\n'+'## ROUTING')
    f.write('\n'+'n_multi                   random       0.1        10           none    none    none   # manning`s n')
    f.write('\n'+'c_multi                   random       0.1        10           none    none    none   # celerity')
    f.write('\n'+'d_multi                   random       0.1        10           none    none    none   # diffusivity')
    f.write('\n'+'k_multi                   random       0.1        10           none    none    none   # lake crest width multiplier')
    ## 1.3 Individual crest    widths for observed    lake
    f.write('\n')
    for Hylakid in CW_para_list:
        q=finalcat_hru_info[(finalcat_hru_info['HyLakeId']==Hylakid) & finalcat_hru_info['HRU_IsLake']==1]['Q_Mean'].values[0]
        Obs_NM=finalcat_hru_info[(finalcat_hru_info['HyLakeId']==Hylakid) & finalcat_hru_info['HRU_IsLake']==1]['Obs_NM'].values[0]
        f.write('\nw_%-24d%-13s%-11.2f%-13.2f%-8s%-8s%-5s  #%s'%(Hylakid,'random',lowCW*q,upCW*q,'none','none','none',Obs_NM))
    f.write('\n'+'EndParams')
    #==============================================================
    # Tied Parameters
    #==============================================================
    f.write('\n')
    f.write('\n')
    f.write('\n'+'BeginTiedParams')
    f.write('\n'+'# Xtied = (c1 * X) + c0')
    f.write('\n'+'# --> c0 = 0.0')
    f.write('\n'+'# --> c1 = 1.')
    f.write('\n'+'#   ')
    f.write('\n'+'#Xtied = (c3 × X1 × X2) + (c2 × X2) + (c1 × X1) + c0')
    f.write('\n'+'#<c3> <c2> <c1> <c0> <fmt>')
    f.write('\n'+'%MLT_F%	       2 	%MLT_F_Add%      %MIN_MLT_F%     linear 0 1 1 0  free')
    f.write('\n'+'%Ininc_Soil2%   1 	%FC_BT%                          linear 600 0  free')
    f.write('\n')
    f.write('\n'+'EndTiedParams')
    #==============================================================
    # Response Variables
    #==============================================================
    ### *** read rvt file -->
    # gauge list and order from rvt file
    calGags=read_cal_gagues(RavenDir)
    # evaluation metrics used in rvi file
    Eval_list=read_evaluation_met(RavenDir)
    f.write('\n')
    f.write('\n')
    f.write('\n'+'BeginResponseVars')
    f.write('\n'+'#name                                                         filename  keyword       line     col     token')
    SF_list=[]
    WL_list=[]
    WA_list=[]
    for lineN,calGag in enumerate(calGags,start=1):
        gaguge=calGag.split('_')[2]
        if 'SF' in calGag:
            if len(SF_list)==0:
                f.write('\n')
                f.write('\n'+'# KGE [Discharge]')
            suffix='KG'
            RavenMet='KLING_GUPTA'
            colN=Eval_list.index(RavenMet)+1+2 # convert to starting from 1 + observed_data_series and filename coloums
            gName=suffix+'_'+str(gaguge)
            SF_list.append(gName)
        elif 'WL' in calGag:
            if len(WL_list)==0:
                f.write('\n')
                f.write('\n'+'# KGE deviation [Reservoir stages]')
            suffix='KD'
            RavenMet='KLING_GUPTA_DEVIATION'
            colN=Eval_list.index(RavenMet)+1+2 # convert to starting from 1 + observed_data_series and filename coloums
            gName=suffix+'_'+str(gaguge)
            WL_list.append(gName)
        elif 'WA' in calGag:
            if len(WA_list)==0:
                f.write('\n')
                f.write('\n'+'# R2 [Reservoir area]')
            suffix='R2'
            RavenMet='R2'
            colN=Eval_list.index(RavenMet)+1+2 # convert to starting from 1 + observed_data_series and filename coloums
            gName=suffix+'_'+str(gaguge)
            WA_list.append(gName)
        #----------------------
        # create the name
        #----------------------
        f.write('\n%-26s./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL%10d%10d%10s'%(gName,lineN,colN,"','"))
    f.write('\n')
    f.write('\n'+'EndResponseVars')   
    #==============================================================
    # Tied Response Vars
    #==============================================================
    f.write('\n')
    f.write('\n')
    f.write('\n'+'BeginTiedRespVars')
    f.write('\n\t'+'# <name1> <np1> <pname1,1> <pname1,2> ... <pname1,np1> <type1> <type_data1>')
    #---------------------------------------------------------------
    if len(SF_list)==1:
        f.write('\n')
        f.write('\n\t'+'NegKG_Q%15d%15s%6s%4d'%(len(SF_list),SF_list[0],'wsum',-1))
    #---------------------------------------------------------------
    if len(WL_list)>=1:
        # make chucks
        f.write('\n')
        WL_list_chuncks=list(divide_chunks(WL_list, 15))
        # print (WL_list_chuncks)
        for i, chunck in enumerate(WL_list_chuncks, start=1):
            # print (chunck)
            f.write('\n\t'+'NegKD_LAKE_WL%d%8d%5s'%(i,len(chunck),' ')+
            '  '.join(chunck)+
            '  wsum  '+ '  '.join(['-1']*len(chunck)))
        f.write('\n\t'+'NegKD_LAKE_WL%9d%5s'%(len(WL_list_chuncks),' ')+
        '  '.join(['NegKD_LAKE_WL%d'%(k) for k in range(1,len(WL_list_chuncks)+1)])+
        '  wsum  '+ '  '.join(['1']*len(WL_list_chuncks)))
        # final objective function
        f.write('\n\t%-20s%2d%12s%15s%8s%2d%6.3f'%(str(costFunc),2,'NegKG_Q','NegKD_LAKE_WL','wsum',1,1/float(len(WL_list))))
    #---------------------------------------------------------------
    if len(WA_list)>=1:
        # make chucks
        f.write('\n')
        WA_list_chuncks=list(divide_chunks(WA_list, 10))
        # print (WL_list_chuncks)
        for i, chunck in enumerate(WA_list_chuncks, start=1):
            # print (chunck)
            f.write('\n\t'+'NegR2_LAKE_WA%d%8d%5s'%(i,len(chunck),' ')+
            '  '.join(chunck)+
            '  wsum  '+ '  '.join(['-1']*len(chunck)))
        f.write('\n\t'+'NegR2_LAKE_WA%9d%5s'%(len(WA_list_chuncks),' ')+
        '  '.join(['NegR2_LAKE_WA%d'%(k) for k in range(1,len(WA_list_chuncks)+1)])+
        '  wsum  '+ '  '.join(['1']*len(WA_list_chuncks)))
        # final objective function
        f.write('\n\t%-20s%2d%12s%15s%8s%2d%6.3f'%(str(costFunc),2,'NegKG_Q','NegR2_LAKE_WA','wsum',1,1/float(len(WA_list))))
    #---------------------------------------------------------------
    f.write('\n')
    f.write('\n'+'EndTiedRespVars')
    #==============================================================
    # RandomSeed
    #==============================================================
    f.write('\n')
    f.write('\n')
    f.write('\n'+'RandomSeed%15s'%(str(RandomSeed)))
    #==============================================================
    # GOCP
    #==============================================================
    f.write('\n')
    f.write('\n')
    f.write('\n'+'BeginGCOP')
    f.write('\n\t'+'CostFunction%15s'%(str(costFunc)))
    f.write('\n\t'+'PenaltyFunction  APM')
    f.write('\n'+'EndGCOP')
    #==============================================================
    # DDSAlg
    #==============================================================
    f.write('\n')
    f.write('\n')
    f.write('\n'+'BeginDDSAlg')
    f.write('\n\t'+'PerturbationValue   0.20')
    f.write('\n\t'+'MaxIterations%10s'%(str(MaxIter)))
    f.write('\n\t'+'# UseInitialParamValues')
    f.write('\n\t'+'# above initializes DDS to parameter values IN the initial model input files')
    f.write('\n'+'EndDDSAlg')