#!/bin/bash
# set -x 
# trap read debug

expname=${1} #'0a'
ens_num=`printf '%02d\n' "${2}"`
#======================================
cd ./out/${expname}_${ens_num}

# add OstrichWarmStart yes to ostIn.txt
sed -i .bak 's/\([^.]*\)\#OstrichWarmStart/\OstrichWarmStart/g' ostIn.txt

echo "Run Ostrich"

# run Ostrich
./Ostrich

cd ../..

wait