#!/bin/bash

# submit with:
#       sbatch run.sh     

#SBATCH --account=def-btolson
## #SBATCH -n 2                                     # number of CPUs
#SBATCH --mem-per-cpu=70M                        # memory; default unit is megabytes
#SBATCH --mail-user=mrevel@uwaterloo.ca          # email address for notifications
#SBATCH --mail-type=FAIL                         # email send only in case of failure
#SBATCH --time=00-48:00:00  
#SBATCH --job-name=S0a 

