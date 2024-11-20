#!/usr/python
'''
plot lake levels
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

#========================================
# odir='../out'
odir='/scratch/menaka/LakeCalibration/out'
mk_dir("../figures/pdf")
ens_num=10
metric=[]
expname='V1d' #"S1z" #"E0a" #"S1z" #"E0b"
lexp=["V0a","V2e","V2d","V2a"]
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
    "V2a":"Obs_WA_SY1",
    "V2b":"Obs_WA_SY1",
    "V2c":"Obs_WA_SY1",
    "V2d":"Obs_WA_SY1",
    "V2e":"Obs_WA_SY0",
    "V3d":"Obs_WA_SY1",
}
#========================================
prefix='IS'
if expname[0]=='V':
    prefix='SY'
#========================================
#========================================
# read final cat 
# final_cat=pd.read_csv('/home/menaka/scratch/LakeCalibration/OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
final_cat=pd.read_csv('../OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
print (final_cat.columns)

SubIds=final_cat[final_cat['HRU_IsLake']==1]['SubId'].dropna().unique()

#========================================
# colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]
colors = [plt.cm.tab10(3),plt.cm.tab10(0),plt.cm.tab10(8),plt.cm.tab10(12),plt.cm.tab10(16),plt.cm.tab10(5),plt.cm.tab10(6)]

num_plots = 10

# Have a look at the colormaps here and decide which one you'd like:
# http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
colormap = plt.cm.gist_ncar
plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, num_plots))))


# locs=[-0.26,0,0.26]
locs=[-0.27,-0.11,0.11,0.27]

va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=4 #(11.69 - 2*va_margin)*(3.0/5.0)
wdt=12 #(8.27 - 2*ho_margin)*(2.0/2.0)
#
# create a pdf file
pdfname='../figures/pdf/d08-lake_Q_'+datetime.datetime.now().strftime("%Y%m%d")+'.pdf'
#========================================
with PdfPages(pdfname) as pdf:
    for point in range(len(SubIds))[0:10]:
        fig = plt.figure(figsize=(wdt,hgt))
        G   = gridspec.GridSpec(ncols=1, nrows=1)
        ax  = fig.add_subplot(G[0,0])
        print ('='*20)
        # print (SubIds[point])
        for cnum, expname in enumerate(lexp):
            for num in range(1,ens_num+1):
                # print (expname, num)
                # read discharge
                df=pd.read_csv(odir+'/%s_%02d/best_Raven/RavenInput/output/Petawawa_Hydrographs.csv'%(expname,num))
                df['date']=pd.to_datetime(df['date'])
                df_diag=pd.read_csv(odir+'/%s_%02d/best_Raven/RavenInput/output/Petawawa_Diagnostics.csv'%(expname,num))
                col='sub%0d [m3/s]'%(SubIds[point])
                # print (col)
                if col not in df.columns:
                    print (col, "not in df")
                    continue
                # print (df_diag.columns)
                if num == 1:
                    colObs='sub%0d (observed) [m3/s]'%(SubIds[point])
                    ax.plot(df['date'],df[colObs],linestyle='-',linewidth=3,label="Truth",color='k')
                #======================
                HyLakeId=final_cat[(final_cat['SubId']==SubIds[point]) & (final_cat['HRU_IsLake']>0)]['HyLakeId'].values
                # kged=df_diag[(df_diag['observed_data_series'].str.contains('CALIBRATION')) & (df_diag['filename']=="./obs/WL_IS_%d_%d.rvt"%(int(HyLakeId[point]),SubIds[point]))]['DIAG_KLING_GUPTA_DEVIATION'].values[0]
                kged=df_diag[df_diag['filename']=="./obs/SF_%s_sub%d_%d.rvt"%(prefix,SubIds[point],SubIds[point])]['DIAG_KLING_GUPTA'].values[0]
                print (expname, num, "./obs/SF_%s_sub%d_%d.rvt"%(prefix,SubIds[point],SubIds[point]),kged)
                ax.plot(df['date'],df[col],linestyle='-',linewidth=1,label='%02d(%3.2f)'%(num,kged),alpha=0.5,color=colors[cnum]) #,color='b'
                #
        ax.xaxis.set_major_locator(mdates.YearLocator())
        fig.suptitle(str(int(HyLakeId))+'-'+str(SubIds[point]))
        plt.legend(framealpha=0.5)
        pdf.savefig()
        plt.close()
    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Discharge at lake catchments '
    d['Author'] = u'Menaka Revel'
    d['Subject'] = 'Discharge at lake catchments of Petawawa'
    d['Keywords'] = 'Discharge, Lakes'
    d['CreationDate'] = datetime.datetime.today()
    d['ModDate'] = datetime.datetime.today()           