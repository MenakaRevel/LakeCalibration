#!/usr/python
'''
plot the costfunction
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
expname="S0b"
#=====================================================
mk_dir("../figures/"+expname)
ens_num=10
metric=[]
objFunction0=1.0
for num in range(1,ens_num+1):
    print (expname, num)
    df=pd.read_csv("../out/S0b_01/OstModel0.txt",sep="\s+",low_memory=False)
    if num == 1:
        dfout=df[['Run','obj.function']]
        dfout.rename(columns={'obj.function':'%02d'%(num)}, inplace=True)
    else:
        dfout['%02d'%(num)]=df['obj.function']
    
dfout['mean']=dfout.iloc[:,1::].mean(axis=1)

print (dfout.head())

fig, ax = plt.subplots()
for num in range(1,ens_num+1):
    dfout.plot(x='Run',y='%02d'%(num),color='grey',alpha=0.5, linewidth=0.2)
    # print (dfout['%02d'%(num)])

dfout.plot(x='Run',y='mean',color='r',alpha=0.5, linewidth=0.5, linestyle="--")

ax.set_ylabel("Cost Function")
plt.savefig('../figures/'+expname+'/f02-costFunction.jpg')
print ('../figures/'+expname+'/f02-costFunction.jpg')