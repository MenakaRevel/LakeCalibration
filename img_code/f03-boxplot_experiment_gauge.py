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
def read_costFunction(expname, ens_num, odir='../out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return df['obj.function'].iloc[-1]
#=====================================================
expname="S1a"
odir='../out'
#=====================================================
mk_dir("../figures/paper")
ens_num=10
metric=[]
lexp=["S0a","S0b","S1a","S1b"]
expriment_name=[]
for expname in lexp:
    objFunction0=1.0
    for num in range(1,ens_num+1):
        print (expname, num)
        # metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
        # print (list(read_diagnostics(expname, num).flatten()).append(read_costFunction(expname, num))) #np.shape(read_diagnostics(expname, num)), 
        row=list(read_diagnostics(expname, num, odir=odir).flatten())
        print (len(row))
        row.append(read_costFunction(expname, num, odir=odir))
        expriment_name.append("Exp"+expname)
        print (len(row))
        print (row)
        metric.append([row])
metric=np.array(metric)[:,0,:]
print (np.shape(metric))
print (metric)

df=pd.DataFrame(metric, columns=['02KB001','KGED_02KB001','KGE_Crow','Crow',
'KGE_LM','LM','KGE_NC','NC','obj.function'])
df['Expriment']=np.array(expriment_name)
print (df.head())

df_melted = pd.melt(df[['02KB001','Crow','LM','NC','Expriment']],
id_vars='Expriment', value_vars=['02KB001','Crow','LM','NC'])
print (df_melted.head())

# df_melted2 = pd.melt(df[['Expriment','obj.function']],
# id_vars='Expriment', value_vars=['obj.function'])
# print (df_melted2.head(50))

# df_melted['obj.function'] = df_melted2['value']
# print (df_melted.head(50))
# colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20c(3),
        #   plt.cm.tab20c(4),plt.cm.tab20c(6),plt.cm.tab20c(7)]

# colors=['#2ba02b','#99df8a','#d62727','#ff9896']
colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]
locs=[-0.28,-0.10,0.10,0.28]

fig, ax = plt.subplots(figsize=(8, 8))
ax=sns.boxplot(data=df_melted,x='variable', y='value',
order=['Crow','LM','NC','02KB001'],hue='Expriment',
palette=colors, boxprops=dict(alpha=0.9))
# Get the colors used for the boxes
box_colors = [box.get_facecolor() for box in ax.artists]
print (box_colors)
for i,expname, color in zip(locs,lexp,colors):
    print ("Exp"+expname, color)
    df_=df[df['Expriment']=="Exp"+expname]
    star=df_.loc[df_['obj.function'].idxmin(),['Crow','LM','NC','02KB001']]#.groupby(['Expriment'])
    # print (star)
    # Calculate x-positions for each box in the boxplot
    box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
    # print (box_positions)
    ax.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='grey', zorder=110)
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
ax.set_ylabel("$KGED/KGE$")
ax.set_xlabel(" ")
plt.savefig('../figures/paper/f03-KGE_boxplot.jpg')