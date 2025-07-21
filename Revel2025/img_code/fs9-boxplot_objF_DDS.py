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
import matplotlib.patches as mpatches
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
# lexp=["E0a","E0b","S1z","V1a","V1b"] #"S0c",
# lexp=["E0a","E0b","V1a","V1b"]#,"E0c"]
# lexp=["E0a","E0b","V1a","V1b","V1c","V1d","S1z"]
# lexp=["V1a","V1b","V1c","V1d","V2a","V2d"] #"V1e",
# lexp=["V0a","V1a","V1d","V2a","V2d","V2e"]
# lexp=["V2d","V2e"]#,"V3d"]
# lexp=["V0a","V2e","V2d"]
# lexp=["V0a","V2e","V2d","V2a","V1d","V1e"]
# lexp=["V0a","V0b","V2d","V2e","V2f","V4d","V4e","V4f","V4g"]
# lexp=["V0a","V2e","V2d","V4e","V4f","V2a","V4k"]
lexp=["V4c","V4e"] #,"V7f"
colname={
    "E0a":"Obs_SF_IS",
    "E0b":"Obs_WL_IS",
    "E0c":"Obs_WL_IS",
    "S0a":"Obs_WL_IS",
    "S0b":"Obs_WL_IS",
    "S0c":"Obs_SF_IS",
    "S1d":"Obs_WA_RS3",
    "S1f":"Obs_WA_RS4",
    "S1h":"Obs_WA_RS5",
    "S1i":"Obs_WA_RS4",
    "S1z":"Obs_WA_RS4",
    "V0a":"Obs_SF_SY",
    "V0b":"Obs_WL_SY0",
    "V1a":"Obs_WA_SY1",
    "V1b":"Obs_WA_SY1",
    "V1c":"Obs_WA_SY1",
    "V1d":"Obs_WA_SY1",
    "V1e":"Obs_WA_SY0",
    "V2a":"Obs_WA_SY1",
    "V2b":"Obs_WA_SY1",
    "V2c":"Obs_WA_SY1",
    "V2d":"Obs_WA_SY1",
    "V2e":"Obs_WA_SY0",
    "V3d":"Obs_WA_SY1",
    "V4e":"Obs_WA_SY0",
    "V4f":"Obs_WA_SY0",
    "V4g":"Obs_WA_SY0",
    "V4h":"Obs_WA_SY0",
    "V4k":"Obs_WA_SY1",
}
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
        # metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
        # print (list(read_diagnostics(expname, num).flatten()).append(read_costFunction(expname, num))) #np.shape(read_diagnostics(expname, num)), 
        if expname[0] == 'V' : #in ['V2a','V2b','V2c','V2d','V2e','V2f','V4d','V4e',]:
            row=list(read_Diagnostics_Raven_best(expname, num, odir=odir).flatten())
        else:
            row=list(read_diagnostics(expname, num, odir=odir).flatten())
        print (len(row))
        if expname in ['E0a','S0i','V0a']:
            row.append(read_costFunction(expname, num, div=1.0, odir=odir))
            ObjLake="NaN"
            row.append(np.nan)
        elif expname in ['E0b','S0a','E0c']:
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
        elif expname in ['S1z']:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WA_RS4']==1]['HyLakeId'].dropna().unique()]#
            # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname in ['V1a','V1b','V1c','V1d','V1e']:
            row.append(read_costFunction(expname, num, div=1.0, odir=odir))
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WA_SY_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WA_SY1']==1]['HyLakeId'].dropna().unique()]#
            print (expname,len(llake) )
            # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname in ['V0b','V1a','V1b','V1c','V1d','V1e','V2a','V2b','V2c','V2d','V2e','V2f','V3d','V4c','V4d','V4e','V4f','V4g','V4h','V4k','V7f']:
            row.append(read_costFunction(expname, num, div=1.0, odir=odir))
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WA_SY_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WA_SY1']==1]['HyLakeId'].dropna().unique()]#
            print (expname,len(llake) )
            # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname in ['V2dd']:
            row.append(read_costFunction(expname, num, div=18.0, odir=odir))
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WA_SY_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in final_cat[final_cat['Obs_WA_SY1']==1]['HyLakeId'].dropna().unique()]#
            # print (expname,len(llake) )
            # final_cat[final_cat['Obs_WA_RS1']==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        else:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WA_RS_%d_%d.rvt"%(lake,subid) for lake,subid in zip(final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique(),
            final_cat[final_cat[colname[expname]]==1]['SubId'].dropna().unique())]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake)) 
        expriment_name.append("Exp"+expname)
        print (len(row))
        # print (ObjLake,row)
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

# --- Filter only objective function ---
df_obj = df[['obj.function', 'Expriment']]

# Create boxplot
fig, ax = plt.subplots(figsize=(6, 6))
sns.boxplot(data=df_obj, x='Expriment', y='obj.function', palette=colors[:len(lexp)], ax=ax, boxprops=dict(alpha=0.9))

# Overlay best (max) obj.function per experiment
for expname, color in zip(lexp, colors[:len(lexp)]):
    df_exp = df_obj[df_obj['Expriment'] == "Exp" + expname]
    best_value = df_exp['obj.function'].max()
    xpos = list(df_obj['Expriment'].unique()).index("Exp" + expname)
    ax.scatter(x=xpos, y=best_value, color=color, edgecolors='k', zorder=110, s=80)


# # Create custom legend
# explabels= ['2a-Lake (w/o obs error)', '2a-Lake (w/ obs error)']
# handles = [mpatches.Patch(color=color, label=exp) for exp, color in zip(explabels, colors[:len(lexp)])]
# ax.legend(handles=handles, title="Experiments", loc='best', frameon=False)

ax.set_xticklabels(['(w/o obs error)', '(w/ obs error)'])


# Style and save plot
ax.set_ylabel("Objective Function")
ax.set_xlabel("Experiment")
ax.set_title("2a-Lake - Objective Function", loc='left')
# plt.xticks(rotation=45)
plt.tight_layout()
fname = '../figures/fs9-ObjectiveFunction_Boxplot_' + datetime.datetime.now().strftime("%Y%m%d") + '.jpg'
print(fname)
plt.savefig(fname)
