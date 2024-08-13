#!/usr/python
'''
plot the reouting parameters mannings diffusivity cerality
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
from matplotlib.ticker import FuncFormatter
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
def read_routing_para(expname, ens_num, para_list=['obj.function', 'n_multi', 'c_multi', 'd_multi', 'k_multi'],odir='../out'): #k_multi
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return df.loc[:,para_list].iloc[-1]
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
def read_crest_width_par(expname, ens_num, odir='../out'):
    fname="%s/%s_%02d/crest_width_par.csv"%(odir,expname,ens_num)
    print (fname)
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(fname)

    # Extract 'a' and 'n' values from the first row
    a = df.loc[0, 'a']
    n = df.loc[0, 'n']

    return a, n
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


# Define drain area data
drain_area_data = {
    'Animoosh': 3287414.949,
    'Big_Trout': 318401683.3,
    'Burntroot': 583234376.4,
    'Cedar': 1523453507,
    'Charles': 1138514.884,
    'Grand': 291881670.8,
    'Hambone': 1651516.376,
    'Hogan': 119376174.1,
    'La_Muir': 38757038.52,
    'Lilypond': 5820597.046,
    'Little_Cauchon': 86847509.09,
    'Loontail': 4898258.149,
    'Misty': 108507344.5,
    'Narrowbag': 730791427.4,
    'North_Depot': 160510034.4,
    'Radiant': 2013243523,
    'Timberwolf': 19225885.19,
    'Traverse': 2929036792,
    'Lavieille': 350700383.9
}

# Create a dictionary of drain areas
DrainArea = [float(drain_area_data[lake]) for lake in order]

# Sort DrainArea list based on lake areas
sorted_DrainArea = np.array(sorted(DrainArea))

# log area
LogDrainArea=[math.log10(drain_area_data[lake]) for lake in order]

# Sort LogDrainArea list based on lake areas
sorted_LogDrainArea = sorted(LogDrainArea)

HylakID_sorted = sorted(order, key=lambda x: drain_area_data[x])
#=====================================================
expname="S1a"
odir='../out'
#=====================================================
mk_dir("../figures/paper")
ens_num=10
metric=[]
best_member={}
# lexp=["S0a","S0b","S1a","S1b"]
lexp=["E0a","E0b","S1a"]
expriment_name=[]
df_rup=pd.DataFrame()
for expname in lexp:
    objFunction=[]
    a_list=[]
    n_list=[]
    for num in range(1,ens_num+1):
        print (expname, num)
        objFunction.append(read_costFunction(expname, num, odir=odir))
        # print (read_Lakes(expname, num, odir=odir).head())
        a,n=1,1 #read_crest_width_par(expname, num)
        print (a, n)
        a_list.append(a)
        n_list.append(n)
        df_rup=pd.concat([df_rup,read_routing_para(expname, num, odir=odir)],axis=0)
        df_=read_Lakes(expname, num, odir=odir)
        # CrestWidth=df_[df_['Reservoir'].isin(HyLakeId)]['CrestWidth'].values
        CrestWidth=[df_[df_['Reservoir']==HylakID_data[lake]]['CrestWidth'].values[0] for lake in lake_names_sorted_by_area]
        print (CrestWidth)
        row=list(["Exp"+expname, num])
        row.extend(read_routing_para(expname, num, odir=odir))
        # row.append(read_costFunction(expname, num, odir=odir))
        # row.append(a)
        # row.append(n)
        print (row)
        metric.append([row])
    # df_cwp["Exp"+expname+"_a"]=np.array(a_list)
    # df_cwp["Exp"+expname+"_n"]=np.array(n_list)
    # df_rup["Exp"+expname+"_k"]=np.array(n_list)
    best_member[expname]=np.array(objFunction).argmin()
metric=np.array(metric)[:,0,:]
# print (np.shape(metric))
# print (metric)
# print (df_rup.head())

print (best_member)
df=pd.DataFrame(metric[:,2:21].astype(float), columns=['obj.function', 'n_multi', 'c_multi', 'd_multi', 'k_multi']) #order)
df['Expriment']=np.array(metric[:,0])
# df['Number']=np.array(metric[:,1])
# df['obj.function']=np.array(metric[:,21])
# df['a']=np.array(metric[:,22])
# df['n']=np.array(metric[:,23])
print (df.head())

df_melted = pd.melt(df[['n_multi', 'c_multi', 'd_multi', 'k_multi','Expriment']],
id_vars='Expriment', value_vars=['n_multi', 'c_multi', 'd_multi', 'k_multi','Expriment'])

print (df_melted.head())

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
order=['n_multi', 'c_multi', 'd_multi', 'k_multi'],
hue='Expriment',boxprops=dict(alpha=0.9))
for i,expname, color in zip(locs,lexp,colors):
    print ("Exp"+expname)#, color)
    df_=df[df['Expriment']=="Exp"+expname]
    print ('='*20+' df_ '+'='*20)
    print (df_.head())
    star=df_.loc[df_['obj.function'].idxmax(),['n_multi', 'c_multi', 'd_multi', 'k_multi']]#.groupby(['Expriment'])
    # print (star)
    # Calculate x-positions for each box in the boxplot
    box_positions = [pos + offset for pos in range(len(df_melted['variable'].unique())) for offset in [i]]
    # print (box_positions)
    ax.scatter(x=box_positions, y=star.values, marker='o', s=40, color=color, edgecolors='k', zorder=110) #'grey'
# Lines between each columns of boxes
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
#
ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
plt.tight_layout()
plt.savefig('../figures/paper/f08-routing_parameters_boxplot_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')