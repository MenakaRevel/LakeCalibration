#!/bin/bash

#SBATCH --account=def-btolson                    
#SBATCH --mem-per-cpu=1024M                       # memory; default unit is megabytes
#SBATCH --mail-user=mrevel@uwaterloo.ca          # email address for notifications
#SBATCH --mail-type=ALL                          # email send only in case of failure
#SBATCH --time=00-24:00:00
#SBATCH --job-name=V6d_02

# load python
module load python/3.10

# load module
module load scipy-stack 

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
finalcat_hru_info='finalcat_hru_info_updated_AEcurve.csv'
RavenDir='./RavenInput'
only_lake_obs='1'
ExpName='V6dd'                       # experiment name
MaxIteration=5000                    # Max Itreation for calibration
RunType='Init'                       # Intitial run or restart for longer run
CostFunction='NegMet'                # Cost function term
CalIndCW='True'                      # Calibrate individual crest width parameter {True|False|All} -> All:  calibrate all CW without considering number of Observations
AEcurve='True'                       # Use hypsometric curve (True | False)
MetSF='KLING_GUPTA'                  # Evaluation metric for SF - streamflow
MetWL='KLING_GUPTA_DEVIATION'        # Evaluation metric for WL - water level KLING_GUPTA_DEVIATION
MetWA='KLING_GUPTA'                  # Evaluation metric for WA - water area
ObsTypes='Obs_SF_SY  Obs_WA_SY1'     # Observation types according to coloumns in finca_cat.csv  #Obs_SF_IS  Obs_WL_IS Obs_WA_RS4 #Obs_WA_SY1
constrains='False'                   # Constrain for Q bias Q_Bias, False
ObsDir='/scratch/menaka/SytheticLakeObs/output/obs1b' #'/scratch/menaka/SytheticLakeObs/output/obs0' # observation folder
#===============================================================
# move to output folder
cd /scratch/menaka/LakeCalibration
# remove scripts
rm -rf run_Init.sh
rm -rf run_Ostrich.sh
rm -rf ./src
# link scprits
ln -sf /project/def-btolson/menaka/LakeCalibration/run_Init.sh .
ln -sf /project/def-btolson/menaka/LakeCalibration/run_Ostrich.sh .
ln -sf /project/def-btolson/menaka/LakeCalibration/src .
#===============================================================
# copy observations
# cp -rf $ObsDir/* ./OstrichRaven/RavenInput/obs/
# ln -sf $ObsDir/* ./OstrichRaven/RavenInput/obs/
# link observations
# rm -rf ./OstrichRaven/RavenInput/obs/*SY* 
cp -rf $ObsDir/* ./OstrichRaven/RavenInput/obs/ 
# link OstrichRaven
ln -sf /project/def-btolson/menaka/LakeCalibration/OstrichRaven .
#===============================================================
# ensemble number
num=1
ens_num=`printf '%02d\n' "${num}"`
mkdir -p ./out/${ExpName}_${ens_num}
#===============================================================
ObsDirCh=$(echo -n ${ObsDir} | tail -c 5)
#===============================================================
echo "===================================================="
echo "Experiment name: $ExpName with $MaxIteration calibration budget"
echo "===================================================="
echo "Experimental Settings"
echo "Experiment Name                   :"${ExpName}_${ens_num}
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
#===================================================="
EOF
#===============================================================
# Copy observations 
# cp -r $ObsDir/* ./OstrichRaven/RavenInput/obs/
#===============================================================
if [[ $RunType == 'Init' ]]; then
    echo $RunType, Initializing.............
    echo './run_Init.sh' $ExpName $num $MaxIteration $RunType $CostFunction $CalIndCW $MetSF $MetWL $MetWA $ObsDir $AEcurve $constrains $ObsTypes
    ./run_Init.sh $ExpName $num $MaxIteration $RunType $CostFunction $CalIndCW $MetSF $MetWL $MetWA $ObsDir $AEcurve $constrains $ObsTypes

    echo './run_Ostrich.sh' $ExpName $num #$MaxIteration
    ./run_Ostrich.sh $ExpName $num #$MaxIteration

    # echo './run_best_Raven_single.sh' $ExpName $num
    # ./run_best_Raven_single.sh $ExpName $num

else
    echo $RunType, Restarting.............
    echo ./run_Restart.sh $ExpName $num $MaxIteration
    ./run_Restart.sh $ExpName $num $MaxIteration
fi
wait