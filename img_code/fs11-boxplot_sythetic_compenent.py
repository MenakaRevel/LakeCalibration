#!/usr/python
'''
plot the ensemble metric
'''
import warnings
warnings.filterwarnings("ignore")
import os
import numpy as np
import scipy
import datetime
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
import matplotlib.colors
mpl.use('Agg')
#===============================================================================================
def mk_dir(dir):
    # Create the download directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)
#=====================================================
def read_diagnostics(expname, ens_num, odir='/scratch/menaka/LakeCalibration/out',output='output',glist=['HYDROGRAPH_CALIBRATION[921]']):
# ,'HYDROGRAPH_CALIBRATION[400]',
# 'HYDROGRAPH_CALIBRATION[288]','HYDROGRAPH_CALIBRATION[265]',
# 'HYDROGRAPH_CALIBRATION[412]']):
# ['WATER_LEVEL_CALIBRATION[265]','WATER_LEVEL_CALIBRATION[400]',
# 'WATER_LEVEL_CALIBRATION[412]','HYDROGRAPH_CALIBRATION[921]']
# ['DIAG_KLING_GUPTA','DIAG_KLING_GUPTA_DEVIATION']
    '''
    read the RunName_Diagnostics.csv
    '''
    # HYDROGRAPH_CALIBRATION[921],./obs/02KB001_921.rvt
    # WATER_LEVEL_CALIBRATION[265],./obs/Crow_265.rvt
    # WATER_LEVEL_CALIBRATION[400],./obs/Little_Madawaska_400.rvt
    # WATER_LEVEL_CALIBRATION[412],./obs/Nippissing_Corrected_412.rvt
    fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,output)
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/output_Raven_v3.7/Petawawa_Diagnostics.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    print (fname) 
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    return df[df['observed_data_series'].isin(glist)]['DIAG_KLING_GUPTA'].values #,'DIAG_SPEARMAN']].values
#=====================================================
def read_costFunction(expname, ens_num, div=1.0, odir='/scratch/menaka/LakeCalibration/out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return (df['obj.function'].iloc[-1]/float(div))*-1.0
#=====================================================
def read_lake_diagnostics(expname, ens_num, ObjLake, llake, odir='/scratch/menaka/LakeCalibration/out',output='output',var='WL'):
    '''
    read the RunName_Diagnostics.csv get average value of the metric given
    DIAG_KLING_GUPTA_DEVIATION
    DIAG_R2
    '''
    # HYDROGRAPH_CALIBRATION[921],./obs/02KB001_921.rvt
    # WATER_LEVEL_CALIBRATION[265],./obs/Crow_265.rvt
    # WATER_LEVEL_CALIBRATION[400],./obs/Little_Madawaska_400.rvt
    # WATER_LEVEL_CALIBRATION[412],./obs/Nippissing_Corrected_412.rvt
    fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,output)
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/output_Raven_v3.7/Petawawa_Diagnostics.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    print (fname) 
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    if var=='WL':
        mean_var_met = df[(df['observed_data_series'].str.contains('CALIBRATION')) & (df['filename'].isin(llake))][ObjLake].mean() #,'DIAG_SPEARMAN']].values
    else: 
        # need to calculate KGED --> ObjLake = [DIAG_KLING_GUPTA_DEVIATION, DIAG_R2]
        syear,smon,sday,eyear,emon,eday = 2015,10,1,2022,9,30
        timetag='CALIBRATION'
        fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/%s/Petawawa_ReservoirMassBalance.csv"%(ens_num,output)
        df_RMB=pd.read_csv(fname)
        df_RMB['date']=pd.to_datetime(df_RMB['date'])
        lkged=[]
        for lake in llake:
            SubBasinID=lake.split('_')[-1].split('.')[0]
            ID_sim='sub'+SubBasinID+' area [m2]'
            ID_obs='value'
            obs_path=odir+"/"+expname+"_%02d/best_Raven/RavenInput/%s"%(ens_num,lake)
            df_obs=read_rvt_file(obs_path)
            # print (df_obs)
            df_obs=df_obs[df_obs['value']!=-1.2345]
            df_sim=df_RMB.loc[:,['date',ID_sim]]
            df=pd.merge(df_obs, df_sim, on='date', suffixes=('_obs', '_sim'))
            df.rename(columns={ID_sim:'sim', 'value':'obs'},inplace=True)
            kged=calc_metric(df,'sim','obs',syear,smon,sday,eyear,emon,eday,timetag=timetag,method=ObjLake)
            lkged.append(kged)
        mean_var_met=np.mean(np.array(lkged))
    return mean_var_met
#===========================================
def read_rvt_file(file_path):
    '''
    # Function to read the file and create a dataframe
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Extract the initial date (ignoring the first line which is the header)
    initial_entry = lines[1].split()
    date = initial_entry[0] + " " + initial_entry[1]

    # Read subsequent values, ignoring the last line (':EndObservationData')
    values = [float(line.strip()) for line in lines[2:-1]]

    # Create a date range starting from the initial date
    date_range = pd.date_range(start=date, periods=len(values), freq='D')

    # Create the dataframe
    df = pd.DataFrame({'date': date_range, 'value': values})
    df['value'] = df['value'].astype(float)
    return df
#===========================================
def cal_KGED(observed, simulated):
    """
    Calculate the Kling-Gupta Efficiency (KGED) without the bias term.

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
    cv_observed = np.std(observed) #/ np.mean(observed)
    cv_simulated = np.std(simulated) #/ np.mean(simulated)
    gamma = cv_simulated / (cv_observed + 1e-20)

    # print ('CV observed: ', cv_observed)
    # print ('CV simulated: ', cv_simulated)
    # print ('gamma: ', gamma)

    # Calculate KGED
    kged = 1 - np.sqrt((r - 1)**2 + (gamma - 1)**2)

    return kged
#===========================================
def cal_R2(observed, simulated):
    """
    Calculate the R2.

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

    return r**2
#===========================================
def calc_metric(df_org,ID_obs,ID_sim,syear,smon,sday,eyear,emon,eday,timetag='CALIBRATION',method='KGED_'):
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
    df.set_index('date',inplace=True)

    if method == 'DIAG_KLING_GUPTA_DEVIATION':
        met=cal_KGED(df.loc[syyyymmdd:eyyyymmdd,ID_obs].values, df.loc[syyyymmdd:eyyyymmdd,ID_sim].values)
    elif method == 'DIAG_R2':
        met=cal_R2(df.loc[syyyymmdd:eyyyymmdd,ID_obs].values, df.loc[syyyymmdd:eyyyymmdd,ID_sim].values)
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
#=====================================================
expname="S1a"
odir='/scratch/menaka/LakeCalibration/out'
#========================================================================================
mk_dir("../figures/paper")
ens_num=10
metric=[]
# lexp=["S0a","S0b","S0c","S1a","S1b"]
# lexp=["S0b","S1a","S1b","S1c","S1d"]
# lexp=["S0b","S1d","S1e","S1f"]
# lexp=["S0b","S1d","S1e","S1f","S1g","S1h"]
# lexp=["S0b","S1d","S1e","S1i","S1j","S1k"]
# lexp=["S0a","S0b","S0e","S0f"] #"S0d",
# lexp=["S0a","S0b","S0e","S0f","S0g"]
# lexp=["S0a","S0b","S0e","S0f","S0g","S0h"]
# lexp=["E0a","E0b","S1a","S1b","S1c"]
# lexp=["E0a","E0b","S1c","S1d","S1e"]
# lexp=["E0a","E0b","S1d","S1f","S1g"]
# lexp=["E0a","E0b","S0a","S1f","S1h"]
# lexp=["E0a","E0b","S0a","S1h","S1i"]
# lexp=["E0a","E0b","S0c","S0b","S1h","S1i"]
# lexp=["E0a","E0b","V1a","V1b"]
# lexp=["E0a","E0b","S1z","V1a","V1b"]
lexp=["V1a","V1b",'V1c',"V1d"]
colname={
    "E0a":"Obs_SF_IS",
    "E0b":"Obs_WL_IS",
    "S0a":"Obs_WL_IS",
    "S0b":"Obs_WL_IS",
    "S0c":"Obs_SF_IS",
    "S1d":"Obs_WA_RS3",
    "S1f":"Obs_WA_RS4",
    "S1h":"Obs_WA_RS5",
    "S1i":"Obs_WA_RS4",
    "S1z":"Obs_WA_RS4",
    "V1a":"Obs_WA_SY1",
    "V1b":"Obs_WA_SY1",
    "V1c":"Obs_WA_SY1",
    "V1d":"Obs_WA_SY1"
}
expriment_name=[]
# read final cat 
final_cat=pd.read_csv(odir+'/../OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
#========================================================================================
for expname in lexp:
    objFunction0=1.0
    for num in range(1,ens_num+1):
        print (expname, num)
        # metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
        # print (list(read_diagnostics(expname, num).flatten()).append(read_costFunction(expname, num))) #np.shape(read_diagnostics(expname, num)), 
        # cost function
        if expname in ['E0a','S0c']:
            row=list([read_costFunction(expname, num, div=1.0, odir=odir)])
        else:
            row=list([read_costFunction(expname, num, div=2.0, odir=odir)])
        # 02KB001
        row.append(list(read_diagnostics(expname, num, odir=odir).flatten())[0])
        ## Lake WL
        if expname in ['V1a','V1b','V1c','V1d']:
            # Lake WL KGED
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WL_SY_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat['HyLakeId'].dropna().unique()]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
            # Lake WL R2
            ObjLake="DIAG_R2"
            llake=["./obs/WL_SY_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat['HyLakeId'].dropna().unique()]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        else:
            # Lake WL KGED
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WL_IS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WL_IS']==1]['HyLakeId'].dropna().unique()]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
            # Lake WL R2
            ObjLake="DIAG_R2"
            llake=["./obs/WL_IS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WL_IS']==1]['HyLakeId'].dropna().unique()]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        ## Lake WA
        if expname in ['S1z']:
            # Lake WA KGED
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique()]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake, var='WA'))
            # Lake WA R2
            ObjLake="DIAG_R2"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique()]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake, var='WA'))
        elif expname in ['V1a','V1b','V1c','V1d']:
            # Lake WA KGED
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WA_SY_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique()]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake, var='WA'))
            # Lake WA R2
            ObjLake="DIAG_R2"
            llake=["./obs/WA_SY_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique()]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake, var='WA'))
        else:
            # Lake WA KGED
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique()]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake, var='WA'))
            # Lake WA R2
            ObjLake="DIAG_R2"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique()]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake, var='WA'))
        print (len(row))
        print (row)
        # # if expname in ['E0a']:
        # #     row.append(read_costFunction(expname, num, div=1.0, odir=odir))
        # #     ObjLake="NaN"
        # #     row.append(np.nan)
        # # elif expname in ['E0b']:
        # #     row.append(read_costFunction(expname, num, div=2.0, odir=odir))
        # #     ObjLake="DIAG_KLING_GUPTA_DEVIATION"
        # #     llake=["./obs/WL_IS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WL_IS']==1]['HyLakeId'].dropna().unique()]#,
        # #     # final_cat[final_cat['Obs_WL_IS']==1]['SubId'].dropna().unique())]
        # #     # print (llake)
        # #     row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        # # elif expname in ['S0a']:
        # #     row.append(read_costFunction(expname, num, div=2.0, odir=odir))
        # #     ObjLake="DIAG_R2"
        # #     llake=["./obs/WL_IS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WL_IS']==1]['HyLakeId'].dropna().unique()]#,
        # #     # final_cat[final_cat['Obs_WL_IS']==1]['SubId'].dropna().unique())]
        # #     # print (llake)
        # #     row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        # # elif expname in ['S1a','S1c']:
        # #     row.append(read_costFunction(expname, num, div=2.0, odir=odir))
        # #     ObjLake="DIAG_R2"
        # #     llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WA_RS1']==1]['HyLakeId'].dropna().unique()]#
        # #     # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
        # #     row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        # # elif expname in ['S1b']:
        # #     row.append(read_costFunction(expname, num, div=2.0, odir=odir))
        # #     ObjLake="DIAG_R2"
        # #     llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WA_RS2']==1]['HyLakeId'].dropna().unique()]#
        # #     # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
        # #     row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        # # else:
        # #     row.append(read_costFunction(expname, num, div=2.0, odir=odir))
        # #     ObjLake="DIAG_R2"
        # #     llake=["./obs/WA_RS_%d_%d.rvt"%(lake,subid) for lake,subid in zip(final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique(),
        # #     final_cat[final_cat[colname[expname]]==1]['SubId'].dropna().unique())]
        # #     row.append(read_lake_diagnostics(expname, num, ObjLake, llake)) 
        expriment_name.append("Exp"+expname)
        # print (len(row))
        # print (ObjLake,row)
        metric.append([row])
metric=np.array(metric)[:,0,:]
print (np.shape(metric))
# print (metric)

# df=pd.DataFrame(metric, columns=['02KB001','KGED_02KB001','KGE_Crow','Crow',
# 'KGE_LM','LM','KGE_NC','NC','obj.function',
# 'mean_Lake'])
# df['Expriment']=np.array(expriment_name)
# print (df.head())

df=pd.DataFrame(metric, columns=['obj.function','02KB001','mean_Lake_WL_KGED',
'mean_Lake_WL_R2','mean_Lake_WA_KGED','mean_Lake_WA_R2'])
df['Expriment']=np.array(expriment_name)
print ('='*20+' df '+'='*20)
print (df.head(5))

df_melted = pd.melt(df[['obj.function','02KB001','mean_Lake_WL_KGED',
'mean_Lake_WL_R2','mean_Lake_WA_KGED','mean_Lake_WA_R2','Expriment']],
id_vars='Expriment', value_vars=['obj.function','02KB001','mean_Lake_WL_KGED',
'mean_Lake_WL_R2','mean_Lake_WA_KGED','mean_Lake_WA_R2'])
print ('='*20+' df_melted '+'='*20)
print (df_melted.head(5))

print ("mean_Lake_WA_KGED")
print (df_melted[df_melted['variable']=='mean_Lake_WA_KGED'])

print ("mean_Lake_WL_KGED")
print (df_melted[df_melted['variable']=='mean_Lake_WL_KGED'])

# df_melted2 = pd.melt(df[['Expriment','obj.function']],
# id_vars='Expriment', value_vars=['obj.function'])
# print (df_melted2.head(50))

# df_melted['obj.function'] = df_melted2['value']
# print (df_melted.head(50))
# colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20c(3),
        #   plt.cm.tab20c(4),plt.cm.tab20c(6),plt.cm.tab20c(7)]

# colors=['#2ba02b','#99df8a','#d62727','#ff9896']
# colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]
# colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(6),plt.cm.tab20c(7)]
colors = [plt.cm.Set1(0),plt.cm.Set1(1),plt.cm.Set1(2),plt.cm.Set1(3),plt.cm.Set1(4),plt.cm.Set1(5)]
# locs=[-0.28,-0.10,0.10,0.28]
locs=[-0.32,-0.18,0.0,0.18,0.32]
if len(lexp) == 2:
    locs=[-0.10,0.10]
    colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(6),plt.cm.tab20c(7)]
elif len(lexp) == 3:
    locs=[-0.26,0,0.26]
    colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(6),plt.cm.tab20c(7)]
elif len(lexp) == 4:
    locs=[-0.30,-0.12,0.11,0.30]
    colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(6),plt.cm.tab20c(7)]
elif len(lexp) == 5:
    locs=[-0.32,-0.18,0.0,0.18,0.32]
    colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(6),plt.cm.tab20c(7)]
elif len(lexp) == 6:
    locs=[-0.33,-0.20,-0.07,0.07,0.20,0.33]
    colors = [plt.cm.Set1(0),plt.cm.Set1(1),plt.cm.tab20(4),plt.cm.tab20(5),plt.cm.tab20(2),plt.cm.tab20(3)]
else:
    locs=[-0.32,-0.15,0.0,0.15,0.32]
    colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(6),plt.cm.tab20c(7)]

# Number of unique variables
n_variables = len(df_melted['variable'].unique())

# Calculate the locs dynamically
offset_range = 0.32  # This is the range to distribute the offsets
locs = np.linspace(-offset_range, offset_range, num=len(lexp))

# colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]
colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]

fig, ax = plt.subplots(figsize=(8, 8))
ax=sns.boxplot(data=df_melted,x='variable', y='value',
order=['obj.function','02KB001','mean_Lake_WL_KGED','mean_Lake_WL_R2',
'mean_Lake_WA_KGED','mean_Lake_WA_R2'],hue='Expriment',
palette=colors, boxprops=dict(alpha=0.9), zorder=110)
# Get the colors used for the boxes
box_colors = [box.get_facecolor() for box in ax.artists]
# print (box_colors)
for i,expname, color in zip(locs,lexp,colors):
    print ("Exp"+expname)#, color)
    df_=df[df['Expriment']=="Exp"+expname]
    print ('='*20+' df_ '+'='*20)
    print (df_.head())
    star=df_.loc[df_['obj.function'].idxmax(),['obj.function','02KB001','mean_Lake_WL_KGED',
    'mean_Lake_WL_R2','mean_Lake_WA_KGED','mean_Lake_WA_R2']]#.groupby(['Expriment'])
    # print (star)
    # Calculate x-positions for each box in the boxplot
    box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
    # print (box_positions)
    ax.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='k', zorder=110) #'grey'
    #==
    unique_variables = df_melted['variable'].unique()
    for ix, box_pos in enumerate(box_positions):
        variable = unique_variables[ix]
        fill = False

        if variable in ['obj.function', '02KB001']:
            fill = True
        elif variable == 'mean_Lake_WL_KGED' and expname in ['E0b','S1i','S1z']:
            fill = True
        elif variable == 'mean_Lake_WL_R2' and expname == 'S0a':
            fill = True
        elif variable == 'mean_Lake_WA_R2' and expname in ['S1f', 'S1h']:
            fill = True
        elif variable == 'mean_Lake_WA_KGED' and expname in ['S1z']:
            fill = True

        print(box_pos, variable, expname, fill)
        if fill:
            ax.fill_betweenx([-1.5, 1], x1=box_pos - 0.07, x2=box_pos + 0.07, color='gray', alpha=0.5, zorder=0)

    # # unique_variables = df_melted['variable'].unique()
    # # for ix in range(len(box_positions)):
    # #     print (box_positions[ix], df_melted['variable'].unique()[ix])
    # #     if df_melted['variable'].unique()[ix] in ['obj.function','02KB001']:
    # #         ax.fill_betweenx([-1.5,1],x1=box_positions[ix]-0.075, x2=box_positions[ix]+0.075, color='gray', alpha=0.5, zorder=0)
    # #     if df_melted['variable'].unique()[ix] == 'mean_Lake_WL_KGED':
    # #         if expname == 'E0b':
    # #             ax.fill_betweenx([-1.5,1],x1=box_positions[ix]-0.075, x2=box_positions[ix]+0.075, color='gray', alpha=0.5, zorder=0)
    # #     if df_melted['variable'].unique()[ix] != 'mean_Lake_WL_R2':
    # #         if expname == 'S0a':
    # #             ax.fill_betweenx([-1.5,1],x1=box_positions[ix]-0.075, x2=box_positions[ix]+0.075, color='gray', alpha=0.5, zorder=0)
    # #     if df_melted['variable'].unique()[ix] != 'mean_Lake_WA_R2': 
    # #         if expname in ['S1f','S1h']:
    # #             ax.fill_betweenx([-1.5,1],x1=box_positions[ix]-0.075, x2=box_positions[ix]+0.075, color='gray', alpha=0.5, zorder=0)
    # #     # ax.fill_betweenx([-1.5,1],x1=box_positions[ix]-0.075, x2=box_positions[ix]+0.075, color='gray', alpha=0.5, zorder=0)
# Updatae labels
ax.set_xticklabels(['objective\nfunction','02KB001','Lake WL\n($KGED$)','Lake WL\n($R^2$)','Lake WA\n($KGED$)','Lake WA\n($R^2$)'],rotation=0)
# Lines between each columns of boxes
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
#
ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
ax.set_ylabel("$Metric$ $($$KGE$/$KGED$/$R^2$$)$")
# add validation and calibration
# ax.text(0.25,1.02,"Calibration",fontsize=12,ha='center',va='center',transform=ax.transAxes)
# ax.text(0.75,1.02,"Validation",fontsize=12,ha='center',va='center',transform=ax.transAxes)
handles, labels = ax.get_legend_handles_labels()
# new_labels = ['Exp 1', 'Exp 2', 'Exp 3']  # Replace these with your desired labels
# new_labels = [
#     labels[0] + "($Q$ [$KGE$])",
#     labels[1] + "($Q$ [$KGE$])+ $WL$ [$KGED$])", 
#     labels[2] + "($Q$ [$KGE$] + $WSA$ [$KGED$])",
#     # labels[3] + "($Q$ [$KGE$] + $WSA$ [$KGED$])"
# ]
new_labels = [
    labels[0] + "($Q$ [$KGE$] + $vWSA w/o (daily)$ [$KGED$])",
    labels[1] + "($Q$ [$KGE$] + $vWSA w/o (16-day)$ [$KGED$])",
    labels[2] + "($Q$ [$KGE$] + $vWSA w/ (16-day)$ [$KGED$])",
    labels[3] + "($Q$ [$KGE$] + $WSA$ [$KGED$])",
    # labels[2] + "($Q$ [$KGE$] + $WSA$ [$KGED$])",
    # labels[3] + "($Q$ [$KGE$] + $WSA$ [$KGED$])"
]
# new_labels = [
#     labels[0] + "($Q$ [$KGE$])", 
#     labels[1] + "($Q$ [$KGE$] + $WL$ [$KGED$])", 
#     labels[2] + "($Q$ [$KGE`$])",
#     labels[3] + "($Q$ [$KGE$] + $KGED'$ [$R^2$])",
#     labels[4] + "($Q$ [$KGE$] + $WA_{g1}(15)$ [$R^2$])", 
#     labels[5] + "($Q$ [$KGE$] + $WA_{g2}(18)$ [$R^2$])"
#     # labels[4] + "($Q$ [$KGE$] + $WA_{g2}(18)$ [$KGED'$])"
# ]
ax.legend(handles=handles, labels=new_labels, loc='lower left')
ax.set_xlabel(" ")
# ax.set_ylim(ymin=-10.75,ymax=1.1)
# plt.savefig('../figures/paper/fs1-KGE_boxplot_S0_CalBugdet_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')

plt.tight_layout()
print ('../figures/paper/fs11-KGE_boxplot_sythetic_metric_comp_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.savefig('../figures/paper/fs11-KGE_boxplot_sythetic_metric_comp_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')