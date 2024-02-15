#!/usr/python
'''
plot the ensemble metric
'''
import warnings
warnings.filterwarnings("ignore")
import os
import math
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
import pandas as pd
#=====================================================
def read_Lakes(expname, ens_num, odir='../out'):

    fname=odir+"/"+expname+"_%02d/best/RavenInput/Lakes.rvh"%(ens_num)
    print (fname)
    reservoir_data = {
        'Reservoir': [],
        'SubBasinID': [],
        'HRUID': [],
        'Type': [],
        'WeirCoefficient': [],
        'CrestWidth': [],
        'MaxDepth': [],
        'LakeArea': [],
        'SeepageParameters1': [],
        'SeepageParameters2': []
    }

    current_reservoir = {}

    # try:
    with open(fname, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith(':Reservoir'):
                current_reservoir = {}
                key, value = line.split(' ', 1)
                current_reservoir['Reservoir']=int(value.split('_',1)[1])
            elif line.startswith(':EndReservoir'):
                for key in reservoir_data.keys():
                    if key in current_reservoir:
                        reservoir_data[key].append(current_reservoir[key])
                    else:
                        reservoir_data[key].append(None)
            else:
                if ':' in line:
                    key, value = line.split(' ', 1)
                    if key[1::] == 'SeepageParameters':
                        current_reservoir['SeepageParameters1']=value.strip().split(' ',1)[0]
                        current_reservoir['SeepageParameters1']=value.strip().split(' ',1)[0]
                    else:
                        current_reservoir[key.strip()[1:]] = value.strip()
                    # print (key[1::], value.strip())

    # except FileNotFoundError:
    #     print(f"Error: File '{file_path}' not found.")

    return pd.DataFrame(reservoir_data)
#=====================================================
# Define the order of lakes
order = ['Animoosh', 'Big_Trout', 'Burntroot', 'Cedar', 'Charles', 'Grand', 'Hambone', 'Hogan', 'La_Muir', 'Lilypond', 'Little_Cauchon', 'Loontail', 'Misty', 'Narrowbag', 'North_Depot', 'Radiant', 'Timberwolf', 'Traverse', 'Lavieille']

# Define HyLakeId data
HylakID_data = {
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
HyLakeId = [HylakID_data[lake] for lake in order]

# Define lake area data
LakeArea_data = {
    'Animoosh': 620000,
    'Big_Trout': 15680000,
    'Burntroot': 2480000,
    'Cedar': 25930000,
    'Charles': 120000,
    'Grand': 7740000,
    'Hambone': 420000,
    'Hogan': 13470000,
    'La_Muir': 7490000,
    'Lilypond': 190000,
    'Little_Cauchon': 4890000,
    'Loontail': 1000000,
    'Misty': 3480000,
    'Narrowbag': 610000,
    'North_Depot': 1240000,
    'Radiant': 6350000,
    'Timberwolf': 1760000,
    'Traverse': 6160000,
    'Lavieille': 25450000
}

# Get list of lake areas in the order specified by the 'order' list
LakeArea=[LakeArea_data[lake] for lake in order]

# Sort LakeArea list based on lake areas
sorted_LakeArea = sorted(LakeArea)

# log area
LogLakeArea=[math.log10(LakeArea_data[lake]) for lake in order]

# Sort LogLakeArea list based on lake areas
sorted_LogLakeArea = sorted(LogLakeArea)

# Sort the lake names based on their lake areas
sorted_lake_names = sorted(LakeArea_data, key=lambda x: LakeArea_data[x])

# Get the list of lake names in the sorted order
lake_names_sorted_by_area = list(sorted_lake_names)


#=====================================================
expname="S1a"
odir='../out'
#=====================================================
mk_dir("../figures/paper")
ens_num=10
metric=[]
best_member={}
lexp=["S0a","S0b","S1a","S1b"]
expriment_name=[]
for expname in lexp:
    objFunction=[]
    for num in range(1,ens_num+1):
        print (expname, num)
        objFunction.append(read_costFunction(expname, num, odir=odir))
        # print (read_Lakes(expname, num, odir=odir).head())
        df_=read_Lakes(expname, num, odir=odir)
        CrestWidth=df_[df_['Reservoir'].isin(HyLakeId)]['CrestWidth'].values
        print (CrestWidth)
        row=list(["Exp"+expname])
        row.extend(CrestWidth)
        row.append(read_costFunction(expname, num, odir=odir))
        print (row)
        metric.append([row])
    best_member[expname]=np.array(objFunction).argmin() + 1
metric=np.array(metric)[:,0,:]
# print (np.shape(metric))
# print (metric)

print (best_member)
df=pd.DataFrame(metric[:,1:20].astype(float), columns=order)
df['Expriment']=np.array(metric[:,0])
df['obj.function']=np.array(metric[:,20])
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

colors = [plt.cm.tab20c(0),plt.cm.tab20c(1),plt.cm.tab20c(4),plt.cm.tab20c(5)] #,plt.cm.tab20c(2)

locs=[-0.26,-0.11,0.11,0.26]
# locs=[-0.27,-0.11,0.0,0.11,0.27]

fig, ax = plt.subplots(figsize=(16, 4))
ax=sns.boxplot(data=df_melted,x='variable', y='value',
order=lake_names_sorted_by_area,hue='Expriment',
       palette=colors, boxprops=dict(alpha=0.9))
# for patch in ax.artists:
#     fc = patch.get_facecolor()
#     patch.set_facecolor(mpl.colors.to_rgba(fc, 0.1))
# ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
ax.set_xticklabels(lake_names_sorted_by_area,rotation=90)
# # Get the colors used for the boxes
# box_colors = [box.get_facecolor() for box in ax.artists]
# print (box_colors)
for i,expname, color in zip(locs,lexp,colors):
    print ("Exp"+expname, color)
    df_=df[df['Expriment']=="Exp"+expname]
    star=df_.loc[df_['obj.function'].idxmin(),lake_names_sorted_by_area]#.groupby(['Expriment'])
    # print (star)
    # Calculate x-positions for each box in the boxplot
    box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
    # print (box_positions)
    ax.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='k', zorder=110)
# ax.xaxis.set_minor_locator(MultipleLocator(0.5))
# ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
ax.set_ylabel("$Lake$ $Crest$ $Width$ $(m)$")
ax.set_xlabel(" ")
plt.tight_layout()
plt.savefig('../figures/paper/f07-CresetWidth_boxplot.jpg')