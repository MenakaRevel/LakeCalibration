# a python wrapper to run parallel

# 0. Copy the ostrich folder to perturbation SXX_NN e.g., S01_12 
# 1. Create ostrich input file - ostIn.txt - main difference is random seed
# 2. run ostrich

def main(inputlist):
    expname=inputlist[0]
    ens_num=inputlist[1]
    # copy ostrich folder to SXX_NN
    mk_dir('./S'+expname+'_'+ens_num)
    os.system('cp '+ostrich_folder+' '+experiment_folder)

    mk_ostIn(randomSeed):

    os.system('./OstrichGCC')
    return 0

def mk_ostIn(randomSeed)