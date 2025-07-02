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
from exp_params import *
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
expname='V4e' #'V7f'#'V4c' #"S1z" #"E0a" #"S1z" #"E0b"
# colname={
#     "E0a":"Obs_SF_IS",
#     "E0b":"Obs_WL_IS",
#     "S0a":"Obs_WL_IS",
#     "S0b":"Obs_WL_IS",
#     "S0c":"Obs_SF_IS",
#     "S1d":"Obs_WA_RS3",
#     "S1f":"Obs_WA_RS4",
#     "S1h":"Obs_WA_RS5",
#     "S1i":"Obs_WA_RS4",
#     "S1z":"Obs_WA_RS4",
#     "V0a":"Obs_SF_SY",
#     "V1a":"Obs_WA_SY1",
#     "V1b":"Obs_WA_SY1",
#     "V1c":"Obs_WA_SY1",
#     "V1d":"Obs_WA_SY1",
#     "V2a":"Obs_WA_SY1",
#     "V2b":"Obs_WA_SY1",
#     "V2c":"Obs_WA_SY1",
#     "V2d":"Obs_WA_SY1",
#     "V2e":"Obs_WA_SY0",
#     "V3d":"Obs_WA_SY1",
# }
colname=get_final_cat_colname()
#========================================
prefix='IS'
if expname[0]=='V':
    prefix='SY'
#========================================
# read final cat 
final_cat=pd.read_csv('/home/menaka/scratch/LakeCalibration/OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
print (final_cat.columns)
# llake=["./obs/WA_RS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in HyLakeId]
HyLakeId=final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique()
# llake=["./obs/WA_RS_%d_%d.rvt"%(lake,subid) for lake,subid in zip(final_cat[final_cat[colname[expname]]==1]['HyLakeId'].dropna().unique(),
#             final_cat[final_cat[colname[expname]]==1]['SubId'].dropna().unique())]
llake=[lake for lake in final_cat[(final_cat[colname[expname]]==1) & (final_cat['HRU_IsLake']==1)]['SubId'].dropna().unique()]
# llake=[241, 135]
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

pdfname = f'../figures/pdf/d11-lakearea_lakes_{expname}_{datetime.datetime.now():%Y%m%d}.pdf'
# === Cache all ensemble data once ===
ensemble_data = {}
for num in range(1, ens_num + 1):
    res_file = f"{odir}/{expname}_{num:02d}/best_Raven/RavenInput/output/Petawawa_ReservoirMassBalance.csv"
    diag_file = f"{odir}/{expname}_{num:02d}/best_Raven/RavenInput/output/Petawawa_Diagnostics.csv"
    
    try:
        df = pd.read_csv(res_file)
        df_diag = pd.read_csv(diag_file)
        ensemble_data[num] = {"df": df, "df_diag": df_diag}
        print(f"Loaded ensemble {num}")
    except FileNotFoundError:
        print(f"Missing files for ensemble {num}, skipping...")
        continue

# === Create PDF with lake plots ===
with PdfPages(pdfname) as pdf:
    for lake_id in llake:
        fig, ax = plt.subplots(figsize=(wdt, hgt))
        print('='*20)
        print(f"Lake ID: {lake_id}")

        hy_lake_ids = final_cat.loc[
            (final_cat['SubId'] == lake_id) & (final_cat['HRU_IsLake'] > 0), 'HyLakeId'
        ].values

        if len(hy_lake_ids) == 0:
            print(f"No HyLakeId found for lake {lake_id}")
            continue

        hy_lake_id = int(hy_lake_ids[0])  # Assume one per lake

        area_col = f"sub{lake_id} area [m2]"

        for num, data in ensemble_data.items():
            df = data["df"]
            df_diag = data["df_diag"]

            if area_col not in df.columns:
                print(f"{area_col} not found in ensemble {num}")
                continue

            diag_filename = f"./obs/WA_{prefix}_{hy_lake_id}_{lake_id}.rvt"
            diag_row = df_diag[df_diag['filename'] == diag_filename]

            if diag_row.empty:
                print(f"{diag_filename} not found in diagnostics for ensemble {num}")
                continue

            kged = diag_row['DIAG_KLING_GUPTA_DEVIATION'].values[0]
            ax.plot(df.index, df[area_col] - df[area_col].mean(),
                    linestyle='-', linewidth=1, label=f'{num:02d} ({kged:.2f})', alpha=0.5)

        ax.xaxis.set_major_locator(mdates.YearLocator())
        fig.suptitle(f"{hy_lake_id} - {lake_id}")
        ax.legend(framealpha=0.5)
        pdf.savefig(fig)
        plt.close(fig)

    # PDF metadata
    meta = pdf.infodict()
    meta.update({
        'Title': 'Lake area timeseries',
        'Author': 'Menaka Revel',
        'Subject': 'Lake area of lakes Petawawa',
        'Keywords': 'Lake area',
        'CreationDate': datetime.datetime.today(),
        'ModDate': datetime.datetime.today()
    })

#
# create a pdf file
#pdfname='../figures/pdf/d11-lakearea_lakes'+datetime.datetime.now().strftime("%Y%m%d")+'.pdf'
#========================================
# #with PdfPages(pdfname) as pdf:
#     for point in range(len(llake)):
#         fig = plt.figure(figsize=(wdt,hgt))
#         G   = gridspec.GridSpec(ncols=1, nrows=1)
#         ax  = fig.add_subplot(G[0,0])
#         print ('='*20)
#         print (llake[point])
#         for num in range(1,ens_num+1):
#             print (expname, num)
#             # read Reservoir Stage
#             df=pd.read_csv(odir+'/%s_%02d/best_Raven/RavenInput/output/Petawawa_ReservoirMassBalance.csv'%(expname,num))
#             df_diag=pd.read_csv(odir+'/%s_%02d/best_Raven/RavenInput/output/Petawawa_Diagnostics.csv'%(expname,num))
#             col='sub%0d area [m2]'%(llake[point]) #sub202 area [m2]
#             print (col)
#             if col not in df.columns:
#                 print (col, "not in df")
#                 continue
#             # print (df_diag.columns)
#             if num == 1:
#                 colWL='sub%0d (observed) [m]'%(llake[point])
#                 # ax.plot(df.index,df[colWL]-df[colWL].mean(),linestyle='-',linewidth=3,label="observation [Lake-stage]",color='k')
#             #======================
#             HyLakeId=final_cat[(final_cat['SubId']==llake[point]) & (final_cat['HRU_IsLake']>0)]['HyLakeId'].values
#             # kged=df_diag[(df_diag['observed_data_series'].str.contains('CALIBRATION')) & (df_diag['filename']=="./obs/WL_IS_%d_%d.rvt"%(int(HyLakeId[point]),llake[point]))]['DIAG_KLING_GUPTA_DEVIATION'].values[0]
#             print ("./obs/WA_%s_%d_%d.rvt"%(prefix,int(HyLakeId),llake[point]))
#             kged=df_diag[df_diag['filename']=="./obs/WA_%s_%d_%d.rvt"%(prefix,int(HyLakeId),llake[point])]['DIAG_KLING_GUPTA_DEVIATION'].values[0]
#             print ("./obs/WA_%s_%d_%d.rvt"%(prefix,int(HyLakeId),llake[point]),kged)
#             ax.plot(df.index,df[col]-df[col].mean(),linestyle='-',linewidth=1,label='%02d(%3.2f)'%(num,kged),alpha=0.5) #,color='b'
#             #
#         ax.xaxis.set_major_locator(mdates.YearLocator())
#         fig.suptitle(str(int(HyLakeId))+'-'+str(llake[point]))
#         plt.legend(framealpha=0.5)
#         pdf.savefig()
#         plt.close()
#     # We can also set the file's metadata via the PdfPages object:
#     d = pdf.infodict()
#     d['Title'] = 'Lake area timeseries'
#     d['Author'] = u'Menaka Revel'
#     d['Subject'] = 'Lake area of lakes Petawawa'
#     d['Keywords'] = 'Lake area, '
#     d['CreationDate'] = datetime.datetime.today()
#     d['ModDate'] = datetime.datetime.today()