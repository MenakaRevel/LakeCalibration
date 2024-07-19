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
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import matplotlib.lines as mlines
from matplotlib.backends.backend_pdf import PdfPages
import datetime
from numpy import ma
mpl.use('Agg')
#===============================================================================================
def mk_dir(dir):
    # Create the download directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)
#========================================
def read_Diagnostics_Raven_best(fname='../out/output/SE_Diagnostics.csv'):
    # df=pd.read_csv('RavenInput/'+exp+'/SE_Diagnostics.csv')
    print (fname)
    df=pd.read_csv(fname)
    df['Obs_NM']=df['filename'].apply(extract_string_from_path)
    print (df.head())
    return df
#========================================
def read_costFunction(expname, ens_num, div=1.0, odir='../out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return (df['obj.function'].iloc[-1]/float(div))*-1.0
#========================================
def read_costFunction_component(expname, ens_num, component='k_multi', odir='../out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return df[component].iloc[-1]
#========================================
def read_diagnostics(expname, ens_num, odir='../out',output='output',
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
    return df[(df['observed_data_series'].str.contains('CALIBRATION')) & (df['filename'].isin(lakes))].set_index('filename').reindex(lakes)['DIAG_KLING_GUPTA_DEVIATION'].values
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
                current_reservoir['Reservoir']=int(value.split('_')[1])
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
                        current_reservoir['SeepageParameters1']=value.strip().split(' ')[1]
                        current_reservoir['SeepageParameters1']=value.strip().split(' ')[2]
                    else:
                        current_reservoir[key.strip()[1:]] = value.strip()
                    # print (key[1::], value.strip())

    # except FileNotFoundError:
    #     print(f"Error: File '{file_path}' not found.")
    df=pd.DataFrame(reservoir_data)
    df['WeirCoefficient']=df['WeirCoefficient'].astype(float)
    df['CrestWidth']     =df['CrestWidth'].astype(float)
    df['MaxDepth']       =df['WeirCoefficient'].astype(float)

    return df
#========================================
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

# read final cat 
final_cat=pd.read_csv('../OstrichRaven/finalcat_hru_info_updated.csv')
llake=["./obs/WL_IS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in HyLakeId]
print (llake)
#========================================
# expname="S1a"
odir='../out'
# lexp=["E0a","E0b","S1a"]#,"S1c","S1d","S1e"]
lexp=["E0a","E0b","S1d"]
expriment_name=[]
#========================================================================================
mk_dir("../figures/pdf")
ens_num=10
metric=[]
for expname in lexp:
    objFunction0=1.0
    for num in range(1,ens_num+1):
        print (expname, num)
        row=list(read_lake_diagnostics(expname, num, llake, odir=odir, best_dir='best_Raven'))
        df_=read_Lakes(expname, num, odir=odir)
        k_=read_costFunction_component(expname, num, component='k_multi', odir='../out')
        if expname in ['E0a','S1c','S1e']:
            k=k_
        else:
            k=1.0
        CrestWidth=[df_[df_['Reservoir']==id]['CrestWidth'].values[0]*k for id in HyLakeId]
        row.extend(CrestWidth)
        row.append("Exp"+expname)
        row.append(num)
        metric.append([row])
metric=np.array(metric)[:,0,:]
print (np.shape(metric))
#===============================================
columns=['KGED_%s'%(id) for id in HyLakeId]
columns.extend(['CW_%s'%(id) for id in HyLakeId])
print (columns)
columns.append('Experiment') #['02KB001','LM','Narrowbag','Crow','NC','obj.function']
columns.append('Enseble_Number')
df=pd.DataFrame(metric, columns=columns)
# df['Experiment']=np.array(expriment_name)
print ('='*20+' df '+'='*20)
print (df.head(10))
#
colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]

# locs=[-0.26,0,0.26]
locs=[-0.27,-0.11,0.11,0.27]

va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=4 #(11.69 - 2*va_margin)*(3.0/5.0)
wdt=12 #(8.27 - 2*ho_margin)*(2.0/2.0)
#
# create a pdf file
pdfname='../figures/pdf/d04-CresetWidth_KGED.pdf'
with PdfPages(pdfname) as pdf:
    for point in range(len(HyLakeId)):
        fig = plt.figure(figsize=(wdt,hgt))
        G   = gridspec.GridSpec(ncols=1, nrows=1)
        ax  = fig.add_subplot(G[0,0])
        print ('='*20)
        hylak=HyLakeId[point]
        df_plot=df.loc[:,['Experiment','CW_%s'%(hylak),'KGED_%s'%(hylak)]]
        df_plot['CW_%s'%(hylak)] = pd.to_numeric(df_plot['CW_%s'%(hylak)])
        # get K_multi
        df_plot['KGED_%s'%(hylak)] = pd.to_numeric(df_plot['KGED_%s'%(hylak)])
        # Plot scatterplot with hue
        sns.scatterplot(data=df_plot, x='CW_%s'%(hylak), y='KGED_%s'%(hylak), hue='Experiment', ax=ax)
        # regression line
        # sns.regplot(data=df_plot, x='CW_%s'%(hylak), y='KGED_%s'%(hylak),ax=ax)
        # plt.legend(framealpha=0.5)
        pdf.savefig()
        plt.close()
    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Lake CW vs KGED'
    d['Author'] = u'Menaka Revel'
    d['Subject'] = 'Lake CW vs KGED'
    d['Keywords'] = 'Lake CW vs KGED'
    d['CreationDate'] = datetime.datetime.today()
    d['ModDate'] = datetime.datetime.today()