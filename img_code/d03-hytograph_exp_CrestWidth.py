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
from  matplotlib.colors import Normalize
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import matplotlib.lines as mlines
from matplotlib.backends.backend_pdf import PdfPages
import datetime
from numpy import ma
import cmasher as cmr
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
def read_lake_diagnostics(expname, ens_num, odir='../out',output='output',best='best'):
    '''
    read the RunName_Diagnostics.csv
    '''
    fname=odir+"/"+expname+"_%02d/%s/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,best,output)
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/output_Raven_v3.7/Petawawa_Diagnostics.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    print (fname) 
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    return df
#=====================================================
def read_WaterLevel(expname, ens_num, odir='../out',syear=2016,smon=1,sday=1,eyear=2020,emon=10,eday=20,best='best_Raven',ftype='ReservoirStages'):
    '''
    read the RunName_WateLevels.csv
    read the ReservoirStages.csv
    '''
    fname=odir+"/"+expname+"_%02d/%s/RavenInput/output/Petawawa_%s.csv"%(ens_num,best,ftype)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_WaterLevels.csv"%(ens_num)
    print (fname)
    df=pd.read_csv(fname)
    # calculate the metrics for syear,smon,sday:eyear,emon,eday [Evaluation Period]
    df.set_index('date',inplace=True)
    start='%04d-%02d-%02d'%(syear,smon,sday)
    end='%04d-%02d-%02d'%(eyear,emon,eday)
    print (start, end)
    df=df.loc[start:end]
    # calculate spearman correlation
    return remove_noobs(df)
#=====================================================
def read_Hydrograph(expname, ens_num, odir='../out',syear=2016,smon=1,sday=1,eyear=2020,emon=10,eday=20):
    '''
    read the RunName_Hydrograph.csv
    '''
    fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/output/Petawawa_Hydrographs.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_WaterLevels.csv"%(ens_num)
    print (fname)
    df=pd.read_csv(fname)
    # calculate the metrics for syear,smon,sday:eyear,emon,eday [Evaluation Period]
    df.set_index('date',inplace=True)
    start='%04d-%02d-%02d'%(syear,smon,sday)
    end='%04d-%02d-%02d'%(eyear,emon,eday)
    print (start, end)
    df=df.loc[start:end]
    # calculate spearman correlation
    return remove_noobs(df) 
#=====================================================
def remove_noobs(df):
    df[df.iloc[:,3::]==-1.2345]=np.nan 
    return df
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
def filter_nan(s,o):
    """
    this functions removed the data  from simulated and observed data
    where ever the observed data contains nan
    """
    data = np.array([s.flatten(),o.flatten()])
    data = np.transpose(data)
    data = data[~np.isnan(data).any(1)]

    return data[:,0],data[:,1]
#=====================================================
def KGED1(s,o):
    """
	Kling Gupta Efficiency Deviation (Kling et al., 2012, http://dx.doi.org/10.1016/j.jhydrol.2012.01.011)
	input:
        s: simulated
        o: observed
    output:
        KGE: Kling Gupta Efficiency
    """
    o=ma.masked_where(o==-9999.0,o).filled(0.0)
    s=ma.masked_where(o==-9999.0,s).filled(0.0)
    o=np.compress(o>0.0,o)
    s=np.compress(o>0.0,s)
    s,o = filter_nan(s,o)
    B = np.mean(s) / np.mean(o)
    y = (np.std(s) / np.mean(s)) / (np.std(o) / np.mean(o))
    r = np.corrcoef(o, s)[0,1]
    return 1 - np.sqrt((r - 1) ** 2 + (y - 1) ** 2)
#=====================================================
def KGED(s, o):
    """
    Kling Gupta Efficiency Deviation (Kling et al., 2012, http://dx.doi.org/10.1016/j.jhydrol.2012.01.011)
    input:
        s: simulated
        o: observed
    output:
        KGE: Kling Gupta Efficiency
    """
    # Masking invalid values in observed data
    o_masked = ma.masked_where(o == -9999.0, o)

    # Filtering non-positive observed values
    o_filtered = np.compress(o_masked > 0.0, o)
    s_filtered = np.compress(o_masked > 0.0, s)

    # Removing NaN values
    mask_nan = ~np.isnan(s_filtered) & ~np.isnan(o_filtered)
    s = s_filtered[mask_nan]
    o = o_filtered[mask_nan]

    if len(s) == 0 or len(o) == 0:
        return np.nan

    # Calculation of B, y, and r
    B = np.mean(s) / np.mean(o)
    # y = (np.std(s) / np.mean(s)) / (np.std(o) / np.mean(o))
    y = np.std(s) / np.std(o)
    r = np.corrcoef(o, s)[0, 1]

    # Calculate KGE
    return 1 - np.sqrt((r - 1) ** 2 + (y - 1) ** 2)
#=====================================================
#np.array([df['sub265 [m]'].corr(df['sub265 (observed) [m]'] ,method='spearman'),
#    df['sub400 [m]'].corr(df['sub400 (observed) [m]'] ,method='spearman'),
#    df['sub412 [m]'].corr(df['sub412 (observed) [m]'] ,method='spearman')])
#=====================================================
# expname="S0b"
odir='../out'
#=====================================================
mk_dir("../figures/pdf")
ens_num=10
expname="S0b"
# lexp=["S0a","S0b","S1a","S1b"]
# best_member={}
df_waterLevel={}
df_diganostics={}
df_lakePara={}
objFunction=[]
for num in range(1,ens_num+1):
    print (expname, num)
    objFunction.append(read_costFunction(expname, num, odir=odir))
    # expriment_name.append("Exp"+expname)
    # best_member[num]=np.array(objFunction).argmin() + 1
    df_waterLevel[num]=read_WaterLevel(expname, num)
    df_diganostics[num]=read_lake_diagnostics(expname, num)
    df_lakePara[num]=read_Lakes(expname, num, odir=odir)
    # df_[df_['Reservoir'].isin(HyLakeId)]['CrestWidth'].values

best_member=np.array(objFunction).argmin() + 1
print (best_member)
# df_waterLevel = {expname: read_WaterLevel(expname, best_member[expname]) for i in range(1,13)}
#===================
namelist = ['./obs/WL_Animoosh_345.rvt',
       './obs/WL_Big_Trout_220.rvt', './obs/WL_Burntroot_228.rvt',
       './obs/WL_Cedar_528.rvt', './obs/WL_Charles_381.rvt',
       './obs/WL_Grand_753.rvt', './obs/WL_Hambone_48.rvt',
       './obs/WL_Hogan_291.rvt', './obs/WL_La_Muir_241.rvt',
       './obs/WL_Lilypond_117.rvt', './obs/WL_Little_Cauchon_449.rvt',
       './obs/WL_Loontail_122.rvt', './obs/WL_Misty_135.rvt',
       './obs/WL_Narrowbag_281.rvt', './obs/WL_North_Depot_497.rvt',
       './obs/WL_Radiant_574.rvt', './obs/WL_Timberwolf_116.rvt',
       './obs/WL_Traverse_767.rvt', './obs/WL_Lavieille_326.rvt']

sub_list= [345, 220, 228, 528, 381, 753, 48, 291, 241, 117, 449, 122, 135, 281, 497, 574, 116, 767, 326]

lake_list=['Animoosh','Big_Trout', 'Burntroot',
       'Cedar', 'Charles','Grand', 'Hambone',
       'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
       'Loontail', 'Misty','Narrowbag', 'North_Depot',
       'Radiant', 'Timberwolf','Traverse', 'Lavieille']

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
#===
# # calculate lake area
# for point in range(len(lake_list)):
#     # read observation file
#     df_waterArea_tmp=pd.read_csv(namelist[point], skiprows=(0, 1), sep='\s+', engine='python')

# df_waterLevel=read_WaterLevel(exp, 4)
# df_waterLevel_=read_WaterLevel(exp, 4, best='best_AdjWidth')
# df_diganostics=read_lake_diagnostics(exp, 4)
# df_diganostics_=read_lake_diagnostics(exp, 4, best='best_AdjWidth')

# colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]
# colors = plt.cm.GnBu(Normalize(vmin=1,vmax=ens_num+1))
cmap = plt.get_cmap('GnBu')  # You can choose any colormap you #
cmap = cmr.get_sub_cmap('GnBu', 0.3, 1.0)
norm = Normalize(vmin=1,vmax=ens_num+1)
# colors =cmap(norm())
# locs=[-0.26,0,0.26]
locs=[-0.27,-0.11,0.11,0.27]

va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=8 #(11.69 - 2*va_margin)*(3.0/5.0)
wdt=12 #(8.27 - 2*ho_margin)*(2.0/2.0)
#
# create a pdf file
pdfname='../figures/pdf/d03-%s_lakes_all_exp.pdf'%(expname)
with PdfPages(pdfname) as pdf:
    for point in range(len(lake_list)):
        fig = plt.figure(figsize=(wdt,hgt))
        G   = gridspec.GridSpec(ncols=2, nrows=2)
        ax  = fig.add_subplot(G[0,:])
        kge_list=[]
        cw_list=[]
        for num in range(1,ens_num+1):
            print (num)
            df=df_waterLevel[num]
            df.index=pd.to_datetime(df.index)
            df_=df_diganostics[num]
            dfP=df_lakePara[num]
            # print (df.columns)
            # print (df_.head())
            if num==1: # plot observations
                # plot WL
                colWL='sub%0d (observed) [m]'%(sub_list[point])
                ax.plot(df.index,df[colWL]-df[colWL].mean(),linestyle='-',linewidth=3,label="observation",color='k')
                # plot WL
                colWA='sub%0d (observed) [m].1'%(sub_list[point])
                axtwin = ax.twinx()
                axtwin.plot(df.index,df[colWA],linestyle='none', marker="o", markersize=4, markerfacecolor="None",markeredgecolor='grey',label="observation [Lake-area]",color='k')
            if num == best_member:
                color='r'
                zorder=110
            else:
                color=cmap(norm(num))
                zorder=100
            # plot simulated
            col='sub%0d '%(sub_list[point])
            kge=df_[(df_['observed_data_series'].str.contains('CALIBRATION')) & (df_['filename'].isin([namelist[point]]))][['DIAG_KLING_GUPTA_DEVIATION']].values
            cw=dfP[dfP['Reservoir']==int(HylakID_data[lake_list[point]])]['CrestWidth'].values
            kge_list.append(kge[0][0])
            cw_list.append(float(cw[0]))
            label='%02d (KGED:%5.2f | CrestWidth:%5.2f)'%(num,kge,cw)
            print (label)
            #KGED(df[col].values,df[colWL].values)
            # df_waterLevel.loc[df_waterLevel.index.month.isin([12,1,2,3]), colWL]=np.nan
            ax.plot(df.index,df[col]-df[col].mean(),linestyle='-',linewidth=1,label=label,color=color,zorder=zorder)
            # kge_=df_diganostics_[(df_diganostics_['observed_data_series'].str.contains('CALIBRATION')) & (df_diganostics_['filename'].isin([namelist[point]]))][['DIAG_KLING_GUPTA_DEVIATION']].values
            # label_=exp+'AdjWidth (%5.2f)'%kge_
            # ax.plot(df.index,df[col]-df[col].mean(),linestyle='--',linewidth=0.5,label=label_,color='b')
        # ask matplotlib for the plotted objects and their labels
        lines2, labels2 = ax.get_legend_handles_labels()
        lines, labels = axtwin.get_legend_handles_labels()
        axtwin.legend(lines + lines2, labels + labels2, loc='upper left',bbox_to_anchor=(0.5,-0.1), framealpha=0.5, ncols=1, prop={'size': 12})
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.set_ylabel('Lake Stage Anomaly $(m)$',fontsize=10)
        axtwin.set_ylabel('Lake Surface Area $(m^2)$',fontsize=10)
        #========================
        ax1  = fig.add_subplot(G[1,0])
        print (cw_list,kge_list)
        ax1.plot(cw_list,kge_list,linestyle='none', marker="o", markersize=4, markerfacecolor="None",markeredgecolor='b',color='k')
        ax1.set_xlabel('Lake Crest Width $(m)$',fontsize=10)
        ax1.set_ylabel('KGED',fontsize=10)
        #========================
        fig.suptitle(lake_list[point])
        # plt.legend(framealpha=0.5)
        pdf.savefig()
        plt.close()
    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Lake water level anomaly timeseries of experiment'
    d['Author'] = u'Menaka Revel'
    d['Subject'] = 'Water levels of lakes Petawawa'
    d['Keywords'] = 'water level, experiment, '+ expname
    d['CreationDate'] = datetime.datetime.today()
    d['ModDate'] = datetime.datetime.today()