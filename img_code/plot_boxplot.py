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
    fname=odir+"/"+expname+"_%02d/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_Diagnostics.csv"%(ens_num)
    print (fname)
    df=pd.read_csv(fname)
    # df=df.loc[0:23,:]
    #  DIAG_KLING_GUPTA
    return df[df['observed_data_series'].isin(['WATER_LEVEL_CALIBRATION[265]',
    'WATER_LEVEL_CALIBRATION[400]','WATER_LEVEL_CALIBRATION[412]',
    'HYDROGRAPH_CALIBRATION[921]'])][['DIAG_KLING_GUPTA','DIAG_KLING_GUPTA_DEVIATION','DIAG_R2','DIAG_SPEARMAN']].values
#=====================================================
def read_WaterLevel(expname, ens_num, odir='../out',syear=2016,smon=1,sday=1,eyear=2020,emon=10,eday=20):
    '''
    read the RunName_WateLevels.csv
    '''
    fname=odir+"/"+expname+"_%02d/best/RavenInput/output/Petawawa_WaterLevels.csv"%(ens_num)
    # fname=odir+"/"+expname+"_%02d_4000/best/RavenInput/output/Petawawa_WaterLevels.csv"%(ens_num)
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
def read_costFunction(expname, ens_num, odir='../out'):
    fname=odir+"/"+expname+"_%02d/OstModel0.txt"%(ens_num)
    print (fname)
    df=pd.read_csv(fname,sep="\s+",low_memory=False)
    # print (df.head())
    return df['obj.function'].iloc[-1]
#=====================================================
expname="S0b"
#=====================================================
mk_dir("../figures/"+expname)
ens_num=10
metric=[]
objFunction0=1.0
for num in range(1,ens_num+1):
    print (expname, num)
    # metric.append(np.concatenate( (read_diagnostics(expname, num), read_WaterLevel(expname, num))))
    # print (list(read_diagnostics(expname, num).flatten()).append(read_costFunction(expname, num))) #np.shape(read_diagnostics(expname, num)), 
    row=list(read_diagnostics(expname, num).flatten())
    row.append(read_costFunction(expname, num))
    print (row)
    metric.append([row])
metric=np.array(metric)[:,0,:]
print (metric)

df=pd.DataFrame(metric, columns=['KGE_02KB001','KGE_Crow','KGE_LM','KGE_NC',
'KGED_02KB001','KGED_Crow','KGED_LM','KGED_NC',
'R2_02KB001','R2_Crow','R2_LM','R2_NC',
'SRCC_02KB001','SRCC_Crow','SRCC_LM','SRCC_NC',
'obj.function'])
print (df.head())

fig, ax = plt.subplots()
sns.boxplot(data=df[['KGE_02KB001','KGE_Crow','KGE_LM','KGE_NC',
'KGED_02KB001','KGED_Crow','KGED_LM','KGED_NC',
'R2_02KB001','R2_Crow','R2_LM','R2_NC',
'SRCC_02KB001','SRCC_Crow','SRCC_LM','SRCC_NC']])
star=df.loc[df['obj.function'].idxmin(),['KGE_02KB001','KGE_Crow','KGE_LM','KGE_NC',
'KGED_02KB001','KGED_Crow','KGED_LM','KGED_NC',
'R2_02KB001','R2_Crow','R2_LM','R2_NC',
'SRCC_02KB001','SRCC_Crow','SRCC_LM','SRCC_NC']]
print (star)
ax.scatter(star.index, star.values, marker='*', s=50, color='k')
ax.set_ylabel("$All$")
plt.savefig('../figures/'+expname+'/f01-metric_boxplot.jpg')

plt.close()
plt.clf()

print (df[['KGE_02KB001','KGED_Crow','KGED_LM','KGED_NC']].head())
fig, ax = plt.subplots()
ax=sns.boxplot(data=df[['KGE_02KB001','KGED_Crow','KGED_LM','KGED_NC']],
order=['KGED_Crow','KGED_LM','KGED_NC','KGE_02KB001'])
star=df.loc[df['obj.function'].idxmin(),['KGE_02KB001','KGED_Crow','KGED_LM','KGED_NC']]
print (star)
ax.scatter(star.index, star.values, marker='*', s=50, color='k')
ax.set_ylabel("$KGED$")
plt.savefig('../figures/'+expname+'/f01-KGE_boxplot.jpg')

plt.close()
plt.clf()

print (df[['R2_02KB001','R2_Crow','R2_LM','R2_NC']].head())

fig, ax = plt.subplots()
ax=sns.boxplot(data=df[['R2_02KB001','R2_Crow','R2_LM','R2_NC']],order=['R2_Crow','R2_LM','R2_NC','R2_02KB001'])
star=df.loc[df['obj.function'].idxmin(),['R2_02KB001','R2_Crow','R2_LM','R2_NC']]
ax.scatter(star.index, star.values, marker='*', s=50, color='k')
ax.set_ylabel("$R^2$")
plt.savefig('../figures/'+expname+'/f01-R2_boxplot.jpg')

fig, ax = plt.subplots()
ax=sns.boxplot(data=df[['SRCC_02KB001','SRCC_Crow','SRCC_LM','SRCC_NC']],order=['SRCC_Crow','SRCC_LM','SRCC_NC','SRCC_02KB001'])
star=df.loc[df['obj.function'].idxmin(),['SRCC_02KB001','SRCC_Crow','SRCC_LM','SRCC_NC']]
ax.scatter(star.index, star.values, marker='*', s=50, color='k')
ax.set_ylabel("$Spearman's Ranked Correlation$")
plt.savefig('../figures/'+expname+'/f01-spearman_correlation_boxplot.jpg')