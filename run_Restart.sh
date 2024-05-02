#!/bin/bash
# set -x 
# trap read debug

cd ./out/S${expname}_${ens_num}

# add OstrichWarmStart yes to ostIn.txt
sed -i .bak 's/\([^.]*\)\#OstrichWarmStart/\OstrichWarmStart/g' ostIn.txt

echo "Run Ostrich"

# run Ostrich
./Ostrich

cd ../..

wait