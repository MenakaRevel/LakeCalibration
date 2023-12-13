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
#===============================================================================================
def mk_dir(dir):
    # Create the download directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)
#=====================================================
def read_diagnostics(expname, ens_num, odir='../out'):
    '''
    read the RunName_Diagnostics.csv
    '''
    # HYDROGRAPH_CALIBRATION[921],./obs/02KB001_921.rvt
    # WATER_LEVEL_CALIBRATION[265],./obs/Crow_265.rvt
    # WATER_LEVEL_CALIBRATION[400],./obs/Little_Madawaska_400.rvt
    # WATER_LEVEL_CALIBRATION[412],./obs/Nippissing_Corrected_412.rvt
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    print (fname)
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    return df[df['observed_data_series'].isin(['WATER_LEVEL_CALIBRATION[265]',
    'WATER_LEVEL_CALIBRATION[400]','WATER_LEVEL_CALIBRATION[412]',
    'HYDROGRAPH_CALIBRATION[921]'])]['DIAG_KLING_GUPTA_DEVIATION'].values
#=====================================================
def read_WaterLevel(expname, ens_num, odir='../out',syear=2016,smon=1,sday=1,eyear=2020,emon=10,eday=20):
    '''
    read the RunName_WateLevels.csv
    '''
    # fname=odir+"/"+expname+"_%02d/best/RavenInput/output/Petawawa_WaterLevels.csv"%(ens_num)
    fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_WaterLevels.csv"%(ens_num)
    print (fname)
    df=pd.read_csv(fname)
    # calculate the metrics for syear,smon,sday:eyear,emon,eday [Evaluation Period]
    df.set_index('date',inplace=True)
    start='%04d-%02d-%02d'%(syear,smon,sday)
    end='%04d-%02d-%02d'%(eyear,emon,eday)
    print (start, end)
    df=df.loc[start:end]
    # calculate spearman correlation
    return np.array([df['sub265 [m]'].corr(df['sub265 (observed) [m]'] ,method='spearman'),
    df['sub400 [m]'].corr(df['sub400 (observed) [m]'] ,method='spearman'),
    df['sub412 [m]'].corr(df['sub412 (observed) [m]'] ,method='spearman')])
#=====================================================
expname="S0b"
#=====================================================
mk_dir("../figures/"+expname)
ens_num=40
metric=[]
for num in range(1,ens_num+1):
    print (expname, num)
    metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
    print (read_diagnostics(expname, num))
metric=np.array(metric)
print (metric)
df=pd.DataFrame(metric, columns=['02KB001','Crow','LM','NC','Crow-SRC','LM-SRC','NC-SRC'])
print (df.head())

fig, ax = plt.subplots()
sns.boxplot(data=df, order=['Crow-SRC','Crow','LM','LM-SRC','NC','NC-SRC','02KB001'])
star=df[['Crow-SRC','Crow','LM','LM-SRC','NC','NC-SRC','02KB001']].max()
print (star)
ax.scatter(star.index, star.values, marker='o', s=50, color='k')
ax.set_ylabel("$All$")
plt.savefig('../figures/'+expname+'/f01-metric_boxplot.jpg')

plt.close()
plt.clf()

print (df[['02KB001','Crow','LM','NC']].head())
fig, ax = plt.subplots()
ax=sns.boxplot(data=df[['02KB001','Crow','LM','NC']],order=['Crow','LM','NC','02KB001'])
star=df[['Crow','LM','NC','02KB001']].max()
print (star)
ax.scatter(star.index, star.values, marker='o', s=50, color='k')
ax.set_ylabel("$KGED$")
plt.savefig('../figures/'+expname+'/f01-KGE_boxplot.jpg')

plt.close()
plt.clf()

print (df[['02KB001','Crow-SRC','LM-SRC','NC-SRC']].head())

fig, ax = plt.subplots()
ax=sns.boxplot(data=df[['02KB001','Crow-SRC','LM-SRC','NC-SRC']],order=['Crow-SRC','LM-SRC','NC-SRC','02KB001'])
star=df[['Crow-SRC','LM-SRC','NC-SRC','02KB001']].max()
ax.scatter(star.index, star.values, marker='o', s=50, color='k')
ax.set_ylabel("$Spearman's Ranked Correlation$")
plt.savefig('../figures/'+expname+'/f01-spearman_correlation_boxplot.jpg')