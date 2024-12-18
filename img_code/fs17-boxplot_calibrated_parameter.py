#!/usr/python
'''
plot the ensemble metric boxplot of all subbasin Q
'''
import warnings
warnings.filterwarnings("ignore")
import os
import numpy as np
import scipy
import datetime
import pandas as pd 
import re
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
import matplotlib.colors
from exp_params import *
import string
mpl.use('Agg')
#===============================================================================================
def mk_dir(dir):
    # Create the download directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)
#========================================================================================
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
#========================================
def read_Diagnostics_Raven_best(expname, ens_num, odir='../out',output='output',
glist=['HYDROGRAPH_CALIBRATION[921]','HYDROGRAPH_CALIBRATION[400]',
'HYDROGRAPH_CALIBRATION[288]','HYDROGRAPH_CALIBRATION[265]',
'HYDROGRAPH_CALIBRATION[412]']):
    # df=pd.read_csv('RavenInput/'+exp+'/SE_Diagnostics.csv')
    fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,output)
    print (fname) 
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    return df[df['observed_data_series'].isin(glist)]['DIAG_KLING_GUPTA'].unique() #,'DIAG_SPEARMAN']].values
#========================================================================================
def read_diagnostics_filename(expname, ens_num, ObjMet='DIAG_KLING_GUPTA',
flist=['./obs/SF_SY_sub921_921.rvt'],
odir='/scratch/menaka/LakeCalibration/out',output='output'):
    '''
    read the RunName_Diagnostics.csv
    '''
    fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,output)
    # print (fname) 
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    return df[df['filename'].isin(flist)][ObjMet].dropna().mean() #,'DIAG_SPEARMAN']].values
#========================================================================================
def get_list_diagnostics_filename(expname, ens_num, ObjMet='DIAG_KLING_GUPTA',
flist=['./obs/SF_SY_sub921_921.rvt'],
odir='/scratch/menaka/LakeCalibration/out',output='output'):
    '''
    read the RunName_Diagnostics.csv
    '''
    fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,output)
    # print (fname) 
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    # print (flist)
    # print (df[(df['observed_data_series'].str.contains('HYDROGRAPH_CALIBRATION')) & (df['filename'].isin(flist))][ObjMet].dropna().unique())
    return df[(df['observed_data_series'].str.contains('RESERVOIR_STAGE_CALIBRATION')) & (df['filename'].isin(flist))][ObjMet].dropna().unique() #,'DIAG_SPEARMAN']].values
#========================================================================================
def read_costFunction(expname, ens_num, div=1.0, odir='/scratch/menaka/LakeCalibration/out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return (df['obj.function'].iloc[-1]/float(div))*-1.0
#========================================================================================
def read_parameters(expname, ens_num, paraList=['n_multi'], odir='/scratch/menaka/LakeCalibration/out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return df.loc[:,paraList].iloc[-1]
#========================================================================================
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
        mean_var_met = df[(df['observed_data_series'].str.contains('CALIBRATION')) & (df['filename'].isin(llake))][ObjLake].dropna().mean() #,'DIAG_SPEARMAN']].values
    elif var=='WA':
        mean_var_met = df[(df['observed_data_series'].str.contains('CALIBRATION')) & (df['filename'].isin(llake))][ObjLake].dropna().mean()
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
#========================================================================================
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
#========================================================================================
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
#========================================================================================
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
#========================================================================================
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
#========================================================================================
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
#========================================================================================
expname="S1a"
odir='/scratch/menaka/LakeCalibration/out'
#========================================================================================
mk_dir("../figures/paper")
ens_num=10
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
# lexp=["V1a","V1b","V1d","S1z"]
# lexp=["V0a","V1a","V1d","V2a","V2d","V2e"]#,"V1e"]
# lexp=["V0a","V2e","V2d","V4e","V4d"]#,"V1e"]
lexp=["V0a","V2e","V2d","V4e","V4f","V2a"]
colname=get_final_cat_colname()
#========================================================================================
# read final cat 
final_cat=pd.read_csv('../OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
#========================================================================================
# vegitation_para = ['%RAIN_ICEPT_PCT%','%SNOW_ICEPT_PCT%','%MAX_CAPACITY%',
# '%MAX_SNOW_CAPACITY%']
# landuse_para = ['%Rfrez_F%','%MLT_F%','%MIN_MLT_F%']
# soil_para = ['%HydCond_FF%','%WFPS%','%PET_CORRECTION%','%FC_FF%','%FC_AT%','%FC_BT%']
# baseflow_para = ['%MAX_PERC_RATE_FF%','%MAX_PERC_RATE_AT%','%MAX_BASEFLOW_RATE_FF%',
# '%MAX_BASEFLOW_RATE_AT%','%MAX_BASEFLOW_RATE_BT%','%MAX_CAP_RISE_RATE%',
# '%BASEFLOW_N_FF%','%BASEFLOW_N_AT%','%BASEFLOW_N_BT%','%FC_FF%','%FC_AT%','%FC_BT%']
# routing_para = ['n_multi', 'q_multi', 'k_multi']

paraLists = get_paraList()
#========================================================================================
for k,paraListNames in enumerate(paraLists.keys(),start=0):
    paraList=paraLists[paraListNames]
    expriment_name=[]
    metric=[]
    objfuns=[]
    for expname in lexp:
        objFunction0=1.0
        for num in range(1,ens_num+1):
            print (expname, num)
            # metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
            # print (list(read_diagnostics(expname, num).flatten()).append(read_costFunction(expname, num))) #np.shape(read_diagnostics(expname, num)), 
            #========================================================================================
            # cost function
            if expname in ['E0a','S0c','V0a','V2a','V2b','V2c','V2d','V2e','V3d','V4d','V4e']: # use one component (Q/Lake) for Obj.Function
                objfun=list([read_costFunction(expname, num, div=1.0, odir=odir)])
            elif expname in ['V2dd']:
                objfun=list([read_costFunction(expname, num, div=18.0, odir=odir)])
            else:
                objfun=list([read_costFunction(expname, num, div=2.0, odir=odir)])
            #========================================================================================
            # parameterList
            row=list([read_parameters(expname, num, paraList=paraList ,odir=odir)])
            # print (len(row))
            # # print (ObjLake,row)
            expriment_name.append("Exp"+expname)
            objfuns.append(objfun)
            metric.append([row])
    metric=np.array(metric)[:,0,:]
    print (np.shape(metric[:,0,:]))
    print (len(paraList))

    df=pd.DataFrame(metric[:,0,:], columns=paraList)
    df['Expriment']=np.array(expriment_name)
    df['obj.function']=np.array(objfuns)
    print ('='*20+' df '+'='*20)
    print (df.head(5))

    print (['Expriment']+paraList)
    df_melted = pd.melt(df[['Expriment']+paraList],
    id_vars='Expriment', value_vars=paraList)

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
    # colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(12),plt.cm.tab20c(13)]
    colors = [plt.cm.tab10(3),plt.cm.tab10(2),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab20(2),plt.cm.tab10(5),plt.cm.tab10(6)]

    print (df_melted)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax=sns.boxplot(data=df_melted,x='variable', 
    y='value',hue='Expriment',
    palette=colors, boxprops=dict(alpha=0.9), zorder=110)
    # Get the colors used for the boxes
    box_colors = [box.get_facecolor() for box in ax.artists]
    # print (box_colors)
    for i,expname, color in zip(locs,lexp,colors):
        print ("Exp"+expname)#, color)
        df_=df[df['Expriment']=="Exp"+expname]
        print ('='*20+' df_'+expname+'='*20)
        print (df_.head())
        star=df_.loc[df_['obj.function'].idxmax(),paraList]#.groupby(['Expriment'])
        # print (star)
        # Calculate x-positions for each box in the boxplot
        box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
        # print (box_positions)
        ax.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='k', zorder=110) #'grey'

    # Update labels
    ax.set_xticklabels(paraList,rotation=90)
    # Lines between each columns of boxes
    ax.xaxis.set_minor_locator(MultipleLocator(0.5))
    #
    ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
    ax.set_ylabel(' ')#"$Metric$ $($$KGE$/$KGED$/$R^2$$)$")
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
    # new_labels = [
    #     labels[0] + "($Q$ [$KGE$] + $vWSA w/o (daily)$ [$KGED$])",
    #     labels[1] + "($Q$ [$KGE$] + $vWSA w/o (16-day)$ [$KGED$])",
    #     labels[2] + "($Q$ [$KGE$] + $vWSA w/ (16-day)$ [$KGED$])",
    #     labels[3] + "($Q$ [$KGE$] + $WSA$ [$KGED$])",
    #     # labels[2] + "($Q$ [$KGE$] + $WSA$ [$KGED$])",
    #     # labels[3] + "($Q$ [$KGE$] + $WSA$ [$KGED$])"
    # ]
    # new_labels = [
    #     labels[0] + " ($vQ$ [$KGE$])", 
    #     labels[1] + " ($vQ$ [$KGE$] + $w/o$ $error$ $vWSA$ $(daily)$ [$KGED$])", 
    #     labels[2] + " ($vQ$ [$KGE$] + $w/$ $error$ $vWSA$ $(per$ $16-day)$ [$KGED$])",
    #     labels[3] + " ($w/o$ $error$ $vWSA$ $(daily)$ [$KGED$])",
    #     # labels[2] + "($Q$ [$KGE$] + $vWSA w/o (16-day)$ [$KGED$])",
    #     # labels[3] + "($Q$ [$KGE$] + $vWSA w/ (16-day)$ [$KGED$])",
    #     labels[4] + " ($w/$ $error$ $vWSA$ $(16-day)$ [$KGED$])",
    #     labels[5] + " ($w/$ $error$ $vWSA$ $(16-day)$ [$KGED$] + $constrain$ [$Q$ $Bias$])",
    #     # labels[4] + "($Q$ [$KGE$] + $WA_{g1}(15)$ [$R^2$])", 
    #     # labels[5] + "($Q$ [$KGE$] + $WA_{g2}(18)$ [$R^2$])"
    #     # labels[4] + "($Q$ [$KGE$] + $WA_{g2}(18)$ [$KGED'$])"
    # ]

    # new_labels = [
    #     labels[0] + " ($vQ$ [$KGE$])", 
    #     labels[1] + " ($w/$ $error$ $vWSA$[$All$ $Lakes$] ($per$ $16-day$) [$KGED$])",
    #     labels[2] + " ($w/$ $error$ $vWSA$[$18$ $Lakes$] ($per$ $16-day$) [$KGED$])",
    #     labels[3] + " ($w$/$o$ $error$ $vWSA$[$18$ $Lakes$] ($per$ $16-day$) [$KGED$])",
    #     # labels[3] + " ($w/$ $error$ $vWSA$ $(16-day)$ [$KGED$] + $constrain$ [$Q$ $Bias$])",
    #     labels[4] + " ($vQ$ [$KGE$] + $w$/ $error$ $vWSA$[$All$ $Lakes$] ($per$ $16-day$) [$KGED$])",
    # ]

    label_char = get_exp_explain()
    new_labels = ["Exp " + label + " " + label_char[label] for label in lexp]

    ax.legend(handles=handles, labels=new_labels, loc='best')

    ax.set_xlabel(" ")
    # ax.set_ylim(ymin=-10.75,ymax=1.1)
    # plt.savefig('../figures/paper/fs1-KGE_boxplot_S0_CalBugdet_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')

    plt.tight_layout()
    print ('../figures/paper/fs17'+string.ascii_lowercase[k]+'-boxplot_paraList_'+paraListNames+'_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
    plt.savefig('../figures/paper/fs17'+string.ascii_lowercase[k]+'-boxplot_paraList_'+paraListNames+'_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')