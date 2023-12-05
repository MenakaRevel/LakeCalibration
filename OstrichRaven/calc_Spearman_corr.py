'''
Update the diagnostics file to add
Spearman Ranked Correlation
'''
import os
import sys
import numpy as np 
import scipy
import pandas as pd
#===========================================
def correlation(df,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag='CALIBRATION',method='spearman'):
    '''
    Calculate correlation coefficient
        pearson  : standard correlation coefficient
        kendall  : Kendall Tau correlation coefficient
        spearman : Spearman rank correlation
    '''
    if timetag=='CALIBRATION':
        syyyymmdd='%04d-%02d-%02d'%(syear,smon,sday)
        eyyyymmdd='%04d-%02d-%02d'%(eyear,emon,eday)
        corr=df.loc[syyyymmdd:eyyyymmdd,ID_sim].corr(df.loc[syyyymmdd:eyyyymmdd,ID_obs],method=method)
    else:
        syyyymmdd='%04d-%02d-%02d'%(syear,smon,sday)
        eyyyymmdd='%04d-%02d-%02d'%(2020,12,31)
        corr=df.loc[syyyymmdd:eyyyymmdd,ID_sim].corr(df.loc[syyyymmdd:eyyyymmdd,ID_obs],method=method)
    return corr
# #===========================================
# def read_observation(pname,path_to_file="./RavenInput/Obs/"):
#     '''
#     read water surface area observation
#     '''
#     filename=os.path.join(path_to_file, pname, '.csv')
#     df=pd.read_csv(filename)
#     # need to convert to daily average 
#     return df
# #===========================================
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
#====
path_to_file=sys.argv[1] #"./RavenInput/output" #
# read diagnostics file
# OstrichRaven/RavenInput/output_new/Petawawa_Diagnostics.csv
# path_to_file="./RavenInput/output"
filename="Petawawa_Diagnostics.csv"
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
df_WL=pd.read_csv(fname)
df_WL.set_index(pd.to_datetime(df_WL['date']),inplace=True)
#=====
# read simulation file [ReservoirStage]
# path_to_file="./RavenInput/output_new"
filename="Petawawa_ReservoirStages.csv"
# fname=os.path.join(path_to_file,filename)
fname=path_to_file+"/"+filename
df_RS=pd.read_csv(fname)
df_RS.set_index(pd.to_datetime(df_WL['date']),inplace=True)

# calibration dates
syear=2016
smon=1
sday=1
eyear=2020
emon=10
eday=20

## need to calculate only the SRCC
corr=[]
for data in df_diag['observed_data_series'][:]:
    filetag,timetag=observation_tag(data)
    # print (data,filetag,timetag)
    SubBasinID='sub'+data.split('[')[1].split(']')[0]
    # print ('sub'+data.split('[')[1].split(']')[0]+' [m]')
    # print (df_sim[SubBasinID])
    if filetag=='HYDROGRAPH':
        ID_sim=SubBasinID+' [m3/s]'
        ID_obs=SubBasinID+' (observed) [m3/s]'
        corr1=correlation(df_SF,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='pearson')
        corr2=correlation(df_SF,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='spearman')
    elif filetag=='RESERVOIR_STAGE':
        ID_sim=SubBasinID+' '
        ID_obs=SubBasinID+' (observed) [m]'
        corr1=correlation(df_RS,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='pearson')
        corr2=correlation(df_RS,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='spearman')
    elif filetag=='WATER_LEVEL':
        ID_sim=SubBasinID+' [m]'
        ID_obs=SubBasinID+' (observed) [m]'
        corr1=correlation(df_WL,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='pearson')
        corr2=correlation(df_WL,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='spearman')
    elif filetag=='RESERVOIR_AREA':
        ID_sim=SubBasinID+' '
        ID_obs=SubBasinID+' (observed) [m2]'
        filename='./RavenInput'+df_diag[df_diag['observed_data_series']==data]['filename'].values[0][1::]
        # print (filename)
        df_WA=pd.read_csv(filename, skiprows=2,skipfooter=1, engine='python',names=[ID_obs])
        df_WA['date']=pd.date_range('1984-01-01',periods=14610)
        df_WA.set_index('date',inplace=True)
        df_WA[ID_obs] = df_WA[ID_obs].astype(float)
        df_WA.loc[df_WA[ID_obs]<0.0,ID_obs]= float('nan') #np.nan
        # df_WA=df_WA.loc['2016-01-01':'2021-1-1',:]
        df_WA[ID_sim]=df_RS[ID_sim]
        # print (df_WA.head())
        corr1=correlation(df_WA,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='pearson')
        corr2=correlation(df_WA,ID_sim,ID_obs,syear,smon,sday,eyear,emon,eday,timetag=timetag,method='spearman')

    # print (data,corr1,corr2)
    # pearson , spearman
    corr.append([corr1,corr2])

corr=np.array(corr)

df_diag["DIAG_PEARSON_CORRELATION"]=corr[:,0]
df_diag["DIAG_SPEARMAN_RANKED_CORRELATION"]=corr[:,1]
df_diag = df_diag.loc[:, ~df_diag.columns.str.contains('Unnamed')]
# print (df_diag.columns)

df_diag.to_csv(path_to_file+"/Petawawa_Diagnostics_Final.csv", index=False)