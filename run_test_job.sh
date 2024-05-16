#!/bin/bash

#### need to load this before salloc
# # load python
# module load python/3.10

# # load module
# module load scipy-stack

#===============================================================
# write the experiment settings
#===============================================================
ProgramType='DDS'
ObjectiveFunction='GCOP'
finalcat_hru_info='finalcat_hru_info_updated.csv'
RavenDir='./RavenInput'
only_lake_obs='1'
ExpName='T03'                            # experiment name
MaxIteration=2                           # Max Itreation for calibration
RunType='Init'                           # Intitial run or restart for longer run
CostFunction='NegKG_Q_WL'                 # Cost function term
ObsTypes='Obs_SF_IS  Obs_WL_IS'       # Observation types according to coloumns in finca_cat.csv
#===============================================================
# ensemble number
num=1
ens_num=`printf '%02d\n' "${num}"`
mkdir -p ./out/${ExpName}_${ens_num}

if [[ $RunType == 'Init' ]]; then
    echo $RunType, Initializing.............
    echo './run_Init.sh' $ExpName $num $MaxIteration $RunType $CostFunction $ObsTypes
    ./run_Init.sh $ExpName $num $MaxIteration $RunType $CostFunction $ObsTypes

    echo './run_Ostrich.sh' $ExpName $num #$MaxIteration
    ./run_Ostrich.sh $ExpName $num #$MaxIteration

    # echo './run_best_Raven_single.sh' $ExpName $num
    # ./run_best_Raven_single.sh $ExpName $num

else
    echo $RunType, Restarting.............
    echo ./run_Restart.sh $ExpName $num $MaxIteration
    './run_Restart.sh' $ExpName $num $MaxIteration
fi
wait