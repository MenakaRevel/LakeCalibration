import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import ma
import datetime
import geopandas
import glob
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
import geopandas
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import colormaps as cmaps
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker
# mpl.use('Agg')
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
#========================================
def plot_routing_product(points_df,path_to_product_folder, collist, 
version_number='', metric='DIAG_KLING_GUPTA',title='map',clabel='KGE/KGED',suffix='shp',ax=None):
    if ax is None:
        ax = plt.gca()
    product_folder = path_to_product_folder
    if version_number != '':
        version_number = '_' + version_number
    path_subbasin = os.path.join(product_folder, 'finalcat_info' + version_number + '.' + suffix)
    path_river = os.path.join(product_folder, 'finalcat_info_riv' + version_number + '.' + suffix)
    path_cllake = os.path.join(product_folder, 'sl_connected_lake' + version_number + '.' + suffix)
    path_ncllake = os.path.join(product_folder, 'sl_non_connected_lake' + version_number + '.' + suffix)
    path_outline = os.path.join(product_folder, 'outline.' + suffix)

    subbasin = geopandas.read_file(path_subbasin)
    subbasin = subbasin.to_crs("EPSG:4326")

    # fig, ax = plt.subplots(figsize=(10, 8))

    subbasin.plot(ax=ax, color='w', edgecolor='w', linewidth=0.5, alpha=0.5)

    if os.path.exists(path_river):
        river = geopandas.read_file(path_river)
        river = river.to_crs("EPSG:4326")
        river.plot(ax=ax, color='#0070FF', linewidth=1, alpha=0.8)

    if os.path.exists(path_cllake):
        cllake = geopandas.read_file(path_cllake)
        cllake = cllake.to_crs("EPSG:4326")
        cllake.plot(ax=ax, color='#0070FF', edgecolor='#0070FF', linewidth=0.5, alpha=0.8)

    if os.path.exists(path_ncllake):
        ncllake = geopandas.read_file(path_ncllake)
        ncllake = ncllake.to_crs("EPSG:4326")
        ncllake.plot(ax=ax, color='#0070FF', edgecolor='#0070FF', linewidth=0.5, alpha=0.8)

    if os.path.exists(path_outline):
        outline = geopandas.read_file(path_outline)
        outline = outline.to_crs("EPSG:4326")
        outline.plot(ax=ax, facecolor="none", edgecolor='k', linewidth=1, alpha=0.8)

    # POI
    # print (subbasin['Obs_NM'].dropna().unique())
    # df_diag=df_metric#read_Diagnostics(experiment)
    # print (df_diag)
    # points_df=subbasin.loc[subbasin['Obs_NM'].isin(collist),['Obs_NM','outletLat','outletLng']]
    # print (points_df)
    # points_df=pd.merge(points_df,df_diag,on='Obs_NM',how='inner')
    # print (points_df)
    # im=ax.scatter(x=points_df['outletLng'], y=points_df['outletLat'], c=points_df['Metric'], 
    # cmap=cmaps.ylgn.discrete(5), vmin=0.0,vmax=1.0, label='Points', zorder=110, s=20, edgecolors='grey')
    # im=ax.imshow(np.array([]), cmap=cmaps.ylgn.discrete(5), vmin=0.0,vmax=1.0)
    # im.set_visible(False)

    for marker in points_df['Marker'].unique():
        # print ('marker:', marker)
        subset = points_df[points_df['Marker'] == marker]
        msize  = points_df[points_df['Marker'] == marker]['Size'].unique()[0]
        print ('marker:', marker,'msize:', msize, "mean:", subset['Metric'].mean(), "median:", subset['Metric'].median())
        im=ax.scatter(x=subset['outletLng'], y=subset['outletLat'], 
                c=subset['Metric'], cmap=cmaps.speed.discrete(10), #cmaps.ylorbr_5, #neon.discrete(100), #.purd, #blugrn.discrete(5), 
                vmin=0.0, vmax=1.0, zorder=110, s=msize, edgecolors='grey', marker=marker)


    # print (points_df.loc[:,['Obs_NM',metric]])
    ax.set_title(title, fontsize=20)
    # ax.set_axis_off()
    # plt.tight_layout()

    # # Create an axis for colorbar with the same width as the main plot
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("bottom", size="5%", pad=0.25)  # adjust size and pad as needed

    # Find position of last contour plot and use this to set position of new
    # colorbar axes.    
    # left, bottom, width, height = ax.get_position().bounds
    # cax = fig.add_axes([left, 0.03, width, 0.05])

    # cbar=plt.colorbar(im,orientation='horizontal',shrink=0.8, extend='min',
    # cax=cax,label=clabel)  # Add colorbar with label
    # cbar.set_label(clabel)

    # Setting tick labels as conventional latitude and longitude
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.2f}'.format(x)))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:.2f}'.format(y)))

    # plt.show()
    # plt.savefig('./figure/'+figname+'.jpg', dpi=500)
    return im
#========================================
# expname="S1a"
# odir='../out'
odir='/scratch/menaka/LakeCalibration/out'
#========================================
# read final cat 
# final_cat=pd.read_csv('../OstrichRaven/finalcat_hru_info_updated.csv')
final_cat=pd.read_csv(odir+'/../OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
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
# HyLakeId = [data[lake] for lake in order]
HyLakeId = final_cat['HyLakeId'].dropna().astype(int).unique()
# HyLakeId = final_cat[final_cat['Obs_WA_SY1']==1]['HyLakeId'].dropna().astype(int).unique()
print (HyLakeId)
#========================================
# llake=["./obs/WL_IS_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in HyLakeId]
llake=["./obs/WL_SY_%d_%d.rvt"%(lake,final_cat[final_cat['HyLakeId']==lake]['SubId']) for lake in HyLakeId]
print (llake)
#========================================
# lexp=["E0a","E0b","S1c","S1d","S1e"]
# lexp=["E0a","E0b"]#,"S1d","S1f"]
lexp=["V1a","V1b","V1c","V1d"]#,"S1d","S1f"]
expriment_name=[]
#========================================================================================
mk_dir("../figures/paper")
ens_num=10
metric=[]
for expname in lexp:
    objFunction0=1.0
    for num in range(1,ens_num+1):
        print (expname, num)
        # metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
        # print (list(read_diagnostics(expname, num).flatten()).append(read_costFunction(expname, num))) #np.shape(read_diagnostics(expname, num)), 
        row=list(read_diagnostics(expname, num, odir=odir).flatten())
        row.extend(list(read_lake_diagnostics(expname, num, llake, odir=odir, best_dir='best_Raven')))
        row.append(read_costFunction(expname, num, div=1.0, odir=odir))
        # print (row)
        print (len(row))
        expriment_name.append("Exp"+expname)
        metric.append([row])
metric=np.array(metric)[:,0,:]
print (np.shape(metric))
#========================================================================================
# columns=['02KB001','LM','NarrowbagR','Crow','NC']
# columns.extend(order)
columns=['02KB001','Little Madawaska Barometer','Petawawa River at Narrowbag','Crow River','Nipissing River']
columns.extend(HyLakeId)
print (columns)
columns.append('obj.function') #['02KB001','LM','Narrowbag','Crow','NC','obj.function']
df=pd.DataFrame(metric, columns=columns)
df['Experiment']=np.array(expriment_name)
print ('='*20+' df '+'='*20)
print (df.head(10))
#==============
# need to replace the column name to match final_cat Obs_NM
# Correct the renaming dictionary
rename_dict = {
    '02KB001': '02KB001',
    'LM': 'Little Madawaska Barometer',
    'NarrowbagR': 'Petawawa River at Narrowbag',
    'Crow': 'Crow River',
    'NC': 'Nipissing River',
    'Animoosh': 'Animoosh',
    'Big_Trout': 'Big Trout',
    'Burntroot': 'Burntroot',
    'Cedar': 'Cedar',
    'Charles': 'Charles',
    'Grand': 'Grand',
    'Hambone': 'Hambone',
    'Hogan': 'Hogan',
    'La_Muir': 'La Muir',
    'Lilypond': 'Lilypond',
    'Little_Cauchon': 'Little Cauchon',
    'Loontail': 'Loontail',
    'Misty': 'Misty',
    'North_Depot': 'North Depot',
    'Radiant': 'Radiant',
    'Timberwolf': 'Timberwolf',
    'Traverse': 'Traverse',
    'Lavieille': 'Lavieille',
    'obj.function': 'obj.function',
    'Experiment': 'Experiment'
}

# # Rename the columns in the DataFrame
# df.rename(columns=rename_dict, inplace=True)

# Verify the column names have been updated
print(df.columns)
#========================================================================================
# Figure
#========================================
# path_to_product_folder='../OstrichRaven/RavenInput/geojsons/'
path_to_product_folder=odir+'/../extraction'
# Adjusting the collist to match the renamed columns
# collist = [
#     '02KB001', 'Little Madawaska Barometer', 'Petawawa River at Narrowbag', 'Crow River',
#     'Nipissing River', 'Animoosh', 'Big Trout', 'Burntroot', 'Cedar',
#     'Charles', 'Grand', 'Hambone', 'Hogan', 'La Muir', 'Lilypond',
#     'Little Cauchon', 'Loontail', 'Misty', 'Narrowbag', 'North Depot',
#     'Radiant', 'Timberwolf', 'Traverse', 'Lavieille'
# ]
collist = [
    '02KB001', 'Little Madawaska Barometer', 'Petawawa River at Narrowbag', 'Crow River',
    'Nipissing River']
collist.extend(HyLakeId)
# Plotting
fig, axes = plt.subplots(figsize=(16, 8), nrows=2, ncols=2)
i = 0
# Expnames=['Exp 1', 'Exp 2', 'Exp 3']
Expnames=lexp
for name, group in df.groupby('Experiment'):
    df_metric = pd.DataFrame()
    df_metric['Metric'] = group.loc[group['obj.function'].idxmax(), collist].values
    df_metric['Obs_NM'] = collist
    # print (i, i // 2, i % 2)
    ax = axes[i // 2, i % 2]
    print ('='*20)
    print (name)
    # print (final_cat.columns) #loc[final_cat['Obs_NM'].dropna().unique(),])
    # df_diag=df_metric#read_Diagnostics(experiment)
    # print (df_diag)
    # Filter the DataFrame for rows where 'Obs_NM' is in collist
    filtered_df = final_cat[final_cat['Obs_NM'].isin(collist) | final_cat['HyLakeId'].isin(collist)]

    # add HylakId into Obs_NM
    filtered_df.loc[final_cat['HyLakeId'].isin(collist),'Obs_NM']=HyLakeId

    # Sort the DataFrame by 'DrainArea' in descending order and then drop duplicates by 'Obs_NM'
    filtered_df = filtered_df.sort_values(by='DrainArea', ascending=False).drop_duplicates(subset='Obs_NM')

    # Select the required columns
    points_df = filtered_df[['Obs_NM', 'HRU_CenY', 'HRU_CenX']]

    # points_df=final_cat.loc[['Obs_NM','HRU_CenY','HRU_CenX']]
    points_df.rename(columns={'HRU_CenY':'outletLat','HRU_CenX':'outletLng'}, inplace=True)
    # print (points_df)
    points_df=pd.merge(points_df,df_metric,on='Obs_NM',how='inner')

    # Add a column for marker type
    points_df['Marker'] = 'o'  # Default to circle

    # Add a column for marker size
    points_df['Size'] = 10  # Default to 30

    # Define marker types
    marker_types = {
        '02KB001': 'd',
        'Petawawa River at Narrowbag': 's',
        'Nipissing River': 's',
        'Little Madawaska Barometer': 's',
        'Crow River': 's'}
    
    # Update the marker type column based on conditions
    points_df.loc[points_df['Obs_NM'].isin(marker_types.keys()), 'Marker'] = points_df['Obs_NM'].map(marker_types)
    points_df.loc[points_df['Obs_NM'].isin(marker_types.keys()), 'Size']   = 100
    points_df.loc[points_df['Obs_NM'].isin(['02KB001']), 'Size']           = 120

    # Update marker for calibration gauges
    points_df.loc[points_df['Obs_NM'].isin(final_cat[final_cat['Obs_WA_SY1']==1]['HyLakeId'].dropna().astype(int).unique()), 'Marker'] = '^'
    points_df.loc[points_df['Obs_NM'].isin(final_cat[final_cat['Obs_WA_SY1']==1]['HyLakeId'].dropna().astype(int).unique()), 'Size']   = 100

    # print (points_df)
    im=plot_routing_product(points_df, path_to_product_folder, collist, 
                         version_number='v1-0', metric='DIAG_KLING_GUPTA', 
                         title=Expnames[i], clabel='KGE', ax=ax)
    i += 1

clabel='$KGE$/$KGED$'
left, bottom, width, height = axes[-1,-1].get_position().bounds
# cax = fig.add_axes([left, bottom+height, width, 0.02])
cax = fig.add_axes([0.05, 0.05, 0.9, 0.01])

cbar=plt.colorbar(im,orientation='horizontal',shrink=0.8, extend='min',
cax=cax,label=clabel)  # Add colorbar with label
# cbar=plt.colorbar(im,orientation='vertical',shrink=0.8, extend='min',
# cax=cax,label=clabel)
cbar.set_label(clabel)

for row in axes:
    for ax in row:
        ax.set_axis_off()
# axes[-1,-1].set_axis_off()

plt.tight_layout()
plt.savefig('../figures/paper/fs5-map_metric_' + datetime.datetime.now().strftime("%Y%m%d") + '.jpg',dpi=500)