#!/usr/python
'''
plot the KGEq vs KGEDl
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
    return df.loc[0,'DIAG_KLING_GUPTA'],df.loc[1:22,'DIAG_KLING_GUPTA_DEVIATION'].mean()
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
    row1,row2=read_diagnostics(expname, num)
    row3=read_costFunction(expname, num)
    print (row1,row2,row3)
    metric.append([row1,row2,row3])

metric=np.array(metric)#[:,0,:]
print (metric)

df=pd.DataFrame(metric, columns=["KGEq","KGEDl","obj.function"])
print (df.head())


fig, ax = plt.subplots()
df.plot(x="KGEq",y="KGEDl",color="grey",marker='o', linestyle=None, linewidth=0,ax=ax)
ax.plot(df.loc[df['obj.function'].idxmin(),'KGEq'],df.loc[df['obj.function'].idxmin(),'KGEDl'], 
color="k",marker='*')
print (df.loc[df['obj.function'].idxmin(),'KGEq'],df.loc[df['obj.function'].idxmin(),'KGEDl'])
ax.set_ylabel(r"$\bar{KGED^{All}_{L}}$")
ax.set_xlabel(r"${KGE}_Q}$")
plt.savefig('../figures/'+expname+'/f03-KGEq_KGED_scatter.jpg')