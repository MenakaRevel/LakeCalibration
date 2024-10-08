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
from scipy.optimize import curve_fit
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
# Define the function
def func(x, a, b):
    return a * np.power(x, b)
#=====================================================
# Define the order of lakes
order = ['Animoosh', 'Big_Trout', 'Burntroot', 'Cedar', 'Charles', 'Grand', 'Hambone', 
'Hogan', 'La_Muir', 'Lilypond', 'Little_Cauchon', 'Loontail', 'Misty', 'Narrowbag', 
'North_Depot', 'Radiant', 'Timberwolf', 'Traverse', 'Lavieille']

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
#=====================================================
expname="S1a"
odir='../out'
#=====================================================
mk_dir("../figures/paper")
ens_num=10
metric=[]
best_member={}
# lexp=["S0a","S0b","S1a","S1e"]
# lexp=["S0b","S1a","S1b","S1c","S1d"]
# lexp=["S0b","S1d","S1e","S1f"]
lexp=["S0b","S1d","S1e","S1f","S1g","S1h"]
expriment_name=[]
for expname in lexp:
    objFunction=[]
    for num in range(1,ens_num+1):
        print (expname, num)
        objFunction.append(read_costFunction(expname, num, odir=odir))
        # print (read_Lakes(expname, num, odir=odir).head())
        df_=read_Lakes(expname, num, odir=odir)
        # CrestWidth=df_[df_['Reservoir'].isin(HyLakeId)]['CrestWidth'].values
        CrestWidth=[df_[df_['Reservoir']==id]['CrestWidth'].values[0] for id in HyLakeId]
        print (CrestWidth)
        row=list(["Exp"+expname])
        row.extend(CrestWidth)
        row.append(read_costFunction(expname, num, odir=odir))
        print (row)
        metric.append([row])
    best_member[expname]=np.array(objFunction).argmin() + 1
metric=np.array(metric)[:,0,:]
print (np.shape(metric))
print (metric)

df=pd.DataFrame(metric[:,1:20].astype(float), columns=order)
df['Expriment']=np.array(metric[:,0])
df['obj.function']=np.array(metric[:,20])
print (df.head())


lakes=['Animoosh','Big_Trout', 'Burntroot',
       'Cedar', 'Charles','Grand', 'Hambone',
       'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
       'Loontail', 'Misty','Narrowbag', 'North_Depot',
       'Radiant', 'Timberwolf','Traverse', 'Lavieille']
# for lake in lakes:
#     # print (lake, df[df['Expriment']=='ExpS0b'][lake].max())
#     lake_array1=np.float32(df[df['Expriment']=='ExpS0b'][lake])
#     lake_array2=np.float32(df[df['Expriment']=='ExpS1d'][lake])
#     print (lake, lake_array1.min(),lake_array1.max(), lake_array2.min(),lake_array2.max())


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

print ('df_melted')
print (df_melted.head())
print (df_melted[df_melted['Expriment']=='ExpS0b'].groupby('variable'))

# col_rename_dict={i:j for lake in }
# make dataframe
for i,expname in enumerate(lexp):
    print (i, "Exp"+expname)
    df__=df[df['Expriment']=="Exp"+expname]
    df_=df__.loc[df__['obj.function'].idxmin(),
        ['Animoosh','Big_Trout', 'Burntroot',
        'Cedar', 'Charles','Grand', 'Hambone',
        'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
        'Loontail', 'Misty','Narrowbag', 'North_Depot',
        'Radiant', 'Timberwolf','Traverse', 'Lavieille']].to_frame()
    df_.columns = [expname]
    if i==0:
        star=df_.copy()
    else:
        star=star.join(df_)#,on='Lakes')
# print (star)
# Initial Crest Width W=a0(DA)^n0
a0=1.8406
n0=0.4845
# Drainage area
DA_list={'Misty': 108507344.5, 'North_Depot': 160510034.4, 'Radiant': 2013243523, 'Cedar': 1523453507, 
'Animoosh': 3287414.949, 'Little_Cauchon': 86847509.09, 'La_Muir': 38757038.52, 'Traverse': 2929036792, 
'Burntroot': 583234376.397, 'Big_Trout': 291881670.8, 'Grand': 291881670.8, 'Lavieille': 350700383.9, 
'Hogan': 119376174.1, 'Narrowbag': 730791427.4, 'Charles': 1138514.884, 'Hambone': 1651516.38, 
'Lilypond': 5820597.046, 'Loontail': 4898258.149, 'Timberwolf': 19225885.19}
# Sort the dictionary keys based on their values in ascending order
sorted_lakes = sorted(DA_list, key=lambda x: DA_list[x])

# Lake area 
LA_list = {"Misty": 3480000, "North_Depot": 1240000, "Radiant": 6350000, "Cedar": 25930000, 
"Animoosh": 620000, "Little_Cauchon": 4890000, "La_Muir": 7490000, 
"Traverse": 6160000, "Burntroot": 2480000, "Big_Trout": 15680000, "Grand": 7740000, 
"Lavieille": 25450000, "Hogan": 13470000, "Narrowbag": 610000, "Loontail": 1000000,
'Charles': 120000, 'Hambone': 420000, 'Lilypond': 190000, 'Timberwolf': 1760000}
# Sort the dictionary keys based on their values in ascending order
sorted_lakes = sorted(LA_list, key=lambda x: LA_list[x])

print ('sorted_lakes',sorted_lakes)
# print ([a0*(DA_list[lake]*1e-6)**n0 for lake in star.index.values])
star['Initial_CrestWidth']=[a0*(DA_list[lake]*1e-6)**n0 for lake in star.index.values]
star['Wshd_area']=[DA_list[lake]*1e-6 for lake in star.index.values]
star['Lake_area']=[LA_list[lake]*1e-6 for lake in star.index.values]

# print (star.sort_values('Wshd_area'))
# star=star.sort_values('Wshd_area')

print (star.sort_values('Lake_area'))
star=star.sort_values('Lake_area')
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

fig, ax = plt.subplots(figsize=(16, 4))
ax.plot(np.log10(star['Lake_area'].values),np.log10(star['Initial_CrestWidth'].values), color='grey', label='W~DA',zorder=1)
ax.fill_between(x=np.log10(star['Lake_area'].values), y1=np.log10(star['Initial_CrestWidth'].values*1.5),
y2=np.log10(star['Initial_CrestWidth'].values*0.5), color='grey',alpha=0.2,zorder=0)
for i,expname in enumerate(lexp):
    ax.plot(np.log10(star['Lake_area'].values),np.log10(pd.to_numeric(star[expname].values)), #np.log10(
    marker='o',linestyle='none',color=colors[i],markeredgecolor='k', label=expname,zorder=100)
xticks=ax.get_xticks()
# boxplot
for i,group in df_melted[df_melted['Expriment']=='ExpS0b'].groupby('variable'):
    print (i, np.log10(LA_list[group['variable'].values[0]]*1e-6), np.log10(group['value'].values[0]))
    ax.boxplot(np.log10(group['value'].values),positions=[np.log10(LA_list[group['variable'].values[0]]*1e-6)],
    widths=0.05,manage_ticks=False,patch_artist=True, showfliers=False, medianprops = dict(linestyle='-', linewidth=0.5, color=colors[0]),
    boxprops=dict(linestyle='-', linewidth=1.5, color=colors[0],facecolor="w"), zorder=0) 
# fit a line
df_melted2=df_melted[df_melted['Expriment']=='ExpS0b'].copy()
df_melted2['LakeArea']=[LA_list[lake]*1e-6 for lake in df_melted2['variable'].values]
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(np.log10(df_melted2['LakeArea'].values), np.log10(df_melted2['value'].values))
print (slope, intercept, r_value**2, p_value, std_err)
X=np.linspace(np.min(np.log10(df_melted2['LakeArea'].values)),np.max(np.log10(df_melted2['LakeArea'].values)),100)
Y=slope*X+intercept
# print (X,Y)
ax.plot(X, Y, color=colors[0], label='Fitted ExpS0b (%3.2f)'%(r_value**2),zorder=1)

# Perform the curve fitting
# popt, pcov = curve_fit(func, DrainArea, Initial_width)

# ax.set_xticks(range(0,4))
# ax.set_xticklabels(range(0,4))
ax.set_ylabel("$log_{10}$$(Lake$ $Crest$ $Width)$ $(m)$")
ax.set_xlabel("$log_{10}$$(Lake$ $Area)$ $(km^2)$")
plt.tight_layout()
plt.legend()
plt.savefig('../figures/paper/fs3-CresetWidth_lake_area.jpg')


"""
# colors = [plt.cm.tab20c(0),plt.cm.tab20c(1),plt.cm.tab20c(4),plt.cm.tab20c(5)] #,plt.cm.tab20c(2)
colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(5),plt.cm.tab20c(6),plt.cm.tab20c(7)]

# locs=[-0.26,-0.11,0.11,0.26]
# locs=[-0.27,-0.11,0.0,0.11,0.27]
# locs=[-0.32,-0.18,0.0,0.18,0.32]
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


fig, ax = plt.subplots(figsize=(16, 4))
ax=sns.boxplot(data=df_melted,x='variable', y='value',
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
print (star)
# Initial Crest Width W=a0(DA)^n0
a0=1.8406
n0=0.4845
DA_list={'Misty': 108507344.5, 'North_Depot': 160510034.4, 'Radiant': 2013243523, 'Cedar': 1523453507, 
'Animoosh': 3287414.949, 'Little_Cauchon': 86847509.09, 'La_Muir': 38757038.52, 'Traverse': 2929036792, 
'Burntroot': 583234376.397, 'Big_Trout': 291881670.8, 'Grand': 291881670.8, 'Lavieille': 350700383.9, 
'Hogan': 119376174.1, 'Narrowbag': 730791427.4, 'Charles': 1138514.884, 'Little_Cauchon': 86847509.09,
'Big_Trout': 318401683.3, 'Hambone': 1651516.38, 'Lilypond': 5820597.046, 'Loontail': 4898258.149, 
'Timberwolf': 19225885.19}
axlist=list(ax.get_xticks())
for i,lake in enumerate(order):
    pos=axlist[i]#+0.5
    # ax.axhline(y=a0*(DA_list[lake]*1e-6)**n0,xmin=0.1*(pos)-0.005,xmax=0.1*(pos)+0.005,color ="k", linestyle ="--", zorder=110)
    # ax.axhline(y=a0*(DA_list[lake]*1e-6)**n0,color ="lime", linestyle ="--", zorder=110)
    ax.scatter(x=i, y=a0*(DA_list[lake]*1e-6)**n0, marker='*', s=40, color='grey', edgecolors='grey', zorder=110,alpha=0.5)
    y_upper=a0*(DA_list[lake]*1e-6)**n0*1.5
    y_lower=a0*(DA_list[lake]*1e-6)**n0*0.5
    ax.fill_between(x=[pos-0.5,pos+0.5],y1=[y_upper,y_upper],y2=[y_lower,y_lower],color='grey',alpha=0.2)
    print (lake, '%5.2f'%(a0*(DA_list[lake]*1e-6)**n0), '%5.2f'%(y_lower), '%5.2f'%(y_upper))
# print (ax.get_xticks())
print (ax.get_xlim())
ax.set_xlim(xmin=-0.5,xmax=18.5)
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
ax.set_ylabel("$Lake$ $Crest$ $Width$ $(m)$")
ax.set_xlabel(" ")
plt.tight_layout()
plt.savefig('../figures/paper/f06-CresetWidth_boxplot_RelShoAra_DALA_sensitvity-1.jpg')
"""