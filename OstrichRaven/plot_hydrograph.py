'''
Plot
'''
import os
import numpy as np 
import pandas as pd

#
fname="/Volumes/MENAKA/1.Work/UWaterloo/LakeCalibration/best/output/Petawawa_Hydrographs.csv"
df_best=pd.read_csv(fname)

# initial
fname="/Volumes/MENAKA/1.Work/UWaterloo/LakeCalibration/RavenInput/output_init/Petawawa_Hydrographs.csv"
df_init=pd.read_csv(fname)

#plot
