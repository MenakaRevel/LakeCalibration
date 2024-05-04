#!/bin/bash

#SBATCH --account=def-btolson                    
#SBATCH --mem-per-cpu=100M                       # memory; default unit is megabytes
#SBATCH --mail-user=mrevel@uwaterloo.ca          # email address for notifications
#SBATCH --mail-type=ALL                          # email send only in case of failure
#SBATCH --array=1-10                             # submit as a job array 
#SBATCH --time=00-72:00:00
#SBATCH --job-name=S0i

# load python
module load python/3.10

# load module
module load scipy-stack 

echo "===================================================="
echo "start: $(date)"
echo "===================================================="
echo ""
echo "Job Array ID / Job ID: $SLURM_ARRAY_JOB_ID / $SLURM_JOB_ID"
echo "This is job $SLURM_ARRAY_TASK_ID out of $SLURM_ARRAY_TASK_COUNT jobs."
echo ""
echo "===================================================="

# for graham 
cd $SLURM_TMPDIR
mkdir work
cd work
cp -r /scratch/menaka/LakeCalibration .
cd LakeCalibration
`pwd`

# Experimental Setup - see Experimental_settings

# epxeriment name
expname='0i'

# Max Itreation for calibration
trials=5000

echo './run_Init.sh' $expname $SLURM_ARRAY_TASK_ID
./run_Init.sh $expname $SLURM_ARRAY_TASK_ID

echo './run_Ostrich_single.sh' $expname $SLURM_ARRAY_TASK_ID
./run_Ostrich_single.sh $expname $SLURM_ARRAY_TASK_ID $trials

# echo './run_best_Raven_single.sh' $expname $SLURM_ARRAY_TASK_ID
# ./run_best_Raven_single.sh $expname $SLURM_ARRAY_TASK_ID

# The computations are done, so clean up the data set...
cd /scratch/menaka/LakeCalibration
mkdir -p ./out
cd ./out
# experimet name
num=`printf '%02g' "$SLURM_ARRAY_TASK_ID"`
cp -r $SLURM_TMPDIR/work/LakeCalibration/out/S${expname}_$num .

echo "===================================================="
echo "end: $(date)"
echo "===================================================="

wait