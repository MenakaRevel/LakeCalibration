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
expname="E0b"
colname={
    "E0a":"Obs_SF_IS",
    "E0b":"Obs_WL_IS",
    "S0a":"Obs_WL_IS",
    "S1d":"Obs_WA_RS3",
    "S1f":"Obs_WA_RS4",
    "S1h":"Obs_WA_RS5"
}
#========================================
# read final cat 
final_cat=pd.read_csv('/home/menaka/scratch/LakeCalibration/OstrichRaven/finalcat_hru_info_updated_AEcurve_org.csv')
# llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in HyLakeId]
HyLakeId=final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique()
# llake=["./obs/WA_RS_%d_%d.rvt"%(lake,subid) for lake,subid in zip(final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique(),
#             final_cat[final_cat[colname[expname]]==1]['SubId'].dropna().unique())]
llake=[lake for lake in final_cat[final_cat[colname[expname]]==1]['SubId'].dropna().unique()]
print (llake)
#========================================
colors = [plt.cm.tab20(0),plt.cm.tab20(1),plt.cm.tab20(2),plt.cm.tab20(3)]
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
pdfname='../figures/pdf/d06-waterlevel_lakes'+datetime.datetime.now().strftime("%Y%m%d")+'.pdf'
#========================================
with PdfPages(pdfname) as pdf:
    for point in range(len(llake)):
        fig = plt.figure(figsize=(wdt,hgt))
        G   = gridspec.GridSpec(ncols=1, nrows=1)
        ax  = fig.add_subplot(G[0,0])
        print ('='*20)
        for num in range(1,ens_num+1):
            print (expname, num)
            # read Reservoir Stage
            df=pd.read_csv(odir+'/%s_%02d/best_Raven/RavenInput/output/Petawawa_ReservoirStages.csv'%(expname,num))
            df_diag=pd.read_csv(odir+'/%s_%02d/best_Raven/RavenInput/output/Petawawa_Diagnostics.csv'%(expname,num))
            # print (df_diag.columns)
            if num == 1:
                colWL='sub%0d (observed) [m]'%(llake[point])
                ax.plot(df.index,df[colWL]-df[colWL].mean(),linestyle='-',linewidth=3,label="observation [Lake-stage]",color='k')
            col='sub%0d '%(llake[point])
            HyLakeId=final_cat[(final_cat['SubId']==llake[point]) & (final_cat['HRU_IsLake']>0)]['HyLakeId'].values
            # kged=df_diag[(df_diag['observed_data_series'].str.contains('CALIBRATION')) & (df_diag['filename']=="./obs/WL_IS_%d_%d.rvt"%(int(HyLakeId[point]),llake[point]))]['DIAG_KLING_GUPTA_DEVIATION'].values[0]
            kged=df_diag[df_diag['filename']=="./obs/WL_IS_%d_%d.rvt"%(int(HyLakeId),llake[point])]['DIAG_KLING_GUPTA_DEVIATION'].values[0]
            print ("./obs/WL_IS_%d_%d.rvt"%(int(HyLakeId),llake[point]),kged)
            ax.plot(df.index,df[col]-df[col].mean(),linestyle='-',linewidth=1,label='%02d(%3.2f)'%(num,kged),alpha=0.5) #,color='b'
            #
        ax.xaxis.set_major_locator(mdates.YearLocator())
        fig.suptitle(str(int(HyLakeId))+'-'+str(llake[point]))
        plt.legend(framealpha=0.5)
        pdf.savefig()
        plt.close()
    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'Lake water level anomaly timeseries'
    d['Author'] = u'Menaka Revel'
    d['Subject'] = 'Water levels of lakes Petawawa'
    d['Keywords'] = 'Lake water level, '
    d['CreationDate'] = datetime.datetime.today()
    d['ModDate'] = datetime.datetime.today()