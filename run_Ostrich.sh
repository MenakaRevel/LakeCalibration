#!/bin/bash
# set -x 
# trap read debug

expname=${1} #'0a'
ens_num=`printf '%02d\n' "${2}"`
trials=${3}
#=====================================
# cd into 
cd ./out/${expname}_${ens_num}
#
echo "making ostIn.txt"
# ProgramType='DDS' #ShuffledComplexEvolution
# ObjectiveFunction='GCOP'
RandomSeed=$(od -N 4 -t uL -An /dev/urandom | tr -d " ") ##$RANDOM
MaxIterations=${trials}

ostIn='./ostIn.txt'
# final_cat='./finalcat_hru_info_updated.csv'
# RavenDir='./RavenInput'
# only_lake_obs=1 # use only observations realted to Lake for calibrating lake parameters
echo create_ostIn.py $ostIn $RandomSeed $MaxIterations
python create_ostIn.py $ostIn $RandomSeed $MaxIterations

#'pwd'
echo "Run Ostrich"

# run Ostrich
./Ostrich

#'pwd'

cd ../..

wait