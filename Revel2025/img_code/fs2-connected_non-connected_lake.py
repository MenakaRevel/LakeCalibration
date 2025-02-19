#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore")
import numpy as np
import os
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap, BoundaryNorm, Normalize
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import cartopy
import datetime
import colormaps as cmaps
import seaborn as sns
from sklearn.linear_model import LinearRegression


mpl.use('Agg')

from exp_params import *
#========================================================================================
product_folder = '/project/def-btolson/menaka/LakeCalibration/GIS_files/Petawawa/withlake'
version_number = ''
#========================================================================================
# read non-connected lake
path_cllake = os.path.join(product_folder, 'sl_connected_lake' + version_number + '.shp')    
cllake = geopandas.read_file(path_cllake)
print (cllake.columns)
cllake = cllake.loc[:,['Hylak_id','Lake_area']]
cllake['Type'] = ['connected']*len(cllake)
#========================================================================================
# read connected lake
path_ncllake = os.path.join(product_folder, 'sl_non_connected_lake' + version_number + '.shp')
ncllake = geopandas.read_file(path_ncllake)
ncllake = ncllake.loc[:,['Hylak_id','Lake_area']]
ncllake['Type'] = ['non-connected']*len(ncllake)
#========================================================================================
# combine dataframes
lake=pd.concat([cllake,ncllake],axis=0,ignore_index=True)

print (lake)

#========================================================================================
# figure
va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=(11.69 - 2*va_margin)*(1.0/3.0)
wdt=(8.27 - 2*ho_margin)*(1.0/2.0)

fig = plt.figure(figsize=(wdt, hgt)) #, tight_layout=True)
gs = GridSpec(ncols=1, nrows=1, figure=fig)#, height_ratios=[1.5, 1])
ax1 = fig.add_subplot(gs[0, 0])
# # histogram
# sns.histplot(
#     data=lake,
#     x="Lake_area",
#     stat='count', 
#     bins='auto',
#     hue='Type',
#     cumulative=False, 
#     common_norm=True, 
#     kde=True,
#     # common_grid=True,
#     ax=ax1
#     )

sns.kdeplot(
    data=lake,
    x="Lake_area",
    hue="Type",
    common_norm=True,
    cumulative=False,
    ax=ax1
)

ax1.axvline(x=1.0,linestyle='--',color='k')
ax1.set_xlim(0.0,10.0)

plt.tight_layout()

print ('../figures/fs2-conn_non-conn_'+ datetime.datetime.now().strftime("%Y%m%d") +'.jpg')
plt.savefig('../figures/fs2-conn_non-conn_'+ datetime.datetime.now().strftime("%Y%m%d") +'.jpg', dpi=500) #_summer