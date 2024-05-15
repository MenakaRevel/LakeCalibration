#!/bin/bash

#SBATCH --account=def-btolson                    
#SBATCH --mem-per-cpu=1024M                       # memory; default unit is megabytes
#SBATCH --mail-user=mrevel@uwaterloo.ca          # email address for notifications
#SBATCH --mail-type=ALL                          # email send only in case of failure
#SBATCH --time=00-24:00:00
#SBATCH --job-name=S1a_01

# load python
module load python/3.10

# load module
module load scipy-stack 

echo "===================================================="
echo "start: $(date)"
echo "===================================================="
echo ""
echo "Job ID : $SLURM_JOB_ID"
echo "This is a serial job."
echo ""
echo "===================================================="

# Experimental Setup - see Experimental_settings

# experiment name
expname=`python -c "import params; print (params.ExpName())"` #'S1a'

# Max Itreation for calibration
trials=`python -c "import params; print (params.MaxIteration())"` #1000

echo "Experiment name: $expname with $trials calibration budget"
echo "===================================================="

# Intitial run or restart for longer run
RunType=`python -c "import params; print (params.RunType())"` #'init' # define the additional trails
# RunType='restart' # define the additional trails

# pertubation number
num=1
#===============================================================
# write the experiment settings
#===============================================================
# Routing='ROUTE_DIFFUSIVE_WAVE'               # River routing method
# CatchmentRoute='ROUTE_TRI_CONVOLUTION'       # Catchment routing method

cd $SLURM_TMPDIR
mkdir work
cd work
#===============================================================
# copy directory for calculation
cp -r /scratch/menaka/LakeCalibration .
cd LakeCalibration
#===============================================================
if [[ $RunType = 'Init' ]]; then
    echo "Working directory: `pwd`"
    echo $RunType, Initializing.............

    echo './run_Init.sh' $expname ${num}
    ./run_Init.sh $expname ${num} #$Obs_Type1 $Obs_Type2

    echo './run_Ostrich.sh' $expname ${num}
    ./run_Ostrich.sh $expname ${num} $trials

    # echo './run_best_Raven_single.sh' $expname ${num}
    # ./run_best_Raven_single.sh $expname ${num}
else
    echo "Working directory: `pwd`"
    echo $RunType, Restarting.............

    echo ./run_Restart.sh $expname ${num} $trials
    './run_Restart.sh' $expname ${num} $trials
fi

# The computations are done, so clean up the data set...
cd /scratch/menaka/LakeCalibration
mkdir -p ./out
cd ./out
# experimet name
cnum=`printf '%02g' "${num}"`
cp -r ${SLURM_TMPDIR}/work/LakeCalibration/out/${expname}_${cnum} .

echo "===================================================="
echo "end: $(date)"
echo "===================================================="

wait