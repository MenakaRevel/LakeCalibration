#!/usr/python
'''
remove obs file
'''
import warnings
warnings.filterwarnings("ignore")
import os
import sys
import shutil
import glob
#===========================================
odir='/scratch/menaka/LakeCalibration/out'
ens_num=10
lexp=["E0a","E0b","E0c",
"S0a","S0b","S0c",
"S1i","S1z"]
for expname in lexp:
    for num in range(1,ens_num+1):
        # remove dir1
        dir1=odir+'/'+expname+"_%02d/RavenInput/obs"%(num)
        print (dir1)
        # Check if the 'obs' folder exists and remove it
        if os.path.isdir(dir1):  # Only remove if it's a directory
            try:
                shutil.rmtree(dir1)
            except Exception as e:
                print(f"Failed to remove {dir1}: {e}")
        os.system('ln -sf /projects/def-btolson/menaka/LakeCalibration/obs '+dir1)
        # remove dir1
        dir1=odir+'/'+expname+"_%02d/best/RavenInput/obs"%(num)
        print (dir1)
        # Check if the 'obs' folder exists and remove it
        if os.path.isdir(dir1):  # Only remove if it's a directory
            try:
                shutil.rmtree(dir1)
            except Exception as e:
                print(f"Failed to remove {dir1}: {e}")
        os.system('ln -sf /projects/def-btolson/menaka/LakeCalibration/obs '+dir1)
        # remove dir1
        dir1=odir+'/'+expname+"_%02d/best_Raven/RavenInput/obs"%(num)
        print (dir1)
        # Check if the 'obs' folder exists and remove it
        if os.path.isdir(dir1):  # Only remove if it's a directory
            try:
                shutil.rmtree(dir1)
            except Exception as e:
                print(f"Failed to remove {dir1}: {e}")
        os.system('ln -sf /projects/def-btolson/menaka/LakeCalibration/obs '+dir1)
        