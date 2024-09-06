#!/bin/bash

# submit with:
#       sbatch run.sh     

#SBATCH --account=def-btolson
## #SBATCH -n 2                                     # number of CPUs
#SBATCH --mem-per-cpu=1024M                        # memory; default unit is megabytes
#SBATCH --mail-user=mrevel@uwaterloo.ca          # email address for notifications
#SBATCH --mail-type=FAIL                         # email send only in case of failure
#SBATCH --time=00-48:00:00  
#SBATCH --job-name=Best-Raven-E0b

# ***ONLY RUN AFTER OSTRICH***

# # # for graham 
# # cd $SLURM_TMPDIR
# # mkdir work
# # cd work
# # cp -r /scratch/menaka/LakeCalibration .
# # cd LakeCalibration
# # `pwd`
prefix='E'
expname='0b'
ens_num='01'
for ens_num in $(seq -f '%02g' 1 10);
do
    echo ${prefix}${expname}_${ens_num}, `pwd`
    rm -rf /scratch/menaka/LakeCalibration/out/${prefix}${expname}_${ens_num}/best_Raven
    mkdir -p /scratch/menaka/LakeCalibration/out/${prefix}${expname}_${ens_num}/best_Raven
    cd /scratch/menaka/LakeCalibration/out/${prefix}${expname}_${ens_num}/best_Raven
    cp -rf /scratch/menaka/LakeCalibration/out/${prefix}${expname}_${ens_num}/best/* . 
    cd RavenInput

    # # # copy observations
    # # rm -rf ./obs 
    # # ln -sf /scratch/menaka/LakeCalibration/OstrichRaven/RavenInput/obs .

    # cd into 
    # cd /scratch/menaka/LakeCalibration/out/S${expname}_${ens_num}/best/RavenInput
    # cd /scratch/menaka/LakeCalibration/out_new_obs_OldRaven/S${expname}_${ens_num}/best/RavenInput
    # cd /scratch/menaka/LakeCalibration/out_new_obs_NewRaven/S${expname}_${ens_num}/best/RavenInput
    `pwd`

    # copy Petawawa.rvt
    # cp -r ../../../../OstrichRaven/RavenInput/Petawawa.rvt .

    # copy observations folder
    # cp -r ../../../../OstrichRaven/RavenInput/obs .

    # copy Raven.exe
    # cp -rf /home/menaka/projects/def-btolson/menaka/RavenHydroFramework/src/Raven.exe .

#     ./Raven Petawawa -o ./output

#     # ./Raven.exe Petawawa -o ./output_Raven_v3.7

#     cd ../..

# done
# wait
#----------------------------------------------------------------------------------------
# edit rvi file
rvi='Petawawa.rvi'
rm -r ${rvi}
cat >> ${rvi} << EOF
# ----------------------------------------------
# Raven Input file
# HBV-EC Petawawa River
# ----------------------------------------------
# --Simulation Details -------------------------
:RunName               Petawawa                                                                           
:StartDate             2013-10-01 00:00:00
:EndDate               2022-10-01 00:00:00           
:TimeStep              1.0

#
# --Model Details -------------------------------
:Method                 ORDERED_SERIES
:Interpolation          INTERP_NEAREST_NEIGHBOR
:SoilModel              SOIL_MULTILAYER 3


:Routing                ROUTE_DIFFUSIVE_WAVE  #ROUTE_HYDROLOGIC #ROUTE_HYDROLOGIC 
:CatchmentRoute         ROUTE_TRI_CONVOLUTION
:OW_Evaporation         PET_PRIESTLEY_TAYLOR

##Vegetation impacted processes 
:SWCanopyCorrect        SW_CANOPY_CORR_NONE    #SW_CANOPY_CORR_STATIC  #SW_CANOPY_CORR_NONE #SW_CANOPY_CORR_DYNAMIC
#:PrecipIceptFract       PRECIP_ICEPT_LAI
:Evaporation            PET_PRIESTLEY_TAYLOR   #PET_PENMAN_MONTEITH  #
:PotentialMeltMethod    POTMELT_HBV            #POTMELT_EB #POTMELT_HBV #POTMELT_EB
:RainSnowFraction       RAINSNOW_HBV          # RAINSNOW_DINGMAN                                                                      
#:OroTempCorrect        OROCORR_SIMPLELAPSE                                                                   
#:OroPrecipCorrect      OROCORR_SIMPLELAPSE      

#
# --Hydrologic Processes-------------------------
:Alias       Forest_Floor   SOIL[0]
:Alias       Ablation_Till  SOIL[1]
:Alias       Basal_Till     SOIL[2]


#

:EvaluationPeriod CALIBRATION 2015-10-01 2022-09-30
#:EvaluationPeriod VALIDATION  2018-01-01 2020-10-20


:HydrologicProcesses
#
  :SnowRefreeze      FREEZE_DEGREE_DAY            SNOW_LIQ         SNOW
  :Precipitation     PRECIP_RAVEN                 ATMOS_PRECIP     MULTIPLE
#
  :CanopyEvaporation CANEVP_ALL         CANOPY           ATMOSPHERE
  :CanopySnowEvap    CANEVP_ALL         CANOPY_SNOW      ATMOSPHERE
#   
  :SnowBalance       SNOBAL_SIMPLE_MELT           SNOW             SNOW_LIQ                    #:SnowBalance       SNOBAL_TWO_LAYER   MULTIPLE         MULTIPLE     # :SnowBalance       SNOBAL_SIMPLE_MELT SNOW             PONDED_WATER
  :-->Overflow       RAVEN_DEFAULT                SNOW_LIQ         PONDED_WATER                                                                                                                                                            #:-->Overflow     RAVEN_DEFAULT      SNOW_LIQ         PONDED_WATER
#
## Added by Menaka 2024/01/12 as in Ming's Experiment S10_1
  :OpenWaterEvaporation  OPEN_WATER_EVAP  PONDED_WATER   ATMOSPHERE   # OPEN WATER EVAP FOR LAKE HRU
        :-->Conditional LAND_CLASS IS LAKE
  :Flush              RAVEN_DEFAULT  PONDED_WATER   SURFACE_WATER  # P from lake hru to channel 
        :-->Conditional LAND_CLASS IS LAKE		
#    
  :Infiltration      INF_GREEN_AMPT               PONDED_WATER     MULTIPLE   
  ### Forest_Floor
  :SoilEvaporation   SOILEVAP_SEQUEN              Forest_Floor     ATMOSPHERE
#
  :Percolation       PERC_GAWSER_CONSTRAIN        Forest_Floor     Ablation_Till   
  :Baseflow          BASE_THRESH_POWER            Forest_Floor     SURFACE_WATER 
  ### Ablation_Till
  :Baseflow          BASE_THRESH_POWER             Ablation_Till    SURFACE_WATER
  :Percolation       PERC_GAWSER_CONSTRAIN         Ablation_Till    Basal_Till
  ### Basal_Till
  :Baseflow          BASE_THRESH_POWER             Basal_Till       SURFACE_WATER
  :CapillaryRise     CRISE_HBV                     Basal_Till       Ablation_Till
#  
:EndHydrologicProcesses


#---------------------------------------------------------                                                 
# Output Options                                                                                           
#
:WriteForcingFunctions 
:WriteWaterLevels 
:WriteMassBalanceFile 
:WriteReservoirMBFile
:EvaluationMetrics NASH_SUTCLIFFE RMSE KLING_GUPTA KLING_GUPTA_DEVIATION R2 SPEARMAN KLING_GUPTA_PRIME KLING_GUPTA_DEVIATION_PRIME
EOF

#----------------------------------------------------------------------------------------
# edit rvi file
rvt='Petawawa.rvt'
rm -r ${rvt}
cat >> ${rvt} << EOF
#########################################################################                                  
:FileType          rvt ASCII Raven 2.8.2                                                                              
:WrittenBy         Juliane Mai & James Craig                                                                             
:CreationDate      Sep 2018
#
# Simulation of Petawawa                                                          
#------------------------------------------------------------------------

# meteorological forcings
:Gauge ECCC_PETAWAWAHOFFMAN
  :Latitude    45.8684
  :Longitude   -77.7567
  :Elevation  227.63021851
  :RedirectToFile forcing/ECCC_PETAWAWAHOFFMAN.rvt
:EndGauge

:Gauge MNRF_Achray
  :Latitude    45.88
  :Longitude   -77.25
  :Elevation  153
  :RedirectToFile forcing/MNRF_Achray.rvt
:EndGauge

:Gauge MNRF_Hogan
  :Latitude    45.8558
  :Longitude   -78.434
  :Elevation  442.86273193
  :RedirectToFile forcing/MNRF_Hogan.rvt
:EndGauge

:Gauge MNRF_Tim
  :Latitude    45.7872
  :Longitude   -78.9369
  :Elevation  452.98544312
  :RedirectToFile forcing/MNRF_Tim.rvt
:EndGauge


# Stream Flow Observation
:RedirectToFile    ./obs/SF_IS_02KB001_921.rvt   #02KB001

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/SF_IS_02KB001_921_weight.rvt


# Lake Water Level Observation
:RedirectToFile    ./obs/WL_IS_108083_767.rvt    #Traverse
:RedirectToFile    ./obs/WL_IS_108369_241.rvt    #La Muir
:RedirectToFile    ./obs/WL_IS_108564_135.rvt    #Misty
:RedirectToFile    ./obs/WL_IS_1032844_281.rvt   #Narrowbag
:RedirectToFile    ./obs/WL_IS_108015_449.rvt    #Little Cauchon
:RedirectToFile    ./obs/WL_IS_108347_753.rvt    #Grand
:RedirectToFile    ./obs/WL_IS_108126_574.rvt    #Radiant
:RedirectToFile    ./obs/WL_IS_8767_326.rvt      #Lavieille
:RedirectToFile    ./obs/WL_IS_108404_122.rvt    #Loontail
:RedirectToFile    ./obs/WL_IS_8741_528.rvt      #Cedar
:RedirectToFile    ./obs/WL_IS_8781_220.rvt      #Big Trout
:RedirectToFile    ./obs/WL_IS_8762_291.rvt      #Hogan
:RedirectToFile    ./obs/WL_IS_108027_497.rvt    #North Depot
:RedirectToFile    ./obs/WL_IS_1034779_345.rvt   #Animoosh
:RedirectToFile    ./obs/WL_IS_108379_228.rvt    #Burntroot
:RedirectToFile    ./obs/WL_IS_1033439_381.rvt   #Charles
:RedirectToFile    ./obs/WL_IS_1035812_48.rvt    #Hambone
:RedirectToFile    ./obs/WL_IS_1036038_117.rvt   #Lilypond
:RedirectToFile    ./obs/WL_IS_108585_116.rvt    #Timberwolf

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/WL_IS_108083_767_weight.rvt
:RedirectToFile    ./obs/WL_IS_108369_241_weight.rvt
:RedirectToFile    ./obs/WL_IS_108564_135_weight.rvt
:RedirectToFile    ./obs/WL_IS_1032844_281_weight.rvt
:RedirectToFile    ./obs/WL_IS_108015_449_weight.rvt
:RedirectToFile    ./obs/WL_IS_108347_753_weight.rvt
:RedirectToFile    ./obs/WL_IS_108126_574_weight.rvt
:RedirectToFile    ./obs/WL_IS_8767_326_weight.rvt
:RedirectToFile    ./obs/WL_IS_108404_122_weight.rvt
:RedirectToFile    ./obs/WL_IS_8741_528_weight.rvt
:RedirectToFile    ./obs/WL_IS_8781_220_weight.rvt
:RedirectToFile    ./obs/WL_IS_8762_291_weight.rvt
:RedirectToFile    ./obs/WL_IS_108027_497_weight.rvt
:RedirectToFile    ./obs/WL_IS_1034779_345_weight.rvt
:RedirectToFile    ./obs/WL_IS_108379_228_weight.rvt
:RedirectToFile    ./obs/WL_IS_1033439_381_weight.rvt
:RedirectToFile    ./obs/WL_IS_1035812_48_weight.rvt 
:RedirectToFile    ./obs/WL_IS_1036038_117_weight.rvt
:RedirectToFile    ./obs/WL_IS_108585_116_weight.rvt

# Lake Water Area 
:RedirectToFile    ./obs/WA_RS_1035335_41.rvt    #1035335.0
:RedirectToFile    ./obs/WA_RS_108435_315.rvt    #108435.0
:RedirectToFile    ./obs/WA_RS_1034038_142.rvt   #1034038.0
:RedirectToFile    ./obs/WA_RS_1033025_277.rvt   #1033025.0
:RedirectToFile    ./obs/WA_RS_1032273_747.rvt   #1032273.0
:RedirectToFile    ./obs/WA_RS_1032168_803.rvt   #1032168.0
:RedirectToFile    ./obs/WA_RS_1033541_327.rvt   #1033541.0
:RedirectToFile    ./obs/WA_RS_1034546_36.rvt    #1034546.0
:RedirectToFile    ./obs/WA_RS_108585_116.rvt    #Timberwolf
:RedirectToFile    ./obs/WA_RS_108316_126.rvt    #108316.0
:RedirectToFile    ./obs/WA_RS_1031109_415.rvt   #1031109.0
:RedirectToFile    ./obs/WA_RS_1034014_307.rvt   #1034014.0
:RedirectToFile    ./obs/WA_RS_1033787_138.rvt   #1033787.0
:RedirectToFile    ./obs/WA_RS_1033705_861.rvt   #1033705.0
:RedirectToFile    ./obs/WA_RS_1032918_405.rvt   #1032918.0
:RedirectToFile    ./obs/WA_RS_1033851_794.rvt   #1033851.0
:RedirectToFile    ./obs/WA_RS_1035236_113.rvt   #1035236.0
:RedirectToFile    ./obs/WA_RS_1032359_843.rvt   #1032359.0
:RedirectToFile    ./obs/WA_RS_1032522_737.rvt   #1032522.0
:RedirectToFile    ./obs/WA_RS_1033727_313.rvt   #1033727.0
:RedirectToFile    ./obs/WA_RS_1035983_50.rvt    #1035983.0
:RedirectToFile    ./obs/WA_RS_1035248_217.rvt   #1035248.0
:RedirectToFile    ./obs/WA_RS_1035231_112.rvt   #1035231.0
:RedirectToFile    ./obs/WA_RS_1031942_352.rvt   #1031942.0
:RedirectToFile    ./obs/WA_RS_1035677_207.rvt   #1035677.0
:RedirectToFile    ./obs/WA_RS_1033627_921.rvt   #02KB001
:RedirectToFile    ./obs/WA_RS_108506_78.rvt     #108506.0
:RedirectToFile    ./obs/WA_RS_1032769_399.rvt   #1032769.0
:RedirectToFile    ./obs/WA_RS_1033915_720.rvt   #1033915.0
:RedirectToFile    ./obs/WA_RS_1031014_304.rvt   #1031014.0
:RedirectToFile    ./obs/WA_RS_1032691_646.rvt   #1032691.0
:RedirectToFile    ./obs/WA_RS_1034075_544.rvt   #1034075.0
:RedirectToFile    ./obs/WA_RS_108394_258.rvt    #108394.0
:RedirectToFile    ./obs/WA_RS_108604_111.rvt    #108604.0
:RedirectToFile    ./obs/WA_RS_1032780_596.rvt   #1032780.0
:RedirectToFile    ./obs/WA_RS_1034708_344.rvt   #1034708.0
:RedirectToFile    ./obs/WA_RS_108348_754.rvt    #108348.0
:RedirectToFile    ./obs/WA_RS_1034574_321.rvt   #1034574.0
:RedirectToFile    ./obs/WA_RS_108257_704.rvt    #108257.0
:RedirectToFile    ./obs/WA_RS_1031839_452.rvt   #1031839.0
:RedirectToFile    ./obs/WA_RS_1033850_543.rvt   #1033850.0
:RedirectToFile    ./obs/WA_RS_1034091_536.rvt   #1034091.0
:RedirectToFile    ./obs/WA_RS_1033704_379.rvt   #1033704.0
:RedirectToFile    ./obs/WA_RS_1034122_859.rvt   #1034122.0
:RedirectToFile    ./obs/WA_RS_108175_276.rvt    #108175.0
:RedirectToFile    ./obs/WA_RS_1035432_87.rvt    #1035432.0
:RedirectToFile    ./obs/WA_RS_1032797_650.rvt   #1032797.0
:RedirectToFile    ./obs/WA_RS_1031844_427.rvt   #1031844.0
:RedirectToFile    ./obs/WA_RS_1035069_216.rvt   #1035069.0
:RedirectToFile    ./obs/WA_RS_108083_767.rvt    #Traverse
:RedirectToFile    ./obs/WA_RS_1032285_354.rvt   #1032285.0
:RedirectToFile    ./obs/WA_RS_1031986_430.rvt   #1031986.0
:RedirectToFile    ./obs/WA_RS_1031979_429.rvt   #1031979.0
:RedirectToFile    ./obs/WA_RS_1034245_267.rvt   #1034245.0
:RedirectToFile    ./obs/WA_RS_1034926_319.rvt   #1034926.0
:RedirectToFile    ./obs/WA_RS_1033549_847.rvt   #1033549.0
:RedirectToFile    ./obs/WA_RS_108233_377.rvt    #108233.0
:RedirectToFile    ./obs/WA_RS_108379_228.rvt    #Burntroot
:RedirectToFile    ./obs/WA_RS_1031908_623.rvt   #1031908.0
:RedirectToFile    ./obs/WA_RS_1033206_496.rvt   #1033206.0
:RedirectToFile    ./obs/WA_RS_1031173_391.rvt   #1031173.0
:RedirectToFile    ./obs/WA_RS_108500_73.rvt     #108500.0
:RedirectToFile    ./obs/WA_RS_1031664_299.rvt   #1031664.0
:RedirectToFile    ./obs/WA_RS_1033877_140.rvt   #1033877.0
:RedirectToFile    ./obs/WA_RS_1031300_421.rvt   #1031300.0
:RedirectToFile    ./obs/WA_RS_1034933_655.rvt   #1034933.0
:RedirectToFile    ./obs/WA_RS_108226_901.rvt    #108226.0
:RedirectToFile    ./obs/WA_RS_1032827_786.rvt   #1032827.0
:RedirectToFile    ./obs/WA_RS_1033173_615.rvt   #1033173.0
:RedirectToFile    ./obs/WA_RS_1033422_407.rvt   #1033422.0
:RedirectToFile    ./obs/WA_RS_1034625_658.rvt   #1034625.0
:RedirectToFile    ./obs/WA_RS_1034874_205.rvt   #1034874.0
:RedirectToFile    ./obs/WA_RS_108470_164.rvt    #108470.0
:RedirectToFile    ./obs/WA_RS_1032869_876.rvt   #1032869.0
:RedirectToFile    ./obs/WA_RS_1034674_343.rvt   #1034674.0
:RedirectToFile    ./obs/WA_RS_1034400_341.rvt   #1034400.0
:RedirectToFile    ./obs/WA_RS_1032819_282.rvt   #1032819.0
:RedirectToFile    ./obs/WA_RS_108369_241.rvt    #La Muir
:RedirectToFile    ./obs/WA_RS_1035755_46.rvt    #1035755.0
:RedirectToFile    ./obs/WA_RS_1032552_667.rvt   #1032552.0
:RedirectToFile    ./obs/WA_RS_1034337_123.rvt   #1034337.0
:RedirectToFile    ./obs/WA_RS_108451_260.rvt    #108451.0
:RedirectToFile    ./obs/WA_RS_1032502_738.rvt   #1032502.0
:RedirectToFile    ./obs/WA_RS_1034293_147.rvt   #1034293.0
:RedirectToFile    ./obs/WA_RS_1032227_504.rvt   #1032227.0
:RedirectToFile    ./obs/WA_RS_1034100_237.rvt   #1034100.0
:RedirectToFile    ./obs/WA_RS_1033519_751.rvt   #1033519.0
:RedirectToFile    ./obs/WA_RS_1031634_451.rvt   #1031634.0
:RedirectToFile    ./obs/WA_RS_1034317_724.rvt   #1034317.0
:RedirectToFile    ./obs/WA_RS_1033548_312.rvt   #1033548.0
:RedirectToFile    ./obs/WA_RS_1032102_673.rvt   #1032102.0
:RedirectToFile    ./obs/WA_RS_1031744_426.rvt   #1031744.0
:RedirectToFile    ./obs/WA_RS_1032101_525.rvt   #1032101.0
:RedirectToFile    ./obs/WA_RS_1033884_863.rvt   #1033884.0
:RedirectToFile    ./obs/WA_RS_1035551_62.rvt    #1035551.0
:RedirectToFile    ./obs/WA_RS_1034132_144.rvt   #1034132.0
:RedirectToFile    ./obs/WA_RS_1033712_792.rvt   #1033712.0
:RedirectToFile    ./obs/WA_RS_1031604_744.rvt   #1031604.0
:RedirectToFile    ./obs/WA_RS_1033084_375.rvt   #1033084.0
:RedirectToFile    ./obs/WA_RS_1034246_657.rvt   #1034246.0
:RedirectToFile    ./obs/WA_RS_1035297_218.rvt   #1035297.0
:RedirectToFile    ./obs/WA_RS_1033094_403.rvt   #1033094.0
:RedirectToFile    ./obs/WA_RS_108564_135.rvt    #Misty
:RedirectToFile    ./obs/WA_RS_1031318_443.rvt   #1031318.0
:RedirectToFile    ./obs/WA_RS_1031964_501.rvt   #1031964.0
:RedirectToFile    ./obs/WA_RS_1035727_57.rvt    #1035727.0
:RedirectToFile    ./obs/WA_RS_1033905_795.rvt   #1033905.0
:RedirectToFile    ./obs/WA_RS_1031261_419.rvt   #1031261.0
:RedirectToFile    ./obs/WA_RS_1033145_902.rvt   #1033145.0
:RedirectToFile    ./obs/WA_RS_1035794_58.rvt    #1035794.0
:RedirectToFile    ./obs/WA_RS_1034212_335.rvt   #1034212.0
:RedirectToFile    ./obs/WA_RS_1032851_610.rvt   #1032851.0
:RedirectToFile    ./obs/WA_RS_1033900_236.rvt   #1033900.0
:RedirectToFile    ./obs/WA_RS_1034741_654.rvt   #1034741.0
:RedirectToFile    ./obs/WA_RS_1032953_582.rvt   #1032953.0
:RedirectToFile    ./obs/WA_RS_1034144_553.rvt   #1034144.0
:RedirectToFile    ./obs/WA_RS_1032844_281.rvt   #Narrowbag
:RedirectToFile    ./obs/WA_RS_1034866_82.rvt    #1034866.0
:RedirectToFile    ./obs/WA_RS_1034854_69.rvt    #1034854.0
:RedirectToFile    ./obs/WA_RS_1033635_273.rvt   #1033635.0
:RedirectToFile    ./obs/WA_RS_108303_919.rvt    #108303.0
:RedirectToFile    ./obs/WA_RS_1032345_666.rvt   #1032345.0
:RedirectToFile    ./obs/WA_RS_1031870_502.rvt   #1031870.0
:RedirectToFile    ./obs/WA_RS_1031683_450.rvt   #1031683.0
:RedirectToFile    ./obs/WA_RS_1034140_227.rvt   #1034140.0
:RedirectToFile    ./obs/WA_RS_108193_875.rvt    #108193.0
:RedirectToFile    ./obs/WA_RS_108015_449.rvt    #Little Cauchon
:RedirectToFile    ./obs/WA_RS_1034409_549.rvt   #1034409.0
:RedirectToFile    ./obs/WA_RS_1032458_580.rvt   #1032458.0
:RedirectToFile    ./obs/WA_RS_1033144_810.rvt   #1033144.0
:RedirectToFile    ./obs/WA_RS_1034597_268.rvt   #1034597.0
:RedirectToFile    ./obs/WA_RS_1032986_692.rvt   #1032986.0
:RedirectToFile    ./obs/WA_RS_1033299_330.rvt   #1033299.0
:RedirectToFile    ./obs/WA_RS_1032795_520.rvt   #1032795.0
:RedirectToFile    ./obs/WA_RS_1033132_495.rvt   #1033132.0
:RedirectToFile    ./obs/WA_RS_1031873_745.rvt   #1031873.0
:RedirectToFile    ./obs/WA_RS_1034695_148.rvt   #1034695.0
:RedirectToFile    ./obs/WA_RS_1031362_500.rvt   #1031362.0
:RedirectToFile    ./obs/WA_RS_1034101_760.rvt   #1034101.0
:RedirectToFile    ./obs/WA_RS_1031919_428.rvt   #1031919.0
:RedirectToFile    ./obs/WA_RS_1031624_442.rvt   #1031624.0
:RedirectToFile    ./obs/WA_RS_1031745_789.rvt   #1031745.0
:RedirectToFile    ./obs/WA_RS_1033557_862.rvt   #1033557.0
:RedirectToFile    ./obs/WA_RS_1033131_376.rvt   #1033131.0
:RedirectToFile    ./obs/WA_RS_1032609_739.rvt   #1032609.0
:RedirectToFile    ./obs/WA_RS_1031283_441.rvt   #1031283.0
:RedirectToFile    ./obs/WA_RS_107949_294.rvt    #107949.0
:RedirectToFile    ./obs/WA_RS_1033211_310.rvt   #1033211.0
:RedirectToFile    ./obs/WA_RS_1032312_587.rvt   #1032312.0
:RedirectToFile    ./obs/WA_RS_108509_215.rvt    #108509.0
:RedirectToFile    ./obs/WA_RS_1034633_659.rvt   #1034633.0
:RedirectToFile    ./obs/WA_RS_108446_77.rvt     #108446.0
:RedirectToFile    ./obs/WA_RS_1034801_71.rvt    #1034801.0
:RedirectToFile    ./obs/WA_RS_1030966_302.rvt   #1030966.0
:RedirectToFile    ./obs/WA_RS_1035858_210.rvt   #1035858.0
:RedirectToFile    ./obs/WA_RS_1034048_143.rvt   #1034048.0
:RedirectToFile    ./obs/WA_RS_108614_47.rvt     #108614.0
:RedirectToFile    ./obs/WA_RS_1034740_221.rvt   #1034740.0
:RedirectToFile    ./obs/WA_RS_1030543_417.rvt   #1030543.0
:RedirectToFile    ./obs/WA_RS_1031538_422.rvt   #1031538.0
:RedirectToFile    ./obs/WA_RS_1031841_808.rvt   #1031841.0
:RedirectToFile    ./obs/WA_RS_1033765_338.rvt   #1033765.0
:RedirectToFile    ./obs/WA_RS_1032210_499.rvt   #1032210.0
:RedirectToFile    ./obs/WA_RS_108347_753.rvt    #Grand
:RedirectToFile    ./obs/WA_RS_1032551_559.rvt   #1032551.0
:RedirectToFile    ./obs/WA_RS_1034612_342.rvt   #1034612.0
:RedirectToFile    ./obs/WA_RS_1034890_83.rvt    #1034890.0
:RedirectToFile    ./obs/WA_RS_1034185_687.rvt   #1034185.0
:RedirectToFile    ./obs/WA_RS_1034662_167.rvt   #1034662.0
:RedirectToFile    ./obs/WA_RS_1034213_547.rvt   #1034213.0
:RedirectToFile    ./obs/WA_RS_1033490_250.rvt   #1033490.0
:RedirectToFile    ./obs/WA_RS_1034585_202.rvt   #1034585.0
:RedirectToFile    ./obs/WA_RS_1034487_165.rvt   #1034487.0
:RedirectToFile    ./obs/WA_RS_1035566_43.rvt    #1035566.0
:RedirectToFile    ./obs/WA_RS_108126_574.rvt    #Radiant
:RedirectToFile    ./obs/WA_RS_1032092_802.rvt   #1032092.0
:RedirectToFile    ./obs/WA_RS_1031002_303.rvt   #1031002.0
:RedirectToFile    ./obs/WA_RS_1033817_235.rvt   #1033817.0
:RedirectToFile    ./obs/WA_RS_1033345_328.rvt   #1033345.0
:RedirectToFile    ./obs/WA_RS_1034389_243.rvt   #1034389.0
:RedirectToFile    ./obs/WA_RS_1034707_67.rvt    #1034707.0
:RedirectToFile    ./obs/WA_RS_1033977_864.rvt   #1033977.0
:RedirectToFile    ./obs/WA_RS_1033509_717.rvt   #1033509.0
:RedirectToFile    ./obs/WA_RS_1032906_283.rvt   #1032906.0
:RedirectToFile    ./obs/WA_RS_1032671_740.rvt   #1032671.0
:RedirectToFile    ./obs/WA_RS_1034033_129.rvt   #1034033.0
:RedirectToFile    ./obs/WA_RS_1033908_229.rvt   #1033908.0
:RedirectToFile    ./obs/WA_RS_1032634_575.rvt   #1032634.0
:RedirectToFile    ./obs/WA_RS_1034632_65.rvt    #1034632.0
:RedirectToFile    ./obs/WA_RS_1033298_278.rvt   #1033298.0
:RedirectToFile    ./obs/WA_RS_1033116_361.rvt   #1033116.0
:RedirectToFile    ./obs/WA_RS_1034436_133.rvt   #1034436.0
:RedirectToFile    ./obs/WA_RS_1034867_204.rvt   #1034867.0
:RedirectToFile    ./obs/WA_RS_1032404_279.rvt   #1032404.0
:RedirectToFile    ./obs/WA_RS_1033077_406.rvt   #1033077.0
:RedirectToFile    ./obs/WA_RS_1034634_203.rvt   #1034634.0
:RedirectToFile    ./obs/WA_RS_8767_326.rvt      #Lavieille
:RedirectToFile    ./obs/WA_RS_1034936_74.rvt    #1034936.0
:RedirectToFile    ./obs/WA_RS_1031452_770.rvt   #1031452.0
:RedirectToFile    ./obs/WA_RS_1031609_462.rvt   #1031609.0
:RedirectToFile    ./obs/WA_RS_1032580_887.rvt   #1032580.0
:RedirectToFile    ./obs/WA_RS_1033643_554.rvt   #1033643.0
:RedirectToFile    ./obs/WA_RS_1034584_201.rvt   #1034584.0
:RedirectToFile    ./obs/WA_RS_1033363_247.rvt   #1033363.0
:RedirectToFile    ./obs/WA_RS_107978_459.rvt    #107978.0
:RedirectToFile    ./obs/WA_RS_1033852_867.rvt   #1033852.0
:RedirectToFile    ./obs/WA_RS_1031410_807.rvt   #1031410.0
:RedirectToFile    ./obs/WA_RS_1034034_230.rvt   #1034034.0
:RedirectToFile    ./obs/WA_RS_1033350_716.rvt   #1033350.0
:RedirectToFile    ./obs/WA_RS_1033491_311.rvt   #1033491.0
:RedirectToFile    ./obs/WA_RS_1032591_481.rvt   #1032591.0
:RedirectToFile    ./obs/WA_RS_1033162_457.rvt   #1033162.0
:RedirectToFile    ./obs/WA_RS_108541_81.rvt     #108541.0
:RedirectToFile    ./obs/WA_RS_1031779_529.rvt   #1031779.0
:RedirectToFile    ./obs/WA_RS_1031889_799.rvt   #1031889.0
:RedirectToFile    ./obs/WA_RS_1034841_214.rvt   #1034841.0
:RedirectToFile    ./obs/WA_RS_8778_322.rvt      #8778.0
:RedirectToFile    ./obs/WA_RS_1031887_424.rvt   #1031887.0
:RedirectToFile    ./obs/WA_RS_108275_246.rvt    #108275.0
:RedirectToFile    ./obs/WA_RS_1030949_301.rvt   #1030949.0
:RedirectToFile    ./obs/WA_RS_108465_200.rvt    #108465.0
:RedirectToFile    ./obs/WA_RS_1034611_124.rvt   #1034611.0
:RedirectToFile    ./obs/WA_RS_1032645_480.rvt   #1032645.0
:RedirectToFile    ./obs/WA_RS_108618_61.rvt     #108618.0
:RedirectToFile    ./obs/WA_RS_1031008_390.rvt   #1031008.0
:RedirectToFile    ./obs/WA_RS_1034453_225.rvt   #1034453.0
:RedirectToFile    ./obs/WA_RS_1036081_51.rvt    #1036081.0
:RedirectToFile    ./obs/WA_RS_1034051_130.rvt   #1034051.0
:RedirectToFile    ./obs/WA_RS_1032421_584.rvt   #1032421.0
:RedirectToFile    ./obs/WA_RS_108404_122.rvt    #Loontail
:RedirectToFile    ./obs/WA_RS_1034755_68.rvt    #1034755.0
:RedirectToFile    ./obs/WA_RS_1035996_211.rvt   #1035996.0
:RedirectToFile    ./obs/WA_RS_1031625_298.rvt   #1031625.0
:RedirectToFile    ./obs/WA_RS_1035399_136.rvt   #1035399.0
:RedirectToFile    ./obs/WA_RS_1033669_253.rvt   #1033669.0
:RedirectToFile    ./obs/WA_RS_1035854_59.rvt    #1035854.0
:RedirectToFile    ./obs/WA_RS_1035235_86.rvt    #1035235.0
:RedirectToFile    ./obs/WA_RS_1033970_540.rvt   #1033970.0
:RedirectToFile    ./obs/WA_RS_1032603_585.rvt   #1032603.0
:RedirectToFile    ./obs/WA_RS_1033546_251.rvt   #1033546.0
:RedirectToFile    ./obs/WA_RS_1033458_538.rvt   #1033458.0
:RedirectToFile    ./obs/WA_RS_1033837_541.rvt   #1033837.0
:RedirectToFile    ./obs/WA_RS_1034552_336.rvt   #1034552.0
:RedirectToFile    ./obs/WA_RS_1034444_120.rvt   #1034444.0
:RedirectToFile    ./obs/WA_RS_1033127_886.rvt   #1033127.0
:RedirectToFile    ./obs/WA_RS_1034705_66.rvt    #1034705.0
:RedirectToFile    ./obs/WA_RS_1032539_280.rvt   #1032539.0
:RedirectToFile    ./obs/WA_RS_1033117_612.rvt   #1033117.0
:RedirectToFile    ./obs/WA_RS_1033678_274.rvt   #1033678.0
:RedirectToFile    ./obs/WA_RS_1034386_548.rvt   #1034386.0
:RedirectToFile    ./obs/WA_RS_1032218_503.rvt   #1032218.0
:RedirectToFile    ./obs/WA_RS_1035622_63.rvt    #1035622.0
:RedirectToFile    ./obs/WA_RS_1033862_128.rvt   #1033862.0
:RedirectToFile    ./obs/WA_RS_8741_528.rvt      #Cedar
:RedirectToFile    ./obs/WA_RS_108298_249.rvt    #108298.0
:RedirectToFile    ./obs/WA_RS_1033916_869.rvt   #1033916.0
:RedirectToFile    ./obs/WA_RS_1031292_420.rvt   #1031292.0
:RedirectToFile    ./obs/WA_RS_1032749_742.rvt   #1032749.0
:RedirectToFile    ./obs/WA_RS_1032083_800.rvt   #1032083.0
:RedirectToFile    ./obs/WA_RS_1031451_460.rvt   #1031451.0
:RedirectToFile    ./obs/WA_RS_1032794_519.rvt   #1032794.0
:RedirectToFile    ./obs/WA_RS_1032390_579.rvt   #1032390.0
:RedirectToFile    ./obs/WA_RS_1036038_117.rvt   #Lilypond
:RedirectToFile    ./obs/WA_RS_1034125_131.rvt   #1034125.0
:RedirectToFile    ./obs/WA_RS_1034305_316.rvt   #1034305.0
:RedirectToFile    ./obs/WA_RS_8781_220.rvt      #Big Trout
:RedirectToFile    ./obs/WA_RS_1031843_465.rvt   #1031843.0
:RedirectToFile    ./obs/WA_RS_1032676_397.rvt   #1032676.0
:RedirectToFile    ./obs/WA_RS_1030917_389.rvt   #1030917.0
:RedirectToFile    ./obs/WA_RS_1032677_398.rvt   #1032677.0
:RedirectToFile    ./obs/WA_RS_1031435_295.rvt   #1031435.0
:RedirectToFile    ./obs/WA_RS_1031042_305.rvt   #1031042.0
:RedirectToFile    ./obs/WA_RS_1031615_466.rvt   #1031615.0
:RedirectToFile    ./obs/WA_RS_1033733_555.rvt   #1033733.0
:RedirectToFile    ./obs/WA_RS_1033035_402.rvt   #1033035.0
:RedirectToFile    ./obs/WA_RS_1035731_45.rvt    #1035731.0
:RedirectToFile    ./obs/WA_RS_1031965_586.rvt   #1031965.0
:RedirectToFile    ./obs/WA_RS_1033133_906.rvt   #1033133.0
:RedirectToFile    ./obs/WA_RS_1031162_363.rvt   #1031162.0
:RedirectToFile    ./obs/WA_RS_8762_291.rvt      #Hogan
:RedirectToFile    ./obs/WA_RS_1033928_865.rvt   #1033928.0
:RedirectToFile    ./obs/WA_RS_108324_552.rvt    #108324.0
:RedirectToFile    ./obs/WA_RS_1035812_48.rvt    #Hambone
:RedirectToFile    ./obs/WA_RS_1031733_464.rvt   #1031733.0
:RedirectToFile    ./obs/WA_RS_1034937_84.rvt    #1034937.0
:RedirectToFile    ./obs/WA_RS_1031714_522.rvt   #1031714.0
:RedirectToFile    ./obs/WA_RS_1032135_353.rvt   #1032135.0
:RedirectToFile    ./obs/WA_RS_108422_231.rvt    #108422.0
:RedirectToFile    ./obs/WA_RS_1034486_35.rvt    #1034486.0
:RedirectToFile    ./obs/WA_RS_1032240_665.rvt   #1032240.0
:RedirectToFile    ./obs/WA_RS_1032437_844.rvt   #1032437.0
:RedirectToFile    ./obs/WA_RS_1033508_248.rvt   #1033508.0
:RedirectToFile    ./obs/WA_RS_1035728_44.rvt    #1035728.0
:RedirectToFile    ./obs/WA_RS_1033670_718.rvt   #1033670.0
:RedirectToFile    ./obs/WA_RS_1034131_132.rvt   #1034131.0
:RedirectToFile    ./obs/WA_RS_1033831_719.rvt   #1033831.0
:RedirectToFile    ./obs/WA_RS_1034660_653.rvt   #1034660.0
:RedirectToFile    ./obs/WA_RS_108004_531.rvt    #108004.0
:RedirectToFile    ./obs/WA_RS_108027_497.rvt    #North Depot
:RedirectToFile    ./obs/WA_RS_1034459_290.rvt   #1034459.0
:RedirectToFile    ./obs/WA_RS_1033680_393.rvt   #1033680.0
:RedirectToFile    ./obs/WA_RS_1035210_85.rvt    #1035210.0
:RedirectToFile    ./obs/WA_RS_108494_652.rvt    #108494.0
:RedirectToFile    ./obs/WA_RS_1030908_388.rvt   #1030908.0
:RedirectToFile    ./obs/WA_RS_1031780_798.rvt   #1031780.0
:RedirectToFile    ./obs/WA_RS_1034198_686.rvt   #1034198.0
:RedirectToFile    ./obs/WA_RS_1031842_423.rvt   #1031842.0
:RedirectToFile    ./obs/WA_RS_1034133_308.rvt   #1034133.0
:RedirectToFile    ./obs/WA_RS_1035821_49.rvt    #1035821.0
:RedirectToFile    ./obs/WA_RS_1032796_598.rvt   #1032796.0
:RedirectToFile    ./obs/WA_RS_1034951_39.rvt    #1034951.0
:RedirectToFile    ./obs/WA_RS_1033587_127.rvt   #1033587.0
:RedirectToFile    ./obs/WA_RS_1032864_597.rvt   #1032864.0
:RedirectToFile    ./obs/WA_RS_1034779_345.rvt   #Animoosh
:RedirectToFile    ./obs/WA_RS_108638_209.rvt    #108638.0
:RedirectToFile    ./obs/WA_RS_1032044_578.rvt   #1032044.0
:RedirectToFile    ./obs/WA_RS_1031603_297.rvt   #1031603.0
:RedirectToFile    ./obs/WA_RS_1033439_381.rvt   #Charles
:RedirectToFile    ./obs/WA_RS_1034989_75.rvt    #1034989.0
:RedirectToFile    ./obs/WA_RS_1033959_880.rvt   #1033959.0
:RedirectToFile    ./obs/WA_RS_1035387_42.rvt    #1035387.0
:RedirectToFile    ./obs/WA_RS_1033280_669.rvt   #1033280.0
:RedirectToFile    ./obs/WA_RS_1032834_401.rvt   #1032834.0
:RedirectToFile    ./obs/WA_RS_1033982_542.rvt   #1033982.0
:RedirectToFile    ./obs/WA_RS_1033935_796.rvt   #1033935.0
:RedirectToFile    ./obs/WA_RS_1033803_758.rvt   #1033803.0
:RedirectToFile    ./obs/WA_RS_108357_334.rvt    #108357.0
:RedirectToFile    ./obs/WA_RS_1032651_649.rvt   #1032651.0
:RedirectToFile    ./obs/WA_RS_1034169_723.rvt   #1034169.0
:RedirectToFile    ./obs/WA_RS_108567_110.rvt    #108567.0
:RedirectToFile    ./obs/WA_RS_1031232_461.rvt   #1031232.0
:RedirectToFile    ./obs/WA_RS_1034859_317.rvt   #1034859.0
:RedirectToFile    ./obs/WA_RS_1034840_38.rvt    #1034840.0
:RedirectToFile    ./obs/WA_RS_1032373_355.rvt   #1032373.0
:RedirectToFile    ./obs/WA_RS_1031409_806.rvt   #1031409.0
:RedirectToFile    ./obs/WA_RS_1033237_616.rvt   #1033237.0
:RedirectToFile    ./obs/WA_RS_1034739_37.rvt    #1034739.0
:RedirectToFile    ./obs/WA_RS_1032217_483.rvt   #1032217.0
:RedirectToFile    ./obs/WA_RS_107912_485.rvt    #107912.0
:RedirectToFile    ./obs/WA_RS_1032652_645.rvt   #1032652.0
:RedirectToFile    ./obs/WA_RS_1033619_378.rvt   #1033619.0
:RedirectToFile    ./obs/WA_RS_1032579_396.rvt   #1032579.0
:RedirectToFile    ./obs/WA_RS_1034121_722.rvt   #1034121.0
:RedirectToFile    ./obs/WA_RS_1033838_793.rvt   #1033838.0
:RedirectToFile    ./obs/WA_RS_1030960_413.rvt   #1030960.0
:RedirectToFile    ./obs/WA_RS_1033971_797.rvt   #1033971.0
:RedirectToFile    ./obs/WA_RS_1033798_752.rvt   #1033798.0
:RedirectToFile    ./obs/WA_RS_1033034_384.rvt   #1033034.0
:RedirectToFile    ./obs/WA_RS_1035581_52.rvt    #1035581.0
:RedirectToFile    ./obs/WA_RS_1035460_88.rvt    #1035460.0
:RedirectToFile    ./obs/WA_RS_1032532_479.rvt   #1032532.0
:RedirectToFile    ./obs/WA_RS_1032963_611.rvt   #1032963.0
:RedirectToFile    ./obs/WA_RS_108041_351.rvt    #108041.0
:RedirectToFile    ./obs/WA_RS_1034663_660.rvt   #1034663.0
:RedirectToFile    ./obs/WA_RS_1033532_272.rvt   #1033532.0
:RedirectToFile    ./obs/WA_RS_1031710_463.rvt   #1031710.0
:RedirectToFile    ./obs/WA_RS_1034345_259.rvt   #1034345.0
:RedirectToFile    ./obs/WA_RS_1033588_252.rvt   #1033588.0
:RedirectToFile    ./obs/WA_RS_1035657_53.rvt    #1035657.0
:RedirectToFile    ./obs/WA_RS_1034361_261.rvt   #1034361.0
:RedirectToFile    ./obs/WA_RS_1034534_651.rvt   #1034534.0
:RedirectToFile    ./obs/WA_RS_1033640_539.rvt   #1033640.0
:RedirectToFile    ./obs/WA_RS_1033500_329.rvt   #1033500.0
:RedirectToFile    ./obs/WA_RS_1031153_440.rvt   #1031153.0
:RedirectToFile    ./obs/WA_RS_1032731_785.rvt   #1032731.0

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/WA_RS_1035335_41_weight.rvt
:RedirectToFile    ./obs/WA_RS_108435_315_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034038_142_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033025_277_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032273_747_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032168_803_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033541_327_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034546_36_weight.rvt
:RedirectToFile    ./obs/WA_RS_108585_116_weight.rvt
:RedirectToFile    ./obs/WA_RS_108316_126_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031109_415_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034014_307_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033787_138_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033705_861_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032918_405_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033851_794_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035236_113_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032359_843_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032522_737_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033727_313_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035983_50_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035248_217_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035231_112_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031942_352_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035677_207_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033627_921_weight.rvt
:RedirectToFile    ./obs/WA_RS_108506_78_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032769_399_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033915_720_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031014_304_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032691_646_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034075_544_weight.rvt
:RedirectToFile    ./obs/WA_RS_108394_258_weight.rvt
:RedirectToFile    ./obs/WA_RS_108604_111_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032780_596_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034708_344_weight.rvt
:RedirectToFile    ./obs/WA_RS_108348_754_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034574_321_weight.rvt
:RedirectToFile    ./obs/WA_RS_108257_704_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031839_452_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033850_543_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034091_536_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033704_379_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034122_859_weight.rvt
:RedirectToFile    ./obs/WA_RS_108175_276_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035432_87_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032797_650_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031844_427_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035069_216_weight.rvt
:RedirectToFile    ./obs/WA_RS_108083_767_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032285_354_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031986_430_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031979_429_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034245_267_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034926_319_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033549_847_weight.rvt
:RedirectToFile    ./obs/WA_RS_108233_377_weight.rvt
:RedirectToFile    ./obs/WA_RS_108379_228_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031908_623_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033206_496_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031173_391_weight.rvt
:RedirectToFile    ./obs/WA_RS_108500_73_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031664_299_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033877_140_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031300_421_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034933_655_weight.rvt
:RedirectToFile    ./obs/WA_RS_108226_901_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032827_786_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033173_615_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033422_407_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034625_658_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034874_205_weight.rvt
:RedirectToFile    ./obs/WA_RS_108470_164_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032869_876_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034674_343_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034400_341_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032819_282_weight.rvt
:RedirectToFile    ./obs/WA_RS_108369_241_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035755_46_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032552_667_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034337_123_weight.rvt
:RedirectToFile    ./obs/WA_RS_108451_260_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032502_738_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034293_147_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032227_504_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034100_237_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033519_751_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031634_451_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034317_724_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033548_312_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032102_673_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031744_426_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032101_525_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033884_863_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035551_62_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034132_144_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033712_792_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031604_744_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033084_375_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034246_657_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035297_218_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033094_403_weight.rvt
:RedirectToFile    ./obs/WA_RS_108564_135_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031318_443_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031964_501_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035727_57_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033905_795_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031261_419_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033145_902_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035794_58_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034212_335_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032851_610_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033900_236_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034741_654_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032953_582_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034144_553_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032844_281_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034866_82_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034854_69_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033635_273_weight.rvt
:RedirectToFile    ./obs/WA_RS_108303_919_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032345_666_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031870_502_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031683_450_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034140_227_weight.rvt
:RedirectToFile    ./obs/WA_RS_108193_875_weight.rvt
:RedirectToFile    ./obs/WA_RS_108015_449_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034409_549_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032458_580_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033144_810_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034597_268_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032986_692_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033299_330_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032795_520_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033132_495_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031873_745_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034695_148_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031362_500_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034101_760_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031919_428_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031624_442_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031745_789_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033557_862_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033131_376_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032609_739_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031283_441_weight.rvt
:RedirectToFile    ./obs/WA_RS_107949_294_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033211_310_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032312_587_weight.rvt
:RedirectToFile    ./obs/WA_RS_108509_215_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034633_659_weight.rvt
:RedirectToFile    ./obs/WA_RS_108446_77_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034801_71_weight.rvt
:RedirectToFile    ./obs/WA_RS_1030966_302_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035858_210_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034048_143_weight.rvt
:RedirectToFile    ./obs/WA_RS_108614_47_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034740_221_weight.rvt
:RedirectToFile    ./obs/WA_RS_1030543_417_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031538_422_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031841_808_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033765_338_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032210_499_weight.rvt
:RedirectToFile    ./obs/WA_RS_108347_753_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032551_559_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034612_342_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034890_83_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034185_687_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034662_167_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034213_547_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033490_250_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034585_202_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034487_165_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035566_43_weight.rvt
:RedirectToFile    ./obs/WA_RS_108126_574_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032092_802_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031002_303_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033817_235_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033345_328_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034389_243_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034707_67_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033977_864_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033509_717_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032906_283_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032671_740_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034033_129_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033908_229_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032634_575_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034632_65_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033298_278_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033116_361_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034436_133_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034867_204_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032404_279_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033077_406_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034634_203_weight.rvt
:RedirectToFile    ./obs/WA_RS_8767_326_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034936_74_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031452_770_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031609_462_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032580_887_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033643_554_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034584_201_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033363_247_weight.rvt
:RedirectToFile    ./obs/WA_RS_107978_459_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033852_867_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031410_807_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034034_230_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033350_716_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033491_311_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032591_481_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033162_457_weight.rvt
:RedirectToFile    ./obs/WA_RS_108541_81_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031779_529_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031889_799_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034841_214_weight.rvt
:RedirectToFile    ./obs/WA_RS_8778_322_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031887_424_weight.rvt
:RedirectToFile    ./obs/WA_RS_108275_246_weight.rvt
:RedirectToFile    ./obs/WA_RS_1030949_301_weight.rvt
:RedirectToFile    ./obs/WA_RS_108465_200_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034611_124_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032645_480_weight.rvt
:RedirectToFile    ./obs/WA_RS_108618_61_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031008_390_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034453_225_weight.rvt
:RedirectToFile    ./obs/WA_RS_1036081_51_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034051_130_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032421_584_weight.rvt
:RedirectToFile    ./obs/WA_RS_108404_122_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034755_68_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035996_211_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031625_298_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035399_136_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033669_253_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035854_59_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035235_86_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033970_540_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032603_585_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033546_251_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033458_538_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033837_541_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034552_336_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034444_120_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033127_886_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034705_66_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032539_280_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033117_612_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033678_274_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034386_548_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032218_503_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035622_63_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033862_128_weight.rvt
:RedirectToFile    ./obs/WA_RS_8741_528_weight.rvt
:RedirectToFile    ./obs/WA_RS_108298_249_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033916_869_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031292_420_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032749_742_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032083_800_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031451_460_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032794_519_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032390_579_weight.rvt
:RedirectToFile    ./obs/WA_RS_1036038_117_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034125_131_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034305_316_weight.rvt
:RedirectToFile    ./obs/WA_RS_8781_220_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031843_465_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032676_397_weight.rvt
:RedirectToFile    ./obs/WA_RS_1030917_389_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032677_398_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031435_295_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031042_305_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031615_466_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033733_555_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033035_402_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035731_45_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031965_586_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033133_906_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031162_363_weight.rvt
:RedirectToFile    ./obs/WA_RS_8762_291_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033928_865_weight.rvt
:RedirectToFile    ./obs/WA_RS_108324_552_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035812_48_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031733_464_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034937_84_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031714_522_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032135_353_weight.rvt
:RedirectToFile    ./obs/WA_RS_108422_231_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034486_35_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032240_665_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032437_844_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033508_248_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035728_44_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033670_718_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034131_132_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033831_719_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034660_653_weight.rvt
:RedirectToFile    ./obs/WA_RS_108004_531_weight.rvt
:RedirectToFile    ./obs/WA_RS_108027_497_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034459_290_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033680_393_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035210_85_weight.rvt
:RedirectToFile    ./obs/WA_RS_108494_652_weight.rvt
:RedirectToFile    ./obs/WA_RS_1030908_388_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031780_798_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034198_686_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031842_423_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034133_308_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035821_49_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032796_598_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034951_39_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033587_127_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032864_597_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034779_345_weight.rvt
:RedirectToFile    ./obs/WA_RS_108638_209_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032044_578_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031603_297_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033439_381_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034989_75_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033959_880_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035387_42_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033280_669_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032834_401_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033982_542_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033935_796_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033803_758_weight.rvt
:RedirectToFile    ./obs/WA_RS_108357_334_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032651_649_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034169_723_weight.rvt
:RedirectToFile    ./obs/WA_RS_108567_110_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031232_461_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034859_317_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034840_38_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032373_355_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031409_806_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033237_616_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034739_37_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032217_483_weight.rvt
:RedirectToFile    ./obs/WA_RS_107912_485_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032652_645_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033619_378_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032579_396_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034121_722_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033838_793_weight.rvt
:RedirectToFile    ./obs/WA_RS_1030960_413_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033971_797_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033798_752_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033034_384_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035581_52_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035460_88_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032532_479_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032963_611_weight.rvt
:RedirectToFile    ./obs/WA_RS_108041_351_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034663_660_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033532_272_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031710_463_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034345_259_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033588_252_weight.rvt
:RedirectToFile    ./obs/WA_RS_1035657_53_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034361_261_weight.rvt
:RedirectToFile    ./obs/WA_RS_1034534_651_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033640_539_weight.rvt
:RedirectToFile    ./obs/WA_RS_1033500_329_weight.rvt
:RedirectToFile    ./obs/WA_RS_1031153_440_weight.rvt
:RedirectToFile    ./obs/WA_RS_1032731_785_weight.rvt

# Discharge stream [for validation]
:RedirectToFile    ./obs/SF_IS_LittleMadawaska_400.rvt      #Little Madawaska Barometer
:RedirectToFile    ./obs/SF_IS_PetawawaRNarrowbag_288.rvt   #Petawawa River at Narrowbag
:RedirectToFile    ./obs/SF_IS_Crow_265.rvt                 #Crow River
:RedirectToFile    ./obs/SF_IS_NippissingCorrected_412.rvt  #Nipissing River

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/SF_IS_LittleMadawaska_400_weight.rvt
:RedirectToFile    ./obs/SF_IS_PetawawaRNarrowbag_288_weight.rvt
:RedirectToFile    ./obs/SF_IS_Crow_265_weight.rvt
:RedirectToFile    ./obs/SF_IS_NippissingCorrected_412_weight.rvt

# Water Level Stream [for validation]
:RedirectToFile    ./obs/WL_IS_LittleMadawaska_400.rvt      #Little Madawaska Barometer
:RedirectToFile    ./obs/WL_IS_PetawawaRNarrowbag_288.rvt   #Petawawa River at Narrowbag
:RedirectToFile    ./obs/WL_IS_Crow_265.rvt                 #Crow River
:RedirectToFile    ./obs/WL_IS_NippissingCorrected_412.rvt  #Nipissing River

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/WL_IS_LittleMadawaska_400_weight.rvt
:RedirectToFile    ./obs/WL_IS_PetawawaRNarrowbag_288_weight.rvt
:RedirectToFile    ./obs/WL_IS_Crow_265_weight.rvt
:RedirectToFile    ./obs/WL_IS_NippissingCorrected_412_weight.rvt
EOF
    ./Raven.exe Petawawa -o ./output

    cd ../../../..

done

wait

# # # The computations are done, so clean up the data set...
# # cd /scratch/menaka/LakeCalibrationout/out/${prefix}${expname}_${ens_num}
# # # mkdir -p out
# # # cd ./out  
# # rm -rf ./best_Raven
# # cp -r $SLURM_TMPDIR/work/LakeCalibration/out/${prefix}${expname}_${ens_num}/best_Raven . 