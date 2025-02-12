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
lexp=["V0h","V4e","V4d"] #["V0a","V0h","V2e","V4e","V4k","V4d"] #["V0h","V2e","V4e"] #["V0a","V4k","V4d"] #["V0a","V4e","V4k"] #["V0a","V4k","V4d","V4l"]
colname=get_final_cat_colname()
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
#===================
# colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]
colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]
colors = [plt.cm.tab10(3),plt.cm.tab10(2),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab20(2),plt.cm.tab10(5),plt.cm.tab10(6)]

# locs=[-0.26,0,0.26]
locs=[-0.27,-0.11,0.11,0.27]

va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=(11.69 - 2*va_margin)*(5.0/5.0)
wdt=(8.27 - 2*ho_margin)*(2.0/2.0)

fig = plt.figure(figsize=(wdt, hgt)) #, tight_layout=True)
gs = GridSpec(ncols=1, nrows=5, figure=fig) #, height_ratios=[1, 1])

df1=read_Hydrograph(lexp[0], met[lexp[0]], odir=odir)
df2=read_Hydrograph(lexp[1], met[lexp[1]], odir=odir)
df3=read_Hydrograph(lexp[2], met[lexp[2]], odir=odir)


ObjQ="DIAG_KLING_GUPTA"
SubIds = [921, 412, 400, 767, 220]
lq=["./obs/SF_SY_sub%d_%d.rvt"%(subid,subid) for subid in SubIds]
KB_Q1=get_list_diagnostics_filename(lexp[0], met[lexp[0]],ObjMet=ObjQ,flist=lq)
KB_Q2=get_list_diagnostics_filename(lexp[1], met[lexp[1]],ObjMet=ObjQ,flist=lq)
KB_Q3=get_list_diagnostics_filename(lexp[2], met[lexp[2]],ObjMet=ObjQ,flist=lq)

print (lq)
print (KB_Q1)
print (KB_Q2)
print (KB_Q3)
# Lake subbasin
#  767 --> Traverse
#  528 --> Cedar
#  220 --> Big Trout

# non-Lake subbasin
#  921 --> 02KB001
#  265 --> Crow
#  400 --> LittleMadawaska
#  412 --> NippissingCorrected
ax0 = fig.add_subplot(gs[0,0])
ax1 = fig.add_subplot(gs[1,0])
ax2 = fig.add_subplot(gs[2,0])
ax3 = fig.add_subplot(gs[3,0])
ax4 = fig.add_subplot(gs[4,0])

# Observations
ax0.plot(df1.index,df1['sub921 (observed) [m3/s]'],linestyle='-',linewidth=3,label="Truth",color='k',zorder=100)
ax1.plot(df1.index,df1['sub412 (observed) [m3/s]'],linestyle='-',linewidth=3,label="Truth",color='k',zorder=100)
ax2.plot(df1.index,df1['sub400 (observed) [m3/s]'],linestyle='-',linewidth=3,label="Truth",color='k',zorder=100)
ax3.plot(df1.index,df1['sub767 (observed) [m3/s]'],linestyle='-',linewidth=3,label="Truth",color='k',zorder=100)
ax4.plot(df1.index,df1['sub220 (observed) [m3/s]'],linestyle='-',linewidth=3,label="Truth",color='k',zorder=100)

# exp 1
ax0.plot(df1.index,df1['sub921 [m3/s]'],linestyle='-',linewidth=1,label='1-Q (KGE:%3.2f)'%(KB_Q1[0]),color=colors[0],zorder=101)
ax1.plot(df1.index,df1['sub412 [m3/s]'],linestyle='-',linewidth=1,label='1-Q (KGE:%3.2f)'%(KB_Q1[1]),color=colors[0],zorder=101)
ax2.plot(df1.index,df1['sub400 [m3/s]'],linestyle='-',linewidth=1,label='1-Q (KGE:%3.2f)'%(KB_Q1[2]),color=colors[0],zorder=101)
ax3.plot(df1.index,df1['sub767 [m3/s]'],linestyle='-',linewidth=1,label='1-Q (KGE:%3.2f)'%(KB_Q1[3]),color=colors[0],zorder=101)
ax4.plot(df1.index,df1['sub220 [m3/s]'],linestyle='-',linewidth=1,label='1-Q (KGE:%3.2f)'%(KB_Q1[4]),color=colors[0],zorder=101)

# exp 2
ax0.plot(df2.index,df2['sub921 [m3/s]'],linestyle='-',linewidth=0.8,label='2-Lake (KGE:%3.2f)'%(KB_Q2[0]),color=colors[1],zorder=102)
ax1.plot(df2.index,df2['sub412 [m3/s]'],linestyle='-',linewidth=0.8,label='2-Lake (KGE:%3.2f)'%(KB_Q2[1]),color=colors[1],zorder=102)
ax2.plot(df2.index,df2['sub400 [m3/s]'],linestyle='-',linewidth=0.8,label='2-Lake (KGE:%3.2f)'%(KB_Q2[2]),color=colors[1],zorder=102)
ax3.plot(df2.index,df2['sub767 [m3/s]'],linestyle='-',linewidth=0.8,label='2-Lake (KGE:%3.2f)'%(KB_Q2[3]),color=colors[1],zorder=102)
ax4.plot(df2.index,df2['sub220 [m3/s]'],linestyle='-',linewidth=0.8,label='2-Lake (KGE:%3.2f)'%(KB_Q2[4]),color=colors[1],zorder=102)

# exp 2
ax0.plot(df3.index,df3['sub921 [m3/s]'],linestyle='-',linewidth=0.6,label='3-Lake (KGE:%3.2f)'%(KB_Q3[0]),color=colors[2],zorder=103)
ax1.plot(df3.index,df3['sub412 [m3/s]'],linestyle='-',linewidth=0.6,label='3-Lake (KGE:%3.2f)'%(KB_Q3[1]),color=colors[2],zorder=103)
ax2.plot(df3.index,df3['sub400 [m3/s]'],linestyle='-',linewidth=0.6,label='3-Lake (KGE:%3.2f)'%(KB_Q3[2]),color=colors[2],zorder=103)
ax3.plot(df3.index,df3['sub767 [m3/s]'],linestyle='-',linewidth=0.6,label='3-Lake (KGE:%3.2f)'%(KB_Q3[3]),color=colors[2],zorder=103)
ax4.plot(df3.index,df3['sub220 [m3/s]'],linestyle='-',linewidth=0.6,label='3-Lake (KGE:%3.2f)'%(KB_Q3[4]),color=colors[2],zorder=103)

# legend
ax0.legend(fontsize=8)
ax1.legend(fontsize=8)
ax2.legend(fontsize=8)
ax3.legend(fontsize=8)
ax4.legend(fontsize=8)

# y-label
ax0.set_ylabel('discharge $m^3/s$')
ax1.set_ylabel('discharge $m^3/s$')
ax2.set_ylabel('discharge $m^3/s$')
ax3.set_ylabel('discharge $m^3/s$')
ax4.set_ylabel('discharge $m^3/s$')

# titles
ax0.set_title("a) Subbasin 921 at 02KB001", loc='left')
ax1.set_title("b) Subbasin 412 at Nippissing", loc='left')
ax2.set_title("c) Subbasin 400 at Little Madawaska", loc='left')
ax3.set_title("d) Subbasin 767 at Downstream of Lake Traverse", loc='left')
ax4.set_title("e) Subbasin 220 at Downstream of Big Trout Lake", loc='left')


plt.tight_layout()
# print ('../figures/f04-KGE_02KB001_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
# plt.savefig('../figures/f04-KGE_02KB001_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
print ('../figures/f05-hydrographs_exp.jpg')
plt.savefig('../figures/f05-hydrographs_exp.jpg', dpi=500)