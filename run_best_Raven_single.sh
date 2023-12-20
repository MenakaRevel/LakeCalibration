#!/bin/bash

expname=${1} #'0a'
ens_num=`printf '%02d\n' "${2}"`

echo $expname $ens_num

# cd into 
cd ./out/S${expname}_${ens_num}/best/RavenInput
`pwd`

# edit rvi file
rvi='Petawawa.rvi'
rm -r ${rvi}
cat >> ${rvi} << EOF
# ----------------------------------------------
# Raven Input file
# HBV-EC Nith River emulation test case
# ----------------------------------------------
# --Simulation Details -------------------------
:RunName               Petawawa                                                                           
:StartDate             2015-01-01 00:00:00
:EndDate               2021-01-01 00:00:00           
:TimeStep              1.0

#
# --Model Details -------------------------------
:Method                 ORDERED_SERIES
:Interpolation          INTERP_NEAREST_NEIGHBOR
:SoilModel              SOIL_MULTILAYER 3


:Routing                ROUTE_HYDROLOGIC #ROUTE_HYDROLOGIC ROUTE_DIFFUSIVE_WAVE
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

:EvaluationPeriod CALIBRATION 2016-01-01 2020-10-20
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
:EvaluationMetrics NASH_SUTCLIFFE RMSE KLING_GUPTA KLING_GUPTA_DEVIATION R2 SPEARMAN
EOF

./Raven Petawawa -o ./output

cd ../..

wait 