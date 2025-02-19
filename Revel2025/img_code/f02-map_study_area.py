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
from shapely.geometry import Point
from adjustText import adjust_text
#====================================================================================
product_folder1 = '/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction'
version_number1 = '_v1-0'
product_folder = '/project/def-btolson/menaka/LakeCalibration/GIS_files/Petawawa/withlake'
version_number = ''
#====================================================================================
# read final cat 
final_cat=pd.read_csv('../../OstrichRaven/finalcat_hru_info_updated.csv')
#====================================================================================
if version_number != '':
    version_number = '_' + version_number
path_subbasin = os.path.join(product_folder, 'finalcat_info' + version_number + '.geojson')
path_river = os.path.join(product_folder, 'finalcat_info_riv' + version_number + '.geojson')
path_cllake = os.path.join(product_folder1, 'sl_connected_lake' + version_number1 + '.geojson')
path_ncllake = os.path.join(product_folder1, 'sl_non_connected_lake' + version_number1 + '.geojson')
path_outline = os.path.join('/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction', 'outline.geojson')
path_province = os.path.join('/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction', 'Ontario.shp')

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

# print (subbasin.columns)

# print (subbasin['Obs_NM'].dropna())

# forcing
forcing='/home/menaka/projects/def-btolson/menaka/LakeCalibration/GIS_files/Petawawa/forcing.shp'
forcing_df = gpd.read_file(forcing)
forcing_df = forcing_df.to_crs("EPSG:4326")
# New row data -- > PETAWAWA HOFFMAN 
# New row as a GeoDataFrame
new_row = gpd.GeoDataFrame(pd.DataFrame({
    "Name": ["Petawawa"],
    "Latitude": [45.8558],  # Convert DMS to decimal degrees
    "Longitude": [-78.434],
    "geometry": [Point(-78.434, 45.8558)]
}), crs="EPSG:4326")

# Use concat instead of append
forcing_df = pd.concat([forcing_df, new_row], ignore_index=True)

#
forcing_df['Obs_NM'] = [
    'Achary',
    'Petawawa-Hoffman',
    'Tim',
    'Hogan'
]
# print (forcing_df)

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
    ['SubId', 'geometry']
]

q_df = subbasin.loc[
    subbasin['Obs_NM'] == '02KB001',
    ['SubId', 'Obs_NM', 'geometry']
]

gaguge_df = subbasin.loc[
    subbasin['Obs_NM'].isin([
        'Nipissing River',
        'Petawawa River at Narrowbag',
        'Little Madawaska Barometer'
        ]),
    ['SubId', 'Obs_NM', 'geometry']
]

# observation river - Load study area shapefile
path_obs_gau = os.path.join(product_folder, 'obs_gauges_river' + '.shp')
obs_gau = gpd.read_file(path_obs_gau)
obs_gau = obs_gau.to_crs("EPSG:4326")
# print (obs_gau['Site_name'].dropna())

# observation all - Load study area shapefile
path_obs_gau0 = os.path.join(product_folder, 'obs_gauges' + '.shp')
obs_gau0 = gpd.read_file(path_obs_gau0)
obs_gau0 = obs_gau0.to_crs("EPSG:4326")
# print (obs_gau0['Site_name'].dropna())

# observation lake level - Load study area shapefile
path_obs_lake = os.path.join(product_folder, 'lake_level_gauge_final' + '.shp')
obs_lake = gpd.read_file(path_obs_lake)
obs_lake = obs_lake.to_crs("EPSG:4326")
# print (obs_lake['Site_name'].dropna())
# Create main plot with cartopy for Canada
# fig, (ax_main, ax_inset) = plt.subplots(1, 2, figsize=(16, 10),
#  subplot_kw={'projection': ccrs.PlateCarree()})
# ax_main.set_extent([-140, -50, 40, 70], crs=ccrs.PlateCarree())  # Canada extents

# figure
va_margin= 0.0#1.38#inch 
ho_margin= 0.0#1.18#inch
hgt=(11.69 - 2*va_margin)*(1.0/3.0)
wdt=(8.27 - 2*ho_margin)*(2.0/2.0)

# Create figure and GridSpec layout
fig = plt.figure(figsize=(wdt, hgt)) #, tight_layout=True)
gs = GridSpec(ncols=2, nrows=2, figure=fig, width_ratios=[4, 1])

# Plot Canada and add study area inset
# ax_main = fig.add_subplot(gs[1, 1], projection=ccrs.PlateCarree())
# ax_main.set_extent([-142.0, -52.0, 48.0, 90.0], crs=ccrs.PlateCarree())  # Extent for Canada

ax_main = fig.add_subplot(gs[0, 1], projection=ccrs.AlbersEqualArea(central_lon, central_lat))
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
ax_main.add_feature(ocean, linewidth=0.1 )
ax_main.add_feature(lakes, zorder=5)
ax_main.add_feature(rivers, linewidth=0.5, zorder=6)

ax_main.add_feature(country_bodr, linestyle='--', linewidth=0.1, edgecolor="k", zorder=10)  #USA/Canada
ax_main.add_feature(provinc_bodr, linestyle='--', linewidth=0.1, edgecolor="k", zorder=10)


# ax_main.add_feature(cartopy.feature.OCEAN, color='lightblue')

# ax_main.gridlines(draw_labels=True, lw=0.2, edgecolor="darkblue", zorder=12)


if os.path.exists(path_outline):
    outline = gpd.read_file(path_outline).to_crs("EPSG:4326")
    outline.plot(ax=ax_main, facecolor="none", edgecolor='r', 
    linewidth=1, alpha=0.8, zorder=110, 
    transform=ccrs.PlateCarree())

# if os.path.exists(path_province):
#     province = gpd.read_file(path_province).to_crs("EPSG:4326")
#     province.plot(ax=ax_main, facecolor="none", edgecolor='k', linewidth=1, alpha=0.8)

# print (q_df['outletLng'].values[0], q_df['outletLat'].values[0])
# ax_main.plot(q_df['outletLng'].values[0], q_df['outletLat'].values[0], 
#               linewidth=0, marker='*', markersize=20, color='r', 
#               markeredgecolor='k', zorder=110, 
#               transform=ccrs.PlateCarree())

obs_gau0[obs_gau0['Site_name']=='02KB001'].plot(
    ax=ax_main,
    linewidth=0, marker='o', markersize=200, color='r', 
    # markeredgecolor='k', zorder=110, 
    transform=ccrs.PlateCarree())


# ax_main.set_extent([-142.0, -52.0, 48.0, 90.0], crs=ccrs.LambertAzimuthalEqualArea())

ax_main.set_title("b) Canada", fontsize=10, loc='left')


#============================
# # Inset for the study area
ax_inset = fig.add_subplot(gs[:, 0], projection=ccrs.PlateCarree())

# # Plot study area features
# subbasin.plot(ax=ax_inset, color='#418e41', edgecolor='grey', linewidth=0.5, alpha=0.5)

# print (subbasin.columns)

# Plot rivers, lakes, outlines if files exist
if os.path.exists(path_river):
    river = gpd.read_file(path_river).to_crs("EPSG:4326")
    river.plot(ax=ax_inset, color='#0070FF', linewidth=1, alpha=1.0, zorder=101)

if os.path.exists(path_cllake):
    # print (path_cllake)
    cllake = gpd.read_file(path_cllake).to_crs("EPSG:4326")
    cllake.plot(ax=ax_inset, color='#0070FF', edgecolor='#0070FF', linewidth=0.5, alpha=1.0, zorder=102)

if os.path.exists(path_ncllake):
    ncllake = gpd.read_file(path_ncllake).to_crs("EPSG:4326")
    ncllake.plot(ax=ax_inset, color='#0070FF', edgecolor='#0070FF', linewidth=0.5, alpha=0.8, zorder=103)

if os.path.exists(path_outline):
    outline = gpd.read_file(path_outline).to_crs("EPSG:4326")
    outline.plot(ax=ax_inset, facecolor="#418e41", edgecolor='k', linewidth=1, alpha=0.8, zorder=90)

# ax_inset.plot(points_df['outletLng'], points_df['outletLat'], 
#               linewidth=0, marker='d', markersize=10, color='r', 
#               markeredgecolor='k', zorder=110)

# ax_inset.plot(q_df['outletLng'], q_df['outletLat'], 
#               linewidth=0, marker='^', markersize=10, color='r', 
#               markeredgecolor='k', zorder=110)

plot_obs=[
    'Little Madawaska Barometer',
    'Nipissing River',
    '02KB001',
    'Petawawa River at Narrowbag',
    'Crow River',
    'Big Trout'
]
# obs_gau0[obs_gau0['Site_name'].isin(plot_obs)].plot(
#     ax=ax_inset,
#     linewidth=0, marker='^', markersize=80, color='#d95f03', 
#     # markeredgecolor='k', zorder=110, 
#     transform=ccrs.PlateCarree(),
#     zorder=110
#     )
# # Add annotations
# print ("obs_gau0")
# for x, y, label in zip(obs_gau0[obs_gau0['Site_name'].isin(plot_obs)].geometry.x, obs_gau0[obs_gau0['Site_name'].isin(plot_obs)].geometry.y, obs_gau0[obs_gau0['Site_name'].isin(plot_obs)]["Site_name"]):
#     print (x, y, label)
#     ax_inset.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=10, color='blue', zorder=110)
texts=[]
for label,marker,color in zip(['02KB001','Nipissing River', 'Big Trout'],['^','^','d'],['#d95f03','#d95f03','#c6b0d5']):
    # print (label,marker,color)
    # Filter for the specific site
    site_data = obs_gau0[obs_gau0['Site_name'] == label]
    
    if site_data.empty:
        print(f"Warning: No data found for {label}")
        continue  # Skip to the next iteration if no data is found
    
    # Plot the marker
    site_data.plot(
        ax=ax_inset,
        linewidth=0, marker=marker, markersize=80, color=color, 
        transform=ccrs.PlateCarree(),
        zorder=110
    )
    
    # Extract the first point's coordinates for annotation
    x, y = site_data.geometry.iloc[0].x, site_data.geometry.iloc[0].y
    
    # Add annotation
    texts.append(
        ax_inset.text(x, y,
        label, 
        # xytext=(0, 0), textcoords="offset points", 
        fontsize=8, color='blue', zorder=110
        )
    )


# # obs_gau.plot(
# #     ax=ax_inset,
# #     linewidth=0, marker='d', markersize=80, color='#ffb103', 
# #     # markeredgecolor='k', zorder=110, 
# #     transform=ccrs.PlateCarree(), 
# #     zorder=110
# #     )
# # # Add annotations
# # print ("obs_gau")
# # for x, y, label in zip(obs_gau.geometry.x, obs_gau.geometry.y, obs_gau["Site_name"]):
# #     print (x, y, label)
# #     ax_inset.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=10, color='blue', zorder=110)

# print (obs_lake)
# obs_lake.plot(
#     ax=ax_inset,
#     linewidth=0, marker='D', markersize=50, color='#c6b0d5', 
#     # markeredgecolor='k', zorder=110, 
#     transform=ccrs.PlateCarree(),
#     zorder=110
#     )
# # Add annotations
# for x, y, label in zip(obs_lake.geometry.x, obs_lake.geometry.y, obs_lake["Site_name"]):
#     ax_inset.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=10, color='blue', zorder=110)


forcing_df.plot(
    ax=ax_inset,
    linewidth=0, marker='s', markersize=50, color='#ff9896', 
    # markeredgecolor='k', zorder=110, 
    transform=ccrs.PlateCarree(),
    zorder=110
    )
# Add annotations
for x, y, label in zip(forcing_df.geometry.x, forcing_df.geometry.y, forcing_df["Obs_NM"]):
    # print (x, y, label) 
    texts.append(
        ax_inset.text(x, y, label,
        # xytext=(0, 0), textcoords="offset points", 
        fontsize=8, color='k', zorder=110)
    )


# Title and formatting
ax_inset.set_title("a) Petawawa Watershed", fontsize=10,  loc='left')

# Adjust text to reduce overlap
adjust_text(
    texts,
    ax=ax_inset,
    arrowprops=dict(arrowstyle="-", color='grey')
    # only_move={'points': 'y', 'text': 'xy'},  # Allow labels to move along y-axis and text to move freely
    # arrowprops=dictk(arrowstyle="->", color='gray', lw=0.5)  # Optional: Add arrows pointing to points
)

# Set tick labels to latitude and longitude format
ax_inset.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:.2f}'.format(x)))
ax_inset.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:.2f}'.format(y)))

ax_inset.set_axis_off()


# Get the position of the inset axis
left1, bottom1, width1, height1 = ax_inset.get_position().bounds

# Create a new axes for the legend (adjust positioning as needed)
ax_legend = fig.add_axes([left1 + 0.20, bottom1, width1 * 0.5, height1 * 0.1])
ax_legend.set_axis_off()  # Hide the new axes since it's only for the legend


# Create a custom legend
legend_elements = [
    mpatches.Patch(color='#0070FF', label='Lake'),
    plt.Line2D([0], [0], color='#0070FF', lw=1, label='River'),
    plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='#d95f03', markeredgecolor='#d95f03', markersize=10, label='River Gauge'),
    plt.Line2D([0], [0], marker='d', color='w', markerfacecolor='#c6b0d5', markeredgecolor='#c6b0d5', markersize=10, label='Lake Outlet'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#ff9896', markeredgecolor='#ff9896', markersize=10, label='Input Forcing'),
    # plt.Line2D([0], [0], color='#0070FF', lw=0.5, label='Connected Lake'),
    # plt.Line2D([0], [0], color='k', lw=1, label='Outline')
    ]

# Add legend to the dedicated legend axes
ax_legend.legend(handles=legend_elements, loc='center', ncol=3, fontsize=8, frameon=False)


# fig.add_wspace()

# plt.tight_layout()

plt.savefig('../figures/f02-map_study_area_' + datetime.datetime.now().strftime("%Y%m%d") + '.jpg',
dpi=500, bbox_inches='tight')
print (path_cllake)