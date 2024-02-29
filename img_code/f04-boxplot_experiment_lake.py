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
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, FixedLocator
import matplotlib.colors
from mpl_toolkits.axes_grid1.inset_locator import mark_inset, zoomed_inset_axes
mpl.use('Agg')
#===============================================================================================
def mk_dir(dir):
    # Create the download directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)
#=====================================================
def read_lake_diagnostics(expname, ens_num, odir='../out',output='output'):
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
    return df[(df['observed_data_series'].str.contains('CALIBRATION')) & (df['filename'].isin(['./obs/WL_Animoosh_345.rvt',
       './obs/WL_Big_Trout_220.rvt', './obs/WL_Burntroot_228.rvt',
       './obs/WL_Cedar_528.rvt', './obs/WL_Charles_381.rvt',
       './obs/WL_Grand_753.rvt', './obs/WL_Hambone_48.rvt',
       './obs/WL_Hogan_291.rvt', './obs/WL_La_Muir_241.rvt',
       './obs/WL_Lilypond_117.rvt', './obs/WL_Little_Cauchon_449.rvt',
       './obs/WL_Loontail_122.rvt', './obs/WL_Misty_135.rvt',
       './obs/WL_Narrowbag_281.rvt', './obs/WL_North_Depot_497.rvt',
       './obs/WL_Radiant_574.rvt', './obs/WL_Timberwolf_116.rvt',
       './obs/WL_Traverse_767.rvt', './obs/WL_Lavieille_326.rvt']))][['DIAG_KLING_GUPTA_DEVIATION']].values #,'DIAG_SPEARMAN']].values
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
# lexp=["S0a","S0b","S1a","S1b"] #"S0c",
lexp=["S0b","S1a","S1b","S1c","S1d"]
expriment_name=[]
for expname in lexp:
    objFunction0=1.0
    for num in range(1,ens_num+1):
        print (expname, num)
        # metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
        # print (list(read_diagnostics(expname, num).flatten()).append(read_costFunction(expname, num))) #np.shape(read_diagnostics(expname, num)), 
        row=list(read_lake_diagnostics(expname, num, odir=odir).flatten())
        print (len(row))
        row.append(read_costFunction(expname, num, odir=odir))
        expriment_name.append("Exp"+expname)
        print (len(row))
        print (row)
        metric.append([row])
metric=np.array(metric)[:,0,:]
print (np.shape(metric))
print (metric)


columns=['Animoosh','Big_Trout', 'Burntroot',
       'Cedar', 'Charles','Grand', 'Hambone',
       'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
       'Loontail', 'Misty','Narrowbag', 'North_Depot',
       'Radiant', 'Timberwolf','Traverse', 'Lavieille',
       'obj.function']
df=pd.DataFrame(metric, columns=columns)
df['Expriment']=np.array(expriment_name)
print (df.head())


df_melted = pd.melt(df[['Animoosh','Big_Trout', 'Burntroot',
       'Cedar', 'Charles','Grand', 'Hambone',
       'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
       'Loontail', 'Misty','Narrowbag', 'North_Depot',
       'Radiant', 'Timberwolf','Traverse', 'Lavieille', 'Expriment']],
id_vars='Expriment', value_vars=['Animoosh','Big_Trout', 'Burntroot',
       'Cedar', 'Charles','Grand', 'Hambone',
       'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
       'Loontail', 'Misty','Narrowbag', 'North_Depot',
       'Radiant', 'Timberwolf','Traverse', 'Lavieille'])
print (df_melted.head())

# df_melted2 = pd.melt(df[['Expriment','obj.function']],
# id_vars='Expriment', value_vars=['obj.function'])
# print (df_melted2.head(50))

# df_melted['obj.function'] = df_melted2['value']
# print (df_melted.head(50))
# colors=['#3274a1','#e28129','#418e41']
# colors=['#2ba02b','#99df8a','#d62727','#ff9896','#9467bd','#c6b0d5']
# colors=['#2ba02b','#99df8a','#d62727','#ff9896']
# colors = [plt.cm.tab20c(0),plt.cm.tab20c(1),plt.cm.tab20c(4),plt.cm.tab20c(5)] #plt.cm.tab20c(2),
colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(6),plt.cm.tab20c(7)]

# locs=[-0.26,0,0.26]
# locs=[-0.26,-0.11,0.11,0.26]
# locs=[-0.27,-0.11,0.0,0.11,0.27]
locs=[-0.32,-0.18,0.0,0.18,0.32]

fig, (axins, ax) = plt.subplots(figsize=(16, 8), nrows=2)
sns.boxplot(ax=ax,data=df_melted,x='variable', y='value',
order=['Animoosh','Big_Trout', 'Burntroot',
       'Cedar', 'Charles','Grand', 'Hambone',
       'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
       'Loontail', 'Misty','Narrowbag', 'North_Depot',
       'Radiant', 'Timberwolf','Traverse', 'Lavieille'],hue='Expriment',
       palette=colors, boxprops=dict(alpha=0.9))
# for patch in ax.artists:
#     fc = patch.get_facecolor()
#     patch.set_facecolor(mpl.colors.to_rgba(fc, 0.1))
ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
# # Get the colors used for the boxes
# box_colors = [box.get_facecolor() for box in ax.artists]
# print (box_colors)
for i,expname, color in zip(locs,lexp,colors):
    print ("Exp"+expname, color)
    df_=df[df['Expriment']=="Exp"+expname]
    star=df_.loc[df_['obj.function'].idxmin(),['Animoosh','Big_Trout', 'Burntroot',
       'Cedar', 'Charles','Grand', 'Hambone',
       'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
       'Loontail', 'Misty','Narrowbag', 'North_Depot',
       'Radiant', 'Timberwolf','Traverse', 'Lavieille']]#.groupby(['Expriment'])
    # print (star)
    # Calculate x-positions for each box in the boxplot
    box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
    # print (box_positions)
    ax.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='k', zorder=110)
# Add horizontal line at y=0
ax.axhline(y=0, color='orange', linestyle='--', linewidth=1)
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
#
ax.set_ylim(ymin=-8.5, ymax=0.0)
#
ax.set_ylabel("$KGED$")
ax.set_xlabel(" ")
print (ax.yaxis.get_major_ticks())
ax.yaxis.get_major_ticks()[0].label1.set_visible(False)
ax.yaxis.get_major_ticks()[-1].label1.set_visible(False)
##
# Create the zoomed axes
# axins = zoomed_inset_axes(ax, 1, loc='upper center', bbox_to_anchor=(0.5,1.05)) # zoom = 3, location = upper center
sns.boxplot(ax=axins, data=df_melted,x='variable', y='value',
order=['Animoosh','Big_Trout', 'Burntroot',
       'Cedar', 'Charles','Grand', 'Hambone',
       'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
       'Loontail', 'Misty','Narrowbag', 'North_Depot',
       'Radiant', 'Timberwolf','Traverse', 'Lavieille'],hue='Expriment',
       palette=colors, boxprops=dict(alpha=0.9))

for i,expname, color in zip(locs,lexp,colors):
    print ("Exp"+expname, color)
    df_=df[df['Expriment']=="Exp"+expname]
    star=df_.loc[df_['obj.function'].idxmin(),['Animoosh','Big_Trout', 'Burntroot',
       'Cedar', 'Charles','Grand', 'Hambone',
       'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
       'Loontail', 'Misty','Narrowbag', 'North_Depot',
       'Radiant', 'Timberwolf','Traverse', 'Lavieille']]#.groupby(['Expriment'])
    # print (star)
    # Calculate x-positions for each box in the boxplot
    box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
    # print (box_positions)
    axins.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='k', zorder=110)

axins.axhline(y=0.44, color='red', linestyle='--', linewidth=1)

# axins.xaxis.set_minor_locator(MultipleLocator(0.5,1.0))
# axins.xaxis.set_minor_locator(MultipleLocator(base=0.5, offset=1.0))
axins.xaxis.set_minor_locator(FixedLocator(list(np.arange(-0.5,len(columns)-1,1.0))))
axins.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
axins.xaxis.grid(False, which='major', color='grey', lw=0, ls="--")

axins.set_ylim(ymin=0.0, ymax=1.0)

axins.set_ylabel("$KGED$")
axins.set_xlabel(" ")
axins.set_xticks([])
axins.get_legend().set_visible(False)
# 
fig.subplots_adjust(left=0.05,
                    bottom=0.15, 
                    right=0.95, 
                    top=0.95, 
                    wspace=0.01, 
                    hspace=0.01)
# plt.tight_layout()
plt.savefig('../figures/paper/f04-KGED_lake_stage_boxplot_S01.jpg')