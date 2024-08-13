#!/usr/python
'''
plot the ensemble metric
'''
import warnings
warnings.filterwarnings("ignore")
import os
import numpy as np
import scipy
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
import matplotlib.colors
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import matplotlib.lines as mlines
import datetime
mpl.use('Agg')
#===============================================================================================
def mk_dir(dir):
    # Create the download directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)
#=====================================================
def read_costFunction(expname, ens_num, odir='../out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return df['obj.function'].iloc[-1]
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
#=====================================================
expname="S1a"
odir='../out'
#=====================================================
mk_dir("../figures/paper")
ens_num=10
# lexp=["S0a","S0b","S1a","S1b"]
lexp=["E0a","E0b","S1d"]
best_member={}
for expname in lexp:
    objFunction=[]
    for num in range(1,ens_num+1):
        print (expname, num)
        objFunction.append(read_costFunction(expname, num, odir=odir))
        # expriment_name.append("Exp"+expname)
    best_member[expname]=np.array(objFunction).argmin() + 1

print (best_member)
#===================
# colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]
colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]

# locs=[-0.26,0,0.26]
locs=[-0.27,-0.11,0.11,0.27]

va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=(11.69 - 2*va_margin)*(3.0/5.0)
wdt=(8.27 - 2*ho_margin)*(2.0/2.0)

fig = plt.figure(figsize=(wdt,hgt))
G   = gridspec.GridSpec(ncols=1, nrows=4)
ax1 = fig.add_subplot(G[0,0])
ax2 = fig.add_subplot(G[1,0])
ax3 = fig.add_subplot(G[2,0])
ax4 = fig.add_subplot(G[3,0])
# sub921 [m3/s],sub921 (observed) [m3/s]
df=read_Hydrograph(lexp[0], best_member[lexp[0]])
# ax1.plot(df.index,df['sub921 (observed) [m3/s]'],linestyle='-',linewidth=3,color='k')
ax1.plot(df.index,df['sub288 (observed) [m3/s]'],linestyle='-',linewidth=3,color='k')
ax2.plot(df.index,df['sub265 (observed) [m3/s]'],linestyle='-',linewidth=3,color='k')
ax3.plot(df.index,df['sub400 (observed) [m3/s]'],linestyle='-',linewidth=3,color='k')
ax4.plot(df.index,df['sub412 (observed) [m3/s]'],linestyle='-',linewidth=3,color='k')
for i,expname in enumerate(lexp):
    df_=read_Hydrograph(expname, best_member[expname])
    # ax1.plot(df_.index,df_['sub921 [m3/s]'],linestyle='-',linewidth=1,color=colors[i])
    ax1.plot(df_.index,df_['sub288 [m3/s]'],linestyle='-',linewidth=1,color=colors[i])
    ax2.plot(df_.index,df_['sub265 [m3/s]'],linestyle='-',linewidth=1,color=colors[i])
    ax3.plot(df_.index,df_['sub400 [m3/s]'],linestyle='-',linewidth=1,color=colors[i])
    ax4.plot(df_.index,df_['sub412 [m3/s]'],linestyle='-',linewidth=1,color=colors[i])

# df=read_WaterLevel(lexp[0], best_member[lexp[0]])
# ax2.plot(df.index,df['sub265 (observed) [m]']-df['sub265 (observed) [m]'].mean(),linestyle='-',linewidth=3,color='k')
# ax3.plot(df.index,df['sub400 (observed) [m]']-df['sub400 (observed) [m]'].mean(),linestyle='-',linewidth=3,color='k')
# ax4.plot(df.index,df['sub412 (observed) [m]']-df['sub412 (observed) [m]'].mean(),linestyle='-',linewidth=3,color='k')
# for i,expname in enumerate(lexp):
#     df_=read_WaterLevel(expname, best_member[expname])
#     ax2.plot(df_.index,df_['sub265 [m]']-df_['sub265 [m]'].mean(),linestyle='-',linewidth=1,color=colors[i])
#     ax3.plot(df_.index,df_['sub400 [m]']-df_['sub400 [m]'].mean(),linestyle='-',linewidth=1,color=colors[i])
#     ax4.plot(df_.index,df_['sub412 [m]']-df_['sub412 [m]'].mean(),linestyle='-',linewidth=1,color=colors[i])
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax2.xaxis.set_major_locator(mdates.YearLocator())
ax3.xaxis.set_major_locator(mdates.YearLocator())
ax4.xaxis.set_major_locator(mdates.YearLocator())
# titles '02KB001','Crow','LM','NC'
# ax1.text(0.05,1.06,'a) 02KB001',ha='center',va='center',transform=ax1.transAxes,fontsize=10)
ax1.text(0.05,1.06,'a) Narrowbag',ha='center',va='center',transform=ax1.transAxes,fontsize=10)
ax2.text(0.05,1.06,'b) Crow',ha='center',va='center',transform=ax2.transAxes,fontsize=10)
ax3.text(0.05,1.06,'c) LM',ha='center',va='center',transform=ax3.transAxes,fontsize=10)
ax4.text(0.05,1.06,'d) NC',ha='center',va='center',transform=ax4.transAxes,fontsize=10)
# legend 
features=[]
pnum=len(lexp)
new_labels = ['Exp 1', 'Exp 2', 'Exp 3']
for i in np.arange(pnum):
    # label="Exp %s"%(lexp[i])
    label=new_labels[i]
    features.append(mlines.Line2D([], [], color=colors[i],label=label))
legend=plt.legend(handles=features,loc="lower center", bbox_to_anchor=[0.5,0.03],bbox_transform=fig.transFigure, 
    ncol=4,  borderaxespad=0.0, frameon=False, prop={'size': 8})#

plt.tight_layout()
plt.savefig('../figures/paper/f05-hydrograph_gagues'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')