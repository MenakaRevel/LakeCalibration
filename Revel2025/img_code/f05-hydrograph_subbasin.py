#!/usr/python
'''
plot the ensemble metric
'''
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
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import cartopy
import datetime
import colormaps as cmaps
import seaborn as sns
mpl.use('Agg')

from exp_params import *
#===============================================================================================
def mk_dir(dir):
    # Create the download directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)
#=====================================================
def read_costFunction(expname, ens_num, div=1.0, odir='/scratch/menaka/LakeCalibration/out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return (df['obj.function'].iloc[-1]/float(div))*-1.0
#=====================================================
def read_WaterLevel(expname, ens_num, odir='../out',syear=2016,smon=1,sday=1,eyear=2020,emon=10,eday=20):
    '''
    read the RunName_WateLevels.csv
    '''
    fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/output/Petawawa_WaterLevels.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_WaterLevels.csv"%(ens_num)
    print (fname)
    df=pd.read_csv(fname)
    # calculate the metrics for syear,smon,sday:eyear,emon,eday [Evaluation Period]
    df.set_index('date',inplace=True)
    df.index=pd.to_datetime(df.index)
    start='%04d-%02d-%02d'%(syear,smon,sday)
    end='%04d-%02d-%02d'%(eyear,emon,eday)
    print (start, end)
    df=df.loc[start:end]
    # calculate spearman correlation
    return remove_noobs(df)
#=====================================================
def read_Hydrograph(expname, ens_num, odir='../out',syear=2015,smon=10,sday=1,eyear=2022,emon=9,eday=30):
    '''
    read the RunName_Hydrograph.csv
    '''
    fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/output/Petawawa_Hydrographs.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_WaterLevels.csv"%(ens_num)
    print (fname)
    df=pd.read_csv(fname)
    # calculate the metrics for syear,smon,sday:eyear,emon,eday [Evaluation Period]
    df.set_index('date',inplace=True)
    df.index=pd.to_datetime(df.index)
    start='%04d-%02d-%02d'%(syear,smon,sday)
    end='%04d-%02d-%02d'%(eyear,emon,eday)
    print (start, end)
    df=df.loc[start:end]
    # calculate spearman correlation
    return remove_noobs(df) 
#=====================================================
def remove_noobs(df):
    df[df.iloc[:,3::]==-1.2345]=np.nan 
    return df 
#np.array([df['sub265 [m]'].corr(df['sub265 (observed) [m]'] ,method='spearman'),
#    df['sub400 [m]'].corr(df['sub400 (observed) [m]'] ,method='spearman'),
#    df['sub412 [m]'].corr(df['sub412 (observed) [m]'] ,method='spearman')])
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
    print (flist)
    print (df[(df['observed_data_series'].str.contains('HYDROGRAPH_CALIBRATION')) & (df['filename'].isin(flist))]) #[ObjMet])#.dropna().unique())
    # return df[(df['observed_data_series'].str.contains('HYDROGRAPH_CALIBRATION')) & (df['filename'].isin(flist))][ObjMet].dropna().unique() #,'DIAG_SPEARMAN']].values
    return orderList(df,flist,ObjMet)
#=====================================================
def orderList(df,flist,ObjMet):
    df_filtered = df[
        (df['observed_data_series'].str.contains('HYDROGRAPH_CALIBRATION')) & 
        (df['filename'].isin(flist))
        ]

    # Ensure order matches `flist`
    df_filtered['filename'] = pd.Categorical(df_filtered['filename'], categories=flist, ordered=True)
    df_filtered = df_filtered.sort_values('filename')

    # Get unique non-null values of ObjMet
    unique_values = df_filtered[ObjMet].dropna().unique()

    return unique_values
#=====================================================
expname="S1a"
odir='/scratch/menaka/LakeCalibration/out'
#=====================================================
mk_dir("../figures")
ens_num=10
lexp=["V0z","V0h","V4e","V7f","V6e"] ##["V0z","V0h","V4e","V4d","V6d"] #["V0z","V0a","V0h","V4e","V4d","V6d"] #["V0h","V4e","V4d"] #["V0a","V0h","V2e","V4e","V4k","V4d"] #["V0h","V2e","V4e"] #["V0a","V4k","V4d"] #["V0a","V4e","V4k"] #["V0a","V4k","V4d","V4l"]
colname=get_final_cat_colname()
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
#===================
# colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]
# colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]


# # fig = plt.figure(figsize=(wdt, hgt)) #, tight_layout=True)
# # gs = GridSpec(ncols=1, nrows=5, figure=fig) #, height_ratios=[1, 1])

# # df1=read_Hydrograph(lexp[0], met[lexp[0]], odir=odir)
# # df2=read_Hydrograph(lexp[1], met[lexp[1]], odir=odir)
# # df3=read_Hydrograph(lexp[2], met[lexp[2]], odir=odir)
# # df4=read_Hydrograph(lexp[3], met[lexp[3]], odir=odir)
# # df5=read_Hydrograph(lexp[4], met[lexp[4]], odir=odir)
# # df6=read_Hydrograph(lexp[5], met[lexp[5]], odir=odir)


# # ObjQ="DIAG_KLING_GUPTA"
# # SubIds = [921, 412, 220] #400, 767, 
# # lq=["./obs/SF_SY_sub%d_%d.rvt"%(subid,subid) for subid in SubIds]
# # KB_Q1=get_list_diagnostics_filename(lexp[0], met[lexp[0]],ObjMet=ObjQ,flist=lq)
# # KB_Q2=get_list_diagnostics_filename(lexp[1], met[lexp[1]],ObjMet=ObjQ,flist=lq)
# # KB_Q3=get_list_diagnostics_filename(lexp[2], met[lexp[2]],ObjMet=ObjQ,flist=lq)
# # KB_Q4=get_list_diagnostics_filename(lexp[3], met[lexp[3]],ObjMet=ObjQ,flist=lq)
# # KB_Q5=get_list_diagnostics_filename(lexp[4], met[lexp[4]],ObjMet=ObjQ,flist=lq)
# # KB_Q6=get_list_diagnostics_filename(lexp[5], met[lexp[5]],ObjMet=ObjQ,flist=lq)

# # print (lq)
# # print (KB_Q1)
# # print (KB_Q2)
# # print (KB_Q3)
# # print (KB_Q4)
# # print (KB_Q5)
# # print (KB_Q6)
# Lake subbasin
#  767 --> Traverse
#  528 --> Cedar
#  220 --> Big Trout

# non-Lake subbasin
#  921 --> 02KB001
#  265 --> Crow
#  400 --> LittleMadawaska
#  412 --> NippissingCorrected

#========================================================================================
# Read hydrograph data dynamically
dfs = [read_Hydrograph(lexp[i], met[lexp[i]], odir=odir) for i in range(len(lexp))]

# Define objective metric and subbasin IDs
ObjQ = "DIAG_KLING_GUPTA"
SubIds = [921, 412, 220]  # 400, 767,
locNames = {
    921:'02KB001', 
    412:'Nippissing', 
    400:'Little Madawaska', 
    767:'Downstream of Lake Traverse',
    220:'Downstream of Big Trout Lake'
} 

# Generate diagnostic file paths
lq = [f"./obs/SF_SY_sub{subid}_{subid}.rvt" for subid in SubIds]

# Get diagnostics dynamically
KB_Q = [get_list_diagnostics_filename(lexp[i], met[lexp[i]], ObjMet=ObjQ, flist=lq) for i in range(len(lexp))]

#========================================================================================
# making figure
colors = [plt.cm.tab10(3),plt.cm.tab10(2),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab20(2),plt.cm.tab10(5),plt.cm.tab10(6)]
colors = [plt.cm.tab10(3),plt.cm.tab10(2),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab20(2),plt.cm.tab10(5),plt.cm.tab10(6)]

# locs=[-0.26,0,0.26]
locs=[-0.27,-0.11,0.11,0.27]

va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=(11.69 - 2*va_margin)*(float(len(SubIds))/5.0)
wdt=(8.27 - 2*ho_margin)*(2.0/2.0)
# Define subplots dynamically
fig, gs = plt.figure(figsize=(wdt, hgt)), plt.GridSpec(len(SubIds), 1)
axes = [fig.add_subplot(gs[i, 0]) for i in range(len(SubIds))]

# Define subbasin indices and titles
subbasin_indices = range(len(SubIds))
titles = [
    "a) Subbasin {} at {}",
    "b) Subbasin {} at {}",
    "c) Subbasin {} at {}",
    "d) Subbasin {} at {}",
    "e) Subbasin {} at {}",
]

expname_list=[
    '0-base',
    '1-Q',
    # '1b-Q',
    '2a-Lake',
    '2b-Lake',
    '3-Lake'
    ]
# Observations and Experiments
experiments = [
    (dfs[i], KB_Q[i], expname_list[i], '-', 0.5, colors[i], 101 + i) for i in range(len(lexp))
]

for ax, idx, title in zip(axes, subbasin_indices, titles):
    # Observations
    ax.plot(dfs[0].index, dfs[0][f'sub{SubIds[idx]} (observed) [m3/s]'],
            linestyle='-', linewidth=3, label="Truth", color='k', zorder=100)
    
    # Experiments
    for df, KB_Q_exp, label, linestyle, linewidth, color, zorder in experiments:
        ax.plot(df.index, df[f'sub{SubIds[idx]} [m3/s]'],
                linestyle=linestyle, linewidth=linewidth, 
                label=f'{label} (KGE:{KB_Q_exp[subbasin_indices.index(idx)]:.2f})', 
                color=color, zorder=zorder)
    
    # Labels and Titles
    ax.set_ylabel('discharge $m^3/s$')
    ax.set_title(title.format(SubIds[idx],locNames[SubIds[idx]]), loc='left')
    ax.legend(fontsize=8)

plt.tight_layout()

print ('../figures/f05-hydrographs_exp_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.savefig('../figures/f05-hydrographs_exp_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
# print ('../figures/f05-hydrographs_exp.jpg')
# plt.savefig('../figures/f05-hydrographs_exp.jpg', dpi=500)