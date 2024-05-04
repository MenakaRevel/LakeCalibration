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
def read_diagnostics(expname, ens_num, odir='../out',output='output'):
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
    return df[df['observed_data_series'].isin(['WATER_LEVEL_CALIBRATION[265]',
    'WATER_LEVEL_CALIBRATION[400]','WATER_LEVEL_CALIBRATION[412]',
    'HYDROGRAPH_CALIBRATION[921]'])][['DIAG_KLING_GUPTA','DIAG_KLING_GUPTA_DEVIATION']].values #,'DIAG_SPEARMAN']].values
#=====================================================
def read_costFunction(expname, ens_num, div=1.0, odir='../out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return (df['obj.function'].iloc[-1]/float(div))*-1.0
#=====================================================
def read_lake_diagnostics(expname, ens_num, ObjLake, llake, odir='../out',output='output'):
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
odir='../out'
#=====================================================
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
lexp=["S0a","S0b","S0e","S0g","S0h"]
# lexp=["S0a","S0b","S0d"]
expriment_name=[]


# lake_list1 = ['Animoosh_497', 'Loontail_136', 'Narrowbag_467', 'Lavieille_326', 'Hogan_518', 'Big_Trout_353', 'Burntroot_390', 'Cedar_857', 'Grand_1179', 'La_Muir_385', 'Little_Cauchon_754', 'Misty_233', 'North_Depot_836', 'Radiant_944', 'Traverse_1209']
lake_list1 = [
    'Animoosh_345',
    'Big_Trout_220',
    'Burntroot_228',
    'Cedar_528',
    'Grand_753',
    'Hogan_291',
    'La_Muir_241',
    'Little_Cauchon_449',
    'Loontail_122',
    'Misty_135',
    'Narrowbag_281',
    'North_Depot_497',
    'Radiant_574',
    'Traverse_767',
    'Lavieille_326'
]
# lake_list2 = ['Narrowbag_467', 'Grand_1179', 'Radiant_944', 'Misty_233', 'Traverse_1209', 'Big_Trout_353']
lake_list2 = [
    'Narrowbag_281',
    'Grand_753',
    'Radiant_574',
    'Misty_135',
    'Traverse_767',
    'Big_Trout_220'
]

llist={
    'S0a': ['none'],
    'S0b': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Loontail_122',
            'Misty_135',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S0c': ['none'],
    'S0d': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Loontail_122',
            'Misty_135',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S0e': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Loontail_122',
            'Misty_135',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S0f': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Loontail_122',
            'Misty_135',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S0g': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Loontail_122',
            'Misty_135',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S0h': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Loontail_122',
            'Misty_135',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S0i': [  'Animoosh_345',
            'Big_Trout_220',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Loontail_122',
            'Misty_135',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S1a': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Loontail_122',
            'Misty_135',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S1b': [  'Narrowbag_281',
            'Grand_753',
            'Radiant_574',
            'Misty_135',
            'Traverse_767',
            'Big_Trout_220'],
    'S1c': ['none'],
    'S1d': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Loontail_122',
            'Misty_135',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S1e': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S1f': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Loontail_122',
            'Misty_135',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S1g': [  'Burntroot_228',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',],
    'S1h': [  'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Little_Cauchon_449',
            'Misty_135',
            'Narrowbag_281',
            'North_Depot_497',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S1i': [  'Animoosh_345',
            'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Hogan_291',
            'La_Muir_241',
            'Little_Cauchon_449',
            'Narrowbag_281',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S1j': [  'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Little_Cauchon_449',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
    'S1k': [  'Big_Trout_220',
            'Burntroot_228',
            'Cedar_528',
            'Grand_753',
            'Little_Cauchon_449',
            'Narrowbag_281',
            'Radiant_574',
            'Traverse_767',
            'Lavieille_326'],
}

for expname in lexp:
    objFunction0=1.0
    for num in range(1,ens_num+1):
        print (expname, num)
        # metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
        # print (list(read_diagnostics(expname, num).flatten()).append(read_costFunction(expname, num))) #np.shape(read_diagnostics(expname, num)), 
        row=list(read_diagnostics(expname, num, odir=odir).flatten())
        print (len(row))
        if expname in ['S0a','S0c','S1c']:
            row.append(read_costFunction(expname, num, div=1.0, odir=odir))
            row.append(np.nan)
        elif expname in ['S0b','S0d','S0e','S0f','S0g','S0h','S0i']:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WL_"+lake+".rvt" for lake in llist[expname]]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        else:
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WA_"+lake+".rvt" for lake in llist[expname]]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        '''            
        if expname == 'S0a':
            row.append(read_costFunction(expname, num, div=1.0, odir=odir))
            row.append(np.nan)
        elif expname == 'S0b':
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_KLING_GUPTA_DEVIATION"
            llake=["./obs/WL_"+lake+".rvt" for lake in lake_list1]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname == 'S0c':
            row.append(read_costFunction(expname, num, div=1.0, odir=odir))
            row.append(np.nan)
        elif expname == 'S1a':
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WA_"+lake+".rvt" for lake in lake_list1]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname == 'S1b':
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WA_"+lake+".rvt" for lake in lake_list2]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))
        elif expname == 'S1c':
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WA_"+lake+".rvt" for lake in lake_list1]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake))   
        elif expname == 'S1d':
            row.append(read_costFunction(expname, num, div=2.0, odir=odir))
            ObjLake="DIAG_R2"
            llake=["./obs/WA_"+lake+".rvt" for lake in lake_list1]
            row.append(read_lake_diagnostics(expname, num, ObjLake, llake)) 
        '''   
        expriment_name.append("Exp"+expname)
        print (len(row))
        print (row)
        metric.append([row])
metric=np.array(metric)[:,0,:]
print (np.shape(metric))
print (metric)

df=pd.DataFrame(metric, columns=['02KB001','KGED_02KB001','KGE_Crow','Crow',
'KGE_LM','LM','KGE_NC','NC','obj.function',
'mean_ObjLake'])
df['Expriment']=np.array(expriment_name)
print (df.head())

df_melted = pd.melt(df[['02KB001','Crow','LM','NC',
'obj.function','mean_ObjLake','Expriment']],
id_vars='Expriment', value_vars=['02KB001','Crow','LM','NC',
'obj.function','mean_ObjLake','Expriment'])
print (df_melted.head())

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
if len(lexp) == 3:
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

colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]

fig, ax = plt.subplots(figsize=(8, 8))
ax=sns.boxplot(data=df_melted,x='variable', y='value',
order=['obj.function','02KB001','mean_ObjLake','Crow','LM','NC'],hue='Expriment',
palette=colors, boxprops=dict(alpha=0.9))
# Get the colors used for the boxes
box_colors = [box.get_facecolor() for box in ax.artists]
print (box_colors)
for i,expname, color in zip(locs,lexp,colors):
    print ("Exp"+expname, color)
    df_=df[df['Expriment']=="Exp"+expname]
    star=df_.loc[df_['obj.function'].idxmax(),['obj.function','02KB001','mean_ObjLake','Crow','LM','NC']]#.groupby(['Expriment'])
    # print (star)
    # Calculate x-positions for each box in the boxplot
    box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
    # print (box_positions)
    ax.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='k', zorder=110) #'grey'
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
ax.set_ylabel("$Metric$ $($$KGE$/$KGED$/$R^2$$)$")
# add validation and calibration
ax.text(0.25,1.02,"Calibration",fontsize=12,ha='center',va='center',transform=ax.transAxes)
ax.text(0.75,1.02,"Validation",fontsize=12,ha='center',va='center',transform=ax.transAxes)
ax.set_xlabel(" ")
# plt.savefig('../figures/paper/fs1-KGE_boxplot_S0_CalBugdet_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.savefig('../figures/paper/fs1-KGE_boxplot_S0_DiffWave_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')