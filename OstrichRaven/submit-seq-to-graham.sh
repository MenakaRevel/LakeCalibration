#!/bin/bash

# submit with:
#       sbatch submit-seq-to-graham.sh     

#SBATCH --account=def-btolson
#SBATCH --mem-per-cpu=70M                        # memory; default unit is megabytes
#SBATCH --mail-user=mrevel@uwaterloo.ca          # email address for notifications
#SBATCH --mail-type=FAIL                         # email send only in case of failure
#SBATCH --time=00-48:00  
#SBATCH --job-name=S23_1  

cd $SLURM_TMPDIR
mkdir work
cd work
cp -r /home/m43han/scratch/par_uncertainty_lakes/Models/setup_1/S23_1 ./   
cd S23_1  
./OstrichGCC                  # job

# The computations are done, so clean up the data set...
cd /home/m43han/scratch/par_uncertainty_lakes/Models/setup_1_out/   
cp -r $SLURM_TMPDIR/work/S23_1 ./   
