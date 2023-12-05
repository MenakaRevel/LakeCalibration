#!/bin/bash

set -e
python3 create_lake_rvh.py
cp ./Petawawa.rvp RavenInput/Petawawa.rvp
cp ./Petawawa.rvh RavenInput/Petawawa.rvh
cp ./Petawawa.rvc RavenInput/Petawawa.rvc
cp ./Lakes.rvh RavenInput/Lakes.rvh

cd RavenInput

rm -r ./output
./Raven.exe Petawawa -o output/

cd ..

# ## add program to calculate Spearman Ranked Correlation Coefficient
# python3 calc_Spearman_corr.py RavenInput/output

exit 0

