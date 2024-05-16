#!/bin/bash

#SBATCH --account=def-btolson                    
#SBATCH --mem-per-cpu=1024M                       # memory; default unit is megabytes
#SBATCH --mail-user=mrevel@uwaterloo.ca          # email address for notifications
#SBATCH --mail-type=ALL                          # email send only in case of failure
#SBATCH --array=1-10                             # submit as a job array 
#SBATCH --time=00-48:00:00
#SBATCH --job-name=S1c

# load python
module load python/3.10

# load module
module load scipy-stack 

#===============================================================
# write the experiment settings
#===============================================================
ProgramType='DDS'
ObjectiveFunction='GCOP'
finalcat_hru_info='finalcat_hru_info_updated.csv'
RavenDir='./RavenInput'
only_lake_obs='1'
ExpName='S1c'                            # experiment name
MaxIteration=5000                       # Max Itreation for calibration
RunType='Init'                           # Intitial run or restart for longer run
CostFunction='NegKGR2_Q_WA'                # Cost function term # NegKG_Q, NegKG_Q_WL, NegKGR2_Q_WA NegKGR2_Q_WL_WA 
CalIndCW='False'                 # Calibrate individual crest width parameters
ObsTypes='Obs_SF_IS  Obs_WA_RS1' # Observation types according to coloumns in finca_cat.csv #Obs_SF_IS  Obs_WL_IS Obs_WA_RS1
#===============================================================
Num=`printf '%02g' "${SLURM_ARRAY_TASK_ID}"`
#===============================================================
echo "===================================================="
echo "start: $(date)"
echo "===================================================="
echo ""
echo "Job Array ID / Job ID: $SLURM_ARRAY_JOB_ID / $SLURM_JOB_ID"
echo "This is job $SLURM_ARRAY_TASK_ID out of $SLURM_ARRAY_TASK_COUNT jobs."
echo ""
echo "===================================================="
echo "Experiment name: $ExpName with $MaxIteration calibration budget"
echo "===================================================="
echo "Experimental Settings"
echo "Experiment Name                   :"${ExpName}_${Num}
echo "Run Type                          :"${RunType}
echo "Observation Types                 :"${ObsTypes}
echo "Maximum Iterations                :"${MaxIteration}
echo "Calibration Method                :"${ProgramType}
echo "Cost Function                     :"${CostFunction}
echo "Calibrate Individual Creset Width :"${CalIndCW}
echo ""====================================================""
echo ""
echo ""
#===============================================================
cd $SLURM_TMPDIR
mkdir work
cd work
#===============================================================
# copy directory for calculation
cp -r /scratch/menaka/LakeCalibration .
cd LakeCalibration
#===============================================================
# write the experiment settings
# create param.py
#===============================================================
# Start calibration trails
#===============================================================
if [[ $RunType == 'Init' ]]; then
    echo "Working directory: `pwd`"
    echo $RunType, Initializing.............

    echo './run_Init.sh' $ExpName ${SLURM_ARRAY_TASK_ID} $MaxIteration $RunType $CostFunction $CalIndCW $ObsTypes
    ./run_Init.sh $ExpName ${SLURM_ARRAY_TASK_ID} $MaxIteration $RunType $CostFunction $CalIndCW $ObsTypes

    echo './run_Ostrich.sh' $ExpName ${SLURM_ARRAY_TASK_ID}
    ./run_Ostrich.sh $ExpName ${SLURM_ARRAY_TASK_ID} #$MaxIteration

    # echo './run_best_Raven_single.sh' $ExpName ${SLURM_ARRAY_TASK_ID}
    # ./run_best_Raven_single.sh $ExpName ${SLURM_ARRAY_TASK_ID}
else
    echo "Working directory: `pwd`"
    echo $RunType, Restarting.............

    echo ./run_Restart.sh $ExpName ${SLURM_ARRAY_TASK_ID} $MaxIteration
    './run_Restart.sh' $ExpName ${SLURM_ARRAY_TASK_ID} $MaxIteration
fi
#===============================================================
# The computations are done, so clean up the data set...
cd /scratch/menaka/LakeCalibration
mkdir -p ./out
cd ./out
# experiment name
cp -r ${SLURM_TMPDIR}/work/LakeCalibration/out/${ExpName}_${Num} .
#===============================================================
echo "===================================================="
echo "end: $(date)"
echo "===================================================="
#===============================================================
wait