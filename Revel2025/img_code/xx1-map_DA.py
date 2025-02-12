#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore")
import numpy as np
import os
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap, BoundaryNorm, Normalize
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
def plot_routing_product(path_to_product_folder, ax=None, version_number='v1-0'):
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

    subbasin.plot(ax=ax, color='w', edgecolor='#6E6E6E', linewidth=0.5, alpha=0.5)

    if os.path.exists(path_river):
        river = geopandas.read_file(path_river)
        # river = river.set_crs("EPSG:3161", allow_override=True)
        river = river.to_crs("EPSG:4326")
        river.plot(ax=ax, color='#0070FF', linewidth=1.0)

    if os.path.exists(path_cllake):
        cllake = geopandas.read_file(path_cllake)
        # cllake = cllake.set_crs("EPSG:3161", allow_override=True)
        cllake = cllake.to_crs("EPSG:4326")
        cllake.plot(ax=ax, color='#0070FF', edgecolor='#6E6E6E', linewidth=0.1, alpha=1.0)

    if os.path.exists(path_ncllake):
        ncllake = geopandas.read_file(path_ncllake)
        # ncllake = ncllake.set_crs("EPSG:3161", allow_override=True)
        ncllake = ncllake.to_crs("EPSG:4326")
        ncllake.plot(ax=ax, color='#0070FF', edgecolor='#6E6E6E', linewidth=0.1, alpha=0.8)

    if os.path.exists(path_outline):
        outline = geopandas.read_file(path_outline)
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
def plot_grouped_numeric(xlist, ylist, color, ax=None, bins=None):
    ax = ax or plt.gca()
    
    # Bin or group numeric xlist values
    if bins is not None:
        # Bin xlist into specified bins
        x_bins = pd.cut(xlist, bins=bins, include_lowest=True)
        grouped = ylist.groupby(x_bins).mean()  # Group by bins and calculate mean
        x_grouped = [f"{interval.left:.2f}-{interval.right:.2f}" for interval in grouped.index]
    else:
        # Use unique numeric values of xlist directly as groups
        grouped = ylist.groupby(xlist).mean()
        x_grouped = grouped.index

    y_grouped = grouped.values

    # Drop NaN values
    valid_indices = ~np.isnan(y_grouped)
    x_grouped_valid = np.array(x_grouped)[valid_indices]
    y_grouped_valid = y_grouped[valid_indices]

    # Fit a linear regression model to the grouped data
    x_numeric = np.arange(len(x_grouped_valid)).reshape(-1, 1)  # Sequential integers for x-axis positions
    model = LinearRegression().fit(x_numeric, y_grouped_valid)
    trendline = model.predict(x_numeric)

    # Plot grouped data as bars
    ax.bar(x_grouped_valid, y_grouped_valid, color=color, alpha=0.7, label='Grouped Values')
    
    # Plot trendline
    ax.plot(x_numeric.flatten(), trendline, color=color, linestyle='-', linewidth=2, label='Trendline')
   
    # # Adjust x-axis for numeric labels
    # if bins is not None:
    #     ax.set_xticks(range(len(x_grouped)))
    #     ax.set_xticklabels(x_grouped, rotation=45, ha='right')
    
    # # Add labels and legend
    # ax.set_xlabel('Grouped Numeric Values' if bins else 'Unique Numeric Values')
    # ax.set_ylabel('Y Values')
    # ax.legend()
#====================================================================================================
def plot_boxplot_numeric(xlist, ylist, color, ax=None, bins=None):
    ax = ax or plt.gca()
    
    # Bin or group numeric xlist values
    if bins is not None:
        # Bin xlist into specified bins
        x_bins = pd.cut(xlist, bins=bins, include_lowest=True)
        grouped = ylist.groupby(x_bins)
        x_grouped = [f"{interval.left:.2f}-{interval.right:.2f}" for interval in grouped.groups.keys()]
    else:
        # Use unique numeric values of xlist directly as groups
        grouped = ylist.groupby(xlist)
        x_grouped = list(grouped.groups.keys())

    # Prepare data for the boxplot
    boxplot_data = [group.values for _, group in grouped]

    # Create the boxplot
    bp = ax.boxplot(
        boxplot_data, 
        patch_artist=True,  # Enables coloring of the boxes
        boxprops=dict(facecolor=color, color=color),  # Colors for the box
        medianprops=dict(color='black'),  # Style for the median line
        whiskerprops=dict(color=color),  # Whisker color
        capprops=dict(color=color)  # Cap color
    )
    
    # Set x-axis labels
    ax.set_xticks(range(1, len(x_grouped) + 1))
    ax.set_xticklabels(x_grouped, rotation=45, ha='right')
    
    # Add labels
    ax.set_xlabel('Grouped Numeric Values' if bins else 'Unique Numeric Values')
    ax.set_ylabel('KGE')
    ax.set_title('Boxplot of Grouped Values')
#====================================================================================================
def plot_boxplot_numeric_with_hue(xlist, ylist, hue, ax=None, xlabel='Grouped Values',ylabel='KGE',title='title'):
    colors = [plt.cm.tab10(3),plt.cm.tab10(2),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab20(2),plt.cm.tab10(5),plt.cm.tab10(6)]

    ax = ax or plt.gca()

    # Prepare DataFrame for plotting
    data = pd.DataFrame({'x_grouped': xlist, 'y': ylist, 'hue': hue})

    # Create the boxplot with hue
    sns.boxplot(
        x='x_grouped', 
        y='y', 
        hue='hue', 
        data=data, 
        ax=ax, 
        palette=colors,  # Adjust palette for better distinction
        showfliers=False,  # Hide outliers for clarity (optional)
        # legend=False
    )

    # Add trendlines for each hue
    hue_groups = data.groupby(['x_grouped', 'hue'])
    median_data = hue_groups['y'].median().reset_index()  # Compute median y for each x_grouped and hue
    print ("="*20)
    print (title)
    print (median_data)
    # # # Get unique positions of the boxplot categories (considering both x_grouped and hue)
    # # positions = []
    # # for i, x_val in enumerate(data['x_grouped'].unique()):
    # #     for j, hue_val in enumerate(data['hue'].unique()):
    # #         positions.append((i, j))

    # # # Create a dictionary to map (x_grouped, hue) combinations to their positions on the x-axis
    # # position_map = {f"{x_val}-{hue_val}": pos for (x_val, hue_val), pos in zip(data.groupby(['x_grouped', 'hue']).groups.keys(), range(len(hue_groups)))}

    # # # Plot trendlines for each hue
    # # for idx, hue_value in enumerate(data['hue'].unique()):
    # #     hue_data = median_data[median_data['hue'] == hue_value]

    # #     # Calculate x positions for each (x_grouped, hue) combination
    # #     x_positions = [position_map[f"{x}-{hue_value}"] for x in hue_data['x_grouped']]

    # #     ax.plot(
    # #         x_positions,
    # #         hue_data['y'],
    # #         label=f"Trendline ({hue_value})",
    # #         color=colors[idx % len(colors)],
    # #         linestyle='--',
    # #         marker='o',
    # #         linewidth=2,
    # #     )

    # Style the plot
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    # ax.legend(title='Exp Name', loc='upper left')  # Adjust legend title
#====================================================================================================
def plot_barplot_numeric_with_hue(xlist, ylist, hue, ax=None, xlabel='Grouped Values', ylabel='KGE', title='title',ymin=-0.4,ymax=1.02):
    # Define a custom color palette
    colors = [plt.cm.tab10(3), plt.cm.tab10(2), plt.cm.tab10(8), 
              plt.cm.tab10(12), plt.cm.tab20(2), plt.cm.tab10(5), plt.cm.tab10(6)]

    # Use existing axes or create new ones
    ax = ax or plt.gca()

    # Prepare DataFrame for plotting
    data = pd.DataFrame({'x_grouped': xlist, 'y': ylist, 'hue': hue})

    # Create the barplot with hue
    sns.barplot(
        x='x_grouped', 
        y='y', 
        hue='hue', 
        data=data, 
        ax=ax, 
        palette=colors, 
        # ci=None,  # Disable confidence intervals for clarity,
        legend=False  # disable the legend in this subplot
    )

    # Compute median values for trendlines
    hue_groups = data.groupby(['x_grouped', 'hue'])
    median_data = hue_groups['y'].median().reset_index()
    print ("="*20)
    print (title)
    print (median_data)

    # # Add trendlines for each hue
    # for idx, hue_value in enumerate(median_data['hue'].unique()):
    #     hue_data = median_data[median_data['hue'] == hue_value]

    #     ax.plot(
    #         hue_data['x_grouped'], 
    #         hue_data['y'], 
    #         label=f"Trendline ({hue_value})", 
    #         color=colors[idx % len(colors)], 
    #         linestyle='--', 
    #         marker='o', 
    #         linewidth=2
    #     )
    
    # Remove the legend that Seaborn automatically creates
    # ax.legend_.remove()

    # # # Try removing the legend if it exists.
    # # # Method 1: Using ax.legend_ (this is often set by Seaborn)
    # # if hasattr(ax, 'legend_') and ax.legend_ is not None:
    # #     ax.legend_.remove()
    # # # Method 2: Alternatively, try getting the legend and removing it.
    # # else:
    # #     lgd = ax.get_legend()
    # #     if lgd is not None:
    # #         lgd.remove()

    # ylim
    ax.set_ylim(ymin=ymin,ymax=ymax)

    # Style the plot
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc='left')
    ax.legend(title='Hue', loc='upper left')  # Adjust legend title
#====================================================================================================
expname="S1a"
odir='/scratch/menaka/LakeCalibration/out'
#========================================================================================
mk_dir("../figures")
ens_num=10
metric=[]
lexp=["V0h","V4e","V4d"] #["V0a","V0h","V2e","V4e","V4k","V4d"] #["V0h","V4e","V4k"] #["V0h","V2e","V4e"] #["V0a","V4k","V4d"] #["V0a","V4e","V4k"] #["V0a","V4k","V4d","V4l"]
colname=get_final_cat_colname()
#========================================================================================
# read final cat 
final_cat=pd.read_csv('/project/def-btolson/menaka/LakeCalibration/OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
# #========================================================================================
# met={}
# #========================================================================================
# expriment_name=[]
# for expname in lexp:
#     objFunction0=-1.0
#     for num in range(1,ens_num+1):
#         # row=list(read_Diagnostics_Raven_best(expname, num, odir=odir).flatten())
#         # row.extend(list(read_lake_diagnostics(expname, num, llake, odir=odir, best_dir='best_Raven')))
#         # row.append(read_costFunction(expname, num, div=1.0, odir=odir))
#         objFunction=read_costFunction(expname, num, div=1.0, odir=odir)
#         if objFunction > objFunction0:
#             objFunction0=objFunction
#             met[expname]=num
# print (met)
#========================================================================================
# df_Q=pd.DataFrame(columns=lexp)
#========================================================================================
# plot the KGE values
subbasin = pd.read_csv('/project/def-btolson/menaka/LakeCalibration/OstrichRaven/finalcat_hru_info.csv')
print (subbasin.columns)

subids = subbasin[subbasin['HRU_IsLake']==1]['SubId'].unique()
subids = set(subids)

subbasin=subbasin.loc[:,['SubId', 'HyLakeId','Obs_NM','DrainArea','MeanElev']]
subbasin=subbasin.assign(Obs_NM=subbasin['Obs_NM'].str.split('&')).explode('Obs_NM')

# # Split the 'Obs_NM' values in 'df_diag' by '&' and create a new DataFrame with the split values
# points_split = points_df.assign(Obs_NM=points_df['Obs_NM'].str.split('&')).explode('Obs_NM')
# points_split = pd.merge(points_split,df_met,on='Obs_NM',how='inner')

hru_info=pd.read_csv("/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction/HRU.txt", sep="\s+")
hru_info.rename(columns={'Attributes':'SubId'}, inplace=True)
hru_info=hru_info.loc[:,['SubId', 'LATITUDE','LONGITUDE']]
# print (hru_info.columns)

points_df = pd.merge(subbasin,hru_info,on='SubId',how='inner')
print (hru_info.columns)
# print (hru_info.loc[:,['Attributes','LATITUDE','LONGITUDE']])
#====================================================================================
product_folder = '/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction'
version_number = 'v1-0'
# # #========================================================================================
# # ExpNames=[]
# # hues=[]
# # values=[]

# # for i,expname in enumerate(lexp):
# #     objFunction0=1.0
# #     num = met[expname]

# #     lq=["./obs/SF_SY_sub%d_%d.rvt"%(subid,subid) for subid in final_cat['SubId'].dropna().unique()]
# #     df_met=get_df_diagnostics_filename(expname, num, flist=lq)
# #     # print (df_met.columns)
# #     points_df = pd.merge(points_df,df_met.loc[:,['SubId','DIAG_KLING_GUPTA']],on='SubId',how='inner')
# #     # points_df['Lake_cat']=[1 if subid in subids else 0 for subid in points_met['SubId'].values]
# #     if i==0:
# #         points_df['Lake_cat'] = points_df['SubId'].isin(subids).astype(int)

# #     points_df.rename(columns={'DIAG_KLING_GUPTA':expname},inplace=True)
#==========================================================
# Calculate the percentiles for each group
percentiles = [0,  20, 40, 60, 80, 100] #np.linspace(0, 100, 6)

#==========================================================
# Drainage Area

# Create an empty list to store the group names
points_df['DA_groups'] = ''
points_df['DA_groups_name'] = ''

# Iterate over each pair of consecutive percentiles
for i, (lower_percentile, upper_percentile) in enumerate(zip(percentiles[0:5], percentiles[1:]), 1):
    # Create a boolean mask for the current group
    print (
        lower_percentile, 
        upper_percentile, 
        np.percentile(points_df['DrainArea'], lower_percentile), 
        np.percentile(points_df['DrainArea'], upper_percentile)
        )
    if lower_percentile == 0:
        mask = (points_df['DrainArea'] >= np.percentile(points_df['DrainArea'], lower_percentile)) & (points_df['DrainArea'] <= np.percentile(points_df['DrainArea'], upper_percentile))
    else:
        mask = (points_df['DrainArea'] > np.percentile(points_df['DrainArea'], lower_percentile)) & (points_df['DrainArea'] <= np.percentile(points_df['DrainArea'], upper_percentile))

    points_df.loc[mask,'DA_groups'] = i

    points_df.loc[mask,'DA_groups_name'] = '<%3.2f'%(upper_percentile*0.01) #np.percentile(points_df['DrainArea'], upper_percentile)*1e-6)

#==========================================================
# Elevation

# Create an empty list to store the group names
points_df['Elevtn_groups'] = ''
points_df['Elevtn_groups_name'] = ''

# Iterate over each pair of consecutive percentiles
for i, (lower_percentile, upper_percentile) in enumerate(zip(percentiles[0:5], percentiles[1:]), 1):
    # Create a boolean mask for the current group
    print (
        lower_percentile, 
        upper_percentile, 
        np.percentile(points_df['MeanElev'], lower_percentile), 
        np.percentile(points_df['MeanElev'], upper_percentile)
        )
    if lower_percentile == 0:
        mask = (points_df['MeanElev'] >= np.percentile(points_df['MeanElev'], lower_percentile)) & (points_df['MeanElev'] <= np.percentile(points_df['MeanElev'], upper_percentile))
    else:
        mask = (points_df['MeanElev'] > np.percentile(points_df['MeanElev'], lower_percentile)) & (points_df['MeanElev'] <= np.percentile(points_df['MeanElev'], upper_percentile))

    points_df.loc[mask,'Elevtn_groups'] = i

    points_df.loc[mask,'Elevtn_groups_name'] = '<%3.2f'%(upper_percentile*0.01) #np.percentile(points_df['DrainArea'], upper_percentile)*1e-6)
#==========================================================
print (points_df.head(5))
#==========================================================
# read 
product_folder = '/project/def-btolson/menaka/LakeCalibration/GIS_files/Petawawa/withlake'
version_number = ''

path_subbasin = os.path.join(product_folder, 'finalcat_hru_info' + version_number + '.shp')
# path_subbasin = os.path.join(product_folder, 'finalcat_info_riv' + version_number + '.shp')
subbasin = geopandas.read_file(path_subbasin)
subbasin = subbasin.to_crs("EPSG:4326")

fig = plt.figure(figsize=(16, 10), tight_layout=True)
gs = GridSpec(ncols=1, nrows=1, figure=fig) #, height_ratios=[1, 1])

ax1 = fig.add_subplot(gs[0, 0])

points_df = pd.merge(points_df, subbasin.loc[:,['SubId','geometry']], on='SubId', how='outer')

# Convert to GeoDataFrame if not already
points_gdf = geopandas.GeoDataFrame(points_df, geometry='geometry')

# Identify rows where DrainArea is NaN
nan_subids = points_gdf[points_gdf['DrainArea'].isna()]['SubId'].unique()

# Print the SubIds with NaN DrainArea
print("SubIds with NaN DrainArea:", nan_subids)

# Drop rows where DrainArea is NaN
points_gdf = points_gdf.dropna(subset=['DrainArea'])

print (points_gdf)
'''
colors = [plt.cm.tab10(3),plt.cm.tab10(2),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab20(2),plt.cm.tab10(5),plt.cm.tab10(6)]

unique_groups = sorted(points_gdf['DA_groups'].unique())

# Create a ListedColormap and BoundaryNorm for discrete mapping
# cmap = ListedColormap(colors[:len(unique_groups)])

cmap = plt.get_cmap('viridis_r', len(points_gdf['DA_groups'].unique()))  # Discrete colormap
norm = BoundaryNorm(unique_groups + [max(unique_groups) + 1], cmap.N)

# for i in range(1,5+1):
#     print (i, points_gdf[points_gdf['DA_groups']==i]['DrainArea'].mean())
#     color = cmap(norm(group))
#     points_gdf[points_gdf['DA_groups']==i].plot(ax=ax1,color=colors[i-1],linewidth=0.5, alpha=0.7, legend=True) #edgecolor='grey',
'''
'''
# Loop through DA_groups and plot with colors
for i, group in enumerate(sorted(points_gdf['DA_groups'].unique())):
    subset = points_gdf[points_gdf['DA_groups'] == group]
    color = cmap(norm(group))  # Get color from colormap
    print(group, subset['DrainArea'].mean())  # Print mean DrainArea for each group
    subset.plot(ax=ax1, color=color, markersize=10, alpha=0.7, label=f'DA_group {group}')




# Add discrete colorbar with specified colors
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Required for colorbar to work
cbar = fig.colorbar(sm, ax=ax1, orientation='vertical', ticks=unique_groups)
cbar.set_label('DA_groups')
cbar.set_ticks(unique_groups)  # Ensure ticks align with groups
cbar.set_ticklabels([f'Group {g}' for g in unique_groups])  # Custom tick labels

# Add legend manually
ax1.legend(title="DA Groups", loc='upper right')
'''

subbasin = subbasin.dropna(subset=['DrainArea'])
subbasin = subbasin[subbasin['SubId'].isin(subbasin['SubId'].unique())]

# Plot the subbasin layer as a background
subbasin.plot(ax=ax1, color='w', edgecolor='#6E6E6E', linewidth=0.5, alpha=0.5)

# Fix colormap and normalization
cmap = cm.viridis_r  # Use a perceptually uniform colormap
vmin, vmax = subbasin['DrainArea'].min(), subbasin['DrainArea'].max()
norm = Normalize(vmin=vmin, vmax=vmax)

# Plot points with correct colormap
sc = subbasin.plot(ax=ax1, column='DrainArea', cmap=cmap, markersize=10, alpha=0.8, legend=False)

# Add colorbar with correct scaling
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax1, orientation='vertical')
cbar.set_label('DrainArea')


# plt.colorbar()
plt.savefig('../figures/xx1-map_DA.jpg')