import numpy as np
import pandas as pd
import sys
import glob
import re
import os
sys.path.append('../')
# import params as pm
#=================================
# read finalcat_hru_info.csv
final_cat=pd.read_csv('./OstrichRaven/finalcat_hru_info.csv')
print (final_cat.head())

# update observation filenames
for inname in glob.glob('./OstrichRaven/RavenInput/obs/WL*'):
    if 'weight' not in inname:
        # print (fname)
        match = re.search(r'\d+', inname)
        if match:
            SubId = match.group()
            # print(SubId)
            if not final_cat[final_cat['SubId']==int(SubId)]['HyLakeId'].dropna().empty:
                Hylakid=final_cat[final_cat['SubId']==int(SubId)]['HyLakeId'].dropna().values.astype(int)[0]
                # print(fname)#,Hylakid)
                parts = inname.split(".")
                weighted_inname = '.' + parts[1] + "_weight." + parts[2]
                outname='./obs/WL_IS_'+str(Hylakid)+'_'+SubId+'.rvt'
                weighted_outname = './obs/WL_IS_'+str(Hylakid)+'_'+SubId+'_weight.rvt'
                print('cp '+inname+' '+outname)
                os.system('cp -r '+inname+' '+outname)
                print('cp '+weighted_inname+' '+weighted_outname)
                os.system('cp -r '+weighted_inname+' '+weighted_outname)

             
