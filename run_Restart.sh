#!/bin/bash
# set -x 
# trap read debug

expname=${1} #'0a'
ens_num=`printf '%02d\n' "${2}"`
trials=${3}
#======================================
cd ./out/${expname}_${ens_num}

# add OstrichWarmStart yes to ostIn.txt
sed -i '/#OstrichWarmStart      yes/c\OstrichWarmStart      yes' ostIn.txt

# update  ostIn.txt
sed -i "/MaxIterations/c\	MaxIterations         $trials" ostIn.txt

echo "Run Ostrich"

# run Ostrich
./Ostrich

cd ../..

wait