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

# ***ONLY RUN AFTER OSTRICH***

# # for graham 
# cd $SLURM_TMPDIR
# mkdir work
# cd work
# cp -r /scratch/menaka/LakeCalibration .
# cd LakeCalibration
# `pwd`

expname='0b'
ens_num='01'
for ens_num in $(seq -f '%02g' 1 10);
do
    echo $ens_num, `pwd`
    # cd into 
    # cd /scratch/menaka/LakeCalibration/out/S${expname}_${ens_num}/best/RavenInput
    # cd /scratch/menaka/LakeCalibration/out_new_obs_OldRaven/S${expname}_${ens_num}/best/RavenInput
    cd /scratch/menaka/LakeCalibration/out_new_obs_NewRaven/S${expname}_${ens_num}/best/RavenInput
    `pwd`

    # copy Petawawa.rvt
    # cp -r ../../../../OstrichRaven/RavenInput/Petawawa.rvt .

    # copy observations folder
    # cp -r ../../../../OstrichRaven/RavenInput/obs .

    # copy Raven.exe

    # cp /scratch/menaka/RavenSource_v3.7/Raven.exe .

    # ./Raven Petawawa -o ./output_Raven_v3.8

    ./Raven.exe Petawawa -o ./output_Raven_v3.7

    cd ../..

done
wait

# # edit rvi file
# rvi='Petawawa.rvi'
# rm -r ${rvi}
# cat >> ${rvi} << EOF
# # ----------------------------------------------
# # Raven Input file
# # HBV-EC Nith River emulation test case
# # ----------------------------------------------
# # --Simulation Details -------------------------
# :RunName               Petawawa                                                                           
# :StartDate             2015-01-01 00:00:00
# :EndDate               2021-01-01 00:00:00           
# :TimeStep              1.0

# #
# # --Model Details -------------------------------
# :Method                 ORDERED_SERIES
# :Interpolation          INTERP_NEAREST_NEIGHBOR
# :SoilModel              SOIL_MULTILAYER 3


# :Routing                ROUTE_HYDROLOGIC #ROUTE_HYDROLOGIC ROUTE_DIFFUSIVE_WAVE
# :CatchmentRoute         ROUTE_TRI_CONVOLUTION
# :OW_Evaporation         PET_PRIESTLEY_TAYLOR

# ##Vegetation impacted processes 
# :SWCanopyCorrect        SW_CANOPY_CORR_NONE    #SW_CANOPY_CORR_STATIC  #SW_CANOPY_CORR_NONE #SW_CANOPY_CORR_DYNAMIC
# #:PrecipIceptFract       PRECIP_ICEPT_LAI
# :Evaporation            PET_PRIESTLEY_TAYLOR   #PET_PENMAN_MONTEITH  #
# :PotentialMeltMethod    POTMELT_HBV            #POTMELT_EB #POTMELT_HBV #POTMELT_EB
# :RainSnowFraction       RAINSNOW_HBV          # RAINSNOW_DINGMAN                                                                      
# #:OroTempCorrect        OROCORR_SIMPLELAPSE                                                                   
# #:OroPrecipCorrect      OROCORR_SIMPLELAPSE      

# #
# # --Hydrologic Processes-------------------------
# :Alias       Forest_Floor   SOIL[0]
# :Alias       Ablation_Till  SOIL[1]
# :Alias       Basal_Till     SOIL[2]


# #

# :EvaluationPeriod CALIBRATION 2016-01-01 2020-10-20
# #:EvaluationPeriod VALIDATION  2018-01-01 2020-10-20


# :HydrologicProcesses
# #
#   :SnowRefreeze      FREEZE_DEGREE_DAY            SNOW_LIQ         SNOW
#   :Precipitation     PRECIP_RAVEN                 ATMOS_PRECIP     MULTIPLE
# #
#   :CanopyEvaporation CANEVP_ALL         CANOPY           ATMOSPHERE
#   :CanopySnowEvap    CANEVP_ALL         CANOPY_SNOW      ATMOSPHERE
# #   
#   :SnowBalance       SNOBAL_SIMPLE_MELT           SNOW             SNOW_LIQ                    #:SnowBalance       SNOBAL_TWO_LAYER   MULTIPLE         MULTIPLE     # :SnowBalance       SNOBAL_SIMPLE_MELT SNOW             PONDED_WATER
#   :-->Overflow       RAVEN_DEFAULT                SNOW_LIQ         PONDED_WATER                                                                                                                                                            #:-->Overflow     RAVEN_DEFAULT      SNOW_LIQ         PONDED_WATER
# #    
#   :Infiltration      INF_GREEN_AMPT               PONDED_WATER     MULTIPLE   
#   ### Forest_Floor
#   :SoilEvaporation   SOILEVAP_SEQUEN              Forest_Floor     ATMOSPHERE
# #
#   :Percolation       PERC_GAWSER_CONSTRAIN        Forest_Floor     Ablation_Till   
#   :Baseflow          BASE_THRESH_POWER            Forest_Floor     SURFACE_WATER 
#   ### Ablation_Till
#   :Baseflow          BASE_THRESH_POWER             Ablation_Till    SURFACE_WATER
#   :Percolation       PERC_GAWSER_CONSTRAIN         Ablation_Till    Basal_Till
#   ### Basal_Till
#   :Baseflow          BASE_THRESH_POWER             Basal_Till       SURFACE_WATER
#   :CapillaryRise     CRISE_HBV                     Basal_Till       Ablation_Till
# #  
# :EndHydrologicProcesses


# #---------------------------------------------------------                                                 
# # Output Options                                                                                           
# #
# :WriteForcingFunctions 
# :WriteWaterLevels 
# :WriteMassBalanceFile 
# :WriteReservoirMBFile
# :EvaluationMetrics NASH_SUTCLIFFE RMSE KLING_GUPTA KLING_GUPTA_DEVIATION DIAG_R2
# EOF

#     ./Raven.exe Petawawa -o ./output

#     cd ../..

# done
# wait

# # The computations are done, so clean up the data set...
# cd /scratch/menaka/LakeCalibration
# mkdir -p out
# cd ./out  
# cp -r $SLURM_TMPDIR/work/LakeCalibration/out/* . 