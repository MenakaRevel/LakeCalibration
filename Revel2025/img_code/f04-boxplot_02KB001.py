#!/usr/python
'''
plot the 02KB001 dischrge 
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
from matplotlib.gridspec import GridSpec
mpl.use('Agg')

from exp_params import *
#===============================================================================================
def mk_dir(dir):
    # Create the download directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)
#=====================================================
def read_diagnostics(expname, ens_num, odir='/scratch/menaka/LakeCalibration/out',output='output',
glist=['HYDROGRAPH_CALIBRATION[921]','HYDROGRAPH_CALIBRATION[400]',
'HYDROGRAPH_CALIBRATION[288]','HYDROGRAPH_CALIBRATION[265]',
'HYDROGRAPH_CALIBRATION[412]']):
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
    fname=odir+"/"+expname+"_%02d/best/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,output)
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/output_Raven_v3.7/Petawawa_Diagnostics.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    print (fname) 
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    # if expname == 'V0a':
    df.drop_duplicates(subset=['observed_data_series'], keep='first', inplace=True)
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
#=====================================================
def read_costFunction(expname, ens_num, div=1.0, odir='/scratch/menaka/LakeCalibration/out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return (df['obj.function'].iloc[-1]/float(div))*-1.0
#=====================================================
def read_lake_diagnostics(expname, ens_num, ObjLake, llake, odir='/scratch/menaka/LakeCalibration/out',output='output'):
    '''
    read the RunName_Diagnostics.csv get average value of the metric given
    DIAG_KLING_GUPTA_DEVIATION
    DIAG_R2
    '''
    # HYDROGRAPH_CALIBRATION[921],./obs/02KB001_921.rvt
    # WATER_LEVEL_CALIBRATION[265],./obs/Crow_265.rvt
    # WATER_LEVEL_CALIBRATION[400],./obs/Little_Madawaska_400.rvt
    # WATER_LEVEL_CALIBRATION[412],./obs/Nippissing_Corrected_412.rvt
    fname=odir+"/"+expname+"_%02d/best/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,output)
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/output_Raven_v3.7/Petawawa_Diagnostics.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    print (fname) 
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    return df[(df['observed_data_series'].str.contains('CALIBRATION')) & (df['filename'].isin(llake))][ObjLake].mean() #,'DIAG_SPEARMAN']].values
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
#=====================================================
expname="S1a"
odir='/scratch/menaka/LakeCalibration/out'
#========================================================================================
mk_dir("../figures")
ens_num=10
metric=[]
lexp=["V0a","V0h","V2e","V4e","V4k","V4d"]
colname=get_final_cat_colname()
expriment_name=[]
# read final cat 
# final_cat=pd.read_csv(odir+'/../OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
final_cat=pd.read_csv('../../OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
print (final_cat.columns)
#========================================================================================
for expname in lexp:
    objFunction0=1.0
    for num in range(1,ens_num+1):
        print ("="*20)
        print (expname,"_",num)
        row=[read_costFunction(expname, num, div=1.0, odir=odir)]
        SubIds = final_cat[final_cat['Obs_NM']=='02KB001']['SubId'].dropna().unique()
        lq=["./obs/SF_SY_sub%d_%d.rvt"%(subid,subid) for subid in SubIds]
        ObjQ="DIAG_KLING_GUPTA"
        row.append(get_list_diagnostics_filename(expname, num,ObjMet=ObjQ,flist=lq)[0])
        ObjQ="DIAG_R2"
        row.append(get_list_diagnostics_filename(expname, num,ObjMet=ObjQ,flist=lq)[0])
        ObjQ="DIAG_PCT_BIAS"
        row.append(get_list_diagnostics_filename(expname, num,ObjMet=ObjQ,flist=lq)[0])
        expriment_name.append("Exp"+expname)
        print (len(row))
        # print (ObjLake,row)
        metric.append([row])
metric=np.array(metric)[:,0,:]
print (np.shape(metric))

df=pd.DataFrame(metric, columns=['obj.function','KGE','R2','pBIAS'])
df['Expriment']=np.array(expriment_name)
print ('='*20+' df '+'='*20)
print (df.head(100))

# df_melted = pd.melt(df[['KGE','Expriment']], #'obj.function',
# id_vars='Expriment', value_vars=['KGE']) # ,'obj.function'
# print ('='*20+' df_melted '+'='*20)
# print (df_melted.head(50))


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
    colors = [plt.cm.tab10(2),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11),plt.cm.tab20c(12),plt.cm.tab20c(0),plt.cm.tab20c(8)]
elif len(lexp) == 7:
    locs=[-0.35,-0.22,-0.10,0.0,0.10,0.22,0.35]
    colors = [plt.cm.Set1(0),plt.cm.Set1(1),plt.cm.tab20(4),plt.cm.tab20(5),plt.cm.tab20(2),plt.cm.tab20(3)]
# else:
#     locs=[-0.32,-0.18,0.0,0.18,0.32]
#     colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(6),plt.cm.tab20c(7)]

# colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]
# colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]
# colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11),plt.cm.tab20c(12)]
# colors = [plt.cm.tab10(3),plt.cm.tab10(0),plt.cm.tab10(1),plt.cm.tab10(2),plt.cm.tab10(4),plt.cm.tab10(5),plt.cm.tab10(6)]
# colors = [plt.cm.tab10(3),plt.cm.tab10(0),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab10(4),plt.cm.tab10(5),plt.cm.tab10(6)]
colors = [plt.cm.tab10(3),plt.cm.tab10(2),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab20(2),plt.cm.tab10(5),plt.cm.tab10(6)]

# tab:blue : #1f77b4
# tab:orange : #ff7f0e
# tab:green : #2ca02c
# tab:red : #d62728
# tab:purple : #9467bd
# tab:brown : #8c564b
# tab:pink : #e377c2
# tab:gray : #7f7f7f
# tab:olive : #bcbd22
# tab:cyan : #17becf

metName={
    'DIAG_KLING_GUPTA':'KGE',
    'DIAG_R2':'R2',
    'DIAG_PCT_BIAS':'pBias'
}
# fig, ax = plt.subplots(figsize=(16, 8))
fig = plt.figure(figsize=(16, 16)) #, tight_layout=True)
gs = GridSpec(ncols=2, nrows=2, figure=fig, height_ratios=[1, 1])

# ax1 = fig.add_subplot(gs[0, 0])
# ax2 = fig.add_subplot(gs[0, 1])
# ax3 = fig.add_subplot(gs[1, 0])
# ax4 = fig.add_subplot(gs[1, 1])
for j,objMet in enumerate(['KGE','R2','pBIAS']):
    xx=int(j/2.0)
    yy=int(j%2.0)
    print (xx, yy)
    if objMet == 'pBIAS':
        ylim = 12.52
        yadd = 0.25
    else:
        ylim = 1.02
        yadd = 0.02
    ax = fig.add_subplot(gs[xx, yy])

    df_melted = pd.DataFrame()
    for expname in df['Expriment'].unique():
        print (expname, df[df['Expriment']==expname][objMet])
        df_melted[expname]=df[df['Expriment']==expname][objMet].values
    print ('='*20+' df_melted '+'='*20)
    print (df_melted.head(50))
    # ax=sns.boxplot(data=df_melted,x='variable', y='value',
    # order=['KGE'],hue='Expriment',
    # palette=colors, boxprops=dict(alpha=0.9))
    sns.boxplot(data=df_melted,palette=colors, boxprops=dict(alpha=0.9),ax=ax)
    # Get the colors used for the boxes
    box_colors = [box.get_facecolor() for box in ax.artists]
    # print (box_colors)
    # for i,expname, color in zip(locs,lexp,colors):

    for i, expname in enumerate(lexp):
        # print ("Exp"+expname)#, color)
        df_=df[df['Expriment']=="Exp"+expname]
        # print ('='*20+' df_ '+'='*20)
        # print (df_.head(10))
        star=df_.loc[df_['obj.function'].idxmax(),objMet]#.groupby(['Expriment'])
        # print (star)
        # Calculate x-positions for each box in the boxplot
        box_positions = [pos + offset for pos in range(len(df_melted.columns)) for offset in [i]]
        # print (box_positions, star)
        ax.scatter(x=i, y=star, marker='o', s=250, color=colors[i], edgecolors='k', zorder=110) #'grey'
        #========================================================
        subset = df_.loc[:,objMet]
        print (subset)
        if not subset.empty:
            # Calculate and annotate the median
            median_val = subset.median()
            ax.text(i, ylim+yadd, f'({median_val:.2f})', ha='center', va='center', 
                    color='k', fontsize=12, fontweight='bold')

            print (expname, median_val)

    # Updatae labels
    # ax.set_xticklabels(['KGE'],rotation=0)
    # Lines between each columns of boxes
    ax.xaxis.set_minor_locator(MultipleLocator(0.5))
    #
    # ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
    ax.set_ylabel("$"+objMet+"$", fontsize=14) #/$R^2$$

    ax.set_xticklabels([
        '1-Q a\n(02KB001)',
        '1-Q b\n(02KB001)',
        '2-AllLake a\n(365 Lake WSA)',
        '2-AllLake b\n(365 Lake WSA)',
        '2-AllLake c\n(18 Lake WSA)',
        '3-18Lake a\n(18 Lake WSA)',
        ]
        , fontsize=10)

    ax.set_xlabel(" ")
    if objMet == 'pBIAS':
        ax.set_ylim(ymin=-8.2,ymax=ylim)
    else:
        ax.set_ylim(ymin=-0.2,ymax=ylim)

    # ax.set_ylim(ymin=-2.2,ymax=1.1)
    # ax.set_ylim(ymin=-0.2,ymax=1.1)
# plt.savefig('../figures/paper/fs1-KGE_boxplot_S0_CalBugdet_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.tight_layout()
print ('../figures/f04-KGE_02KB001_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.savefig('../figures/f04-KGE_02KB001_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')