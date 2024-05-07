import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
#===================================================================================
def write_rvt(df,MetName,odir='./'):
    syear=df['Date'][0].year
    smon=df['Date'][0].month
    sday=df['Date'][0].day
    # write it to a file
    fname=odir+'/MNRF_'+MetName+".rvt"
    with open(fname,'w') as f:
        f.write(':MultiData\n')
        f.write('%04d-%02d-%02d 00:00:00  1.00  %6d\n'%(syear,smon,sday,len(df)))
        f.write(':Parameters  TEMP_DAILY_MIN  TEMP_DAILY_MAX  PRECIP\n')
        f.write(':Units		   C	   C     mm/d\n')
        # write the content
        for minT, maxT, Precp in df.loc[:,['TEMP_DAILY_MIN','TEMP_DAILY_MAX','PRECIP']].values:
        # print (minT, maxT, Precp)
        f.write('%7.2f%10.2f%10.2f\n'%(minT, maxT, Precp))
        # end the file
        f.write(':EndMultiData')
#===================================================================================
# read forcing file
# Achray_daily.csv, Hogan_daily.csv, Tim_daily.csv
# write to 
# MNRF_Achray.rvt, 
for metsta in ['Achray','Hogan','Tim']:
    # read file
    metdata=pd.read_csv('/content/drive/MyDrive/Petawawa_data/MNRF_Data/Daily/'+metsta+'_daily.csv')
    metdata['Date']=pd.to_datetime(metdata['Date'])
    # read from rvt file
    metRaven=pd.read_csv('/content/drive/MyDrive/Petawawa_data/forcing/MNRF_Achray.rvt',sep='\s+',skiprows=4,header=None,names=['TEMP_DAILY_MIN', 'TEMP_DAILY_MAX', 'PRECIP'])
    metRaven['Date']=pd.date_range("2000-01-01", periods=len(metRaven), freq="D")
    metRaven=metRaven.iloc[0:-1]
    # combine data
    df=pd.merge(metRaven,metdata.loc[:,['Date','AirTemp_min','AirTemp_max','Precip']],on='Date',how='outer')
    df['TEMP_DAILY_MIN'].fillna(df['AirTemp_min'], inplace=True)
    df.drop(columns=['AirTemp_min'], inplace=True)
    df['TEMP_DAILY_MAX'].fillna(df['AirTemp_max'], inplace=True)
    df.drop(columns=['AirTemp_max'], inplace=True)
    df['PRECIP'].fillna(df['Precip'], inplace=True)
    df.drop(columns=['Precip'], inplace=True)
    df['TEMP_DAILY_MIN']=pd.to_numeric(df['TEMP_DAILY_MIN'], errors='coerce')
    df['TEMP_DAILY_MAX']=pd.to_numeric(df['TEMP_DAILY_MAX'], errors='coerce')
    df['PRECIP']=pd.to_numeric(df['PRECIP'], errors='coerce')
    write_rvt(df,metsta,odir='/content/drive/MyDrive/Petawawa_data/forcing_update')