#!/usr/python
'''
compare observations
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
#===============================================================================================
def read_rvt_file(file_path):
    '''
    # Function to read the file and create a dataframe
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Extract the initial date (ignoring the first line which is the header)
    initial_entry = lines[1].split()
    date = initial_entry[0] + " " + initial_entry[1]

    # Read subsequent values, ignoring the last line (':EndObservationData')
    values = [float(line.strip()) for line in lines[2:-1]]

    # Create a date range starting from the initial date
    date_range = pd.date_range(start=date, periods=len(values), freq='D')

    # Create the dataframe
    df = pd.DataFrame({'date': date_range, 'value': values})

    # Remove the unobserved values
    df = df[df['value']!=-1.2345]

    return df
#===============================================================================================
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
HyLakeId=final_cat[final_cat['Obs_WL_IS']==1]['HyLakeId'].dropna().unique()
# llake=["./obs/WA_RS_%d_%d.rvt"%(lake,subid) for lake,subid in zip(final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique(),
#             final_cat[final_cat[colname[expname]]==1]['SubId'].dropna().unique())]
llake=[lake for lake in final_cat[final_cat['Obs_WL_IS']==1]['SubId'].dropna().unique()]
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
pdfname='../figures/pdf/d07-compare_lakes_obs_'+datetime.datetime.now().strftime("%Y%m%d")+'.pdf'
#========================================
#========================================
with PdfPages(pdfname) as pdf:
    for point in range(len(HyLakeId)):
        fig = plt.figure(figsize=(wdt,hgt))
        G   = gridspec.GridSpec(ncols=1, nrows=1)
        ax  = fig.add_subplot(G[0,0])
        #===
        # read observations
        Hylakid=int(HyLakeId[point])
        SubId=final_cat[final_cat['HyLakeId']==Hylakid]['SubId'].dropna().unique()[0]
        # original observations
        WL_name='/scratch/menaka/LakeCalibration/OstrichRaven/RavenInput/obs/WL_IS_'+str(Hylakid)+'_'+str(SubId)+'.rvt'
        WL_org = read_rvt_file(WL_name)
        #
        WA_name='/scratch/menaka/LakeCalibration/OstrichRaven/RavenInput/obs/WA_RS_'+str(Hylakid)+'_'+str(SubId)+'.rvt'
        WA_org = read_rvt_file(WA_name)
        # combine
        df_org=pd.merge(WL_org,WA_org,on='date',how='inner',suffixes=('_WL', '_WA'))
        #==============================================================
        # plot
        ax.plot(df_org['value_WL']-df_org['value_WL'].mean(),df_org['value_WA'],marker='o',color='k',linestyle='none',linewidth=0,label='Org')
        # sythetic observations
        WL_name='/home/menaka/scratch/SytheticLakeObs/output/obs1b/WL_SY_'+str(Hylakid)+'_'+str(SubId)+'.rvt'
        WL_syt = read_rvt_file(WL_name)
        #
        WA_name='/home/menaka/scratch/SytheticLakeObs/output/obs1b/WA_SY_'+str(Hylakid)+'_'+str(SubId)+'.rvt'
        WA_syt = read_rvt_file(WA_name)
        # combine
        df_syt=pd.merge(WL_syt,WA_syt,on='date',how='inner',suffixes=('_WL', '_WA'))
        #==============================================================
        # plot
        ax.plot(df_syt['value_WL']-df_syt['value_WL'].mean(),df_syt['value_WA'],marker='o',color='r',linestyle='none',linewidth=0,label='Sythetic')
        #
        fig.suptitle(str(int(Hylakid))+'-'+str(SubId))
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