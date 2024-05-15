#!/bin/bash

#### need to load this before salloc
# # load python
# module load python/3.10

# # load module
# module load scipy-stack

# Experimental Setup - see Experimental_settings

# epxeriment name
expname='S1a'

# Max Itreation for calibration
trials=2

# Experiment Pertubation
num=1

# RunType='Init'
RunType='Restart'

if [[ $RunType == 'Init' ]]; then
    echo $RunType, Initializing.............
    echo './run_Init.sh' $expname $num
    ./run_Init.sh $expname $num

    echo './run_Ostrich.sh' $expname $num $trials
    ./run_Ostrich.sh $expname $num $trials

    # echo './run_best_Raven_single.sh' $expname $num
    # ./run_best_Raven_single.sh $expname $num

else
    echo $RunType, Restarting.............
    echo ./run_Restart.sh $expname $num $trials
    './run_Restart.sh' $expname $num $trials
fi
wait