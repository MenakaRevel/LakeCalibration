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
    return df[df['observed_data_series'].isin(glist)]['DIAG_KLING_GUPTA'].values #,'DIAG_SPEARMAN']].values
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
# lexp=["E0a","E0b","S0a","S1f","S1i"]
# lexp=["E0a","E0b","S0b","S1f","S1i"]
# lexp=["E0a","S0c","S0b","S1f","S1i"] #"E0b","S0b",,"S1i"
# lexp=["E0a","S0c","E0b","S0b"]
lexp=["S0b","S1i"] #"S0c",
colname={
    "E0a":"Obs_SF_IS",
    "E0b":"Obs_WL_IS",
    "S0a":"Obs_WL_IS",
    "S0b":"Obs_WL_IS",
    "S0c":"Obs_SF_IS",
    "S1d":"Obs_WA_RS3",
    "S1f":"Obs_WA_RS4",
    "S1h":"Obs_WA_RS5",
    "S1i":"Obs_WA_RS4"
}
expriment_name=[]
# read final cat 
final_cat=pd.read_csv('../OstrichRaven/finalcat_hru_info_updated.csv')
#========================================================================================
for expname in lexp:
    objFunction0=1.0
    for num in range(1,ens_num+1):
        print (expname, num)
        # metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
        # print (list(read_diagnostics(expname, num).flatten()).append(read_costFunction(expname, num))) #np.shape(read_diagnostics(expname, num)), 
        row=list(read_diagnostics(expname, num, odir=odir).flatten())
        print (len(row))
        if expname in ['E0a','S0i']:
            row.append(read_costFunction(expname, num, div=1.0, odir=odir))
            ObjLake="NaN"
            row.append(np.nan)
        elif expname in ['E0b','S0a']:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WL_IS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WL_IS']==1]['HyLakeId'].dropna().unique()]#,
            # final_cat[final_cat['Obs_WL_IS']==1]['SubId'].dropna().unique())]
            # print (llake)
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname in ['S0a']:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WL_IS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WL_IS']==1]['HyLakeId'].dropna().unique()]#,
            # final_cat[final_cat['Obs_WL_IS']==1]['SubId'].dropna().unique())]
            # print (llake)
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname in ['S0b','S0c']:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_KLING_GUPTA_DEVIATION_PRIME"
            llake=["./obs/WL_IS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WL_IS']==1]['HyLakeId'].dropna().unique()]#
            # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname in ['S1a','S1c']:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WA_RS1']==1]['HyLakeId'].dropna().unique()]#
            # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname in ['S1b']:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WA_RS2']==1]['HyLakeId'].dropna().unique()]#
            # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname in ['S1f']:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WA_RS4']==1]['HyLakeId'].dropna().unique()]#
            # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname in ['S1i']:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_KLING_GUPTA_DEVIATION_PRIME"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WA_RS4']==1]['HyLakeId'].dropna().unique()]#
            # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        else:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,subid) for lake,subid in zip(final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique(),
            final_cat[final_cat[colname[expname]]==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake)) 
        expriment_name.append("Exp"+expname)
        # print (len(row))
        print (ObjLake,row)
        metric.append([row])
metric=np.array(metric)[:,0,:]
print (np.shape(metric))
# print (metric)

# df=pd.DataFrame(metric, columns=['02KB001','KGED_02KB001','KGE_Crow','Crow',
# 'KGE_LM','LM','KGE_NC','NC','obj.function',
# 'mean_Lake'])
# df['Expriment']=np.array(expriment_name)
# print (df.head())

df=pd.DataFrame(metric, columns=['02KB001','LM','Narrowbag','Crow','NC',
'obj.function','mean_Lake'])
df['Expriment']=np.array(expriment_name)
print ('='*20+' df '+'='*20)
print (df.head(10))

df_melted = pd.melt(df[['02KB001','Narrowbag',
'Crow','LM','NC','obj.function','mean_Lake','Expriment']],
id_vars='Expriment', value_vars=['02KB001','Narrowbag','Crow','LM','NC',
'obj.function','mean_Lake','Expriment'])
print ('='*20+' df_melted '+'='*20)
print (df_melted.head(50))

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
    locs=[-0.32,-0.18,0.0,0.18,0.32]
    colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(6),plt.cm.tab20c(7)]

# colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]
colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]

fig, ax = plt.subplots(figsize=(8, 8))
ax=sns.boxplot(data=df_melted,x='variable', y='value',
order=['obj.function','02KB001','mean_Lake','Narrowbag','Crow','LM','NC'],hue='Expriment',
palette=colors, boxprops=dict(alpha=0.9))
# Get the colors used for the boxes
box_colors = [box.get_facecolor() for box in ax.artists]
print (box_colors)
for i,expname, color in zip(locs,lexp,colors):
    print ("Exp"+expname)#, color)
    df_=df[df['Expriment']=="Exp"+expname]
    print ('='*20+' df_ '+'='*20)
    print (df_.head())
    star=df_.loc[df_['obj.function'].idxmax(),['obj.function','02KB001','mean_Lake','Narrowbag','Crow','LM','NC']]#.groupby(['Expriment'])
    # print (star)
    # Calculate x-positions for each box in the boxplot
    box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
    # print (box_positions)
    ax.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='k', zorder=110) #'grey'
# Updatae labels
ax.set_xticklabels(['objective\nfunction','02KB001','Lake WL/WA','Narrowbag','Crow','LM','NC'],rotation=0)
# Lines between each columns of boxes
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
#
ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
ax.set_ylabel("$Metric$ $($$KGE'$/$KGED'$$)$") #/$R^2$$
# add validation and calibration
# ax.text(0.25,1.02,"Calibration",fontsize=12,ha='center',va='center',transform=ax.transAxes)
# ax.text(0.75,1.02,"Validation",fontsize=12,ha='center',va='center',transform=ax.transAxes)
ax.set_xlabel(" ")
# ax.set_ylim(ymin=-0.75,ymax=1.1)
ax.set_ylim(ymin=-2.2,ymax=1.1)
# plt.savefig('../figures/paper/fs1-KGE_boxplot_S0_CalBugdet_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.tight_layout()
print ('../figures/paper/fs1-KGE_boxplot_DiffWave_Dis_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.savefig('../figures/paper/fs1-KGE_boxplot_DiffWave_Dis_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')