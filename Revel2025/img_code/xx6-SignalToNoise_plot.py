import numpy as np
import pandas as pd
import geopandas as gpd
import sys
import os
import geopandas
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap, BoundaryNorm, Normalize
import matplotlib.colors as mcolors
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import cartopy
import datetime
import colormaps as cmaps
import seaborn as sns
from sklearn.linear_model import LinearRegression
mpl.use('Agg')

from exp_params import *
#===============================================================================================
#=================================
def IS_gauges(Has_Gauge, Obs_NM, gagues):
  if Has_Gauge == 1:
    if str(Obs_NM) in gagues:
      return 1
  else:
    return 0
#=================================
def RS_gauges(HyLakeId, gagues):
  if HyLakeId in gagues:
    return 1
  else:
    return 0
#=================================
#===============================================================================================
def read_rvt_file(file_path, headerlines=2):
    '''
    Function to read an RVT file and create a dataframe
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # print (lines[0:10])
    # Ignore the first line containing metadata
    data_lines = lines[headerlines-1:]  
    # print (data_lines)

    # print (data_lines) #[headerlines-1])
    # Extract the initial date from the first valid data entry
    first_valid_line = data_lines[0].strip().split()
    
    if len(first_valid_line) < 2:
        raise ValueError("Unexpected file format: First data line does not contain a valid date.")

    # print (first_valid_line)
    date = first_valid_line[0] + " " + first_valid_line[1]
    # print (date)
    # Extract numeric values from subsequent lines, ignoring `:EndObservationData`
    values = []
    for line in data_lines[1:]:
        line = line.strip()
        # print (line)
        if line == ":EndObservationData":
            break
        try:
            values.append(float(line))
            # print (values)
        except ValueError:
            continue  # Ignore any non-numeric lines
    
    if not values:
        raise ValueError("No valid numeric data found in the file.")

    # Create a date range starting from the initial date
    date_range = pd.date_range(start=date, periods=len(values), freq='D')

    # Create the dataframe
    df = pd.DataFrame({'date': date_range, 'value': values})

    # Convert to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Remove unobserved values
    df = df[df['value'] != -1.2345]

    # print (df)

    return df
#===============================================================================================
def get_data_yearly_range(Hylak_id, SubId, syear=2015, eyear=2022, prefix='WA_RS', obs_dir='/home/menaka/projects/def-btolson/menaka/LakeCalibration/obs_real'):
  '''
  Get yearly mean ranges
  '''
  # read GEE-GWW data
  file_path = obs_dir+'/'+prefix+'_'+str(Hylak_id)+'_'+str(SubId)+'.rvt'
#   print ("\t\t"+file_path)
  df = read_rvt_file(file_path)
#   print ("\t\tdf >>>>>>> \n",df)
  df['date'] = pd.to_datetime(df['date'])
  df.index = df['date']
  df = df.loc[str(syear)+'-01-01':str(eyear)+'-12-31']
#   print ("\t\tdf >>>>>>> \n\t",df)
  return df.groupby([df.index.year])['value'].max().dropna().mean()*1e-6 - df.groupby([df.index.year])['value'].min().dropna().mean()*1e-6
#===============================================================================================
thr_shorline=8*30*1e-3 #km
thr_lakearea=5.0 #7.5 #km2
thr_PotObs=2.0 #1.75 # ratio
#===============================================================================================
# obs_dir='/home/menaka/projects/def-btolson/menaka/LakeCalibration/obs_real'
# prefix='WA_RS'
obs_dir='/home/menaka/scratch/SytheticLakeObs/output/obs1b'
prefix='WA_SY'
print ("\n\t"+obs_dir)
#===============================================================================================
print ("\n\t>>>>>>> reading 'finalcat_hru_info_updated_AEcurve.csv'")
final_cat=pd.read_csv('/home/menaka/projects/def-btolson/menaka/LakeCalibration/OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
# Lake_List=final_cat.loc[final_cat['HRU_IsLake'] > 0,['HyLakeId','SubId']]
Lake_List=final_cat.loc[(final_cat['HRU_IsLake'] > 0) & (final_cat['LakeArea']>=thr_lakearea),'HyLakeId'].values

petawawa_lakes = gpd.read_file('/home/menaka/projects/def-btolson/menaka/LakeCalibration/extraction/Petawawa_lakes.shp') #,engine="pyogrio")

# print (final_cat.columns)
# print (petawawa_lakes.columns)

# print (final_cat['Obs_NM'].dropna())
selected_list=[]
print ("\t%10s%12s%12s%12s%12s"%("Obs_NM","HylakeId","LakeArea","LakeShoLng","PotObs"))
for Lake in Lake_List:
    Hylak_id = int(Lake)
    SubId = final_cat[final_cat['HyLakeId']==Lake]['SubId'].values[0]
    try:
        # get Lake Shoreline Length
        shorline = petawawa_lakes[petawawa_lakes['Hylak_id']==Lake]['Shore_len'].values[0]
        if shorline < thr_shorline:
            continue
        # get the Lake Area
        lakearea = final_cat[final_cat['HyLakeId']==Lake]['LakeArea'].values[0]*1e-6
        if lakearea < thr_lakearea:
            continue
        # get the yearly range data 
        yr_range = get_data_yearly_range(Hylak_id,SubId,syear=2015, eyear=2022, prefix=prefix, obs_dir=obs_dir)
        PotObs = (yr_range)/(shorline*30*1e-3)
        if PotObs < thr_PotObs:
            continue
        Obs_NM = final_cat[final_cat['HyLakeId']==Lake]['Obs_NM'].values[0]
        print ("\t%10s%12d%10.2f%10.2f%10.2f"%(Obs_NM, Lake, shorline, lakearea, PotObs))
        selected_list.append(Lake)
    except:
        print ("\t >>> No File", obs_dir+'/'+prefix+'_'+str(Hylak_id)+'_'+str(SubId)+'.rvt')
