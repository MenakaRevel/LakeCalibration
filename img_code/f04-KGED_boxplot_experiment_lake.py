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
def read_lake_diagnostics(expname, ens_num, lakes, odir='../out',output='output',best_dir='best'):
    '''
    read the RunName_Diagnostics.csv
    '''
    # HYDROGRAPH_CALIBRATION[921],./obs/02KB001_921.rvt
    # WATER_LEVEL_CALIBRATION[265],./obs/Crow_265.rvt
    # WATER_LEVEL_CALIBRATION[400],./obs/Little_Madawaska_400.rvt
    # WATER_LEVEL_CALIBRATION[412],./obs/Nippissing_Corrected_412.rvt
    fname=odir+"/"+expname+"_%02d/%s/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,best_dir,output)
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/output_Raven_v3.7/Petawawa_Diagnostics.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    print (fname) 
    df=pd.read_csv(fname,on_bad_lines='skip')
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA lakes
#     print (df.head())
#     print (df[(df['observed_data_series'].str.contains('CALIBRATION')) & (df['filename'].isin(lakes))]
#     ['DIAG_KLING_GUPTA_DEVIATION'].values)
    return df[(df['observed_data_series'].str.contains('CALIBRATION')) & (df['filename'].isin(lakes))]['DIAG_KLING_GUPTA_DEVIATION'].values

#     return df[(df['observed_data_series'].str.contains('CALIBRATION')) & (df['filename'].isin(['./obs/WL_Animoosh_345.rvt',
#        './obs/WL_Big_Trout_220.rvt', './obs/WL_Burntroot_228.rvt',
#        './obs/WL_Cedar_528.rvt', './obs/WL_Charles_381.rvt',
#        './obs/WL_Grand_753.rvt', './obs/WL_Hambone_48.rvt',
#        './obs/WL_Hogan_291.rvt', './obs/WL_La_Muir_241.rvt',
#        './obs/WL_Lilypond_117.rvt', './obs/WL_Little_Cauchon_449.rvt',
#        './obs/WL_Loontail_122.rvt', './obs/WL_Misty_135.rvt',
#        './obs/WL_Narrowbag_281.rvt', './obs/WL_North_Depot_497.rvt',
#        './obs/WL_Radiant_574.rvt', './obs/WL_Timberwolf_116.rvt',
#        './obs/WL_Traverse_767.rvt', './obs/WL_Lavieille_326.rvt']))][['DIAG_KLING_GUPTA_DEVIATION']].values #,'DIAG_SPEARMAN']].values
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
# Define the order of lakes
order = ['Animoosh', 'Big_Trout', 'Burntroot', 'Cedar', 'Charles', 'Grand', 'Hambone', 
'Hogan', 'La_Muir', 'Lilypond', 'Little_Cauchon', 'Loontail', 'Misty', 'Narrowbag', 
'North_Depot', 'Radiant', 'Timberwolf', 'Traverse', 'Lavieille']

# # Define the order of lakes
# order = ['Animoosh', 'Big_Trout', 'Cedar', 'Grand', 
# 'Hogan', 'La_Muir', 'Little_Cauchon', 'Loontail', 'Misty', 'Narrowbag', 
# 'North_Depot', 'Radiant', 'Traverse', 'Lavieille']
#=====================================================
# Define HyLakeId data
data = {
    'Animoosh': 1034779,
    'Big_Trout': 8781,
    'Burntroot': 108379,
    'Cedar': 8741,
    'Charles': 1033439,
    'Grand': 108347,
    'Hambone': 1035812,
    'Hogan': 8762,
    'La_Muir': 108369,
    'Lilypond': 1036038,
    'Little_Cauchon': 108015,
    'Loontail': 108404,
    'Misty': 108564,
    'Narrowbag': 1032844,
    'North_Depot': 108027,
    'Radiant': 108126,
    'Timberwolf': 108585,
    'Traverse': 108083,
    'Lavieille': 8767
}

# Get list of HyLakeId in the order specified by the 'order' list
HyLakeId = [data[lake] for lake in order]
print (HyLakeId)
#=====================================================
# read final cat 
final_cat=pd.read_csv('../OstrichRaven/finalcat_hru_info_updated.csv')
llake=["./obs/WL_IS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in HyLakeId]
print (llake)
#=====================================================
mk_dir("../figures/paper")
ens_num=10
metric=[]
# lexp=["S0a","S0b","S1a","S1b"] #"S0c",
# lexp=["S0b","S1a","S1b","S1c","S1d"]
# lexp=["S0b","S1d","S1e","S1f"]
# lexp=["S0b","S1d","S1e","S1f","S1g","S1h"]
# lexp=["S0b","S1d","S1e","S1i","S1j","S1k"]
# lexp=["S0a","S0b","S0e","S0f"]
# lexp=["S0a","S0b","S0e","S0f","S0g"]
# lexp=["S0a","S0b","S0e","S0f","S0g","S0h"]
# lexp=["E0a","E0b","S1a","S1b","S1c"]
# lexp=["E0a","E0b","S1c","S1d","S1e"]
# lexp=["E0a","E0b","S1d"]
lexp=["E0a","E0b","S1d","S1f","S1g"]
# lexp=["E0b"]
expriment_name=[]
for expname in lexp:
    objFunction0=1.0
    for num in range(1,ens_num+1):
        print (expname, num)
        # metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
        # print (list(read_diagnostics(expname, num).flatten()).append(read_costFunction(expname, num))) #np.shape(read_diagnostics(expname, num)), 
        row=list(read_lake_diagnostics(expname, num, llake, odir=odir, best_dir='best_Raven')) #.flatten() #)#.flatten())
        # print (len(row))
        # print (row)
        row.append(read_costFunction(expname, num, odir=odir))
        expriment_name.append("Exp"+expname)
        print (len(row))
        # print (row)
        metric.append([row])
print (metric)
metric=np.array(metric)[:,0,:]
print (np.shape(metric))
print (metric)

print (final_cat[final_cat['HyLakeId'].isin(HyLakeId)]['Obs_NM'].values)

# columns=['Animoosh','Big_Trout', 'Burntroot',
#        'Cedar', 'Charles','Grand', 'Hambone',
#        'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
#        'Loontail', 'Misty','Narrowbag', 'North_Depot',
#        'Radiant', 'Timberwolf','Traverse', 'Lavieille',
#        'obj.function']
# columns=['Animoosh', 'Big_Trout', 'Cedar', 'Grand', 
# 'Hogan', 'La_Muir', 'Little_Cauchon', 'Loontail', 'Misty', 'Narrowbag', 
# 'North_Depot', 'Radiant', 'Traverse', 'Lavieille', 'obj.function']

columns=list(final_cat[final_cat['HyLakeId'].isin(HyLakeId)]['Obs_NM'].values)
columns.append('obj.function')
df=pd.DataFrame(metric, columns=columns)
df['Expriment']=np.array(expriment_name)
print (df.head())

# df_melted = pd.melt(df[['Animoosh','Big_Trout', 'Burntroot',
#        'Cedar', 'Charles','Grand', 'Hambone',
#        'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
#        'Loontail', 'Misty','Narrowbag', 'North_Depot',
#        'Radiant', 'Timberwolf','Traverse', 'Lavieille', 'Expriment']],
# id_vars='Expriment', value_vars=['Animoosh','Big_Trout', 'Burntroot',
#        'Cedar', 'Charles','Grand', 'Hambone',
#        'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
#        'Loontail', 'Misty','Narrowbag', 'North_Depot',
#        'Radiant', 'Timberwolf','Traverse', 'Lavieille'])

melt_columns=list(final_cat[final_cat['HyLakeId'].isin(HyLakeId)]['Obs_NM'].values)
melt_columns.append('Expriment')
melt_values=list(final_cat[final_cat['HyLakeId'].isin(HyLakeId)]['Obs_NM'].values)
print (melt_columns)
df_melted = pd.melt(df[melt_columns],id_vars='Expriment', value_vars=melt_values)

# df_melted = pd.melt(df[['Animoosh', 'Big_Trout', 'Cedar', 'Grand', 
# 'Hogan', 'La_Muir', 'Little_Cauchon', 'Loontail', 'Misty', 'Narrowbag', 
# 'North_Depot', 'Radiant', 'Traverse', 'Lavieille', 'Expriment']],
# id_vars='Expriment', value_vars=['Animoosh', 'Big_Trout', 'Cedar', 'Grand', 
# 'Hogan', 'La_Muir', 'Little_Cauchon', 'Loontail', 'Misty', 'Narrowbag', 
# 'North_Depot', 'Radiant', 'Traverse', 'Lavieille'])
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

# locs=[-0.27,-0.11,0.0,0.11,0.27]
# locs=[-0.32,-0.18,0.0,0.18,0.32]

llist={
    'E0a': ['none'],
    'E0b': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Loontail',
            'Misty',
            'Narrowbag',
            'North_Depot',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S0c': ['none'],
    'S0d': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Loontail',
            'Misty',
            'Narrowbag',
            'North_Depot',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S0e': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Loontail',
            'Misty',
            'Narrowbag',
            'North_Depot',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S0f': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Loontail',
            'Misty',
            'Narrowbag',
            'North_Depot',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S0g': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Loontail',
            'Misty',
            'Narrowbag',
            'North_Depot',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S0h': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Loontail',
            'Misty',
            'Narrowbag',
            'North_Depot',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S1a': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Loontail',
            'Misty',
            'Narrowbag',
            'North_Depot',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S1b': [  'Narrowbag',
            'Grand',
            'Radiant',
            'Misty',
            'Traverse',
            'Big_Trout'],
    'S1c': ['none'],
    'S1d': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Loontail',
            'Misty',
            'Narrowbag',
            'North_Depot',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S1e': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S1f': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Loontail',
            'Misty',
            'North_Depot',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S1g': [  'Burntroot',
            'Narrowbag',
            'North_Depot',
            'Radiant',
            'Traverse',],
    'S1h': [  'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Little_Cauchon',
            'Misty',
            'Narrowbag',
            'North_Depot',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S1i': [  'Animoosh',
            'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Hogan',
            'La_Muir',
            'Little_Cauchon',
            'Narrowbag',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S1j': [  'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Little_Cauchon',
            'Radiant',
            'Traverse',
            'Lavieille'],
    'S1k': [  'Big_Trout',
            'Burntroot',
            'Cedar',
            'Grand',
            'Little_Cauchon',
            'Narrowbag',
            'Radiant',
            'Traverse',
            'Lavieille'],
}

# order based on watershed area
DA_list={'Misty': 108507344.5, 'North_Depot': 160510034.4, 'Radiant': 2013243523, 'Cedar': 1523453507, 
'Animoosh': 3287414.949, 'Little_Cauchon': 86847509.09, 'La_Muir': 38757038.52, 'Traverse': 2929036792, 
'Burntroot': 583234376.397, 'Big_Trout': 291881670.8, 'Grand': 291881670.8, 'Lavieille': 350700383.9, 
'Hogan': 119376174.1, 'Narrowbag': 730791427.4, 'Charles': 1138514.884, 'Little_Cauchon': 86847509.09,
'Big_Trout': 318401683.3, 'Hambone': 1651516.38, 'Lilypond': 5820597.046, 'Loontail': 4898258.149, 
'Timberwolf': 19225885.19}

# Sort the dictionary keys based on their values in ascending order
# sorted_lakes = sorted(DA_list, key=lambda x: DA_list[x]) #order #
# sorted_lakes = sorted(DA_list[x] for x in order)

sorted_lakes = final_cat[final_cat['HyLakeId'].isin(HyLakeId)].sort_values(by='DrainArea')['Obs_NM'].values

fig, (axins, ax) = plt.subplots(figsize=(16, 8), nrows=2)
sns.boxplot(ax=ax,data=df_melted,x='variable', y='value',
order=sorted_lakes,hue='Expriment',palette=colors, boxprops=dict(alpha=0.9))
# order=['Animoosh','Big_Trout', 'Burntroot',
#        'Cedar', 'Charles','Grand', 'Hambone',
#        'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
#        'Loontail', 'Misty','Narrowbag', 'North_Depot',
#        'Radiant', 'Timberwolf','Traverse', 'Lavieille'],hue='Expriment',
#        palette=colors, boxprops=dict(alpha=0.9))
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
    star=df_.loc[df_['obj.function'].idxmin(),sorted_lakes]
    # ,['Animoosh','Big_Trout', 'Burntroot',
    #    'Cedar', 'Charles','Grand', 'Hambone',
    #    'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
    #    'Loontail', 'Misty','Narrowbag', 'North_Depot',
    #    'Radiant', 'Timberwolf','Traverse', 'Lavieille']]#.groupby(['Expriment'])
    # print (star)
    # Calculate x-positions for each box in the boxplot
    box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
    # print (box_positions)
    ax.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='k', zorder=110)
    for ix in range(len(box_positions)):
        if sorted_lakes[ix] in llist[expname]:
            # print (sorted_lakes[ix], box_positions[ix], star.values[ix])
            ax.scatter(x=box_positions[ix], y=0.99, marker='*', s=40, color=color, edgecolors=color, zorder=110)
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
order=sorted_lakes,hue='Expriment',palette=colors, boxprops=dict(alpha=0.9))
# order=['Animoosh','Big_Trout', 'Burntroot',
#        'Cedar', 'Charles','Grand', 'Hambone',
#        'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
#        'Loontail', 'Misty','Narrowbag', 'North_Depot',
#        'Radiant', 'Timberwolf','Traverse', 'Lavieille'],hue='Expriment',
#        palette=colors, boxprops=dict(alpha=0.9))

for i,expname, color in zip(locs,lexp,colors):
    print ("Exp"+expname, color)
    df_=df[df['Expriment']=="Exp"+expname]
    star=df_.loc[df_['obj.function'].idxmin(),sorted_lakes]
    # ,['Animoosh','Big_Trout', 'Burntroot',
    #    'Cedar', 'Charles','Grand', 'Hambone',
    #    'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
    #    'Loontail', 'Misty','Narrowbag', 'North_Depot',
    #    'Radiant', 'Timberwolf','Traverse', 'Lavieille']]#.groupby(['Expriment'])
    # print (star)
    # Calculate x-positions for each box in the boxplot
    box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
    # print (box_positions)
    axins.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='k', zorder=110)
    for ix in range(len(box_positions)):
        if sorted_lakes[ix] in llist[expname]:
            # print (sorted_lakes[ix], box_positions[ix], star.values[ix])
            axins.scatter(x=box_positions[ix], y=0.98, marker='*', s=40, color=color, edgecolors=color, zorder=110)

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
# plt.savefig('../figures/paper/f04-KGED_lake_stage_boxplot_S0_CalBugdet_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.savefig('../figures/paper/f04-KGED_lake_stage_boxplot_DiffWave_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')