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
#=====================================================
def read_costFunction(expname, ens_num, odir='../out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return df['obj.function'].iloc[-1]
#=====================================================
def read_lake_diagnostics(expname, ens_num, odir='../out',output='output'):
    '''
    read the RunName_Diagnostics.csv
    '''
    fname=odir+"/"+expname+"_%02d/best/RavenInput/%s/Petawawa_Diagnostics.csv"%(ens_num,output)
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/output_Raven_v3.7/Petawawa_Diagnostics.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    print (fname) 
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    return df
#=====================================================
def read_WaterLevel(expname, ens_num, odir='../out',syear=2016,smon=1,sday=1,eyear=2020,emon=10,eday=20,ftype='ReservoirStages'):
    '''
    read the RunName_WateLevels.csv
    read the ReservoirStages.csv
    '''
    fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/output/Petawawa_%s.csv"%(ens_num,ftype)
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
expname="S1a"
odir='/scratch/menaka/LakeCalibration/out'
#=====================================================
mk_dir("../figures/pdf")
ens_num=10
# lexp=["S0a","S0b","S1a","S1b"]
lexp=["E0a","E0b","S1z"]
best_member={}
df_waterLevel={}
df_diganostics={}
for expname in lexp:
    objFunction=[]
    for num in range(1,ens_num+1):
        print (expname, num)
        objFunction.append(read_costFunction(expname, num, odir=odir))
        # expriment_name.append("Exp"+expname)
    best_member[expname]=np.array(objFunction).argmin() + 1
    df_waterLevel[expname]=read_WaterLevel(expname, best_member[expname],odir=odir)
    df_diganostics[expname]=read_lake_diagnostics(expname, best_member[expname],odir=odir)

print (best_member)
# df_waterLevel = {expname: read_WaterLevel(expname, best_member[expname]) for i in range(1,13)}
#===================
namelist = ['./obs/WL_Animoosh_345.rvt',
       './obs/WL_IS_Big_Trout_220.rvt', './obs/WL_IS_Burntroot_228.rvt',
       './obs/WL_IS_Cedar_528.rvt', './obs/WL_IS_Charles_381.rvt',
       './obs/WL_IS_Grand_753.rvt', './obs/WL_IS_Hambone_48.rvt',
       './obs/WL_IS_Hogan_291.rvt', './obs/WL_IS_La_Muir_241.rvt',
       './obs/WL_IS_Lilypond_117.rvt', './obs/WL_IS_Little_Cauchon_449.rvt',
       './obs/WL_IS_Loontail_122.rvt', './obs/WL_IS_Misty_135.rvt',
       './obs/WL_IS_Narrowbag_281.rvt', './obs/WL_IS_North_Depot_497.rvt',
       './obs/WL_IS_Radiant_574.rvt', './obs/WL_IS_Timberwolf_116.rvt',
       './obs/WL_IS_Traverse_767.rvt', './obs/WL_IS_Lavieille_326.rvt']

sub_list= [345, 220, 228, 528, 381, 753, 48, 291, 241, 117, 449, 122, 135, 281, 497, 574, 116, 767, 326]

lake_list=['Animoosh','Big_Trout', 'Burntroot',
       'Cedar', 'Charles','Grand', 'Hambone',
       'Hogan', 'La_Muir','Lilypond', 'Little_Cauchon',
       'Loontail', 'Misty','Narrowbag', 'North_Depot',
       'Radiant', 'Timberwolf','Traverse', 'Lavieille']
#===
# # calculate lake area
# for point in range(len(lake_list)):
#     # read observation file
#     df_waterArea_tmp=pd.read_csv(namelist[point], skiprows=(0, 1), sep='\s+', engine='python')

colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]

# locs=[-0.26,0,0.26]
locs=[-0.27,-0.11,0.11,0.27]

va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=4 #(11.69 - 2*va_margin)*(3.0/5.0)
wdt=12 #(8.27 - 2*ho_margin)*(2.0/2.0)
#
# create a pdf file
pdfname='../figures/pdf/d01-waterlevel_lakes'+datetime.datetime.now().strftime("%Y%m%d")+'.pdf'
with PdfPages(pdfname) as pdf:
    for point in range(len(lake_list)):
        fig = plt.figure(figsize=(wdt,hgt))
        G   = gridspec.GridSpec(ncols=1, nrows=1)
        ax  = fig.add_subplot(G[0,0])
        print ('='*20)
        for i,expname in enumerate(lexp):
            print (expname)
            df=df_waterLevel[expname]
            df.index=pd.to_datetime(df.index)
            df_=df_diganostics[expname]
            # print (df.columns)
            # print (df_.head())
            if i==0: # plot observations
                colWL='sub%0d (observed) [m]'%(sub_list[point])
                ax.plot(df.index,df[colWL]-df[colWL].mean(),linestyle='-',linewidth=3,label="observation [Lake-stage]",color='k')
                colWA='sub%0d (observed) [m].1'%(sub_list[point])
                axtwin = ax.twinx()
                axtwin.plot(df.index,df[colWA],linestyle='none', marker="o", markersize=4, markerfacecolor="None",markeredgecolor='k',label="observation [Lake-area]")
                # ax.plot([],[],linestyle='none', marker="o", markersize=4, markerfacecolor="None",markeredgecolor='k',label="observation [Lake-area]")
            col='sub%0d '%(sub_list[point])
            kge=df_[(df_['observed_data_series'].str.contains('CALIBRATION')) & (df_['filename'].isin([namelist[point]]))][['DIAG_KLING_GUPTA_DEVIATION']].values
            label=expname+' (%5.2f)'%kge
            #KGED(df[col].values,df[colWL].values)
            print (label)
            df.loc[df.index.month.isin([12,1,2,3]), colWL]=np.nan
            # print (lake_list[point], expname, kge, KGED(df.loc['2016-01-01':'2020-10-20',col].values,df.loc['2016-01-01':'2020-10-20',colWL].values)) #KGED(np.nan_to_num(df[col].values),np.nan_to_num(df[colWL].values)))
            # print (filter_nan(np.nan_to_num(df[col].values),np.nan_to_num(df[colWL].values)))
            ax.plot(df.index,df[col]-df[col].mean(),linestyle='-',linewidth=1,label=label,color=colors[i])
        # ask matplotlib for the plotted objects and their labels
        lines2, labels2 = ax.get_legend_handles_labels()
        lines, labels = axtwin.get_legend_handles_labels()
        axtwin.legend(lines + lines2, labels + labels2, loc='upper center',bbox_to_anchor=(0.5,-0.05), framealpha=0.5, ncols=6)
        #
        ax.xaxis.set_major_locator(mdates.YearLocator())
        fig.suptitle(lake_list[point])
        # plt.legend(framealpha=0.5)
        pdf.savefig()
        plt.close()
    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Lake water level anomaly timeseries of best calibration trail'
    d['Author'] = u'Menaka Revel'
    d['Subject'] = 'Water levels of lakes Petawawa'
    d['Keywords'] = 'water level, best calibration trail'
    d['CreationDate'] = datetime.datetime.today()
    d['ModDate'] = datetime.datetime.today()