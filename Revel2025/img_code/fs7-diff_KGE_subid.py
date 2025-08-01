#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore")
import numpy as np
import os
import string
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap, BoundaryNorm, Normalize
import matplotlib.colors as mcolors
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import cartopy
import datetime
import colormaps as cmaps
import seaborn as sns
from sklearn.linear_model import LinearRegression
mpl.use('Agg')
from exp_params import *
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
    return df[(df['observed_data_series'].str.contains('HYDROGRAPH_CALIBRATION')) & (df['filename'].isin(flist))][ObjMet].dropna().unique() #,'DIAG_SPEARMAN']].values
#========================================================================================
def read_costFunction(expname, ens_num, div=1.0, odir='/scratch/menaka/LakeCalibration/out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return (df['obj.function'].iloc[-1]/float(div))*-1.0
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
def plot_routing_product(path_to_product_folder, ax=None, version_number=''):
    product_folder = path_to_product_folder
    if version_number != '':
        version_number = '_' + version_number
    # path_subbasin = os.path.join(product_folder, 'finalcat_info' + version_number + '.geojson')
    # path_river = os.path.join(product_folder, 'finalcat_info_riv' + version_number + '.geojson')
    # path_cllake = os.path.join(product_folder, 'sl_connected_lake' + version_number + '.geojson')
    # path_ncllake = os.path.join(product_folder, 'sl_non_connected_lake' + version_number + '.geojson')
    # path_outline = os.path.join(product_folder, 'outline.geojson')

    path_subbasin = os.path.join(product_folder, 'finalcat_info' + version_number + '.shp')
    path_river = os.path.join(product_folder, 'finalcat_info_riv' + version_number + '.shp')
    path_cllake = os.path.join(product_folder, 'sl_connected_lake' + version_number + '.shp')
    path_ncllake = os.path.join(product_folder, 'sl_non_connected_lake' + version_number + '.shp')
    path_outline = os.path.join(product_folder, 'outline.shp')

    subbasin = geopandas.read_file(path_subbasin)
    # subbasin = subbasin.set_crs("EPSG:3161", allow_override=True)
    # print("Original CRS:", subbasin.crs)
    subbasin = subbasin.to_crs("EPSG:4326")
    # print("Updated CRS:", subbasin.crs)
    # subbasin.crs = "EPSG:4326"

    # print (subbasin)

    ax = ax or plt.gca()

    # subbasin.plot(ax=ax, color='w', edgecolor='#6E6E6E', linewidth=0.5, alpha=0.5)

    # if os.path.exists(path_river):
    #     river = geopandas.read_file(path_river)
    #     # river = river.set_crs("EPSG:3161", allow_override=True)
    #     river = river.to_crs("EPSG:4326")
    #     river.plot(ax=ax, color='#0070FF', linewidth=1.0)

    # if os.path.exists(path_cllake):
    #     cllake = geopandas.read_file(path_cllake)
    #     # cllake = cllake.set_crs("EPSG:3161", allow_override=True)
    #     cllake = cllake.to_crs("EPSG:4326")
    #     cllake.plot(ax=ax, color='#0070FF', edgecolor='#6E6E6E', linewidth=0.1, alpha=1.0)

    # if os.path.exists(path_ncllake):
    #     ncllake = geopandas.read_file(path_ncllake)
    #     # ncllake = ncllake.set_crs("EPSG:3161", allow_override=True)
    #     ncllake = ncllake.to_crs("EPSG:4326")
    #     ncllake.plot(ax=ax, color='#0070FF', edgecolor='#6E6E6E', linewidth=0.1, alpha=0.8)

    if os.path.exists(path_outline):
        outline = geopandas.read_file(path_outline)
        # outline = outline.set_crs("EPSG:3161", allow_override=True)
        outline = outline.to_crs("EPSG:4326")
        outline.plot(ax=ax, facecolor="none", edgecolor='k', linewidth=1, alpha=0.8)
    else:
        outline = geopandas.read_file('/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction/outline.shp')
        # outline = outline.set_crs("EPSG:3161", allow_override=True)
        outline = outline.to_crs("EPSG:4326")
        outline.plot(ax=ax, facecolor="none", edgecolor='k', linewidth=1, alpha=0.8)
#====================================================================================================
def extract_string_from_path(file_path):
    # Extract filename from the file path
    filename = os.path.basename(file_path)
    
    # Remove extension from filename
    filename_no_ext = os.path.splitext(filename)[0]
    
    # Split filename by underscore
    parts = filename_no_ext.split('_')
    
    # Extract the desired string
    desired_string = parts[3] #+ parts[2]
    
    return desired_string
#========================================================================================
def get_df_diagnostics_filename(expname, ens_num, ObjMet='DIAG_KLING_GUPTA',
flist=['./obs/SF_SY_sub921_921.rvt'],
odir='/scratch/menaka/LakeCalibration/out',output='output'):
    '''
    read the RunName_Diagnostics.csv
    '''
    fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,output)
    # print (fname) 
    df=pd.read_csv(fname)
    df['SubId']=df['filename'].apply(extract_string_from_path)
    df['SubId']=df['SubId'].astype(int)
    return df[(df['observed_data_series'].str.contains('HYDROGRAPH_CALIBRATION')) & (df['filename'].isin(flist))]#[ObjMet].dropna().unique() #,'DIAG_SPEARMAN']].values
#====================================================================================================
def plot_scatter(xlist,ylist,color, ax=None):
    ax=ax or plt.gca()
    x1 = xlist.values.reshape(-1, 1)  # Reshape for sklearn
    y1 = ylist.values
    model1 = LinearRegression().fit(x1, y1)
    trendline1 = model1.predict(x1)
    
    ax.plot(x1, y1, marker='o', linewidth=0, linestyle='none', color=colors[i])
    ax.plot(x1, trendline1, color=colors[i], linestyle='-', linewidth=2, label='Trendline')
#====================================================================================================
expname="S1a"
odir='/scratch/menaka/LakeCalibration/out'
#========================================================================================
mk_dir("../figures/paper")
ens_num=10
metric=[]
lexp=["V7t","V7f","V0z","V0a"] #["V4d","V0h"] #["V4d","V4k"] #["V4d","V0a"] #["V0a","V0h","V2e","V4e","V4k","V4d"] #["V0h","V4e","V4k"] #["V0h","V2e","V4e"] #["V0a","V4k","V4d"] #["V0a","V4e","V4k"] #["V0a","V4k","V4d","V4l"]
colname=get_final_cat_colname()
#========================================================================================
# read final cat 
final_cat=pd.read_csv('/project/def-btolson/menaka/LakeCalibration/OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
#========================================================================================
met={}
#========================================================================================
expriment_name=[]
for expname in lexp:
    objFunction0=-1.0
    # if expname=='V6d':
    #     met[expname]=1
    #     continue
    for num in range(1,ens_num+1):
        # row=list(read_Diagnostics_Raven_best(expname, num, odir=odir).flatten())
        # row.extend(list(read_lake_diagnostics(expname, num, llake, odir=odir, best_dir='best_Raven')))
        # row.append(read_costFunction(expname, num, div=1.0, odir=odir))
        objFunction=read_costFunction(expname, num, div=1.0, odir=odir)
        if objFunction > objFunction0:
            objFunction0=objFunction
            met[expname]=num
print (met)
#========================================================================================
# df_Q=pd.DataFrame(columns=lexp)
#========================================================================================
# # # plot the KGE values
subbasin = pd.read_csv('/project/def-btolson/menaka/LakeCalibration/OstrichRaven/finalcat_hru_info.csv')
# print (subbasin.columns)
subids = subbasin[subbasin['HRU_IsLake']==1]['SubId'].unique()
subids = set(subids)

# # subbasin=subbasin.loc[:,['SubId', 'HyLakeId','Obs_NM','DrainArea','MeanElev']]
# # subbasin=subbasin.assign(Obs_NM=subbasin['Obs_NM'].str.split('&')).explode('Obs_NM')

# # # # Split the 'Obs_NM' values in 'df_diag' by '&' and create a new DataFrame with the split values
# # # points_split = points_df.assign(Obs_NM=points_df['Obs_NM'].str.split('&')).explode('Obs_NM')
# # # points_split = pd.merge(points_split,df_met,on='Obs_NM',how='inner')

# # hru_info=pd.read_csv("/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction/HRU.txt", sep="\s+")
# # hru_info.rename(columns={'Attributes':'SubId'}, inplace=True)
# # hru_info=hru_info.loc[:,['SubId', 'LATITUDE','LONGITUDE']]
# # # print (hru_info.columns)

# # points_df = pd.merge(subbasin,hru_info,on='SubId',how='inner')
# # # print (hru_info.columns)
# # # print (hru_info.loc[:,['Attributes','LATITUDE','LONGITUDE']])
#====================================================================================
# product_folder = '/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction'
# version_number = 'v1-0'
product_folder = '/project/def-btolson/menaka/LakeCalibration/GIS_files/Petawawa/withlake'
version_number = ''
#========================================================================================
ExpNames=[]
hues=[]
values=[]

colors = [plt.cm.tab10(3),plt.cm.tab10(2),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab20(2),plt.cm.tab10(5),plt.cm.tab10(6)]

# path_subbasin = os.path.join(product_folder, 'finalcat_hru_info' + version_number + '.shp')
path_subbasin = os.path.join(product_folder, 'finalcat_info_riv' + version_number + '.shp')
subbasin = geopandas.read_file(path_subbasin)
subbasin = subbasin.to_crs("EPSG:4326")

# subbasin = subbasin.dropna(subset=['DrainArea'])
subbasin = subbasin[subbasin['SubId'].isin(subbasin['SubId'].unique())]

points_df = subbasin.loc[:,['SubId','geometry']]
points_df = points_df[points_df['SubId'].isin(points_df['SubId'].unique())]
# points_df = subbasin.loc[:,['SubId','geometry']] #pd.merge(points_df, subbasin.loc[:,['SubId','geometry']], on='SubId', how='inner')

# subids = subbasin[subbasin['HRU_IsLake']==1]['SubId'].unique()
# # subids = set(subids)

for i,expname in enumerate(lexp):
    if expname == 'V0z':
        # get ensemble mean
        # Dictionary to store results for each iteration
        df_mean = pd.DataFrame()

        for num in range(1, 10+1):  # Loop from 1 to 10
            lq = ["./obs/SF_SY_sub%d_%d.rvt" % (subid, subid) for subid in final_cat['SubId'].dropna().unique()]
            df_met = get_df_diagnostics_filename(expname, num, flist=lq)
            df_met = df_met.loc[:,['SubId','DIAG_KLING_GUPTA']]
            df_met.rename(columns={'DIAG_KLING_GUPTA': expname+'_'+'%02d'%(num)}, inplace=True)
            
            if num ==1:
                df_mean = df_met.copy()
            else:
                df_mean = pd.merge(df_mean, df_met, on='SubId')
        
        # Compute row-wise mean across all DIAG_KLING_GUPTA columns while keeping SubId
        df_mean['Row_Mean'] = df_mean.loc[:, df_mean.columns != 'SubId'].mean(axis=1)
        df_mean = df_mean.loc[:,['SubId','Row_Mean']]
        df_met = df_mean.copy()
        df_met.rename(columns={'Row_Mean': expname}, inplace=True)

    else:
        num = met[expname]

        lq=["./obs/SF_SY_sub%d_%d.rvt"%(subid,subid) for subid in final_cat['SubId'].dropna().unique()]
        df_met=get_df_diagnostics_filename(expname, num, flist=lq)
        df_met=df_met.loc[:,['SubId','DIAG_KLING_GUPTA']]
        df_met.rename(columns={'DIAG_KLING_GUPTA':expname}, inplace=True)

    # print (df_met.columns)
    points_df = pd.merge(points_df,df_met,on='SubId',how='inner')

points_df['diffKGE_1']  = points_df[lexp[0]] - points_df[lexp[-2]]
points_df['diffKGE_2']  = points_df[lexp[1]] - points_df[lexp[-2]]
points_df['diffKGE_0']  = points_df[lexp[-1]] - points_df[lexp[-2]] #1.0 - points_df[lexp[-1]].values #
points_df['rKGE_1']     = points_df['diffKGE_1'] / (points_df['diffKGE_0']+1e-20)
points_df['rKGE_2']     = points_df['diffKGE_2'] / (points_df['diffKGE_0']+1e-20)
points_df['Lake_cat'] = points_df['SubId'].apply(lambda x: "lake" if x in subids else "non-lake")

print (lexp[0], "-", lexp[-2])
print (lexp[1], "-", lexp[-2])
print (lexp[-1], "-", lexp[-2])
print (points_df) 
# for row in points_df.iterrows():
#     print ('%3d%6.2f%6.2f'%(row[1]['SubId'],row[1]['diffKGE_1'],row[1]['diffKGE_2']))

print ("len",len(points_df['SubId'].unique()), len(subbasin['SubId'].unique()))
# Convert to GeoDataFrame if not already
points_gdf = geopandas.GeoDataFrame(points_df, geometry='geometry')
#========================================================================================
titleList=[
    '(2b-Lake - 1a-Q)',
    '(3-Lake - 1a-Q)'
]
titleList=[
    '(2b-Lake - 1b-Q)',
    '(3-Lake - 1b-Q)'
]
if lexp[-1] == "V0a":
    titleList=[
        '(2b-Lake)',
        '(3-Lake)'
    ]
else:
    titleList=[
        '(2b-Lake)',
        '(3-Lake)'
    ]
#========================================================================================
plotFun='rKGE' #'diffKGE' # 
label=r'$rKGE$'
#========================================================================================
# figure
va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=(11.69 - 2*va_margin)*(1.0/2.0)
wdt=(8.27 - 2*ho_margin)*(2.0/2.0)

fig = plt.figure(figsize=(wdt, hgt)) #, tight_layout=True)
gs = GridSpec(ncols=3, nrows=2, figure=fig)#, height_ratios=[1.5, 1])

# Fix colormap and normalization
# cmap = cmaps.fusion.discrete(16) #cm.viridis_r  # Use a perceptually uniform colormap
cmap = mcolors.ListedColormap(cmaps.fusion.discrete(18).colors[1:-1])
vmin, vmax = -1.0, 1.0 #points_gdf['diffKGE'].min(), points_gdf['diffKGE'].max()
norm = Normalize(vmin=vmin, vmax=vmax)

# ax1 = fig.add_subplot(gs[0, 0:2])
# ax2 = fig.add_subplot(gs[1, 0])
# ax3 = fig.add_subplot(gs[1, 1])
# ax4 = fig.add_subplot(gs[1, 1])

for ii in range(2):
    # plot_routing_product(product_folder, ax=ax1)
    ax1 = fig.add_subplot(gs[ii, 0:2])
    # outline
    outline = geopandas.read_file('/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction/outline.shp')
    # outline = outline.set_crs("EPSG:3161", allow_override=True)
    outline = outline.to_crs("EPSG:4326")
    outline.plot(ax=ax1, facecolor="none", edgecolor='k', linewidth=1, alpha=0.8)

    # lakes
    path_cllake = os.path.join(product_folder, 'sl_connected_lake' + version_number + '.shp')    
    cllake = geopandas.read_file(path_cllake)
    # cllake = cllake.set_crs("EPSG:3161", allow_override=True)
    cllake = cllake.to_crs("EPSG:4326")
    cllake.plot(ax=ax1, color='w', edgecolor='grey', linewidth=0.5, alpha=1.0)

    path_ncllake = os.path.join(product_folder, 'sl_non_connected_lake' + version_number + '.shp')
    ncllake = geopandas.read_file(path_ncllake)
    # ncllake = ncllake.set_crs("EPSG:3161", allow_override=True)
    ncllake = ncllake.to_crs("EPSG:4326")
    ncllake.plot(ax=ax1, color='w', edgecolor='grey', linewidth=0.5, alpha=0.8)


    # # Plot the subbasin layer as a background
    # subbasin.plot(ax=ax1, color='w', edgecolor='#6E6E6E', linewidth=0.5, alpha=0.5)

    # Plot points with correct colormap
    # sc = subbasin.plot(ax=ax1, column='diffKGE', cmap=cmap, markersize=10, alpha=0.8, legend=False)

    # im=ax1.scatter(x=points_df['LONGITUDE'], y=points_df['LATITUDE'], c=points_df["diffKGE"], marker='o',
    #         edgecolor='k', cmap=cmaps.fusion.discrete(10), vmin=-1.0,vmax=1.0, label=r"$\Delta$KGE", zorder=110, s=50)

    im=points_gdf.plot(
        ax=ax1, column="%s_%d"%(plotFun,ii+1), 
        cmap=cmap, norm=norm, markersize=10, alpha=0.8, legend=False)

    print (
        "%s_%d"%(plotFun,ii+1),
        "%3.2f"%(points_df["%s_%d"%(plotFun,ii+1)].mean()), 
        "%3.2f"%(points_df["%s_%d"%(plotFun,ii+1)].median()))

    # ax.set_title(titleList[i], loc='left')

    ax1.text(0.0, 0.5,
        titleList[ii],
        rotation=90,
        transform=ax1.transAxes
        )

    ax1.set_title(
        string.ascii_lowercase[2*ii]+') Map of '+ label + ' ' + titleList[ii], 
        loc='left',
        )

    ax1.set_axis_off()


    #============================================================================================================
    ax2 = fig.add_subplot(gs[ii, -1])
    # histogram
    sns.histplot(
        data=points_df,
        x="%s_%d"%(plotFun,ii+1),
        stat='count', 
        bins='auto',
        hue='Lake_cat',
        cumulative=False, 
        common_norm=True, 
        kde=False,
        # common_grid=True,
        ax=ax2
        )

    ax2.set_xlim(-2.2,2.2)
    ax2.set_title(string.ascii_lowercase[2*ii+1]+') Distribution of ' + label  + ' ' + titleList[ii], loc='left')

    print (
        "lake mean | median :",
        "%3.2f"%(points_df[points_df['Lake_cat']=='lake']["%s_%d"%(plotFun,ii+1)].mean()), 
        "%3.2f"%(points_df[points_df['Lake_cat']=='lake']["%s_%d"%(plotFun,ii+1)].median()),
        "\n non-lake mean | median :",
        "%3.2f"%(points_df[points_df['Lake_cat']=='non-lake']["%s_%d"%(plotFun,ii+1)].mean()), 
        "%3.2f"%(points_df[points_df['Lake_cat']=='non-lake']["%s_%d"%(plotFun,ii+1)].median()),
        )

    ax2.set_xlabel(label) #'e) 2-All-Lake c','f) 3-18-Lake a'


# Add colorbar with correct scaling
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

left1, bottom1, width1, height1 = ax1.get_position().bounds
# left2, bottom2, width2, height2 = axes[-1].get_position().bounds
cax = fig.add_axes([left1-0.05, bottom1-0.05, width1, 0.01])

clabel=label #r"$\Delta$KGE"
cbar=plt.colorbar(sm,orientation='horizontal',shrink=0.8, extend='both',cax=cax,label=clabel)  # Add colorbar with label
cbar.set_label(clabel, fontsize=12)


# fig.tight_layout()
fig.subplots_adjust(wspace=0.0)

plt.tight_layout()

print ('../figures/fs7-map_diff_KGE_exp_'+lexp[0]+'_'+lexp[1]+'_'+lexp[-1]+'_'+ datetime.datetime.now().strftime("%Y%m%d") +'.jpg')
plt.savefig('../figures/fs7-map_diff_KGE_exp_'+lexp[0]+'_'+lexp[1]+'_'+lexp[-1]+'_'+ datetime.datetime.now().strftime("%Y%m%d") +'.jpg', dpi=500) #_summer