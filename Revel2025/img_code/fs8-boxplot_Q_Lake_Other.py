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
import geopandas
import re
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
import matplotlib.colors
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
expname="S1a"
odir='/scratch/menaka/LakeCalibration/out'
#========================================================================================
mk_dir("../figures/paper")
ens_num=10
metric=[]
lexp=["V0h","V4e","V4d"] #["V0a","V0h","V2e","V4e","V4k","V4d"] #["V0h","V2e","V4e"] #["V0a","V4k","V4d"] #["V0a","V4e","V4k"] #["V0a","V4k","V4d","V4l"]
colname=get_final_cat_colname()
#========================================================================================
# read final cat 
final_cat=pd.read_csv('../../OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
#====================================================================================
# product_folder = '/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction'
# version_number = 'v1-0'
product_folder = '/project/def-btolson/menaka/LakeCalibration/GIS_files/Petawawa/withlake'
version_number = ''
#========================================================================================
path_subbasin = os.path.join(product_folder, 'finalcat_info_riv' + version_number + '.shp')
subbasin = geopandas.read_file(path_subbasin)
subbasin = subbasin.to_crs("EPSG:4326")
#========================================================================================
final_cat=pd.merge(final_cat,subbasin.loc[:,['SubId','geometry']],on='SubId',how='inner')
final_cat.drop(columns='geometry',inplace=True)
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
ExpNames=[]
hues=[]
values=[]
for expname in lexp:
    objFunction0=1.0
    num = met[expname]
    # for num in range(1,ens_num+1):
    print (expname, num)
    ObjQ="DIAG_KLING_GUPTA"
    SubIds = final_cat[final_cat['Obs_NM']=='02KB001']['SubId'].dropna().unique()
    lq=["./obs/SF_SY_sub%d_%d.rvt"%(subid,subid) for subid in SubIds]
    KB_Q=get_list_diagnostics_filename(expname, num,ObjMet=ObjQ,flist=lq)
    lq=["./obs/SF_SY_sub%d_%d.rvt"%(subid,subid) for subid in final_cat[final_cat['HRU_IsLake']==1]['SubId'].dropna().unique()]
    lake_Q=get_list_diagnostics_filename(expname, num,ObjMet=ObjQ,flist=lq)
    lq=["./obs/SF_SY_sub%d_%d.rvt"%(subid,subid) for subid in final_cat[final_cat['HRU_IsLake']!=1]['SubId'].dropna().unique()]
    nonlake_Q=get_list_diagnostics_filename(expname, num,ObjMet=ObjQ,flist=lq)
    #========================================================================================
    print (len(KB_Q), (len(lake_Q) + len(nonlake_Q)))
    ExpNames.extend([expname]*(len(KB_Q)+len(lake_Q)+len(nonlake_Q)))
    hues.extend(['02KB001']*len(KB_Q)+['Lake_Q']*len(lake_Q)+['non-Lake_Q']*len(nonlake_Q))
    values.extend(np.concatenate([KB_Q,lake_Q,nonlake_Q]))

#========================================================================================
df_Q = pd.DataFrame({
    'ExpNames': ExpNames,
    'Value': values,
    'Hue': hues
})
print (df_Q.head())
# Plot the boxplot

# Set a nice seaborn color palette
# sns.set_palette("muted")  # Choose your preferred palette here
# sns.color_palette("Pastel",len(df_Q['ExpNames'].unique())*len(df_Q['Hue'].unique()))

custom_palette = ['#253750','#e2a474','#a65628']

# Filter out rows where 'Hue' == '02KB001'
df_Q_filtered = df_Q.copy()
df_Q_filtered.loc[df_Q_filtered['Hue'] == '02KB001', 'Value'] = -9999.0

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

# Create the boxplot with a custom palette
sns.boxplot(
    data=df_Q_filtered,
    x='ExpNames',
    y='Value',
    hue='Hue',
    palette=custom_palette, #"muted",  # Apply the palette to the boxplot
    showmeans=False,
    showcaps=True,
    ax=ax
)

# Overlay individual data points
sns.stripplot(
    data=df_Q,
    x='ExpNames',
    y='Value',
    hue='Hue',
    dodge=True,  # Align points with boxes
    palette=custom_palette, #"muted",  # Same palette for consistency
    alpha=0.2,        # Adjust transparency
    jitter=True,       # Slight horizontal spread
    ax=ax
)
# # Annotate the median
# for i, category in enumerate(df_Q['ExpNames'].unique()):
#     mval=[]
#     for j, hue in enumerate(df_Q['Hue'].unique()):
#         median_val = df_Q[(df_Q['ExpNames'] == category) & (df_Q['Hue'] == hue)]['Value'].median()
#         mval.append(median_val)
#         ax.text(i + (j - 0.7) * 0.27, 1.25, f'({median_val:.2f})', ha='center', va='center', 
#                 color='k', fontsize=8, fontweight='bold')
    
#     print (("%s ,   %3.2f ,  %3.2f ,  %3.2f")%(category, mval[0], mval[1], mval[2]))


# Custom Position Mapping (adjust offset for better alignment)
pos_map = {
    (exp, hue): idx + (hue_idx - (len(df_Q['Hue'].unique()) - 1) / 2) * 0.2
    for idx, exp in enumerate(df_Q['ExpNames'].unique())
    for hue_idx, hue in enumerate(df_Q['Hue'].unique())
}

# Extract the x positions of the boxes and hues
# Get the positions of the ExpNames categories on the x-axis
exp_names = df_Q['ExpNames'].unique()
hues = df_Q['Hue'].unique()
positions_map = {}

# Calculate the box positions based on ExpNames and Hue
for i, exp in enumerate(exp_names):
    for j, hue in enumerate(hues):
        # Find the positions of the box and adjust based on Hue
        positions_map[(exp, hue)] = i + (j - (len(hues) - 1) / 2) * 0.27


print (positions_map)

# Annotate the median and single-value points
for (exp, hue), x_pos in positions_map.items():
    subset = df_Q[(df_Q['ExpNames'] == exp) & (df_Q['Hue'] == hue)]
    if not subset.empty:
        # Calculate and annotate the median
        median_val = subset['Value'].median()
        ax.text(x_pos, 1.25, f'({median_val:.2f})', ha='center', va='center', 
                color='k', fontsize=12, fontweight='bold')

        # Plot single-value points
        if len(subset) == 1:
            ax.scatter(x_pos, subset['Value'].iloc[0], color=custom_palette[0], s=100, zorder=10)
    print (exp, hue, median_val)


ax.set_ylabel('$KGE$')

ax.set_ylim(ymin=-0.5,ymax=1.2)

# add xtickslabels
# ax.set_xticklabels(['02KB001\nOnly','All Lakes\n[KGED]','18 Lakes\n[KGED]'])
# ax.set_xticklabels(['02KB001\nOnly','18 Lakes\n[KGED]','18 Lakes\n[KGE]'])
# ax.set_xticklabels(['02KB001\nOnly','18 Lakes\n[KGE]\nindividual CW','18 Lakes\n[KGE]\nCW mutiplier'])
# ax.set_xticklabels(['02KB001\nOnly','18 Lakes\n[KGE]\nCW mutiplier','18 Lakes\n[KGED]\nno obs error'])

# ax.set_xticklabels([
#     'Outlet\nDischarge Only',
#     'Obs all Lakes\n(no bias KGE)\ncal all indi CW',
#     'Obs all Lakes\ncal all indi CW',
#     'Obs 18 Lakes*\ncal all indi CW',
#     'Obs 18 Lakes*\ncal 18 indi CW',
#     ])

ax.set_xticklabels([
    '1-Q\n(02KB001)',
    '2-Lake\n(365 Lake WSA)',
    '3-Lake\n(18 Lake WSA)',
    ]
    , fontsize=10)

# ax.set_xticklabels([
#     '1-Q a\n(02KB001)',
#     '1-Q b\n(02KB001)',
#     '2-AllLake a\n(365 Lake WSA)',
#     '2-AllLake b\n(365 Lake WSA)',
#     '2-AllLake c\n(18 Lake WSA)',
#     '3-18Lake a\n(18 Lake WSA)',
#     # '3-18Lake 2\n(18 daily Lake WSA)',
#     # '2-AllLake 3\n(18 daily Lake WSA)'
#     ],
#     fontsize=12)

ax.set_xlabel('')

# Remove duplicate legends caused by overlaying stripplot
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles[:len(df_Q['Hue'].unique())], labels[:len(df_Q['Hue'].unique())], loc='lower left')

plt.title('')
plt.tight_layout()
print ('../figures/f06-KGE_boxplot_Q_lake_other_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.savefig('../figures/f06-KGE_boxplot_Q_lake_other_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
# print ('../figures/f06-KGE_boxplot_Q_lake_other.jpg')
# plt.savefig('../figures/f06-KGE_boxplot_Q_lake_other.jpg')