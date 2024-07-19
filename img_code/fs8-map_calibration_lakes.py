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
#========================================
def plot_routing_product(colname, final_cat, path_to_product_folder, version_number='', title='map',ax=None):
    if ax is None:
        ax = plt.gca()
    product_folder = path_to_product_folder
    if version_number != '':
        version_number = '_' + version_number
    path_subbasin = os.path.join(product_folder, 'finalcat_info' + version_number + '.geojson')
    path_river = os.path.join(product_folder, 'finalcat_info_riv' + version_number + '.geojson')
    path_cllake = os.path.join(product_folder, 'sl_connected_lake' + version_number + '.geojson')
    path_ncllake = os.path.join(product_folder, 'sl_non_connected_lake' + version_number + '.geojson')
    path_outline = os.path.join(product_folder, 'outline.geojson')

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

    points_df=final_cat.loc[
        (final_cat['HRU_IsLake'] == 1) & (final_cat[colname] == 1),
        ['outletLat', 'outletLng']
        ]

    q_df=final_cat.loc[
        (final_cat['Obs_NM'] == '02KB001') & (final_cat['HRU_IsLake'] != 1),
        ['outletLat', 'outletLng']
        ]

    # POI
    ax.plot(points_df['outletLng'], points_df['outletLat'], linewidth=0, linestyle=None,
     marker='o', markersize=10, color='r', markeredgecolor='k',zorder=110)

    ax.plot(q_df['outletLng'], q_df['outletLat'], linewidth=0, linestyle=None,
     marker='d', markersize=10, color='r', markeredgecolor='k', zorder=110)
    
    ax.set_title(title, fontsize=20)

    # Setting tick labels as conventional latitude and longitude
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.2f}'.format(x)))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:.2f}'.format(y)))

    return 


#=====================================================
# read final cat 
final_cat=pd.read_csv('../OstrichRaven/finalcat_hru_info_updated.csv')

path_to_product_folder='../OstrichRaven/RavenInput/extraction/'

lexp=["E0a","E0b","S1d","S1f"]
colname={
    "E0a":"Obs_SF_IS",
    "E0b":"Obs_WL_IS",
    "S1d":"Obs_WA_RS3",
    "S1f":"Obs_WA_RS4"
}
#=====================================================
# Plotting
fig, axes = plt.subplots(figsize=(16, 8), nrows=2, ncols=2)
i=0
for exp in lexp:
    print (i, i // 2, i % 2)
    ax = axes[i // 2, i % 2]
    print (final_cat.columns) #loc[final_cat['Obs_NM'].dropna().unique(),])
    # df_diag=df_metric#read_Diagnostics(experiment)
    # print (df_diag)
    # Filter the DataFrame for rows where 'Obs_NM' is in collist
    # filtered_df = final_cat.loc[
    #     (final_cat['HRU_IsLake'] == 1) & (final_cat[colname[exp]] == 1),
    #     ['HRU_CenY', 'HRU_CenX']
    # ]

    final_cat.rename(columns={'HRU_CenY':'outletLat','HRU_CenX':'outletLng'}, inplace=True)

    plot_routing_product(colname[exp], final_cat, path_to_product_folder, 
                         version_number='v1-0',  title='Exp'+exp, ax=ax)
    i += 1

for row in axes:
    for ax in row:
        ax.set_axis_off()
# axes[-1,-1].set_axis_off()

plt.tight_layout()
plt.savefig('../figures/paper/fs8-map_cal_points_' + datetime.datetime.now().strftime("%Y%m%d") + '.jpg',dpi=500)