'''
Update the diagnostics file to add
KGE Deviation Prime considering max Lake depth
'''
import os
import sys
import numpy as np 
import scipy
import pandas as pd
#===========================================
def cal_KGED(observed, simulated):
    """
    Calculate the modified Kling-Gupta Efficiency (KGED) without the bias term.

    Parameters:
    observed (array-like): Array of observed data.
    simulated (array-like): Array of simulated data.

    Returns:
    float: KGED value.
    """
    # Ensure inputs are numpy arrays
    observed = np.asarray(observed)
    simulated = np.asarray(simulated)

    # Calculate Pearson correlation coefficient
    r = np.corrcoef(observed, simulated)[0, 1]

    # Calculate coefficient of variation ratio (gamma)
    cv_observed = np.std(observed) / np.mean(observed)
    cv_simulated = np.std(simulated) / np.mean(simulated)
    gamma = cv_simulated / cv_observed

    # print ('CV observed: ', cv_observed)
    # print ('CV simulated: ', cv_simulated)
    # print ('gamma: ', gamma)

    # Calculate KGED
    kged = 1 - np.sqrt((r - 1)**2 + (gamma - 1)**2)

    return kged
#===========================================
def calc_metric(df_org,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag='CALIBRATION',method='KGED_'):
    '''
    Calculate metric
        KGED_  : Kling-Gupta Efficiency Deviation Prime (Kling et al,. 2012)
        KGED   : Kling-Gupta Efficiency Deviation (Kling & Gupta 2009)
    '''
    if timetag=='CALIBRATION':
        syyyymmdd='%04d-%02d-%02d'%(syear,smon,sday)
        eyyyymmdd='%04d-%02d-%02d'%(eyear,emon,eday)
        # corr=df.loc[syyyymmdd:eyyyymmdd,ID_sim].corr(df.loc[syyyymmdd:eyyyymmdd,ID_obs],method=method)
    else:
        syyyymmdd='%04d-%02d-%02d'%(syear,smon,sday)
        eyyyymmdd='%04d-%02d-%02d'%(2020,12,31)
    
    # get df with out nan
    df=df_org.copy()
    df.dropna(subset=[ID_obs,ID_sim],how='any',inplace=True)

    if method == 'KGED_':
        met=cal_KGED(df.loc[syyyymmdd:eyyyymmdd,ID_obs].values, df.loc[syyyymmdd:eyyyymmdd,ID_sim].values)
    else:
        met=cal_KGED(df.loc[syyyymmdd:eyyyymmdd,ID_obs].values, df.loc[syyyymmdd:eyyyymmdd,ID_sim].values)
    
    return met
#===========================================
def observation_tag(label):
    '''
    find the observation tag
    For calibration period
        HYDROGRAPH_CALIBRATION
        RESERVOIR_STAGE_CALIBRATION
        WATER_LEVEL_CALIBRATION
        RESERVOIR_AREA_CALIBRATION
    For all simulation period
        HYDROGRAPH_ALL
        RESERVOIR_STAGE_ALL
        WATER_LEVEL_ALL
        RESERVOIR_AREA_ALL
    '''
    timetag=label.split("_")[-1].split("[")[0]
    filetag=label[0:-len(label.split("_")[-1])-1]
    return filetag, timetag
#===========================================
def read_lake_char(fname):
    "read Lakes.rvt file"
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/Lakes.rvh"%(ens_num)
    # print (fname)
    reservoir_data = {
        'Reservoir': [],
        'SubBasinID': [],
        'HRUID': [],
        'Type': [],
        'WeirCoefficient': [],
        'CrestWidth': [],
        'MaxDepth': [],
        'LakeArea': [],
        'SeepageParameters1': [],
        'SeepageParameters2': []
    }

    current_reservoir = {}

    # try:
    with open(fname, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith(':Reservoir'):
                current_reservoir = {}
                key, value = line.split(' ', 1)
                current_reservoir['Reservoir']=int(value.split('_')[1])
            elif line.startswith(':EndReservoir'):
                for key in reservoir_data.keys():
                    if key in current_reservoir.keys():
                        reservoir_data[key].append(current_reservoir[key])
                    else:
                        reservoir_data[key].append(None)
            else:
                if ':' in line:
                    key, value = line.split(' ', 1)
                    # print (key, value)
                    if key[1::] == 'SeepageParameters':
                        current_reservoir['SeepageParameters1']=value.split(' ')[0].strip()
                        current_reservoir['SeepageParameters2']=value.split(' ')[1].strip()
                    else:
                        current_reservoir[key.strip()[1:]] = value.strip()
            #         print (key[1::], value.strip())
            # print (current_reservoir)

    # except FileNotFoundError:
    #     print(f"Error: File '{file_path}' not found.")
    df=pd.DataFrame(reservoir_data)
    df['WeirCoefficient']=df['WeirCoefficient'].astype(float)
    df['CrestWidth']     =df['CrestWidth'].astype(float)
    df['MaxDepth']       =df['MaxDepth'].astype(float)

    return df
#===========================================
def get_calibration_period(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith(":EvaluationPeriod CALIBRATION"):
                parts = line.split()
                if len(parts) == 4:
                    start_date = parts[2]
                    end_date = parts[3]
                    
                    start_year, start_month, start_day = start_date.split('-')
                    end_year, end_month, end_day = end_date.split('-')
                    
                    return int(start_year), int(start_month), int(start_day), int(end_year), int(end_month), int(end_day)
    return None, None
#===========================================
path_to_file=sys.argv[1] #"./RavenInput/output" #
# read diagnostics file
# OstrichRaven/RavenInput/output_new/Petawawa_Diagnostics.csv
# path_to_file="./RavenInput/output"
filename="Petawawa_Diagnostics.csv"
# filename="../../../RavenInput/output/Petawawa_Diagnostics.csv"
# fname=os.path.join(path_to_file,filename)
fname=path_to_file+"/"+filename
df_diag=pd.read_csv(fname)

#=====
# read simulation file [Streamflow]
# path_to_file="./RavenInput/output_new"
filename="Petawawa_Hydrographs.csv"
# fname=os.path.join(path_to_file,filename)
fname=path_to_file+"/"+filename
df_SF=pd.read_csv(fname)
df_SF.set_index(pd.to_datetime(df_SF['date']),inplace=True)
#=====
# read simulation file [WaterLevel]
# path_to_file="./RavenInput/output"
filename="Petawawa_WaterLevels.csv"
# fname=os.path.join(path_to_file,filename)
fname=path_to_file+"/"+filename
# df_WL=pd.read_csv(fname)
# df_WL.set_index(pd.to_datetime(df_WL['date']),inplace=True)
#=====
# read simulation file [ReservoirStage]
# path_to_file="./RavenInput/output_new"
filename="Petawawa_ReservoirStages.csv"
# fname=os.path.join(path_to_file,filename)
fname=path_to_file+"/"+filename
df_RS=pd.read_csv(fname)
df_RS.set_index(pd.to_datetime(df_RS['date']),inplace=True)
# print (df_RS)
#=====
# read Lakes.rvh file
# path_to_file="./RavenInput/Lakes.rvh"
filename="../Lakes.rvh"
# fname=os.path.join(path_to_file,filename)
fname=path_to_file+"/"+filename
df_Lakes_rvh=read_lake_char(fname)
# print (df_Lakes_rvh)

# edit df_RS using MaxDepth
for res in df_Lakes_rvh['SubBasinID']:
    # print (res)
    subid='sub'+str(res)+' '
    if subid not in df_RS.columns:
        continue
    df_RS[subid]=df_RS[subid]+df_Lakes_rvh[df_Lakes_rvh['SubBasinID']==res]['MaxDepth'].values[0]

# print (df_RS)

# calibration dates
syear=2015
smon=10
sday=1
eyear=2022
emon=9
eday=30
#=====
# calibration dates
# read Petawawa.rvi file
# path_to_file="./RavenInput/Petawawa.rvi"
filename="../Petawawa.rvi"
# fname=os.path.join(path_to_file,filename)
fname=path_to_file+"/"+filename
syear,smon,sday,eyear,emon,eday =get_calibration_period(fname)
# print (syear,smon,sday,eyear,emon,eday)
## need to calculate 
## get the list of Lake data
## RESERVOIR_STAGE_CALIBRATION
lake_list=df_diag[df_diag['observed_data_series'].str.contains('RESERVOIR_STAGE_CALIBRATION')]['observed_data_series'].values
corr=[]
# print (lake_list)
for data in lake_list: #df_diag['observed_data_series'][:]:
    # print (data)
    filetag,timetag=observation_tag(data)
    # print (data,filetag,timetag)
    SubBasinID='sub'+data.split('[')[1].split(']')[0]
    ID_sim=SubBasinID+' '
    ID_obs=SubBasinID+' (observed) [m]'
    kged=calc_metric(df_RS,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='KGED_')
    df_diag.loc[df_diag['observed_data_series']==data,'DIAG_KLING_GUPTA_DEVIATION_PRIME']=kged



# #     # print ('sub'+data.split('[')[1].split(']')[0]+' [m]')
# #     # print (df_sim[SubBasinID])
# #     if filetag=='HYDROGRAPH':
# #         ID_sim=SubBasinID+' [m3/s]'
# #         ID_obs=SubBasinID+' (observed) [m3/s]'
# #         kged=calc_metric(df_SF,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='KGED_')
# #         # corr1=correlation(df_SF,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='pearson')
# #         # corr2=correlation(df_SF,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='spearman')
# #     elif filetag=='RESERVOIR_STAGE':
# #         ID_sim=SubBasinID+' '
# #         ID_obs=SubBasinID+' (observed) [m]'
# #         kged=calc_metric(df_RS,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='KGED_')
# #         # corr1=correlation(df_RS,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='pearson')
# #         # corr2=correlation(df_RS,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='spearman')
# #     elif filetag=='WATER_LEVEL':
# #         ID_sim=SubBasinID+' [m]'
# #         ID_obs=SubBasinID+' (observed) [m]'
# #         kged=calc_metric(df_WL,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='KGED_')
# #         # corr1=correlation(df_WL,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='pearson')
# #         # corr2=correlation(df_WL,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='spearman')
# #     elif filetag=='RESERVOIR_AREA':
# #         ID_sim=SubBasinID+' '
# #         ID_obs=SubBasinID+' (observed) [m2]'
# #         filename='./RavenInput'+df_diag[df_diag['observed_data_series']==data]['filename'].values[0][1::]
# #         # print (filename)
# #         df_WA=pd.read_csv(filename, skiprows=2,skipfooter=1, engine='python',names=[ID_obs])
# #         df_WA['date']=pd.date_range('1984-01-01',periods=14610)
# #         df_WA.set_index('date',inplace=True)
# #         df_WA[ID_obs] = df_WA[ID_obs].astype(float)
# #         df_WA.loc[df_WA[ID_obs]<0.0,ID_obs]= float('nan') #np.nan
# #         # df_WA=df_WA.loc['2016-01-01':'2021-1-1',:]
# #         df_WA[ID_sim]=df_RS[ID_sim]
# #         # print (df_WA.head())
# #         kged=calc_metric(df_WA,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='KGED_')
# #         # corr1=correlation(df_WA,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='pearson')
# #         # corr2=correlation(df_WA,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='spearman')
# #     print (kged)
# #     # print (data,corr1,corr2)
# #     # pearson , spearman
# # #     corr.append([corr1,corr2])

# corr=np.array(corr)

# df_diag["DIAG_KLING_GUPTA_DEVIATION_PRIME"]=corr[:,0]
# df_diag["DIAG_SPEARMAN_RANKED_CORRELATION"]=corr[:,1]
df_diag = df_diag.loc[:, ~df_diag.columns.str.contains('Unnamed')]
# print (df_diag)#.columns)

df_diag.to_csv(path_to_file+"/Petawawa_Diagnostics.csv", index=False)
#===========================================