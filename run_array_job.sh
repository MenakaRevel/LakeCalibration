#!/bin/bash

#SBATCH --account=def-btolson                    
#SBATCH --mem-per-cpu=1024M                       # memory; default unit is megabytes
#SBATCH --mail-user=mrevel@uwaterloo.ca          # email address for notifications
#SBATCH --mail-type=ALL                          # email send only in case of failure
#SBATCH --array=1-10                             # submit as a job array 
#SBATCH --time=00-84:00:00
#SBATCH --job-name=V4e

# load python
module load python/3.12.4

# load module
module load scipy-stack 

#===============================================================
# write the experiment settings
#===============================================================
ProgramType='DDS'
ObjectiveFunction='GCOP'
finalcat_hru_info='finalcat_hru_info_updated_AEcurve.csv'
RavenDir='./RavenInput'
only_lake_obs='1'
ExpName='V4e'                                         # experiment name
MaxIteration=5000                                     # Max Itreation for calibration
RunType='Init'                                        # Intitial run or restart for longer run # Init Restart
CostFunction='NegKGE'                                 # Cost function term # NegKG_Q, NegKG_Q_WL, NegKGR2_Q_WA NegKGR2_Q_WL_WA 
CalIndCW='True'                                       # Calibrate individual crest width parameters
AEcurve='True'                                        # Use hypsometric curve (True | False)
MetSF='KLING_GUPTA'                                   # Evaluation metric for SF - streamflow
MetWL='KLING_GUPTA_DEVIATION'                         # Evaluation metric for WL - water level #KLING_GUPTA_DEVIATION
MetWA='KLING_GUPTA'                                   # Evaluation metric for WA - water area #KLING_GUPTA_DEVIATION
ObsTypes='Obs_WL_SY0'                                 # Observation types according to coloumns in finca_cat.csv # Obs_SF_IS  Obs_WL_IS Obs_WA_RS1 Obs_WA_RS4 Obs_WA_SY1 Obs_WA_SY0 Obs_SF_SY Obs_WL_SY0
constrains='False'                                    # Constrain for Q bias  Q_Bias, False
ObsDir='/scratch/menaka/SytheticLakeObs/output/obs1b' # observation folder #'/scratch/menaka/SytheticLakeObs/output/obs0b' '/projects/def-btolson/menaka/LakeCalibration/OstrichRaven/RavenInput/obs'
#===============================================================
Num=`printf '%02g' "${SLURM_ARRAY_TASK_ID}"`
#===============================================================
ObsDirCh=$(echo -n ${ObsDir} | tail -c 5)
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
echo "Maximum Iterations                :"${MaxIteration}
echo "Calibration Method                :"${ProgramType}
echo "Cost Function                     :"${CostFunction}
echo "  Metric SF                       :"${MetSF}
echo "  Metric WL                       :"${MetWL}
echo "  Metric WA                       :"${MetWA}
echo "Calibrate Individual Creset Width :"${CalIndCW}
echo "Observation Folder                :"${ObsDirCh}
echo "Observation Types                 :"${ObsTypes}
echo "Hypsometric Curve                 :"${AEcurve}
echo "Constrains                        :"${constrains}
echo "===================================================="
echo "Observation Directory"
echo "ObsDir : ${ObsDir}"
echo "===================================================="
echo ""
echo ""
#===============================================================
mkdir -p $SLURM_TMPDIR/work/LakeCalibration
cd $SLURM_TMPDIR/work/LakeCalibration
# srun --ntasks=$SLURM_NNODES --ntasks-per-node=1 mkdir -p $SLURM_TMPDIR/work
# mkdir work
# cd $SLURM_TMPDIR/work
# srun --ntasks=$SLURM_NNODES --ntasks-per-node=1 cd $SLURM_TMPDIR/work
#===============================================================
# copy directory for calculation
if [[ $RunType == 'Init' ]]; then
    cp -r /project/def-btolson/menaka/LakeCalibration/run_Init.sh .
    cp -r /project/def-btolson/menaka/LakeCalibration/run_Ostrich.sh .
    cp -r /project/def-btolson/menaka/LakeCalibration/src .
    # cp -r $ObsDir/* ./OstrichRaven/RavenInput/obs/
else
    cp -r /project/def-btolson/menaka/LakeCalibration . # copy the source codes
    cp -r /scratch/menaka/LakeCalibration/out ./out     # where out is saved
fi
# cd LakeCalibration
#===============================================================
# copy OstrichRaven
# cp -r /scratch/menaka/LakeCalibration/OstrichRaven .
cp -r /project/def-btolson/menaka/LakeCalibration/OstrichRaven .
#===============================================================
# copy observations
# cp -rf /project/def-btolson/menaka/LakeCalibration/OstrichRaven/obs ./OstrichRavenRavenInput/obs
cp -rf $ObsDir/* ./OstrichRaven/RavenInput/obs/
# # link observations
# rm -rf ./OstrichRaven/RavenInput/obs/*SY* 
# cp -rf $ObsDir/* ./OstrichRaven/RavenInput/obs/ 
# copy forcing
# cp -rf /project/def-btolson/menaka/LakeCalibration/OstrichRaven/forcing ./OstrichRavenRavenInput/forcing
# srun --ntasks=$SLURM_NNODES --ntasks-per-node=1 cp -r /scratch/menaka/LakeCalibration .
# srun --ntasks=$SLURM_NNODES --ntasks-per-node=1 cd LakeCalibration
#===============================================================
# write the experiment settings
expfile='./OstrichRaven/ExperimentalSettings.log'
cat >> ${expfile} << EOF
#====================================================
# Experiment name: $ExpName with $MaxIteration calibration budget
#====================================================
# Experimental Settings"
# Experiment Name                   :${ExpName}_${Num}
# Run Type                          :${RunType}
# Observation Types                 :${ObsTypes}
# Maximum Iterations                :${MaxIteration}
# Calibration Method                :${ProgramType}
# Cost Function                     :${CostFunction}
#   Metric SF                       :${MetSF}
#   Metric WL                       :${MetWL}
#   Metric WA                       :${MetWA}
# Calibrate Individual Creset Width :${CalIndCW}
# Observation Folder                :${ObsDirCh}
# Observation Types                 :${ObsTypes}
# Hypsometric Curve                 :${AEcurve}
# Constrains                        :${constrains}
#===================================================="
# Observation Directory
# ObsDir : ${ObsDir}
EOF
#===============================================================
# Start calibration trails
#===============================================================
if [[ $RunType == 'Init' ]]; then
    echo "Working directory: `pwd`"
    echo $RunType, Initializing.............

    echo './run_Init.sh' $ExpName ${SLURM_ARRAY_TASK_ID} $MaxIteration $RunType $CostFunction $CalIndCW $MetSF $MetWL $MetWA $ObsDir $AEcurve $constrains $ObsTypes
    ./run_Init.sh $ExpName ${SLURM_ARRAY_TASK_ID} $MaxIteration $RunType $CostFunction $CalIndCW $MetSF $MetWL $MetWA $ObsDir $AEcurve $constrains $ObsTypes

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
# ** make folder if it is not in scratch **
mkdir -p /scratch/menaka/LakeCalibration
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