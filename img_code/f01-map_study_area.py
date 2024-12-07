import warnings
warnings.filterwarnings("ignore")
import numpy as np
import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.gridspec import GridSpec
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import cartopy
import datetime
#====================================================================================
product_folder = '/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction'
version_number = 'v1-0'
#====================================================================================
# read final cat 
final_cat=pd.read_csv('../OstrichRaven/finalcat_hru_info_updated.csv')
#====================================================================================
if version_number != '':
    version_number = '_' + version_number
path_subbasin = os.path.join(product_folder, 'finalcat_info' + version_number + '.geojson')
path_river = os.path.join(product_folder, 'finalcat_info_riv' + version_number + '.geojson')
path_cllake = os.path.join(product_folder, 'sl_connected_lake' + version_number + '.geojson')
path_ncllake = os.path.join(product_folder, 'sl_non_connected_lake' + version_number + '.geojson')
path_outline = os.path.join(product_folder, 'outline.geojson')
path_province = os.path.join(product_folder, 'Ontario.shp')

# Paths to shapefiles
# path_study_area = "path/to/study_area_shapefile.shp"
# path_river = "path/to/river_shapefile.shp"
# path_cllake = "path/to/cllake_shapefile.shp"
# path_ncllake = "path/to/ncllake_shapefile.shp"
# path_outline = "path/to/outline_shapefile.shp"

# Load study area shapefile
study_area = gpd.read_file(path_subbasin)
study_area = study_area.to_crs("EPSG:4326")

subbasin = study_area  # Assuming study_area is the subbasin shapefile

extent = [-130, -55, 36.5, 75]
central_lon = np.mean(extent[:2])
central_lat = np.mean(extent[2:])

# Plot points of interest
Lakes= [
    1034779, 8781, 108379, 8741, 1033439, 108347, 1035812, 8762, 108369, 
    1036038, 108015, 108404, 108564, 1032844, 108027, 108126, 108585, 
    108083, 8767
]
# points_df = subbasin.loc[
#     (subbasin['Lake_Cat'] == 1) & (subbasin['HyLakeId'].isin(Lakes)),
#     ['outletLat', 'outletLng']
# ]

points_df = subbasin.loc[
    subbasin['Lake_Cat'] == 1,
    ['outletLat', 'outletLng']
]

q_df = subbasin.loc[
    subbasin['Obs_NM'] == '02KB001',
    ['outletLat', 'outletLng']
]

# Create main plot with cartopy for Canada
# fig, (ax_main, ax_inset) = plt.subplots(1, 2, figsize=(16, 10),
#  subplot_kw={'projection': ccrs.PlateCarree()})
# ax_main.set_extent([-140, -50, 40, 70], crs=ccrs.PlateCarree())  # Canada extents

# Create figure and GridSpec layout
fig = plt.figure(figsize=(16, 12), tight_layout=True)
gs = GridSpec(ncols=4, nrows=2, figure=fig, height_ratios=[2, 1])

# Plot Canada and add study area inset
# ax_main = fig.add_subplot(gs[1, 1], projection=ccrs.PlateCarree())
# ax_main.set_extent([-142.0, -52.0, 48.0, 90.0], crs=ccrs.PlateCarree())  # Extent for Canada

ax_main = fig.add_subplot(gs[1, 0], projection=ccrs.AlbersEqualArea(central_lon, central_lat))
ax_main.set_extent(extent)#, crs=ccrs.AlbersEqualArea(central_lon, central_lat))

# ax_main.set_extent([-95.16, -74.34, 41.66, 56.86], crs=ccrs.PlateCarree())  # Extent for Ontario
# ax_main.coastlines()
# ax_main.add_feature(cartopy.feature.BORDERS, linestyle=':')
# ax_main.add_feature(cartopy.feature.LAND, color='w')


# data resolution
resol = '50m'

# country boundaries
country_bodr = cartopy.feature.NaturalEarthFeature(category='cultural', 
    name='admin_0_boundary_lines_land', scale=resol, facecolor='none', edgecolor='k')

# province boundaries
provinc_bodr = cartopy.feature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale=resol, facecolor='none', edgecolor='k')

# land areas
land = cartopy.feature.NaturalEarthFeature('physical', 'land', \
    scale=resol, edgecolor='k', facecolor=cfeature.COLORS['land'])

# Ocean/seas
ocean = cartopy.feature.NaturalEarthFeature('physical', 'ocean', \
    scale=resol, edgecolor='none', facecolor=cfeature.COLORS['water'])

# Lakes
lakes = cartopy.feature.NaturalEarthFeature('physical', 'lakes', \
    scale=resol, edgecolor='b', facecolor=cfeature.COLORS['water'])

# Rivers
rivers = cartopy.feature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', \
    scale=resol, edgecolor='b', facecolor='none')

# Add all features to the map 
ax_main.add_feature(land, facecolor='w', zorder=4)
ax_main.add_feature(ocean, linewidth=0.2 )
ax_main.add_feature(lakes, zorder=5)
ax_main.add_feature(rivers, linewidth=0.5, zorder=6)

ax_main.add_feature(country_bodr, linestyle='--', linewidth=0.8, edgecolor="k", zorder=10)  #USA/Canada
ax_main.add_feature(provinc_bodr, linestyle='--', linewidth=0.6, edgecolor="k", zorder=10)


# ax_main.add_feature(cartopy.feature.OCEAN, color='lightblue')

ax_main.gridlines(draw_labels=True, lw=0.2, edgecolor="darkblue", zorder=12)


if os.path.exists(path_outline):
    outline = gpd.read_file(path_outline).to_crs("EPSG:4326")
    outline.plot(ax=ax_main, facecolor="none", edgecolor='r', 
    linewidth=1, alpha=0.8, zorder=110, 
    transform=ccrs.PlateCarree())

# if os.path.exists(path_province):
#     province = gpd.read_file(path_province).to_crs("EPSG:4326")
#     province.plot(ax=ax_main, facecolor="none", edgecolor='k', linewidth=1, alpha=0.8)

print (q_df['outletLng'].values[0], q_df['outletLat'].values[0])
ax_main.plot(q_df['outletLng'].values[0], q_df['outletLat'].values[0], 
              linewidth=0, marker='*', markersize=20, color='r', 
              markeredgecolor='k', zorder=110, 
              transform=ccrs.PlateCarree())

# ax_main.set_extent([-142.0, -52.0, 48.0, 90.0], crs=ccrs.LambertAzimuthalEqualArea())

ax_main.set_title("Canada", fontsize=20)

# # Inset for the study area
ax_inset = fig.add_subplot(gs[0, :], projection=ccrs.PlateCarree())

# Plot study area features
subbasin.plot(ax=ax_inset, color='#418e41', edgecolor='grey', linewidth=0.5, alpha=0.5)

# print (subbasin.columns)

# Plot rivers, lakes, outlines if files exist
if os.path.exists(path_river):
    river = gpd.read_file(path_river).to_crs("EPSG:4326")
    river.plot(ax=ax_inset, color='#0070FF', linewidth=1, alpha=1.0)

if os.path.exists(path_cllake):
    cllake = gpd.read_file(path_cllake).to_crs("EPSG:4326")
    cllake.plot(ax=ax_inset, color='#0070FF', edgecolor='#0070FF', linewidth=0.5, alpha=1.0)

if os.path.exists(path_ncllake):
    ncllake = gpd.read_file(path_ncllake).to_crs("EPSG:4326")
    ncllake.plot(ax=ax_inset, color='#0070FF', edgecolor='#0070FF', linewidth=0.5, alpha=0.8)

if os.path.exists(path_outline):
    outline = gpd.read_file(path_outline).to_crs("EPSG:4326")
    outline.plot(ax=ax_inset, facecolor="none", edgecolor='k', linewidth=1, alpha=0.8)

# ax_inset.plot(points_df['outletLng'], points_df['outletLat'], 
#               linewidth=0, marker='d', markersize=10, color='r', 
#               markeredgecolor='k', zorder=110)

ax_inset.plot(q_df['outletLng'], q_df['outletLat'], 
              linewidth=0, marker='^', markersize=10, color='r', 
              markeredgecolor='k', zorder=110)

# Title and formatting
ax_inset.set_title("Petawawa Watershed", fontsize=30)


# Set tick labels to latitude and longitude format
ax_inset.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.2f}'.format(x)))
ax_inset.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:.2f}'.format(y)))

ax_inset.set_axis_off()

# Legend (lower left quarter)
ax_legend = fig.add_subplot(gs[1, -1])
ax_legend.axis("off")  # Turn off axis for legend

# Create a custom legend
legend_elements = [
    mpatches.Patch(color='#0070FF', label='Lake'),
    plt.Line2D([0], [0], color='#0070FF', lw=1, label='River'),
    plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='r', markeredgecolor='k', markersize=10, label='Watershed Outlet'),
    # plt.Line2D([0], [0], marker='d', color='w', markerfacecolor='r', markeredgecolor='k', markersize=10, label='Observed POI'),
    # plt.Line2D([0], [0], color='#0070FF', lw=0.5, label='Connected Lake'),
    # plt.Line2D([0], [0], color='k', lw=1, label='Outline')
    ]

# Display legend
ax_legend.legend(handles=legend_elements, loc='center', fontsize=20)


# fig.add_wspace()

plt.tight_layout()

plt.savefig('../figures/paper/f01-map_study_area_' + datetime.datetime.now().strftime("%Y%m%d") + '.jpg',
dpi=500, bbox_inches='tight')