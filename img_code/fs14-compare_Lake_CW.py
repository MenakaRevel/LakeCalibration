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
import re
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
    return df['obj.function'].iloc[-1]*-1.0
#========================================
def read_costFunction_component(expname, ens_num, component='k_multi', odir='../out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return df[component].iloc[-1]
#=====================================================
def read_k_muti(expname, ens_num, odir='../out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return df['k_muti'].iloc[-1]
#=====================================================
def read_CW(expname, ens_num, llakes, odir='../out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return df.iloc[-1:][llakes]
#=====================================================
def read_k_muti_rvh(fname):
    with open(fname) as f:
        lines=f.readlines()
    
    # Pattern to match the required lines and extract XXXXX
    # pattern = r":SBGroupPropertyMultiplier\s+NonObservedLakesubbasins\s+RESERVOIR_CREST_WIDTH\s+([\d.]+)"
    pattern = r":SBGroupPropertyMultiplier\s+NonObservedLakesubbasins\s+RESERVOIR_CREST_WIDTH\s+([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)"

    # # Extract values
    # values = []
    # for line in lines:
    #     match = re.search(pattern, line)
    #     if match:
    #         values.append(float(match.group(1)))  # Convert to float
    
    # Extract values
    values = [float(re.search(pattern, line).group(1)) for line in lines if re.search(pattern, line)]

    print ('RESERVOIR_CREST_WIDTH:', values)
    return values
#=====================================================
def read_Lakes(fname): #expname, ens_num, odir='../out'):
    '''
    Read Lakes.rvh
    '''
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/Lakes.rvh"%(ens_num)
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
                current_reservoir['Reservoir']=int(value.split('_')[1])
            elif line.startswith(':EndReservoir'):
                for key in reservoir_data.keys():
                    if key in current_reservoir:
                        reservoir_data[key].append(current_reservoir[key])
                    else:
                        reservoir_data[key].append(None)
            else:
                if ':' in line:
                    if ':AreaStageRelation' in line or ':EndAreaStageRelation' in line:
                        continue
                    # print (line)
                    key, value = line.split(' ', 1)
                    if key[1::] == 'SeepageParameters':
                        current_reservoir['SeepageParameters1']=value.strip().split(' ')[1]
                        current_reservoir['SeepageParameters1']=value.strip().split(' ')[2]
                    else:
                        current_reservoir[key.strip()[1:]] = value.strip()
                    # print (key[1::], value.strip())

    # except FileNotFoundError:
    #     print(f"Error: File '{file_path}' not found.")
    df=pd.DataFrame(reservoir_data)
    df['Reservoir']      =df['Reservoir'].astype(int)
    df['SubBasinID']     =df['SubBasinID'].astype(int)
    df['WeirCoefficient']=df['WeirCoefficient'].astype(float)
    df['CrestWidth']     =df['CrestWidth'].astype(float)
    df['MaxDepth']       =df['WeirCoefficient'].astype(float)

    return df
#=====================================================
# odir='../out'
odir='/scratch/menaka/LakeCalibration/out'
mk_dir("../figures/pdf")
ens_num=10
# metric=[]
# expname='V1d' #"S1z" #"E0a" #"S1z" #"E0b"
lexp=["V0a","V2e","V2d","V2a","V1d","V1e"]
colname={
    "E0a":"Obs_SF_IS",
    "E0b":"Obs_WL_IS",
    "S0a":"Obs_WL_IS",
    "S0b":"Obs_WL_IS",
    "S0c":"Obs_SF_IS",
    "S1d":"Obs_WA_RS3",
    "S1f":"Obs_WA_RS4",
    "S1h":"Obs_WA_RS5",
    "S1i":"Obs_WA_RS4",
    "S1z":"Obs_WA_RS4",
    "V0a":"Obs_SF_SY",
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
}
#========================================
# read final cat 
# final_cat=pd.read_csv('/home/menaka/scratch/LakeCalibration/OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
final_cat=pd.read_csv('../OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
#=====================================================
met={}
for expname in lexp:
    objFunction0=-1.0
    for num in range(1,ens_num+1):
        # row=list(read_Diagnostics_Raven_best(expname, num, odir=odir).flatten())
        # row.extend(list(read_lake_diagnostics(expname, num, llake, odir=odir, best_dir='best_Raven')))
        # row.append(read_costFunction(expname, num, div=1.0, odir=odir))
        objFunction=read_costFunction(expname, num, div=1.0, odir=odir)
        print (expname, num, objFunction)
        if objFunction > objFunction0:
            objFunction0=objFunction
            met[expname]=num
print (met)
#=====================================================
# read truth CW
fname        = '/project/def-btolson/menaka/LakeCalibration/out/E0b_obs/best_Raven/RavenInput/Lakes.rvh'
df_Lakes_obs = read_Lakes(fname)
fname        = '/project/def-btolson/menaka/LakeCalibration/out/E0b_obs/best_Raven/RavenInput/Petawawa.rvh'
k_multi      = read_k_muti_rvh(fname)[0]
print ('Obs',k_multi)
df_Lakes_obs.loc[df_Lakes_obs['SubBasinID'].isin(final_cat[final_cat[colname['E0b']]==1]['SubId'].dropna().unique()),'CrestWidth'] *= k_multi
print (df_Lakes_obs.loc[df_Lakes_obs['Reservoir'].isin([108083,8741,1034779,1032844]),['Reservoir','CrestWidth']])
df = pd.DataFrame({'Obs':df_Lakes_obs['CrestWidth'].values})
#=====================================================
for cnum, expname in enumerate(lexp):
    print ('='*100)
    print (expname)
    num      = met[expname]
    fname    = odir+"/"+expname+"_%02d/best/RavenInput/Lakes.rvh"%(num)
    df_Lakes = read_Lakes(fname)
    k_multi  = read_costFunction_component(expname, num, component='k_multi', odir=odir)
    print (k_multi)
    df_Lakes.loc[df_Lakes['SubBasinID'].isin(final_cat[final_cat[colname[expname]]==1]['SubId'].dropna().unique()),'CrestWidth'] *= k_multi
    print (df_Lakes.loc[df_Lakes['Reservoir'].isin([108083,8741,1034779,1032844]),['Reservoir','CrestWidth']])
    df[expname] = df_Lakes['CrestWidth'].values

#========================================
# colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]
# colors = [plt.cm.tab10(3),plt.cm.tab10(0),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab10(16),plt.cm.tab10(5),plt.cm.tab10(6)]
colors = [plt.cm.tab10(3),plt.cm.tab10(2),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab20(2),plt.cm.tab10(5),plt.cm.tab10(6)]

print (df)
df_melted = pd.melt(df,id_vars='Obs')

print (df_melted)
# print (df_melted)
fig, ax = plt.subplots(figsize=(8, 8))
ax=sns.scatterplot(data=df_melted, x="Obs", y="value", 
hue="variable", style="variable", s=100, sizes=(100,200),
alpha=0.6)

# Add a 1:1 line
min_val = min(df_melted["Obs"].min(), df_melted["value"].min())
max_val = max(df_melted["Obs"].max(), df_melted["value"].max())
ax.plot([min_val, max_val], [min_val, max_val], color="grey", linestyle="--", linewidth=1, label="1:1 Line")

ax.set_ylim(0.0,100.0)
ax.set_xlim(0.0,100.0)

ax.set_xlabel('Assume-to-be-truth CW')
ax.set_ylabel('Calibrated CW')

plt.tight_layout()
print ('../figures/paper/fs14-CW_boxplot_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.savefig('../figures/paper/fs14-CW_boxplot_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')