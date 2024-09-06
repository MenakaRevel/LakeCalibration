#!/usr/python
'''
check the Lake water area comparison
'''
import warnings
warnings.filterwarnings("ignore")
import os
import sys
import numpy as np
import scipy
import datetime
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
import matplotlib.colors
mpl.use('Agg')
#===========================================
def cal_KGED(observed, simulated):
    """
    Calculate the modified Kling-Gupta Efficiency (KGED) without the bias term.

    Parameters:
    observed (array-like): Array of observed data.
    simulated (array-like): Array of simulated data.

    Returns:
    float: KGED value.
    """
    # Ensure inputs are numpy arrays
    observed = np.asarray(observed)
    simulated = np.asarray(simulated)

    # Calculate Pearson correlation coefficient
    r = np.corrcoef(observed, simulated)[0, 1]

    # Calculate coefficient of variation ratio (gamma)
    cv_observed = np.std(observed) #/ np.mean(observed)
    cv_simulated = np.std(simulated) #/ np.mean(simulated)
    gamma = cv_simulated / cv_observed

    # print ('CV observed: ', cv_observed)
    # print ('CV simulated: ', cv_simulated)
    # print ('gamma: ', gamma)

    # Calculate KGED
    kged = 1 - np.sqrt((r - 1)**2 + (gamma - 1)**2)

    return kged
#===============================================================================================
def read_rvt_file(file_path):
    '''
    # Function to read the file and create a dataframe
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Extract the initial date (ignoring the first line which is the header)
    initial_entry = lines[1].split()
    date = initial_entry[0] + " " + initial_entry[1]

    # Read subsequent values, ignoring the last line (':EndObservationData')
    values = [float(line.strip()) for line in lines[2:-1]]

    # Create a date range starting from the initial date
    date_range = pd.date_range(start=date, periods=len(values), freq='D')

    # Create the dataframe
    df = pd.DataFrame({'date': date_range, 'value': values})

    # open weight
    # print ('weight_file:',file_path.split(".")[1],file_path)
    weight_file=file_path.split(".")[0]+file_path.split(".")[1]+"_weight.rvt"
    df_wgt=read_rvt_weight_file(weight_file)

    df=pd.merge(df,df_wgt,on='date',how='inner',suffixes=('_obs', '_wgt'))

    # Remove the unobserved values
    df = df[(df['value']!=-1.2345) & (df['weight']!=0)]

    return df
#===============================================================================================
def read_rvt_weight_file(file_path):
    '''
    # Function to read the file and create a dataframe
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Extract the initial date (ignoring the first line which is the header)
    initial_entry = lines[1].split()
    date = initial_entry[0] + " " + initial_entry[1]

    # Read subsequent values, ignoring the last line (':EndObservationData')
    values = [float(line.strip()) for line in lines[2:-1]]

    # Create a date range starting from the initial date
    date_range = pd.date_range(start=date, periods=len(values), freq='D')

    # Create the dataframe
    df = pd.DataFrame({'date': date_range, 'weight': values})

    return df
#===============================================================================================
def read_Raven_ReservoirMassBalance(odir):
    '''
    Read the file name Petawawa_ReservoirMassBalance.csv
    '''
    # need to calculate KGED --> ObjLake = [DIAG_KLING_GUPTA_DEVIATION, DIAG_R2]
    syear,smon,sday,eyear,emon,eday = 2015,10,1,2022,9,30
    timetag='CALIBRATION'
    # fname=odir+"/"+expname+"_%02d/best_Raven/RavenInput/%s/Petawawa_ReservoirMassBalance.csv"%(ens_num,output)
    fname=odir+"/Petawawa_ReservoirMassBalance.csv"
    df_RMB=pd.read_csv(fname)
    df_RMB['date']=pd.to_datetime(df_RMB['date'])
    return df_RMB
#===============================================================================================
def create_obs(df_obs,df_Raven,subid_col):
    '''
    create Landsat observation mask for the particular point
    '''
    # merge the observations
    # Merge the two dataframes on the date column
    df = pd.merge(df_obs, df_Raven, on='date', suffixes=('_obs', '_Raven'))
    # df.rename(columns={subid_col:'sim', 'value':'obs'},inplace=True)
    return df
#===============================================================================================
if __name__ == "__main__":
    # read Raven WA 
    # folder contating observation
    basedir = "/home/menaka/scratch/LakeCalibration/out/V1a_01/RavenInput"

    obsdir = os.path.join(basedir,"obs")

    odir = os.path.join(basedir,"output2")

    # print ("\n\t>>>>>>> reading 'Petawawa_ReservoirMassBalance.csv'")
    df_WSA_org=read_Raven_ReservoirMassBalance(odir)
    # print (df_WSA_org.columns)

    # open diagnostic file
    df_diag=pd.read_csv(odir+"/Petawawa_Diagnostics.csv")

    #
    lakeObs=df_diag[df_diag['filename'].str.contains('./obs/WA_SY')]['filename']

    for lake in lakeObs:
        # print ("\n\t>>>>>>> Lake", lake)

        HylakeId=int(lake.split("_")[2])
        subid=int(lake.split("_")[-1].split('.')[0])

        # print ("\n\t>>>>>>> HylakeId: ", HylakeId, "subid :", subid)
        
        # get observations for the particular lake
        subid_col='sub'+str(subid)+' area [m2]'
        df_WSA=df_WSA_org.loc[:,['date',subid_col]]

        # read observations dates
        # fname=obsdir+"/WA_RS_%d_%d.rvt"%(int(lake),int(subid))
        # print ("\n\t>>>>>>> reading "+os.path.join(basedir,lake))
        df_obs=read_rvt_file(os.path.join(basedir,lake))

        # create observation based on Raven simulation
        df_syt=create_obs(df_obs,df_WSA,subid_col)
        # df_syt=df_WSA
        # print (df_syt)

        #
        print ('\n\t>>>>>>>',lake, 'KGED: ',cal_KGED(df_syt['value'], df_syt[subid_col]))