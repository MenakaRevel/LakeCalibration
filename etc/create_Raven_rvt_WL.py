import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
#===================================================================================
def write_rvt(df,HylakeID,SubId,unit='m',Odir='./'):
  '''
  # write WL data as Raven format
  # filled missing values: -1.2345
  # time interval 1 day
  # file name: WL_IS_{HylakeID}_{SubID}.rvt
  '''
  syear=df.index[0].year
  smon=df.index[0].month
  sday=df.index[0].day
  # write it to a file
  fname=Odir+'/WA_'+str(HylakeID)+"_"+str(SubId)+".rvt"
  with open(fname,'w') as f:
    f.write(':ObservationData RESERVOIR_STAGE '+str(SubId)+' '+unit+'\n')
    f.write('%04d-%02d-%02d 00:00:00   1     %6d\n'%(syear,smon,sday,len(df)))
    # write the content
    for val in df[str(HylakeID)]:
      f.write('%5.4f\n'%(val))
    # end the file
    f.write(':EndObservationData')

  return 0
#===================================================================================
# read finalcat_hru_info.csv
final_cat=pd.read_csv('/content/drive/MyDrive/Petawawa_data/finalcat_hru_info.csv')

# Load lakes names and HylakesID
lakesnames_df = pd.read_csv("/content/drive/MyDrive/Petawawa_data/Petawawa_lakes_w_obs.csv") #, 'rb' ,encoding="ISO-8859-1")

# lake stages
lakestage_df = pd.read_csv('/content/drive/MyDrive/Petawawa_data/MNRF_Data/15 Minute/Petawawa_lakes_2022_15minute.csv',low_memory=False)

# Convert 'timestamp' column to datetime format
lakestage_df['timestamp'] = pd.to_datetime(lakestage_df['timestamp'])

# Set 'timestamp' as index
lakestage_df.set_index('timestamp', inplace=True)

lakestage_df=lakestage_df.loc[:,['Animoosh', 'Big Trout', 'Burntroot','Cedar', 'Charles', 'Grand', 'Hambone', 'La Muir', 'Lavieille','Lilypond', 'Little Cauchon', 'Loontail', 'Misty', 'Narrowbag','North Depot', 'Radiant', 'Timberwolf', 'Travers']]

# Iterate through each day in the date range
for day in date_range:
    # Define the start and end dates for the 30-minute interval
    start_date = day + pd.Timedelta(hours=23, minutes=30)
    end_date = (day + pd.Timedelta(days=1)) + pd.Timedelta(minutes=30)
    
    print (lakestage_df.loc[start_date:end_date])

    # Slice the DataFrame for the specified time range
    sliced_df = lakestage_df.loc[start_date:end_date]
    
    print (sliced_df.mean())
    # Resample the sliced DataFrame with a frequency of 15 minutes and calculate the mean
    resampled_data.loc[day,:] = sliced_df.mean()
    
    # # Append the resampled data to the main DataFrame
    # resampled_data = pd.concat([resampled_data, resampled_df])

for i in lakesnames_df.index:
  resampled_data.rename(columns={lakesnames_df['Obs_NM'][i]:'%d'%(lakesnames_df['HyLakeId'][i])}, inplace=True)

resampled_data.rename(columns={'Travers':'108083'}, inplace=True)
resampled_data.fillna(-1.2345,inplace=True)

Hylakids=lakesnames_df[~lakesnames_df['HyLakeId']=='8767']['HyLakeId'].values

for Hylakid in Hylakids[0::]:
  SubId=final_cat[(final_cat['HRU_IsLake']==1) & (final_cat['HyLakeId']==Hylakid)]['SubId'].dropna().values[0]
  print (SubId)
  write_rvt(resampled_data,Hylakid,SubId,unit='m',Odir='/content/drive/MyDrive/Petawawa_data/obs_update')


# Hogan is daily only
