#!/bin/bash

set -e
python3 create_lake_rvh.py
cp ./Petawawa.rvp RavenInput/Petawawa.rvp
cp ./Petawawa.rvh RavenInput/Petawawa.rvh
cp ./Petawawa.rvc RavenInput/Petawawa.rvc
cp ./Lakes.rvh RavenInput/Lakes.rvh

cd RavenInput

rm -r ./output
./Raven Petawawa -o output/

cd ..

exit 0