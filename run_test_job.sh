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
ExpName='T01'                        # experiment name
MaxIteration=10                      # Max Itreation for calibration
RunType='Init'                       # Intitial run or restart for longer run
CostFunction='NegKG_Q_WA'            # Cost function term
CalIndCW='True'                      # Calibrate individual crest width parameter
MetSF='KLING_GUPTA_PRIME'            # Evaluation metric for SF - streamflow
MetWL='KLING_GUPTA_DEVIATION_PRIME'                           # Evaluation metric for WL - water level KLING_GUPTA_DEVIATION
MetWA='KLING_GUPTA_DEVIATION_PRIME'                           # Evaluation metric for WA - water area
ObsTypes='Obs_SF_IS Obs_WL_IS'       # Observation types according to coloumns in finca_cat.csv   
#===============================================================
# ensemble number
num=1
ens_num=`printf '%02d\n' "${num}"`
mkdir -p ./out/${ExpName}_${ens_num}
#===============================================================
echo "===================================================="
echo "Experiment name: $ExpName with $MaxIteration calibration budget"
echo "===================================================="
echo "Experimental Settings"
echo "Experiment Name                   :"${ExpName}_${ens_num}
echo "Run Type                          :"${RunType}
echo "Observation Types                 :"${ObsTypes}
echo "Maximum Iterations                :"${MaxIteration}
echo "Calibration Method                :"${ProgramType}
echo "Cost Function                     :"${CostFunction}
echo "  Metric SF                       :"${MetSF}
echo "  Metric WL                       :"${MetWL}
echo "  Metric WA                       :"${MetWA}
echo "Calibrate Individual Creset Width :"${CalIndCW}
echo "===================================================="
echo ""
echo ""
#===============================================================
# write the experiment settings
expfile=./out/${ExpName}_${ens_num}/ExperimentalSettings.log
cat >> ${expfile} << EOF
#====================================================
# Experiment name: $ExpName with $MaxIteration calibration budget
#====================================================
# Experimental Settings"
# Experiment Name                   :${ExpName}_${ens_num}
# Run Type                          :${RunType}
# Observation Types                 :${ObsTypes}
# Maximum Iterations                :${MaxIteration}
# Calibration Method                :${ProgramType}
# Cost Function                     :${CostFunction}
#   Metric SF                       :${MetSF}
#   Metric WL                       :${MetWL}
#   Metric WA                       :${MetWA}
# Calibrate Individual Creset Width :${CalIndCW}
#===================================================="
EOF
#===============================================================
if [[ $RunType == 'Init' ]]; then
    echo $RunType, Initializing.............
    echo './run_Init.sh' $ExpName $num $MaxIteration $RunType $CostFunction $CalIndCW $MetSF $MetWL $MetWA $ObsTypes
    ./run_Init.sh $ExpName $num $MaxIteration $RunType $CostFunction $CalIndCW $MetSF $MetWL $MetWA $ObsTypes

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