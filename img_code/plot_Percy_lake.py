#!/usr/python
'''
plot the ensemble metric
'''
import warnings
warnings.filterwarnings("ignore")
import os
import numpy as np
import scipy
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')

# read S01_xx hydrograph
df_hy = pd.read_csv('../out/S0b_01/best_Raven/RavenInput/output/Petawawa_Hydrographs.csv')

# read S01_xx Reservoir stage
df_wl = pd.read_csv('../out/S0b_01/best_Raven/RavenInput/output/Petawawa_ReservoirStages.csv')

# sub921 [m3/s],sub921 (observed) [m3/s]
fig, ax = plt.subplots(1,1,figsize=(12,4))
# calculate correlation
corr1=df_hy['sub921 [m3/s]'].corr(df_wl['sub921 '])
corr2=df_hy['sub921 (observed) [m3/s]'].corr(df_wl['sub921 '])
print (corr1, corr2)

df_hy.plot(x='date',y='sub921 [m3/s]',color='b', ax=ax, legend=False, label='Simulated Q (CC:%3.2f)'%(corr1))
df_hy.plot(x='date',y='sub921 (observed) [m3/s]', color='k', ax=ax, legend=False, label='02KB001 Observed Q (CC:%3.2f)'%(corr2))
ax.set_ylabel('Discharge $(m^2/s)$')

axtwin = ax.twinx()
df_wl.plot(x='date',y='sub921 ', color='g', linestyle='--', ax=axtwin, legend=False, label='Percy Lake level')
axtwin.set_ylabel('Lake Stage $(m)$')


fig.legend()
plt.tight_layout()
plt.savefig('../figures/extra/Percy_lake.jpg')