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
from matplotlib.ticker import ScalarFormatter, FuncFormatter
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
# Define the scientific formatter for the x-axis labels
def scientific_formatter(x, pos):
    print (x, pos)
    # Avoid zero or negative values for log calculation
    if x <= 0:
        return str(x)  # Return the original value if it's zero or negative
    
    # Compute the log base 10 of x and format it in scientific notation
    exponent = np.floor(np.log10(x))
    return f'({10**int(exponent)}^{int(exponent)})'
#====================================================================================================
def calculate_upstream_lake_volume(df):
    """
    Function to calculate the upstream lake volume based on river topology.
    """
    # Create a dictionary of subId to their corresponding lake volumes
    lake_vol_dict = dict(zip(df['SubId'], df['LakeVol']))
    
    # Initialize a new column for upstream lake volume
    df['UpstreamLakeVol'] = 0
    
    # For each SubId, calculate the total upstream lake volume
    def get_upstream_volume(sub_id, visited=set()):
        # If the sub_id has been visited, return the cached result (to avoid circular dependencies)
        if sub_id in visited:
            return 0
        visited.add(sub_id)
        
        # Get the lake volume at the current sub-basin
        total_volume = lake_vol_dict.get(sub_id, 0)
        
        # Find the downstream sub-basin (DowSubId)
        downstream_sub_id = df.loc[df['SubId'] == sub_id, 'DowSubId'].values
        
        if downstream_sub_id:
            downstream_sub_id = downstream_sub_id[0]
            # Recursively add the upstream volume of the downstream sub-basin
            total_volume += get_upstream_volume(downstream_sub_id, visited)
        
        return total_volume
    
    # Calculate the upstream lake volume for each sub-basin
    for sub_id in df['SubId']:
        df.loc[df['SubId'] == sub_id, 'UpstreamLakeVol'] = get_upstream_volume(sub_id)
    
    return df
#====================================================================================================
expname="S1a"
odir='/scratch/menaka/LakeCalibration/out'
#========================================================================================
mk_dir("../figures")
ens_num=10
metric=[]
lexp=["V4d","V0h"] #["V0h","V4e","V4d"] #["V0a","V0h","V2e","V4e","V4k","V4d"] #["V0h","V4e","V4k"] #["V0h","V2e","V4e"] #["V0a","V4k","V4d"] #["V0a","V4e","V4k"] #["V0a","V4k","V4d","V4l"]
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
# plot the KGE values
# subbasin = pd.read_csv('/project/def-btolson/menaka/LakeCalibration/OstrichRaven/finalcat_hru_info.csv')
# print (subbasin.columns)

product_folder = '/project/def-btolson/menaka/LakeCalibration/GIS_files/Petawawa/withlake'
version_number = ''

path_subbasin = os.path.join(product_folder, 'finalcat_hru_info' + version_number + '.shp')
# path_subbasin = os.path.join(product_folder, 'finalcat_info_riv' + version_number + '.shp')
subbasin = geopandas.read_file(path_subbasin)

subbasin = subbasin.dropna(subset=['DrainArea'])
subbasin = subbasin[subbasin['SubId'].isin(subbasin['SubId'].unique())]

# subbasin['DrainArea']=subbasin['DrainArea']*1e-6

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
#========================================================================================
ExpNames=[]
hues=[]
values=[]

for i,expname in enumerate(lexp):
    objFunction0=1.0
    num = met[expname]

    lq=["./obs/SF_SY_sub%d_%d.rvt"%(subid,subid) for subid in final_cat['SubId'].dropna().unique()]
    df_met=get_df_diagnostics_filename(expname, num, flist=lq)
    # print (df_met.columns)
    points_df = pd.merge(points_df,df_met.loc[:,['SubId','DIAG_KLING_GUPTA']],on='SubId',how='inner')
    # points_df['Lake_cat']=[1 if subid in subids else 0 for subid in points_met['SubId'].values]
    if i==0:
        points_df['Lake_cat'] = points_df['SubId'].isin(subids).astype(int)

    points_df.rename(columns={'DIAG_KLING_GUPTA':expname},inplace=True)

points_df['diffKGE'] = points_df[lexp[0]] - points_df[lexp[1]]

# Drop NaN values for DrainArea and all KGE columns
filtered_gdf = points_df.dropna(subset=['DrainArea'] + lexp)

logscale=False #True

if not logscale:
    # Calculate the percentiles (e.g., 0%, 25%, 50%, 75%, 100%)
    percentiles = np.percentile(filtered_gdf['DrainArea'], range(0,100+1, 20)) #[0, 25, 50, 75, 100])

    # Round the bin edges up to the nearest 10,000 (or any other desired round number)
    rounded_edges = np.ceil(percentiles / 10000) * 10000

    # Create the bins using pd.cut()
    filtered_gdf['DrainArea_bin'] = pd.cut(filtered_gdf['DrainArea'], bins=rounded_edges)
else:
    # Apply log transformation to DrainArea
    filtered_gdf['log_DrainArea'] = np.log10(filtered_gdf['DrainArea'])

    # Calculate the percentiles on the log-transformed data
    percentiles_log = np.percentile(filtered_gdf['log_DrainArea'], range(0, 100 + 1, 20))

    # Round the bin edges up to the nearest whole number (you can also scale this further)
    rounded_log_edges = np.ceil(percentiles_log)

    # Inverse transform the log bin edges to get the actual DrainArea values
    rounded_edges = np.power(10, rounded_log_edges)  # Inverse log scale

    # Ensure the bin edges are unique
    rounded_edges_unique = np.unique(rounded_edges)

    # Create the bins using pd.cut() on the original 'DrainArea' values
    filtered_gdf['DrainArea_bin'] = pd.cut(filtered_gdf['DrainArea'], bins=rounded_edges_unique)


# # Compute mean KGE for each DrainArea bin
# mean_kge = filtered_gdf.groupby('DrainArea_bin')[lexp].mean().reset_index()

# # Convert DrainArea_bin to a string for bar plot categories
# mean_kge['DrainArea_bin'] = mean_kge['DrainArea_bin'].astype(str)

# # Melt DataFrame for seaborn (long format for grouped bars)
# mean_kge_melted = mean_kge.melt(id_vars='DrainArea_bin', var_name='KGE_Type', value_name='Mean_KGE')



# Define thresholds
threshold = 1e-20

# # Categorize diffKGE into bins
# filtered_gdf['Category'] = pd.cut(
#     filtered_gdf['diffKGE'], 
#     bins=[-np.inf, -threshold, threshold, np.inf], 
#     labels=['Negative', 'No Change', 'Positive']
# )

# # Count occurrences in each DrainArea_bin
# diffKGE_counts = filtered_gdf.groupby(['DrainArea_bin', 'Category']).size().reset_index(name='Count')

# Filter only positive cases
filtered_gdf['Positive'] = filtered_gdf['diffKGE'] > threshold

# Count occurrences in each DrainArea_bin
positive_counts = (
    filtered_gdf[filtered_gdf['Positive']]
    .groupby('DrainArea_bin')
    .size()
    .reset_index(name='Count')
)

# Plot as grouped bar chart
# plt.figure(figsize=(12, 10))
va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=(11.69 - 2*va_margin)*(1.0/3.0)
wdt=(8.27 - 2*ho_margin)*(1.0/2.0)

# Plotting
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(gs[0, 0])

# sns.barplot(
#     ax=ax,
#     data=diffKGE_counts,
#     x='DrainArea_bin',
#     y='Count',
#     hue='Category',
#     palette={'Positive': 'green', 'Negative': 'red', 'No Change': 'gray'}
# )
sns.barplot(
    ax=ax,
    data=positive_counts,
    x='DrainArea_bin',
    y='Count',
    color='green'  # Only positive cases
)

# Customize plot
ax.set_xlabel('Drainage Area ($km^2$)')
ax.set_ylabel('Count of diffKGE Cases')
ax.set_title('Distribution of diffKGE Categories Across Drainage Area Bins')
ax.legend(title='diffKGE Category')


# fig = plt.figure(figsize=(wdt, hgt)) # 12, 10, tight_layout=True)
# gs = GridSpec(ncols=1, nrows=1, figure=fig) #, height_ratios=[1, 1])
# ax = fig.add_subplot(gs[0, 0])
# sns.barplot(
#     ax=ax, 
#     data=mean_kge_melted, 
#     x='DrainArea_bin', 
#     y='Mean_KGE', 
#     hue='KGE_Type', 
#     palette='Set2',
#     legend=False)

# # Customize plot
# ax.set_xlabel('Drainage Area ($km^2$)')
# ax.set_ylabel('Mean KGE')
# ax.set_title('a) Mean KGE with Drainage Area')
# ax.set_xticks(rotation=90, ha='right')  # Rotate x-axis labels for better readability

# # Apply custom scientific notation to x-axis
# plt.gca().xaxis.set_major_formatter(FuncFormatter(scientific_formatter))

# print (mean_kge_melted['DrainArea_bin'].unique())
# Use scientific notation on the x-axis
# plt.gca().xaxis.set_major_formatter(ScalarFormatter('scientific'))

# Convert x-axis tick labels to scientific notation format
labels = ax.get_xticklabels()
formatted_labels = []

for label in labels:
    # Extract the bounds from the label (e.g., '(1000000.0, 10000000.0]')
    left, right = label.get_text()[1:-1].split(',')  # Remove parentheses and split by comma
    left, right = float(left.strip()), float(right.strip())  # Convert to float
    
    # Convert from m^2 to km^2 (divide by 10^6)
    left_km2 = left / 1e6
    right_km2 = right / 1e6
    
    # Format both the left and right bounds in LaTeX scientific notation with superscript
    left_formatted = f'{left_km2:.0e}'  # Format left bound
    right_formatted = f'{right_km2:.0e}'  # Format right bound as scientific notation
    
    # Combine the formatted left and right bounds
    formatted_labels.append(f'(${left_formatted}, {right_formatted}$)')

# Set the new formatted labels for the x-axis
ax.set_xticklabels(formatted_labels)

# # Extract the bar positions and heights for each hue
# hue_levels = mean_kge_melted['KGE_Type'].unique()
# bar_positions = {}
# heights = {}

# Show grid and legend
plt.legend(title="KGE Type")
plt.grid(axis='y', linestyle='--', alpha=0.7)

#==============================
# Create custom legend handles using colored boxes (Patches)
#
colors=[plt.cm.Set2(0),plt.cm.Set2(1),plt.cm.Set2(2),plt.cm.Set2(3),plt.cm.Set2(4),plt.cm.Set2(5),plt.cm.Set2(6)]
#
legend_handles = [Patch(facecolor=color, label=label) for label, color in zip(lexp, colors)]

# Add a common legend to the figure.
# Adjust the loc, ncol, bbox_to_anchor, etc. as desired.
fig.legend(handles=legend_handles, loc='lower center', ncol=len(lexp), fontsize='large', frameon=False)


'''
#==========================================================
# Calculate the percentiles for each group
percentiles = np.linspace(0, 100, 20) #[0,  20, 40, 60, 80, 100] #np.linspace(0, 100, 6)

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

colors = [plt.cm.tab10(3),plt.cm.tab10(2),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab20(2),plt.cm.tab10(5),plt.cm.tab10(6)]

# fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(16, 16))
fig = plt.figure(figsize=(16, 8), tight_layout=True)
gs = GridSpec(ncols=2, nrows=1, figure=fig) #, height_ratios=[1, 1])

#==============================
ax1 = fig.add_subplot(gs[0, 0])
# df_melt
df_sort = points_df.sort_values('DA_groups').copy()
df_melt = pd.melt(
    df_sort.loc[:,lexp+['DA_groups_name']], #df_sort['Lake_cat']!=1
    id_vars='DA_groups_name', 
    value_vars=lexp,
    )

# print (df_melt.head(5))
# print (df_sort['DA_groups'].unique)
# print (df_melt['DA_groups_name'].unique)

# plot_boxplot_numeric_with_hue(
plot_barplot_numeric_with_hue(
    df_melt['DA_groups_name'],
    df_melt['value'],
    df_melt['variable'],
    ax=ax1,
    xlabel= 'Drainage Area Percentile',
    ylabel= 'median KGE',
    title='a) median KGE against drainage area'
    )

#==============================
ax2 = fig.add_subplot(gs[0, 1])
# df_melt
df_sort = points_df.sort_values('Elevtn_groups').copy()
df_melt = pd.melt(
    df_sort.loc[:,lexp+['Elevtn_groups_name']], # df_sort['Lake_cat']!=1
    id_vars='Elevtn_groups_name', 
    value_vars=lexp
    )

# print (df_melt.head(5))

# plot_boxplot_numeric_with_hue(
plot_barplot_numeric_with_hue(
    df_melt['Elevtn_groups_name'],
    df_melt['value'],
    df_melt['variable'],
    ax=ax2,
    xlabel= 'Elevation Percentile',
    ylabel= 'median KGE',
    title='b) median KGE against elevation'
    )
#==============================
# # ax3 = fig.add_subplot(gs[1, 0])
# # # df_melt
# # df_sort = points_df.sort_values('DA_groups').copy()
# # df_melt = pd.melt(
# #     df_sort.loc[df_sort['Lake_cat']==1,lexp+['DA_groups_name']],
# #     id_vars='DA_groups_name', 
# #     value_vars=lexp,
# #     )

# # # print (df_melt.head(5))
# # # print (df_sort['DA_groups'].unique)
# # # print (df_melt['DA_groups_name'].unique)

# # # plot_boxplot_numeric_with_hue(
# # plot_barplot_numeric_with_hue(
# #     df_melt['DA_groups_name'],
# #     df_melt['value'],
# #     df_melt['variable'],
# #     ax=ax3,
# #     xlabel= 'Drainage Area Percentile',
# #     ylabel= 'median KGE',
# #     title='c) Lake subbasins KGE against drainage area'
# #     )

# # #==============================
# # ax4 = fig.add_subplot(gs[1, 1])
# # # df_melt
# # df_sort = points_df.sort_values('Elevtn_groups').copy()
# # df_melt = pd.melt(
# #     df_sort.loc[df_sort['Lake_cat']==1,lexp+['Elevtn_groups_name']],
# #     id_vars='Elevtn_groups_name', 
# #     value_vars=lexp
# #     )

# # # print (df_melt.head(5))

# # # plot_boxplot_numeric_with_hue(
# # plot_barplot_numeric_with_hue(
# #     df_melt['Elevtn_groups_name'],
# #     df_melt['value'],
# #     df_melt['variable'],
# #     ax=ax4,
# #     xlabel= 'Elevation Percentile',
# #     ylabel= 'median KGE',
# #     title='d) Lake subbasins KGE against elevation'
# #     )

#==============================
# Create custom legend handles using colored boxes (Patches)
legend_handles = [Patch(facecolor=color, label=label) for label, color in zip(lexp, colors)]

# Add a common legend to the figure.
# Adjust the loc, ncol, bbox_to_anchor, etc. as desired.
fig.legend(handles=legend_handles, loc='lower center', ncol=len(lexp), fontsize='large', frameon=False)
'''
#==============================
# plt.tight_layout()
# plt.savefig('../figures/f07-scatter_DA_ele_'+ datetime.datetime.now().strftime("%Y%m%d") +'.jpg', dpi=500) #_summer
plt.savefig('../figures/f07-scatter_DA_ele_.jpg', dpi=500) #_summer