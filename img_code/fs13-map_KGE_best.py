import warnings
warnings.filterwarnings("ignore")
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.cm as cm
import datetime

expname = 'V0a'
# Load the shapefile
shapefile_path = '/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction/finalcat_info_riv_v1-0.shp'
gdf = gpd.read_file(shapefile_path)

# Get unique SubId values
unique_subids = gdf['SubId'].unique()

# Create a colormap with the same number of colors as unique SubIds
num_colors = len(unique_subids)
cmap = plt.get_cmap('tab20', num_colors)  # 'tab20' provides discrete colors

# Map SubId to colors
color_map = {subid: cmap(i) for i, subid in enumerate(unique_subids)}
gdf['color'] = gdf['SubId'].map(color_map)

# Plot the polygons with assigned colors
fig, ax = plt.subplots(figsize=(10, 8))
gdf = gdf.to_crs("EPSG:4326")
gdf.plot(ax=ax, color=gdf['color'], edgecolor='black',zorder=110)

# path_subbasin='/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction/finalcat_info_v1-0.shp'
# subbasin = gpd.read_file(path_subbasin)
# subbasin = subbasin.to_crs("EPSG:4326")
# subbasin.plot(ax=ax, color='none', edgecolor='k', linewidth=0.5, alpha=0.5, zorder=90)

path_outline='/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction/outline.shp'
outline = gpd.read_file(path_outline)
outline = outline.to_crs("EPSG:4326")
outline.plot(ax=ax, color='none', edgecolor='k', linewidth=0.5, alpha=0.5, zorder=90)

# Optional: Add a title and remove axis
ax.set_title('Polygons Colored by SubId', fontsize=16)
ax.axis('off')

plt.tight_layout()
print ('../figures/paper/fs13-map_KGE_'+expname+'_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.savefig('../figures/paper/fs13-map_KGE_'+expname+'_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')