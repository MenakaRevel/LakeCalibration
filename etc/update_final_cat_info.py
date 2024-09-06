import numpy as np
import pandas as pd
import sys
sys.path.append('../')
import params as pm
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
# read finalcat_hru_info.csv
# final_cat=pd.read_csv('/content/drive/MyDrive/Petawawa_data/finalcat_hru_info.csv')
final_cat=pd.read_csv('../OstrichRaven/finalcat_hru_info_updated_AEcurve_org.csv')

# obs_lakes=['Misty', 'Animoosh', 'Traverse', 'Lavieille', 'Burntroot', 'La Muir', 'Narrowbag', 'Big Trout', 'Radiant', 'Hogan',
#        'Little Cauchon', 'North Depot', 'Grand', 'Loontail', 'Cedar']

# val_gauges=['Little Madawaska Barometer', 'Petawawa River at Narrowbag','Nipissing River', 'Crow River']

# #Obs_SF_IS
# final_cat['Obs_SF_IS']=np.array([IS_gauges(row[1]['Has_Gauge'], row[1]['Obs_NM'], ['02KB001']) for row in final_cat.iterrows()])

# #Obs_WL_IS
# final_cat['Obs_WL_IS']=np.array([IS_gauges(row[1]['Has_Gauge'], row[1]['Obs_NM'], obs_lakes) for row in final_cat.iterrows()])

# #Obs_WA_RS
# final_cat['Obs_WA_RS']=np.array([RS_gauges(row[1]['HyLakeId'], final_cat['HyLakeId'].dropna().unique().astype(int)) for row in final_cat.iterrows()])

# final_cat['Obs_WA_RS1']=np.array([RS_gauges(row[1]['HyLakeId'], Obs1) for row in final_cat.iterrows()])
# final_cat['Obs_WA_RS2']=np.array([RS_gauges(row[1]['HyLakeId'], Obs2) for row in final_cat.iterrows()])

# #Validation_Gauge
# final_cat['Validation_Gauge']=np.array([SF_gauges(row[1]['Has_Gauge'], row[1]['Obs_NM'], val_gauges) for row in final_cat.iterrows()])

# Sythetic observation
Obs2=final_cat[final_cat['Obs_WA_RS4']==1]['HyLakeId'].unique()
final_cat['Obs_WA_SY1']=np.array([RS_gauges(row[1]['HyLakeId'], Obs2) for row in final_cat.iterrows()])

final_cat.to_csv('../OstrichRaven/finalcat_hru_info_updated_AEcurve.csv')
