#!/bin/bash

expname=${1} #'S0a'
ens_num=`printf '%02d\n' "${2}"`
obsname=${3}
ObsTypes1=${4}
ObsTypes2=${5}

# prefix
prefix="${expname:0:2}"
if [[ $prefix = "Re" ]] ; then
  prefix="${expname:0:2}"
  expname="${expname:2:3}"
  SF_prefix='SF_IS'
  WL_prefix='WL_IS'
  WA_prefix='WA_RS'
elif [[ ${prefix:0:1} = "V" ]] ; then
  prefix="${expname:0:1}"
  expname="${expname:1:3}"
  SF_prefix='SF_SY'
  WL_prefix='WL_SY'
  WA_prefix='WA_SY'
else
  prefix="${expname:0:1}"
  expname="${expname:1:3}"
  SF_prefix='SF_IS'
  WL_prefix='WL_IS'
  WA_prefix='WA_RS'
fi

echo $prefix$expname $SF_prefix $WL_prefix $WL_prefix
echo $prefix$expname $ens_num
echo ${prefix}${expname}_${ens_num}, `pwd`
rm -rf ./out/${prefix}${expname}_${ens_num}/best_Raven
mkdir -p ./out/${prefix}${expname}_${ens_num}/best_Raven
cd ./out/${prefix}${expname}_${ens_num}/best_Raven
cp -rf ../best/* . 
cd RavenInput

# observations
# rm -rf ./obs
# ln -sf $obsname ./obs
#----------------------------------------------------------------------------------------
# edit rvh file
rvh='Petawawa.rvh'
# Use sed to add a new line after a specific pattern (e.g., after line containing 'pattern')
# sed -i '1510a\:GaugedSubBasinGroup NonObservedLakesubbasins' "$rvh"
# sed -i '/:EndSubBasinGroup/a :GaugedSubBasinGroup   NonObservedLakesubbasins' "$rvh"
# # awk '/:SubBasinGroup   NonObservedLakesubbasins/,/:EndSubBasinGroup/ {
# #     print; 
# #     if ($0 ~ /:EndSubBasinGroup/) 
# #         print ":GaugedSubBasinGroup   NonObservedLakesubbasins"; 
# #     next 
# # }1' "$rvh" > temp && mv temp "$rvh"
# get observations for all subbasins
awk '/:SubBasinGroup   NonObservedLakesubbasins/,/:EndSubBasinGroup/ {
    print; 
    if ($0 ~ /:EndSubBasinGroup/) 
        print ":GaugedSubBasinGroup   Allsubbasins"; 
    next 
}1' "$rvh" > temp && mv temp "$rvh"
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
:EvaluationMetrics NASH_SUTCLIFFE RMSE KLING_GUPTA KLING_GUPTA_DEVIATION R2 SPEARMAN PCT_BIAS
EOF
#KLING_GUPTA_PRIME KLING_GUPTA_DEVIATION_PRIME
#----------------------------------------------------------------------------------------
# edit rvi file
rvt='Petawawa.rvt'
rm -r ${rvt}
cat >> ${rvt} << EOF
#########################################################################                                  
:FileType          rvt ASCII Raven                                                                             
:WrittenBy         Menaka                                                                            
:CreationDate      $(date)
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

EOF

#=====================================================================
# Discharge
#=====================================================================
if [[ ${prefix} = "E" || ${prefix} = "S" || ${prefix} = "Re" ]]; then
cat >> ${rvt} << EOF
#=====================================================================
# Stream Flow Observation
:RedirectToFile    ./obs/SF_IS_02KB001_921.rvt   #02KB001

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/SF_IS_02KB001_921_weight.rvt

#=====================================================================
# Calibration
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

#=====================================================================
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
elif [[ ${prefix} = "V" ]]; then
cat >> ${rvt} << EOF
#=====================================================================
# Stream Flow Observation
:RedirectToFile    ./obs/${SF_prefix}_02KB001_921.rvt
:RedirectToFile    ./obs/${SF_prefix}_PetawawaRNarrowbag_288.rvt
:RedirectToFile    ./obs/${SF_prefix}_Crow_265.rvt
:RedirectToFile    ./obs/${SF_prefix}_NippissingCorrected_412.rvt
:RedirectToFile    ./obs/${SF_prefix}_LittleMadawaska_400.rvt

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/${SF_prefix}_02KB001_921_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_PetawawaRNarrowbag_288_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_Crow_265_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_NippissingCorrected_412_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_LittleMadawaska_400_weight.rvt

#=====================================================================
# Stream Flow Observation
:RedirectToFile    ./obs/${SF_prefix}_sub386_386.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub313_313.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub285_285.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub428_428.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub923_923.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub482_482.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub430_430.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub747_747.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub328_328.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub658_658.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub547_547.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub413_413.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub689_689.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub402_402.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub549_549.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub67_67.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub326_326.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub717_717.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub252_252.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub35_35.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub344_344.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub597_597.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub81_81.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub548_548.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub758_758.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub574_574.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub78_78.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub83_83.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub71_71.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub791_791.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub255_255.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub329_329.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub666_666.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub655_655.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub906_906.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub585_585.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub800_800.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub448_448.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub34_34.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub137_137.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub125_125.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub114_114.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub227_227.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub283_283.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub792_792.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub479_479.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub577_577.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub131_131.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub706_706.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub335_335.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub668_668.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub664_664.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub587_587.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub494_494.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub687_687.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub42_42.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub332_332.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub124_124.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub530_530.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub304_304.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub44_44.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub122_122.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub555_555.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub688_688.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub262_262.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub49_49.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub316_316.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub866_866.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub248_248.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub301_301.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub59_59.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub575_575.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub876_876.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub52_52.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub768_768.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub861_861.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub613_613.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub142_142.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub412_412.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub323_323.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub50_50.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub863_863.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub293_293.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub200_200.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub400_400.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub126_126.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub306_306.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub201_201.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub363_363.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub404_404.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub322_322.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub468_468.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub753_753.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub905_905.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub752_752.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub644_644.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub73_73.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub396_396.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub327_327.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub806_806.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub757_757.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub221_221.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub423_423.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub426_426.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub539_539.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub340_340.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub843_843.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub558_558.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub796_796.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub39_39.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub519_519.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub611_611.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub58_58.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub865_865.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub447_447.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub724_724.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub480_480.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub483_483.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub454_454.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub467_467.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub760_760.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub749_749.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub143_143.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub793_793.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub225_225.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub254_254.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub762_762.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub460_460.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub441_441.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub223_223.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub795_795.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub415_415.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub542_542.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub546_546.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub610_610.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub277_277.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub880_880.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub167_167.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub62_62.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub583_583.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub505_505.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub287_287.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub531_531.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub377_377.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub612_612.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub654_654.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub921_921.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub86_86.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub378_378.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub657_657.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub667_667.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub761_761.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub401_401.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub268_268.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub236_236.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub844_844.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub538_538.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub463_463.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub487_487.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub362_362.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub123_123.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub37_37.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub875_875.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub352_352.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub502_502.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub341_341.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub130_130.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub337_337.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub79_79.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub507_507.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub278_278.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub232_232.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub653_653.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub113_113.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub61_61.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub686_686.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub552_552.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub321_321.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub858_858.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub55_55.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub543_543.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub383_383.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub218_218.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub140_140.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub867_867.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub616_616.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub770_770.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub784_784.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub744_744.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub345_345.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub719_719.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub499_499.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub274_274.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub351_351.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub450_450.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub745_745.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub665_665.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub622_622.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub132_132.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub276_276.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub388_388.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub596_596.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub903_903.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub488_488.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub260_260.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub902_902.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub84_84.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub297_297.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub68_68.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub235_235.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub110_110.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub528_528.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub578_578.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub147_147.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub209_209.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub864_864.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub553_553.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub263_263.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub614_614.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub804_804.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub398_398.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub258_258.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub393_393.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub465_465.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub807_807.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub69_69.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub503_503.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub353_353.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub738_738.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub459_459.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub481_481.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub443_443.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub310_310.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub356_356.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub338_338.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub244_244.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub500_500.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub242_242.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub523_523.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub57_57.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub264_264.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub462_462.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub63_63.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub75_75.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub495_495.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub718_718.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub334_334.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub230_230.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub656_656.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub785_785.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub551_551.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub501_501.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub290_290.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub720_720.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub469_469.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub722_722.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub737_737.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub496_496.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub202_202.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub111_111.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub343_343.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub879_879.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub300_300.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub485_485.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub544_544.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub536_536.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub395_395.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub751_751.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub798_798.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub545_545.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub280_280.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub692_692.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub249_249.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub414_414.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub723_723.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub207_207.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub392_392.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub205_205.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub376_376.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub868_868.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub267_267.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub660_660.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub648_648.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub133_133.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub41_41.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub47_47.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub525_525.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub38_38.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub508_508.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub786_786.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub354_354.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub146_146.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub541_541.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub397_397.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub253_253.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub228_228.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub339_339.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub219_219.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub141_141.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub808_808.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub580_580.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub233_233.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub231_231.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub243_243.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub216_216.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub387_387.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub391_391.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub303_303.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub336_336.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub406_406.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub279_279.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub652_652.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub497_497.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub204_204.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub484_484.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub425_425.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub208_208.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub308_308.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub452_452.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub405_405.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub586_586.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub581_581.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub80_80.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub129_129.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub284_284.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub424_424.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub889_889.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub361_361.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub390_390.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub54_54.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub43_43.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub599_599.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub65_65.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub220_220.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub809_809.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub381_381.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub148_148.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub74_74.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub237_237.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub112_112.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub651_651.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub506_506.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub802_802.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub743_743.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub623_623.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub756_756.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub118_118.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub291_291.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub869_869.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub456_456.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub842_842.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub116_116.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub288_288.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub559_559.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub210_210.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub127_127.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub509_509.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub246_246.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub317_317.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub399_399.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub427_427.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub803_803.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub259_259.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub355_355.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub272_272.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub299_299.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub82_82.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub788_788.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub649_649.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub403_403.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub239_239.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub411_411.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub589_589.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub445_445.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub919_919.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub746_746.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub135_135.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub56_56.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub579_579.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub312_312.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub342_342.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub901_901.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub442_442.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub330_330.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub554_554.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub203_203.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub215_215.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub759_759.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub740_740.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub429_429.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub870_870.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub862_862.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub48_48.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub45_45.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub646_646.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub466_466.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub382_382.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub60_60.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub742_742.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub417_417.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub384_384.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub645_645.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub128_128.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub217_217.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub529_529.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub85_85.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub420_420.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub908_908.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub166_166.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub229_229.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub77_77.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub139_139.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub375_375.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub298_298.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub810_810.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub457_457.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub294_294.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub535_535.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub691_691.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub767_767.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub888_888.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub522_522.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub251_251.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub302_302.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub311_311.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub296_296.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub305_305.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub741_741.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub598_598.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub789_789.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub464_464.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub764_764.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub136_136.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub416_416.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub88_88.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub307_307.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub265_265.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub886_886.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub754_754.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub617_617.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub451_451.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub241_241.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub117_117.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub847_847.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub211_211.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub261_261.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub164_164.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub859_859.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub87_87.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub273_273.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub295_295.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub659_659.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub540_540.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub561_561.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub407_407.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub671_671.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub748_748.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub315_315.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub138_138.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub600_600.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub582_582.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub669_669.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub281_281.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub739_739.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub805_805.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub379_379.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub799_799.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub282_282.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub360_360.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub673_673.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub716_716.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub455_455.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub286_286.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub36_36.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub46_46.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub121_121.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub53_53.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub440_440.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub532_532.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub750_750.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub846_846.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub51_51.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub165_165.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub704_704.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub119_119.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub550_550.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub446_446.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub120_120.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub333_333.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub419_419.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub878_878.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub144_144.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub247_247.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub771_771.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub461_461.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub556_556.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub214_214.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub270_270.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub887_887.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub801_801.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub584_584.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub250_250.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub794_794.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub520_520.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub269_269.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub389_389.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub557_557.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub319_319.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub672_672.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub449_449.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub422_422.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub331_331.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub380_380.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub504_504.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub615_615.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub797_797.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub537_537.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub66_66.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub650_650.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub421_421.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub72_72.rvt

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/${SF_prefix}_sub386_386_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub313_313_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub285_285_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub428_428_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub923_923_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub482_482_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub430_430_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub747_747_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub328_328_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub658_658_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub547_547_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub413_413_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub689_689_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub402_402_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub549_549_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub67_67_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub326_326_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub717_717_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub252_252_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub35_35_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub344_344_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub597_597_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub81_81_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub548_548_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub758_758_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub574_574_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub78_78_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub83_83_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub71_71_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub791_791_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub255_255_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub329_329_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub666_666_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub655_655_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub906_906_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub585_585_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub800_800_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub448_448_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub34_34_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub137_137_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub125_125_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub114_114_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub227_227_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub283_283_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub792_792_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub479_479_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub577_577_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub131_131_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub706_706_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub335_335_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub668_668_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub664_664_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub587_587_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub494_494_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub687_687_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub42_42_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub332_332_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub124_124_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub530_530_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub304_304_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub44_44_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub122_122_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub555_555_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub688_688_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub262_262_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub49_49_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub316_316_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub866_866_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub248_248_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub301_301_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub59_59_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub575_575_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub876_876_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub52_52_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub768_768_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub861_861_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub613_613_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub142_142_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub412_412_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub323_323_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub50_50_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub863_863_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub293_293_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub200_200_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub400_400_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub126_126_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub306_306_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub201_201_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub363_363_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub404_404_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub322_322_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub468_468_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub753_753_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub905_905_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub752_752_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub644_644_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub73_73_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub396_396_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub327_327_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub806_806_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub757_757_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub221_221_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub423_423_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub426_426_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub539_539_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub340_340_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub843_843_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub558_558_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub796_796_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub39_39_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub519_519_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub611_611_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub58_58_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub865_865_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub447_447_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub724_724_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub480_480_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub483_483_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub454_454_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub467_467_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub760_760_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub749_749_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub143_143_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub793_793_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub225_225_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub254_254_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub762_762_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub460_460_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub441_441_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub223_223_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub795_795_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub415_415_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub542_542_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub546_546_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub610_610_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub277_277_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub880_880_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub167_167_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub62_62_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub583_583_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub505_505_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub287_287_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub531_531_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub377_377_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub612_612_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub654_654_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub921_921_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub86_86_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub378_378_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub657_657_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub667_667_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub761_761_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub401_401_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub268_268_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub236_236_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub844_844_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub538_538_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub463_463_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub487_487_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub362_362_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub123_123_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub37_37_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub875_875_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub352_352_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub502_502_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub341_341_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub130_130_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub337_337_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub79_79_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub507_507_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub278_278_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub232_232_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub653_653_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub113_113_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub61_61_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub686_686_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub552_552_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub321_321_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub858_858_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub55_55_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub543_543_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub383_383_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub218_218_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub140_140_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub867_867_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub616_616_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub770_770_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub784_784_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub744_744_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub345_345_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub719_719_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub499_499_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub274_274_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub351_351_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub450_450_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub745_745_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub665_665_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub622_622_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub132_132_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub276_276_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub388_388_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub596_596_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub903_903_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub488_488_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub260_260_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub902_902_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub84_84_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub297_297_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub68_68_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub235_235_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub110_110_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub528_528_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub578_578_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub147_147_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub209_209_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub864_864_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub553_553_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub263_263_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub614_614_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub804_804_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub398_398_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub258_258_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub393_393_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub465_465_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub807_807_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub69_69_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub503_503_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub353_353_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub738_738_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub459_459_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub481_481_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub443_443_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub310_310_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub356_356_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub338_338_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub244_244_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub500_500_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub242_242_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub523_523_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub57_57_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub264_264_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub462_462_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub63_63_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub75_75_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub495_495_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub718_718_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub334_334_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub230_230_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub656_656_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub785_785_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub551_551_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub501_501_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub290_290_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub720_720_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub469_469_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub722_722_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub737_737_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub496_496_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub202_202_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub111_111_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub343_343_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub879_879_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub300_300_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub485_485_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub544_544_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub536_536_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub395_395_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub751_751_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub798_798_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub545_545_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub280_280_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub692_692_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub249_249_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub414_414_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub723_723_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub207_207_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub392_392_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub205_205_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub376_376_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub868_868_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub267_267_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub660_660_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub648_648_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub133_133_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub41_41_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub47_47_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub525_525_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub38_38_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub508_508_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub786_786_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub354_354_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub146_146_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub541_541_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub397_397_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub253_253_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub228_228_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub339_339_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub219_219_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub141_141_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub808_808_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub580_580_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub233_233_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub231_231_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub243_243_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub216_216_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub387_387_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub391_391_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub303_303_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub336_336_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub406_406_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub279_279_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub652_652_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub497_497_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub204_204_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub484_484_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub425_425_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub208_208_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub308_308_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub452_452_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub405_405_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub586_586_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub581_581_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub80_80_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub129_129_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub284_284_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub424_424_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub889_889_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub361_361_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub390_390_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub54_54_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub43_43_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub599_599_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub65_65_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub220_220_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub809_809_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub381_381_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub148_148_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub74_74_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub237_237_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub112_112_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub651_651_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub506_506_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub802_802_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub743_743_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub623_623_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub756_756_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub118_118_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub291_291_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub869_869_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub456_456_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub842_842_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub116_116_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub288_288_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub559_559_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub210_210_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub127_127_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub509_509_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub246_246_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub317_317_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub399_399_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub427_427_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub803_803_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub259_259_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub355_355_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub272_272_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub299_299_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub82_82_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub788_788_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub649_649_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub403_403_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub239_239_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub411_411_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub589_589_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub445_445_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub919_919_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub746_746_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub135_135_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub56_56_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub579_579_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub312_312_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub342_342_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub901_901_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub442_442_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub330_330_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub554_554_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub203_203_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub215_215_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub759_759_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub740_740_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub429_429_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub870_870_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub862_862_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub48_48_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub45_45_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub646_646_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub466_466_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub382_382_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub60_60_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub742_742_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub417_417_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub384_384_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub645_645_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub128_128_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub217_217_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub529_529_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub85_85_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub420_420_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub908_908_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub166_166_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub229_229_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub77_77_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub139_139_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub375_375_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub298_298_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub810_810_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub457_457_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub294_294_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub535_535_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub691_691_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub767_767_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub888_888_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub522_522_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub251_251_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub302_302_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub311_311_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub296_296_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub305_305_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub741_741_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub598_598_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub789_789_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub464_464_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub764_764_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub136_136_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub416_416_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub88_88_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub307_307_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub265_265_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub886_886_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub754_754_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub617_617_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub451_451_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub241_241_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub117_117_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub847_847_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub211_211_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub261_261_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub164_164_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub859_859_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub87_87_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub273_273_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub295_295_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub659_659_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub540_540_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub561_561_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub407_407_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub671_671_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub748_748_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub315_315_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub138_138_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub600_600_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub582_582_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub669_669_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub281_281_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub739_739_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub805_805_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub379_379_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub799_799_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub282_282_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub360_360_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub673_673_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub716_716_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub455_455_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub286_286_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub36_36_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub46_46_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub121_121_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub53_53_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub440_440_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub532_532_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub750_750_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub846_846_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub51_51_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub165_165_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub704_704_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub119_119_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub550_550_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub446_446_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub120_120_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub333_333_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub419_419_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub878_878_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub144_144_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub247_247_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub771_771_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub461_461_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub556_556_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub214_214_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub270_270_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub887_887_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub801_801_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub584_584_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub250_250_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub794_794_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub520_520_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub269_269_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub389_389_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub557_557_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub319_319_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub672_672_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub449_449_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub422_422_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub331_331_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub380_380_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub504_504_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub615_615_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub797_797_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub537_537_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub66_66_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub650_650_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub421_421_weight.rvt
:RedirectToFile    ./obs/${SF_prefix}_sub72_72_weight.rvt

EOF
fi

#=====================================================================
# Lake Level
#=====================================================================
if [[ ${prefix} = "E" || ${prefix} = "S" || ${prefix} = "Re" ]]; then
cat >> ${rvt} << EOF
#=====================================================================
# Lake Water Level Observation
:RedirectToFile    ./obs/${WL_prefix}_108083_767.rvt    #Traverse
:RedirectToFile    ./obs/${WL_prefix}_108369_241.rvt    #La Muir
:RedirectToFile    ./obs/${WL_prefix}_108564_135.rvt    #Misty
:RedirectToFile    ./obs/${WL_prefix}_1032844_281.rvt   #Narrowbag
:RedirectToFile    ./obs/${WL_prefix}_108015_449.rvt    #Little Cauchon
:RedirectToFile    ./obs/${WL_prefix}_108347_753.rvt    #Grand
:RedirectToFile    ./obs/${WL_prefix}_108126_574.rvt    #Radiant
:RedirectToFile    ./obs/${WL_prefix}_8767_326.rvt      #Lavieille
:RedirectToFile    ./obs/${WL_prefix}_108404_122.rvt    #Loontail
:RedirectToFile    ./obs/${WL_prefix}_8741_528.rvt      #Cedar
:RedirectToFile    ./obs/${WL_prefix}_8781_220.rvt      #Big Trout
:RedirectToFile    ./obs/${WL_prefix}_8762_291.rvt      #Hogan
:RedirectToFile    ./obs/${WL_prefix}_108027_497.rvt    #North Depot
:RedirectToFile    ./obs/${WL_prefix}_1034779_345.rvt   #Animoosh
:RedirectToFile    ./obs/${WL_prefix}_108379_228.rvt    #Burntroot
:RedirectToFile    ./obs/${WL_prefix}_1033439_381.rvt   #Charles
:RedirectToFile    ./obs/${WL_prefix}_1035812_48.rvt    #Hambone
:RedirectToFile    ./obs/${WL_prefix}_1036038_117.rvt   #Lilypond
:RedirectToFile    ./obs/${WL_prefix}_108585_116.rvt    #Timberwolf

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/${WL_prefix}_108083_767_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108369_241_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108564_135_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032844_281_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108015_449_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108347_753_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108126_574_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_8767_326_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108404_122_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_8741_528_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_8781_220_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_8762_291_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108027_497_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034779_345_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108379_228_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033439_381_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035812_48_weight.rvt 
:RedirectToFile    ./obs/${WL_prefix}_1036038_117_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108585_116_weight.rvt

EOF

elif [[ ${prefix} = "V" ]]; then
cat >> ${rvt} << EOF
#=====================================================================
# Lake Water Level Sythetic Observation
:RedirectToFile    ./obs/${WL_prefix}_1035335_41.rvt    #1035335.0
:RedirectToFile    ./obs/${WL_prefix}_108435_315.rvt    #108435.0
:RedirectToFile    ./obs/${WL_prefix}_1034038_142.rvt   #1034038.0
:RedirectToFile    ./obs/${WL_prefix}_1033025_277.rvt   #1033025.0
:RedirectToFile    ./obs/${WL_prefix}_1032273_747.rvt   #1032273.0
:RedirectToFile    ./obs/${WL_prefix}_1032168_803.rvt   #1032168.0
:RedirectToFile    ./obs/${WL_prefix}_1033541_327.rvt   #1033541.0
:RedirectToFile    ./obs/${WL_prefix}_1034546_36.rvt    #1034546.0
:RedirectToFile    ./obs/${WL_prefix}_108585_116.rvt    #Timberwolf
:RedirectToFile    ./obs/${WL_prefix}_108316_126.rvt    #108316.0
:RedirectToFile    ./obs/${WL_prefix}_1031109_415.rvt   #1031109.0
:RedirectToFile    ./obs/${WL_prefix}_1034014_307.rvt   #1034014.0
:RedirectToFile    ./obs/${WL_prefix}_1033787_138.rvt   #1033787.0
:RedirectToFile    ./obs/${WL_prefix}_1033705_861.rvt   #1033705.0
:RedirectToFile    ./obs/${WL_prefix}_1032918_405.rvt   #1032918.0
:RedirectToFile    ./obs/${WL_prefix}_1033851_794.rvt   #1033851.0
:RedirectToFile    ./obs/${WL_prefix}_1035236_113.rvt   #1035236.0
:RedirectToFile    ./obs/${WL_prefix}_1032359_843.rvt   #1032359.0
:RedirectToFile    ./obs/${WL_prefix}_1032522_737.rvt   #1032522.0
:RedirectToFile    ./obs/${WL_prefix}_1033727_313.rvt   #1033727.0
:RedirectToFile    ./obs/${WL_prefix}_1035983_50.rvt    #1035983.0
:RedirectToFile    ./obs/${WL_prefix}_1035248_217.rvt   #1035248.0
:RedirectToFile    ./obs/${WL_prefix}_1035231_112.rvt   #1035231.0
:RedirectToFile    ./obs/${WL_prefix}_1031942_352.rvt   #1031942.0
:RedirectToFile    ./obs/${WL_prefix}_1035677_207.rvt   #1035677.0
:RedirectToFile    ./obs/${WL_prefix}_1033627_921.rvt   #02KB001
:RedirectToFile    ./obs/${WL_prefix}_108506_78.rvt     #108506.0
:RedirectToFile    ./obs/${WL_prefix}_1032769_399.rvt   #1032769.0
:RedirectToFile    ./obs/${WL_prefix}_1033915_720.rvt   #1033915.0
:RedirectToFile    ./obs/${WL_prefix}_1031014_304.rvt   #1031014.0
:RedirectToFile    ./obs/${WL_prefix}_1032691_646.rvt   #1032691.0
:RedirectToFile    ./obs/${WL_prefix}_1034075_544.rvt   #1034075.0
:RedirectToFile    ./obs/${WL_prefix}_108394_258.rvt    #108394.0
:RedirectToFile    ./obs/${WL_prefix}_108604_111.rvt    #108604.0
:RedirectToFile    ./obs/${WL_prefix}_1032780_596.rvt   #1032780.0
:RedirectToFile    ./obs/${WL_prefix}_1034708_344.rvt   #1034708.0
:RedirectToFile    ./obs/${WL_prefix}_108348_754.rvt    #108348.0
:RedirectToFile    ./obs/${WL_prefix}_1034574_321.rvt   #1034574.0
:RedirectToFile    ./obs/${WL_prefix}_108257_704.rvt    #108257.0
:RedirectToFile    ./obs/${WL_prefix}_1031839_452.rvt   #1031839.0
:RedirectToFile    ./obs/${WL_prefix}_1033850_543.rvt   #1033850.0
:RedirectToFile    ./obs/${WL_prefix}_1034091_536.rvt   #1034091.0
:RedirectToFile    ./obs/${WL_prefix}_1033704_379.rvt   #1033704.0
:RedirectToFile    ./obs/${WL_prefix}_1034122_859.rvt   #1034122.0
:RedirectToFile    ./obs/${WL_prefix}_108175_276.rvt    #108175.0
:RedirectToFile    ./obs/${WL_prefix}_1035432_87.rvt    #1035432.0
:RedirectToFile    ./obs/${WL_prefix}_1032797_650.rvt   #1032797.0
:RedirectToFile    ./obs/${WL_prefix}_1031844_427.rvt   #1031844.0
:RedirectToFile    ./obs/${WL_prefix}_1035069_216.rvt   #1035069.0
:RedirectToFile    ./obs/${WL_prefix}_108083_767.rvt    #Traverse
:RedirectToFile    ./obs/${WL_prefix}_1032285_354.rvt   #1032285.0
:RedirectToFile    ./obs/${WL_prefix}_1031986_430.rvt   #1031986.0
:RedirectToFile    ./obs/${WL_prefix}_1031979_429.rvt   #1031979.0
:RedirectToFile    ./obs/${WL_prefix}_1034245_267.rvt   #1034245.0
:RedirectToFile    ./obs/${WL_prefix}_1034926_319.rvt   #1034926.0
:RedirectToFile    ./obs/${WL_prefix}_1033549_847.rvt   #1033549.0
:RedirectToFile    ./obs/${WL_prefix}_108233_377.rvt    #108233.0
:RedirectToFile    ./obs/${WL_prefix}_108379_228.rvt    #Burntroot
:RedirectToFile    ./obs/${WL_prefix}_1031908_623.rvt   #1031908.0
:RedirectToFile    ./obs/${WL_prefix}_1033206_496.rvt   #1033206.0
:RedirectToFile    ./obs/${WL_prefix}_1031173_391.rvt   #1031173.0
:RedirectToFile    ./obs/${WL_prefix}_108500_73.rvt     #108500.0
:RedirectToFile    ./obs/${WL_prefix}_1031664_299.rvt   #1031664.0
:RedirectToFile    ./obs/${WL_prefix}_1033877_140.rvt   #1033877.0
:RedirectToFile    ./obs/${WL_prefix}_1031300_421.rvt   #1031300.0
:RedirectToFile    ./obs/${WL_prefix}_1034933_655.rvt   #1034933.0
:RedirectToFile    ./obs/${WL_prefix}_108226_901.rvt    #108226.0
:RedirectToFile    ./obs/${WL_prefix}_1032827_786.rvt   #1032827.0
:RedirectToFile    ./obs/${WL_prefix}_1033173_615.rvt   #1033173.0
:RedirectToFile    ./obs/${WL_prefix}_1033422_407.rvt   #1033422.0
:RedirectToFile    ./obs/${WL_prefix}_1034625_658.rvt   #1034625.0
:RedirectToFile    ./obs/${WL_prefix}_1034874_205.rvt   #1034874.0
:RedirectToFile    ./obs/${WL_prefix}_108470_164.rvt    #108470.0
:RedirectToFile    ./obs/${WL_prefix}_1032869_876.rvt   #1032869.0
:RedirectToFile    ./obs/${WL_prefix}_1034674_343.rvt   #1034674.0
:RedirectToFile    ./obs/${WL_prefix}_1034400_341.rvt   #1034400.0
:RedirectToFile    ./obs/${WL_prefix}_1032819_282.rvt   #1032819.0
:RedirectToFile    ./obs/${WL_prefix}_108369_241.rvt    #La Muir
:RedirectToFile    ./obs/${WL_prefix}_1035755_46.rvt    #1035755.0
:RedirectToFile    ./obs/${WL_prefix}_1032552_667.rvt   #1032552.0
:RedirectToFile    ./obs/${WL_prefix}_1034337_123.rvt   #1034337.0
:RedirectToFile    ./obs/${WL_prefix}_108451_260.rvt    #108451.0
:RedirectToFile    ./obs/${WL_prefix}_1032502_738.rvt   #1032502.0
:RedirectToFile    ./obs/${WL_prefix}_1034293_147.rvt   #1034293.0
:RedirectToFile    ./obs/${WL_prefix}_1032227_504.rvt   #1032227.0
:RedirectToFile    ./obs/${WL_prefix}_1034100_237.rvt   #1034100.0
:RedirectToFile    ./obs/${WL_prefix}_1033519_751.rvt   #1033519.0
:RedirectToFile    ./obs/${WL_prefix}_1031634_451.rvt   #1031634.0
:RedirectToFile    ./obs/${WL_prefix}_1034317_724.rvt   #1034317.0
:RedirectToFile    ./obs/${WL_prefix}_1033548_312.rvt   #1033548.0
:RedirectToFile    ./obs/${WL_prefix}_1032102_673.rvt   #1032102.0
:RedirectToFile    ./obs/${WL_prefix}_1031744_426.rvt   #1031744.0
:RedirectToFile    ./obs/${WL_prefix}_1032101_525.rvt   #1032101.0
:RedirectToFile    ./obs/${WL_prefix}_1033884_863.rvt   #1033884.0
:RedirectToFile    ./obs/${WL_prefix}_1035551_62.rvt    #1035551.0
:RedirectToFile    ./obs/${WL_prefix}_1034132_144.rvt   #1034132.0
:RedirectToFile    ./obs/${WL_prefix}_1033712_792.rvt   #1033712.0
:RedirectToFile    ./obs/${WL_prefix}_1031604_744.rvt   #1031604.0
:RedirectToFile    ./obs/${WL_prefix}_1033084_375.rvt   #1033084.0
:RedirectToFile    ./obs/${WL_prefix}_1034246_657.rvt   #1034246.0
:RedirectToFile    ./obs/${WL_prefix}_1035297_218.rvt   #1035297.0
:RedirectToFile    ./obs/${WL_prefix}_1033094_403.rvt   #1033094.0
:RedirectToFile    ./obs/${WL_prefix}_108564_135.rvt    #Misty
:RedirectToFile    ./obs/${WL_prefix}_1031318_443.rvt   #1031318.0
:RedirectToFile    ./obs/${WL_prefix}_1031964_501.rvt   #1031964.0
:RedirectToFile    ./obs/${WL_prefix}_1035727_57.rvt    #1035727.0
:RedirectToFile    ./obs/${WL_prefix}_1033905_795.rvt   #1033905.0
:RedirectToFile    ./obs/${WL_prefix}_1031261_419.rvt   #1031261.0
:RedirectToFile    ./obs/${WL_prefix}_1033145_902.rvt   #1033145.0
:RedirectToFile    ./obs/${WL_prefix}_1035794_58.rvt    #1035794.0
:RedirectToFile    ./obs/${WL_prefix}_1034212_335.rvt   #1034212.0
:RedirectToFile    ./obs/${WL_prefix}_1032851_610.rvt   #1032851.0
:RedirectToFile    ./obs/${WL_prefix}_1033900_236.rvt   #1033900.0
:RedirectToFile    ./obs/${WL_prefix}_1034741_654.rvt   #1034741.0
:RedirectToFile    ./obs/${WL_prefix}_1032953_582.rvt   #1032953.0
:RedirectToFile    ./obs/${WL_prefix}_1034144_553.rvt   #1034144.0
:RedirectToFile    ./obs/${WL_prefix}_1032844_281.rvt   #Narrowbag
:RedirectToFile    ./obs/${WL_prefix}_1034866_82.rvt    #1034866.0
:RedirectToFile    ./obs/${WL_prefix}_1034854_69.rvt    #1034854.0
:RedirectToFile    ./obs/${WL_prefix}_1033635_273.rvt   #1033635.0
:RedirectToFile    ./obs/${WL_prefix}_108303_919.rvt    #108303.0
:RedirectToFile    ./obs/${WL_prefix}_1032345_666.rvt   #1032345.0
:RedirectToFile    ./obs/${WL_prefix}_1031870_502.rvt   #1031870.0
:RedirectToFile    ./obs/${WL_prefix}_1031683_450.rvt   #1031683.0
:RedirectToFile    ./obs/${WL_prefix}_1034140_227.rvt   #1034140.0
:RedirectToFile    ./obs/${WL_prefix}_108193_875.rvt    #108193.0
:RedirectToFile    ./obs/${WL_prefix}_108015_449.rvt    #Little Cauchon
:RedirectToFile    ./obs/${WL_prefix}_1034409_549.rvt   #1034409.0
:RedirectToFile    ./obs/${WL_prefix}_1032458_580.rvt   #1032458.0
:RedirectToFile    ./obs/${WL_prefix}_1033144_810.rvt   #1033144.0
:RedirectToFile    ./obs/${WL_prefix}_1034597_268.rvt   #1034597.0
:RedirectToFile    ./obs/${WL_prefix}_1032986_692.rvt   #1032986.0
:RedirectToFile    ./obs/${WL_prefix}_1033299_330.rvt   #1033299.0
:RedirectToFile    ./obs/${WL_prefix}_1032795_520.rvt   #1032795.0
:RedirectToFile    ./obs/${WL_prefix}_1033132_495.rvt   #1033132.0
:RedirectToFile    ./obs/${WL_prefix}_1031873_745.rvt   #1031873.0
:RedirectToFile    ./obs/${WL_prefix}_1034695_148.rvt   #1034695.0
:RedirectToFile    ./obs/${WL_prefix}_1031362_500.rvt   #1031362.0
:RedirectToFile    ./obs/${WL_prefix}_1034101_760.rvt   #1034101.0
:RedirectToFile    ./obs/${WL_prefix}_1031919_428.rvt   #1031919.0
:RedirectToFile    ./obs/${WL_prefix}_1031624_442.rvt   #1031624.0
:RedirectToFile    ./obs/${WL_prefix}_1031745_789.rvt   #1031745.0
:RedirectToFile    ./obs/${WL_prefix}_1033557_862.rvt   #1033557.0
:RedirectToFile    ./obs/${WL_prefix}_1033131_376.rvt   #1033131.0
:RedirectToFile    ./obs/${WL_prefix}_1032609_739.rvt   #1032609.0
:RedirectToFile    ./obs/${WL_prefix}_1031283_441.rvt   #1031283.0
:RedirectToFile    ./obs/${WL_prefix}_107949_294.rvt    #107949.0
:RedirectToFile    ./obs/${WL_prefix}_1033211_310.rvt   #1033211.0
:RedirectToFile    ./obs/${WL_prefix}_1032312_587.rvt   #1032312.0
:RedirectToFile    ./obs/${WL_prefix}_108509_215.rvt    #108509.0
:RedirectToFile    ./obs/${WL_prefix}_1034633_659.rvt   #1034633.0
:RedirectToFile    ./obs/${WL_prefix}_108446_77.rvt     #108446.0
:RedirectToFile    ./obs/${WL_prefix}_1034801_71.rvt    #1034801.0
:RedirectToFile    ./obs/${WL_prefix}_1030966_302.rvt   #1030966.0
:RedirectToFile    ./obs/${WL_prefix}_1035858_210.rvt   #1035858.0
:RedirectToFile    ./obs/${WL_prefix}_1034048_143.rvt   #1034048.0
:RedirectToFile    ./obs/${WL_prefix}_108614_47.rvt     #108614.0
:RedirectToFile    ./obs/${WL_prefix}_1034740_221.rvt   #1034740.0
:RedirectToFile    ./obs/${WL_prefix}_1030543_417.rvt   #1030543.0
:RedirectToFile    ./obs/${WL_prefix}_1031538_422.rvt   #1031538.0
:RedirectToFile    ./obs/${WL_prefix}_1031841_808.rvt   #1031841.0
:RedirectToFile    ./obs/${WL_prefix}_1033765_338.rvt   #1033765.0
:RedirectToFile    ./obs/${WL_prefix}_1032210_499.rvt   #1032210.0
:RedirectToFile    ./obs/${WL_prefix}_108347_753.rvt    #Grand
:RedirectToFile    ./obs/${WL_prefix}_1032551_559.rvt   #1032551.0
:RedirectToFile    ./obs/${WL_prefix}_1034612_342.rvt   #1034612.0
:RedirectToFile    ./obs/${WL_prefix}_1034890_83.rvt    #1034890.0
:RedirectToFile    ./obs/${WL_prefix}_1034185_687.rvt   #1034185.0
:RedirectToFile    ./obs/${WL_prefix}_1034662_167.rvt   #1034662.0
:RedirectToFile    ./obs/${WL_prefix}_1034213_547.rvt   #1034213.0
:RedirectToFile    ./obs/${WL_prefix}_1033490_250.rvt   #1033490.0
:RedirectToFile    ./obs/${WL_prefix}_1034585_202.rvt   #1034585.0
:RedirectToFile    ./obs/${WL_prefix}_1034487_165.rvt   #1034487.0
:RedirectToFile    ./obs/${WL_prefix}_1035566_43.rvt    #1035566.0
:RedirectToFile    ./obs/${WL_prefix}_108126_574.rvt    #Radiant
:RedirectToFile    ./obs/${WL_prefix}_1032092_802.rvt   #1032092.0
:RedirectToFile    ./obs/${WL_prefix}_1031002_303.rvt   #1031002.0
:RedirectToFile    ./obs/${WL_prefix}_1033817_235.rvt   #1033817.0
:RedirectToFile    ./obs/${WL_prefix}_1033345_328.rvt   #1033345.0
:RedirectToFile    ./obs/${WL_prefix}_1034389_243.rvt   #1034389.0
:RedirectToFile    ./obs/${WL_prefix}_1034707_67.rvt    #1034707.0
:RedirectToFile    ./obs/${WL_prefix}_1033977_864.rvt   #1033977.0
:RedirectToFile    ./obs/${WL_prefix}_1033509_717.rvt   #1033509.0
:RedirectToFile    ./obs/${WL_prefix}_1032906_283.rvt   #1032906.0
:RedirectToFile    ./obs/${WL_prefix}_1032671_740.rvt   #1032671.0
:RedirectToFile    ./obs/${WL_prefix}_1034033_129.rvt   #1034033.0
:RedirectToFile    ./obs/${WL_prefix}_1033908_229.rvt   #1033908.0
:RedirectToFile    ./obs/${WL_prefix}_1032634_575.rvt   #1032634.0
:RedirectToFile    ./obs/${WL_prefix}_1034632_65.rvt    #1034632.0
:RedirectToFile    ./obs/${WL_prefix}_1033298_278.rvt   #1033298.0
:RedirectToFile    ./obs/${WL_prefix}_1033116_361.rvt   #1033116.0
:RedirectToFile    ./obs/${WL_prefix}_1034436_133.rvt   #1034436.0
:RedirectToFile    ./obs/${WL_prefix}_1034867_204.rvt   #1034867.0
:RedirectToFile    ./obs/${WL_prefix}_1032404_279.rvt   #1032404.0
:RedirectToFile    ./obs/${WL_prefix}_1033077_406.rvt   #1033077.0
:RedirectToFile    ./obs/${WL_prefix}_1034634_203.rvt   #1034634.0
:RedirectToFile    ./obs/${WL_prefix}_8767_326.rvt      #Lavieille
:RedirectToFile    ./obs/${WL_prefix}_1034936_74.rvt    #1034936.0
:RedirectToFile    ./obs/${WL_prefix}_1031452_770.rvt   #1031452.0
:RedirectToFile    ./obs/${WL_prefix}_1031609_462.rvt   #1031609.0
:RedirectToFile    ./obs/${WL_prefix}_1032580_887.rvt   #1032580.0
:RedirectToFile    ./obs/${WL_prefix}_1033643_554.rvt   #1033643.0
:RedirectToFile    ./obs/${WL_prefix}_1034584_201.rvt   #1034584.0
:RedirectToFile    ./obs/${WL_prefix}_1033363_247.rvt   #1033363.0
:RedirectToFile    ./obs/${WL_prefix}_107978_459.rvt    #107978.0
:RedirectToFile    ./obs/${WL_prefix}_1033852_867.rvt   #1033852.0
:RedirectToFile    ./obs/${WL_prefix}_1031410_807.rvt   #1031410.0
:RedirectToFile    ./obs/${WL_prefix}_1034034_230.rvt   #1034034.0
:RedirectToFile    ./obs/${WL_prefix}_1033350_716.rvt   #1033350.0
:RedirectToFile    ./obs/${WL_prefix}_1033491_311.rvt   #1033491.0
:RedirectToFile    ./obs/${WL_prefix}_1032591_481.rvt   #1032591.0
:RedirectToFile    ./obs/${WL_prefix}_1033162_457.rvt   #1033162.0
:RedirectToFile    ./obs/${WL_prefix}_108541_81.rvt     #108541.0
:RedirectToFile    ./obs/${WL_prefix}_1031779_529.rvt   #1031779.0
:RedirectToFile    ./obs/${WL_prefix}_1031889_799.rvt   #1031889.0
:RedirectToFile    ./obs/${WL_prefix}_1034841_214.rvt   #1034841.0
:RedirectToFile    ./obs/${WL_prefix}_8778_322.rvt      #8778.0
:RedirectToFile    ./obs/${WL_prefix}_1031887_424.rvt   #1031887.0
:RedirectToFile    ./obs/${WL_prefix}_108275_246.rvt    #108275.0
:RedirectToFile    ./obs/${WL_prefix}_1030949_301.rvt   #1030949.0
:RedirectToFile    ./obs/${WL_prefix}_108465_200.rvt    #108465.0
:RedirectToFile    ./obs/${WL_prefix}_1034611_124.rvt   #1034611.0
:RedirectToFile    ./obs/${WL_prefix}_1032645_480.rvt   #1032645.0
:RedirectToFile    ./obs/${WL_prefix}_108618_61.rvt     #108618.0
:RedirectToFile    ./obs/${WL_prefix}_1031008_390.rvt   #1031008.0
:RedirectToFile    ./obs/${WL_prefix}_1034453_225.rvt   #1034453.0
:RedirectToFile    ./obs/${WL_prefix}_1036081_51.rvt    #1036081.0
:RedirectToFile    ./obs/${WL_prefix}_1034051_130.rvt   #1034051.0
:RedirectToFile    ./obs/${WL_prefix}_1032421_584.rvt   #1032421.0
:RedirectToFile    ./obs/${WL_prefix}_108404_122.rvt    #Loontail
:RedirectToFile    ./obs/${WL_prefix}_1034755_68.rvt    #1034755.0
:RedirectToFile    ./obs/${WL_prefix}_1035996_211.rvt   #1035996.0
:RedirectToFile    ./obs/${WL_prefix}_1031625_298.rvt   #1031625.0
:RedirectToFile    ./obs/${WL_prefix}_1035399_136.rvt   #1035399.0
:RedirectToFile    ./obs/${WL_prefix}_1033669_253.rvt   #1033669.0
:RedirectToFile    ./obs/${WL_prefix}_1035854_59.rvt    #1035854.0
:RedirectToFile    ./obs/${WL_prefix}_1035235_86.rvt    #1035235.0
:RedirectToFile    ./obs/${WL_prefix}_1033970_540.rvt   #1033970.0
:RedirectToFile    ./obs/${WL_prefix}_1032603_585.rvt   #1032603.0
:RedirectToFile    ./obs/${WL_prefix}_1033546_251.rvt   #1033546.0
:RedirectToFile    ./obs/${WL_prefix}_1033458_538.rvt   #1033458.0
:RedirectToFile    ./obs/${WL_prefix}_1033837_541.rvt   #1033837.0
:RedirectToFile    ./obs/${WL_prefix}_1034552_336.rvt   #1034552.0
:RedirectToFile    ./obs/${WL_prefix}_1034444_120.rvt   #1034444.0
:RedirectToFile    ./obs/${WL_prefix}_1033127_886.rvt   #1033127.0
:RedirectToFile    ./obs/${WL_prefix}_1034705_66.rvt    #1034705.0
:RedirectToFile    ./obs/${WL_prefix}_1032539_280.rvt   #1032539.0
:RedirectToFile    ./obs/${WL_prefix}_1033117_612.rvt   #1033117.0
:RedirectToFile    ./obs/${WL_prefix}_1033678_274.rvt   #1033678.0
:RedirectToFile    ./obs/${WL_prefix}_1034386_548.rvt   #1034386.0
:RedirectToFile    ./obs/${WL_prefix}_1032218_503.rvt   #1032218.0
:RedirectToFile    ./obs/${WL_prefix}_1035622_63.rvt    #1035622.0
:RedirectToFile    ./obs/${WL_prefix}_1033862_128.rvt   #1033862.0
:RedirectToFile    ./obs/${WL_prefix}_8741_528.rvt      #Cedar
:RedirectToFile    ./obs/${WL_prefix}_108298_249.rvt    #108298.0
:RedirectToFile    ./obs/${WL_prefix}_1033916_869.rvt   #1033916.0
:RedirectToFile    ./obs/${WL_prefix}_1031292_420.rvt   #1031292.0
:RedirectToFile    ./obs/${WL_prefix}_1032749_742.rvt   #1032749.0
:RedirectToFile    ./obs/${WL_prefix}_1032083_800.rvt   #1032083.0
:RedirectToFile    ./obs/${WL_prefix}_1031451_460.rvt   #1031451.0
:RedirectToFile    ./obs/${WL_prefix}_1032794_519.rvt   #1032794.0
:RedirectToFile    ./obs/${WL_prefix}_1032390_579.rvt   #1032390.0
:RedirectToFile    ./obs/${WL_prefix}_1036038_117.rvt   #Lilypond
:RedirectToFile    ./obs/${WL_prefix}_1034125_131.rvt   #1034125.0
:RedirectToFile    ./obs/${WL_prefix}_1034305_316.rvt   #1034305.0
:RedirectToFile    ./obs/${WL_prefix}_8781_220.rvt      #Big Trout
:RedirectToFile    ./obs/${WL_prefix}_1031843_465.rvt   #1031843.0
:RedirectToFile    ./obs/${WL_prefix}_1032676_397.rvt   #1032676.0
:RedirectToFile    ./obs/${WL_prefix}_1030917_389.rvt   #1030917.0
:RedirectToFile    ./obs/${WL_prefix}_1032677_398.rvt   #1032677.0
:RedirectToFile    ./obs/${WL_prefix}_1031435_295.rvt   #1031435.0
:RedirectToFile    ./obs/${WL_prefix}_1031042_305.rvt   #1031042.0
:RedirectToFile    ./obs/${WL_prefix}_1031615_466.rvt   #1031615.0
:RedirectToFile    ./obs/${WL_prefix}_1033733_555.rvt   #1033733.0
:RedirectToFile    ./obs/${WL_prefix}_1033035_402.rvt   #1033035.0
:RedirectToFile    ./obs/${WL_prefix}_1035731_45.rvt    #1035731.0
:RedirectToFile    ./obs/${WL_prefix}_1031965_586.rvt   #1031965.0
:RedirectToFile    ./obs/${WL_prefix}_1033133_906.rvt   #1033133.0
:RedirectToFile    ./obs/${WL_prefix}_1031162_363.rvt   #1031162.0
:RedirectToFile    ./obs/${WL_prefix}_8762_291.rvt      #Hogan
:RedirectToFile    ./obs/${WL_prefix}_1033928_865.rvt   #1033928.0
:RedirectToFile    ./obs/${WL_prefix}_108324_552.rvt    #108324.0
:RedirectToFile    ./obs/${WL_prefix}_1035812_48.rvt    #Hambone
:RedirectToFile    ./obs/${WL_prefix}_1031733_464.rvt   #1031733.0
:RedirectToFile    ./obs/${WL_prefix}_1034937_84.rvt    #1034937.0
:RedirectToFile    ./obs/${WL_prefix}_1031714_522.rvt   #1031714.0
:RedirectToFile    ./obs/${WL_prefix}_1032135_353.rvt   #1032135.0
:RedirectToFile    ./obs/${WL_prefix}_108422_231.rvt    #108422.0
:RedirectToFile    ./obs/${WL_prefix}_1034486_35.rvt    #1034486.0
:RedirectToFile    ./obs/${WL_prefix}_1032240_665.rvt   #1032240.0
:RedirectToFile    ./obs/${WL_prefix}_1032437_844.rvt   #1032437.0
:RedirectToFile    ./obs/${WL_prefix}_1033508_248.rvt   #1033508.0
:RedirectToFile    ./obs/${WL_prefix}_1035728_44.rvt    #1035728.0
:RedirectToFile    ./obs/${WL_prefix}_1033670_718.rvt   #1033670.0
:RedirectToFile    ./obs/${WL_prefix}_1034131_132.rvt   #1034131.0
:RedirectToFile    ./obs/${WL_prefix}_1033831_719.rvt   #1033831.0
:RedirectToFile    ./obs/${WL_prefix}_1034660_653.rvt   #1034660.0
:RedirectToFile    ./obs/${WL_prefix}_108004_531.rvt    #108004.0
:RedirectToFile    ./obs/${WL_prefix}_108027_497.rvt    #North Depot
:RedirectToFile    ./obs/${WL_prefix}_1034459_290.rvt   #1034459.0
:RedirectToFile    ./obs/${WL_prefix}_1033680_393.rvt   #1033680.0
:RedirectToFile    ./obs/${WL_prefix}_1035210_85.rvt    #1035210.0
:RedirectToFile    ./obs/${WL_prefix}_108494_652.rvt    #108494.0
:RedirectToFile    ./obs/${WL_prefix}_1030908_388.rvt   #1030908.0
:RedirectToFile    ./obs/${WL_prefix}_1031780_798.rvt   #1031780.0
:RedirectToFile    ./obs/${WL_prefix}_1034198_686.rvt   #1034198.0
:RedirectToFile    ./obs/${WL_prefix}_1031842_423.rvt   #1031842.0
:RedirectToFile    ./obs/${WL_prefix}_1034133_308.rvt   #1034133.0
:RedirectToFile    ./obs/${WL_prefix}_1035821_49.rvt    #1035821.0
:RedirectToFile    ./obs/${WL_prefix}_1032796_598.rvt   #1032796.0
:RedirectToFile    ./obs/${WL_prefix}_1034951_39.rvt    #1034951.0
:RedirectToFile    ./obs/${WL_prefix}_1033587_127.rvt   #1033587.0
:RedirectToFile    ./obs/${WL_prefix}_1032864_597.rvt   #1032864.0
:RedirectToFile    ./obs/${WL_prefix}_1034779_345.rvt   #Animoosh
:RedirectToFile    ./obs/${WL_prefix}_108638_209.rvt    #108638.0
:RedirectToFile    ./obs/${WL_prefix}_1032044_578.rvt   #1032044.0
:RedirectToFile    ./obs/${WL_prefix}_1031603_297.rvt   #1031603.0
:RedirectToFile    ./obs/${WL_prefix}_1033439_381.rvt   #Charles
:RedirectToFile    ./obs/${WL_prefix}_1034989_75.rvt    #1034989.0
:RedirectToFile    ./obs/${WL_prefix}_1033959_880.rvt   #1033959.0
:RedirectToFile    ./obs/${WL_prefix}_1035387_42.rvt    #1035387.0
:RedirectToFile    ./obs/${WL_prefix}_1033280_669.rvt   #1033280.0
:RedirectToFile    ./obs/${WL_prefix}_1032834_401.rvt   #1032834.0
:RedirectToFile    ./obs/${WL_prefix}_1033982_542.rvt   #1033982.0
:RedirectToFile    ./obs/${WL_prefix}_1033935_796.rvt   #1033935.0
:RedirectToFile    ./obs/${WL_prefix}_1033803_758.rvt   #1033803.0
:RedirectToFile    ./obs/${WL_prefix}_108357_334.rvt    #108357.0
:RedirectToFile    ./obs/${WL_prefix}_1032651_649.rvt   #1032651.0
:RedirectToFile    ./obs/${WL_prefix}_1034169_723.rvt   #1034169.0
:RedirectToFile    ./obs/${WL_prefix}_108567_110.rvt    #108567.0
:RedirectToFile    ./obs/${WL_prefix}_1031232_461.rvt   #1031232.0
:RedirectToFile    ./obs/${WL_prefix}_1034859_317.rvt   #1034859.0
:RedirectToFile    ./obs/${WL_prefix}_1034840_38.rvt    #1034840.0
:RedirectToFile    ./obs/${WL_prefix}_1032373_355.rvt   #1032373.0
:RedirectToFile    ./obs/${WL_prefix}_1031409_806.rvt   #1031409.0
:RedirectToFile    ./obs/${WL_prefix}_1033237_616.rvt   #1033237.0
:RedirectToFile    ./obs/${WL_prefix}_1034739_37.rvt    #1034739.0
:RedirectToFile    ./obs/${WL_prefix}_1032217_483.rvt   #1032217.0
:RedirectToFile    ./obs/${WL_prefix}_107912_485.rvt    #107912.0
:RedirectToFile    ./obs/${WL_prefix}_1032652_645.rvt   #1032652.0
:RedirectToFile    ./obs/${WL_prefix}_1033619_378.rvt   #1033619.0
:RedirectToFile    ./obs/${WL_prefix}_1032579_396.rvt   #1032579.0
:RedirectToFile    ./obs/${WL_prefix}_1034121_722.rvt   #1034121.0
:RedirectToFile    ./obs/${WL_prefix}_1033838_793.rvt   #1033838.0
:RedirectToFile    ./obs/${WL_prefix}_1030960_413.rvt   #1030960.0
:RedirectToFile    ./obs/${WL_prefix}_1033971_797.rvt   #1033971.0
:RedirectToFile    ./obs/${WL_prefix}_1033798_752.rvt   #1033798.0
:RedirectToFile    ./obs/${WL_prefix}_1033034_384.rvt   #1033034.0
:RedirectToFile    ./obs/${WL_prefix}_1035581_52.rvt    #1035581.0
:RedirectToFile    ./obs/${WL_prefix}_1035460_88.rvt    #1035460.0
:RedirectToFile    ./obs/${WL_prefix}_1032532_479.rvt   #1032532.0
:RedirectToFile    ./obs/${WL_prefix}_1032963_611.rvt   #1032963.0
:RedirectToFile    ./obs/${WL_prefix}_108041_351.rvt    #108041.0
:RedirectToFile    ./obs/${WL_prefix}_1034663_660.rvt   #1034663.0
:RedirectToFile    ./obs/${WL_prefix}_1033532_272.rvt   #1033532.0
:RedirectToFile    ./obs/${WL_prefix}_1031710_463.rvt   #1031710.0
:RedirectToFile    ./obs/${WL_prefix}_1034345_259.rvt   #1034345.0
:RedirectToFile    ./obs/${WL_prefix}_1033588_252.rvt   #1033588.0
:RedirectToFile    ./obs/${WL_prefix}_1035657_53.rvt    #1035657.0
:RedirectToFile    ./obs/${WL_prefix}_1034361_261.rvt   #1034361.0
:RedirectToFile    ./obs/${WL_prefix}_1034534_651.rvt   #1034534.0
:RedirectToFile    ./obs/${WL_prefix}_1033640_539.rvt   #1033640.0
:RedirectToFile    ./obs/${WL_prefix}_1033500_329.rvt   #1033500.0
:RedirectToFile    ./obs/${WL_prefix}_1031153_440.rvt   #1031153.0
:RedirectToFile    ./obs/${WL_prefix}_1032731_785.rvt   #1032731.0

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/${WL_prefix}_1035335_41_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108435_315_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034038_142_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033025_277_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032273_747_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032168_803_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033541_327_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034546_36_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108585_116_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108316_126_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031109_415_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034014_307_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033787_138_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033705_861_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032918_405_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033851_794_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035236_113_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032359_843_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032522_737_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033727_313_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035983_50_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035248_217_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035231_112_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031942_352_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035677_207_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033627_921_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108506_78_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032769_399_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033915_720_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031014_304_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032691_646_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034075_544_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108394_258_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108604_111_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032780_596_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034708_344_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108348_754_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034574_321_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108257_704_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031839_452_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033850_543_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034091_536_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033704_379_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034122_859_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108175_276_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035432_87_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032797_650_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031844_427_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035069_216_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108083_767_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032285_354_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031986_430_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031979_429_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034245_267_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034926_319_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033549_847_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108233_377_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108379_228_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031908_623_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033206_496_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031173_391_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108500_73_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031664_299_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033877_140_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031300_421_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034933_655_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108226_901_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032827_786_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033173_615_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033422_407_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034625_658_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034874_205_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108470_164_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032869_876_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034674_343_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034400_341_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032819_282_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108369_241_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035755_46_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032552_667_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034337_123_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108451_260_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032502_738_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034293_147_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032227_504_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034100_237_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033519_751_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031634_451_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034317_724_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033548_312_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032102_673_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031744_426_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032101_525_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033884_863_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035551_62_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034132_144_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033712_792_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031604_744_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033084_375_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034246_657_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035297_218_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033094_403_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108564_135_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031318_443_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031964_501_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035727_57_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033905_795_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031261_419_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033145_902_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035794_58_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034212_335_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032851_610_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033900_236_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034741_654_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032953_582_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034144_553_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032844_281_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034866_82_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034854_69_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033635_273_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108303_919_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032345_666_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031870_502_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031683_450_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034140_227_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108193_875_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108015_449_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034409_549_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032458_580_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033144_810_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034597_268_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032986_692_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033299_330_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032795_520_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033132_495_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031873_745_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034695_148_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031362_500_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034101_760_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031919_428_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031624_442_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031745_789_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033557_862_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033131_376_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032609_739_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031283_441_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_107949_294_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033211_310_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032312_587_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108509_215_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034633_659_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108446_77_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034801_71_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1030966_302_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035858_210_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034048_143_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108614_47_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034740_221_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1030543_417_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031538_422_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031841_808_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033765_338_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032210_499_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108347_753_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032551_559_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034612_342_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034890_83_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034185_687_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034662_167_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034213_547_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033490_250_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034585_202_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034487_165_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035566_43_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108126_574_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032092_802_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031002_303_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033817_235_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033345_328_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034389_243_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034707_67_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033977_864_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033509_717_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032906_283_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032671_740_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034033_129_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033908_229_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032634_575_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034632_65_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033298_278_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033116_361_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034436_133_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034867_204_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032404_279_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033077_406_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034634_203_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_8767_326_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034936_74_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031452_770_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031609_462_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032580_887_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033643_554_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034584_201_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033363_247_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_107978_459_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033852_867_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031410_807_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034034_230_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033350_716_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033491_311_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032591_481_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033162_457_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108541_81_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031779_529_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031889_799_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034841_214_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_8778_322_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031887_424_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108275_246_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1030949_301_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108465_200_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034611_124_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032645_480_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108618_61_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031008_390_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034453_225_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1036081_51_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034051_130_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032421_584_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108404_122_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034755_68_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035996_211_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031625_298_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035399_136_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033669_253_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035854_59_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035235_86_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033970_540_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032603_585_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033546_251_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033458_538_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033837_541_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034552_336_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034444_120_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033127_886_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034705_66_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032539_280_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033117_612_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033678_274_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034386_548_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032218_503_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035622_63_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033862_128_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_8741_528_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108298_249_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033916_869_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031292_420_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032749_742_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032083_800_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031451_460_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032794_519_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032390_579_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1036038_117_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034125_131_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034305_316_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_8781_220_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031843_465_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032676_397_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1030917_389_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032677_398_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031435_295_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031042_305_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031615_466_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033733_555_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033035_402_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035731_45_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031965_586_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033133_906_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031162_363_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_8762_291_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033928_865_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108324_552_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035812_48_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031733_464_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034937_84_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031714_522_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032135_353_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108422_231_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034486_35_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032240_665_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032437_844_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033508_248_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035728_44_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033670_718_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034131_132_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033831_719_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034660_653_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108004_531_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108027_497_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034459_290_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033680_393_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035210_85_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108494_652_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1030908_388_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031780_798_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034198_686_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031842_423_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034133_308_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035821_49_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032796_598_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034951_39_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033587_127_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032864_597_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034779_345_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108638_209_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032044_578_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031603_297_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033439_381_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034989_75_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033959_880_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035387_42_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033280_669_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032834_401_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033982_542_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033935_796_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033803_758_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108357_334_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032651_649_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034169_723_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108567_110_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031232_461_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034859_317_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034840_38_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032373_355_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031409_806_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033237_616_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034739_37_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032217_483_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_107912_485_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032652_645_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033619_378_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032579_396_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034121_722_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033838_793_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1030960_413_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033971_797_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033798_752_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033034_384_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035581_52_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035460_88_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032532_479_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032963_611_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_108041_351_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034663_660_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033532_272_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031710_463_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034345_259_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033588_252_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1035657_53_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034361_261_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1034534_651_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033640_539_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1033500_329_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1031153_440_weight.rvt
:RedirectToFile    ./obs/${WL_prefix}_1032731_785_weight.rvt
EOF
fi

#=====================================================================
# Lake Area
#=====================================================================
cat >> ${rvt} << EOF
#=====================================================================
# Lake Water Area 
:RedirectToFile    ./obs/${WA_prefix}_1035335_41.rvt    #1035335.0
:RedirectToFile    ./obs/${WA_prefix}_108435_315.rvt    #108435.0
:RedirectToFile    ./obs/${WA_prefix}_1034038_142.rvt   #1034038.0
:RedirectToFile    ./obs/${WA_prefix}_1033025_277.rvt   #1033025.0
:RedirectToFile    ./obs/${WA_prefix}_1032273_747.rvt   #1032273.0
:RedirectToFile    ./obs/${WA_prefix}_1032168_803.rvt   #1032168.0
:RedirectToFile    ./obs/${WA_prefix}_1033541_327.rvt   #1033541.0
:RedirectToFile    ./obs/${WA_prefix}_1034546_36.rvt    #1034546.0
:RedirectToFile    ./obs/${WA_prefix}_108585_116.rvt    #Timberwolf
:RedirectToFile    ./obs/${WA_prefix}_108316_126.rvt    #108316.0
:RedirectToFile    ./obs/${WA_prefix}_1031109_415.rvt   #1031109.0
:RedirectToFile    ./obs/${WA_prefix}_1034014_307.rvt   #1034014.0
:RedirectToFile    ./obs/${WA_prefix}_1033787_138.rvt   #1033787.0
:RedirectToFile    ./obs/${WA_prefix}_1033705_861.rvt   #1033705.0
:RedirectToFile    ./obs/${WA_prefix}_1032918_405.rvt   #1032918.0
:RedirectToFile    ./obs/${WA_prefix}_1033851_794.rvt   #1033851.0
:RedirectToFile    ./obs/${WA_prefix}_1035236_113.rvt   #1035236.0
:RedirectToFile    ./obs/${WA_prefix}_1032359_843.rvt   #1032359.0
:RedirectToFile    ./obs/${WA_prefix}_1032522_737.rvt   #1032522.0
:RedirectToFile    ./obs/${WA_prefix}_1033727_313.rvt   #1033727.0
:RedirectToFile    ./obs/${WA_prefix}_1035983_50.rvt    #1035983.0
:RedirectToFile    ./obs/${WA_prefix}_1035248_217.rvt   #1035248.0
:RedirectToFile    ./obs/${WA_prefix}_1035231_112.rvt   #1035231.0
:RedirectToFile    ./obs/${WA_prefix}_1031942_352.rvt   #1031942.0
:RedirectToFile    ./obs/${WA_prefix}_1035677_207.rvt   #1035677.0
:RedirectToFile    ./obs/${WA_prefix}_1033627_921.rvt   #02KB001
:RedirectToFile    ./obs/${WA_prefix}_108506_78.rvt     #108506.0
:RedirectToFile    ./obs/${WA_prefix}_1032769_399.rvt   #1032769.0
:RedirectToFile    ./obs/${WA_prefix}_1033915_720.rvt   #1033915.0
:RedirectToFile    ./obs/${WA_prefix}_1031014_304.rvt   #1031014.0
:RedirectToFile    ./obs/${WA_prefix}_1032691_646.rvt   #1032691.0
:RedirectToFile    ./obs/${WA_prefix}_1034075_544.rvt   #1034075.0
:RedirectToFile    ./obs/${WA_prefix}_108394_258.rvt    #108394.0
:RedirectToFile    ./obs/${WA_prefix}_108604_111.rvt    #108604.0
:RedirectToFile    ./obs/${WA_prefix}_1032780_596.rvt   #1032780.0
:RedirectToFile    ./obs/${WA_prefix}_1034708_344.rvt   #1034708.0
:RedirectToFile    ./obs/${WA_prefix}_108348_754.rvt    #108348.0
:RedirectToFile    ./obs/${WA_prefix}_1034574_321.rvt   #1034574.0
:RedirectToFile    ./obs/${WA_prefix}_108257_704.rvt    #108257.0
:RedirectToFile    ./obs/${WA_prefix}_1031839_452.rvt   #1031839.0
:RedirectToFile    ./obs/${WA_prefix}_1033850_543.rvt   #1033850.0
:RedirectToFile    ./obs/${WA_prefix}_1034091_536.rvt   #1034091.0
:RedirectToFile    ./obs/${WA_prefix}_1033704_379.rvt   #1033704.0
:RedirectToFile    ./obs/${WA_prefix}_1034122_859.rvt   #1034122.0
:RedirectToFile    ./obs/${WA_prefix}_108175_276.rvt    #108175.0
:RedirectToFile    ./obs/${WA_prefix}_1035432_87.rvt    #1035432.0
:RedirectToFile    ./obs/${WA_prefix}_1032797_650.rvt   #1032797.0
:RedirectToFile    ./obs/${WA_prefix}_1031844_427.rvt   #1031844.0
:RedirectToFile    ./obs/${WA_prefix}_1035069_216.rvt   #1035069.0
:RedirectToFile    ./obs/${WA_prefix}_108083_767.rvt    #Traverse
:RedirectToFile    ./obs/${WA_prefix}_1032285_354.rvt   #1032285.0
:RedirectToFile    ./obs/${WA_prefix}_1031986_430.rvt   #1031986.0
:RedirectToFile    ./obs/${WA_prefix}_1031979_429.rvt   #1031979.0
:RedirectToFile    ./obs/${WA_prefix}_1034245_267.rvt   #1034245.0
:RedirectToFile    ./obs/${WA_prefix}_1034926_319.rvt   #1034926.0
:RedirectToFile    ./obs/${WA_prefix}_1033549_847.rvt   #1033549.0
:RedirectToFile    ./obs/${WA_prefix}_108233_377.rvt    #108233.0
:RedirectToFile    ./obs/${WA_prefix}_108379_228.rvt    #Burntroot
:RedirectToFile    ./obs/${WA_prefix}_1031908_623.rvt   #1031908.0
:RedirectToFile    ./obs/${WA_prefix}_1033206_496.rvt   #1033206.0
:RedirectToFile    ./obs/${WA_prefix}_1031173_391.rvt   #1031173.0
:RedirectToFile    ./obs/${WA_prefix}_108500_73.rvt     #108500.0
:RedirectToFile    ./obs/${WA_prefix}_1031664_299.rvt   #1031664.0
:RedirectToFile    ./obs/${WA_prefix}_1033877_140.rvt   #1033877.0
:RedirectToFile    ./obs/${WA_prefix}_1031300_421.rvt   #1031300.0
:RedirectToFile    ./obs/${WA_prefix}_1034933_655.rvt   #1034933.0
:RedirectToFile    ./obs/${WA_prefix}_108226_901.rvt    #108226.0
:RedirectToFile    ./obs/${WA_prefix}_1032827_786.rvt   #1032827.0
:RedirectToFile    ./obs/${WA_prefix}_1033173_615.rvt   #1033173.0
:RedirectToFile    ./obs/${WA_prefix}_1033422_407.rvt   #1033422.0
:RedirectToFile    ./obs/${WA_prefix}_1034625_658.rvt   #1034625.0
:RedirectToFile    ./obs/${WA_prefix}_1034874_205.rvt   #1034874.0
:RedirectToFile    ./obs/${WA_prefix}_108470_164.rvt    #108470.0
:RedirectToFile    ./obs/${WA_prefix}_1032869_876.rvt   #1032869.0
:RedirectToFile    ./obs/${WA_prefix}_1034674_343.rvt   #1034674.0
:RedirectToFile    ./obs/${WA_prefix}_1034400_341.rvt   #1034400.0
:RedirectToFile    ./obs/${WA_prefix}_1032819_282.rvt   #1032819.0
:RedirectToFile    ./obs/${WA_prefix}_108369_241.rvt    #La Muir
:RedirectToFile    ./obs/${WA_prefix}_1035755_46.rvt    #1035755.0
:RedirectToFile    ./obs/${WA_prefix}_1032552_667.rvt   #1032552.0
:RedirectToFile    ./obs/${WA_prefix}_1034337_123.rvt   #1034337.0
:RedirectToFile    ./obs/${WA_prefix}_108451_260.rvt    #108451.0
:RedirectToFile    ./obs/${WA_prefix}_1032502_738.rvt   #1032502.0
:RedirectToFile    ./obs/${WA_prefix}_1034293_147.rvt   #1034293.0
:RedirectToFile    ./obs/${WA_prefix}_1032227_504.rvt   #1032227.0
:RedirectToFile    ./obs/${WA_prefix}_1034100_237.rvt   #1034100.0
:RedirectToFile    ./obs/${WA_prefix}_1033519_751.rvt   #1033519.0
:RedirectToFile    ./obs/${WA_prefix}_1031634_451.rvt   #1031634.0
:RedirectToFile    ./obs/${WA_prefix}_1034317_724.rvt   #1034317.0
:RedirectToFile    ./obs/${WA_prefix}_1033548_312.rvt   #1033548.0
:RedirectToFile    ./obs/${WA_prefix}_1032102_673.rvt   #1032102.0
:RedirectToFile    ./obs/${WA_prefix}_1031744_426.rvt   #1031744.0
:RedirectToFile    ./obs/${WA_prefix}_1032101_525.rvt   #1032101.0
:RedirectToFile    ./obs/${WA_prefix}_1033884_863.rvt   #1033884.0
:RedirectToFile    ./obs/${WA_prefix}_1035551_62.rvt    #1035551.0
:RedirectToFile    ./obs/${WA_prefix}_1034132_144.rvt   #1034132.0
:RedirectToFile    ./obs/${WA_prefix}_1033712_792.rvt   #1033712.0
:RedirectToFile    ./obs/${WA_prefix}_1031604_744.rvt   #1031604.0
:RedirectToFile    ./obs/${WA_prefix}_1033084_375.rvt   #1033084.0
:RedirectToFile    ./obs/${WA_prefix}_1034246_657.rvt   #1034246.0
:RedirectToFile    ./obs/${WA_prefix}_1035297_218.rvt   #1035297.0
:RedirectToFile    ./obs/${WA_prefix}_1033094_403.rvt   #1033094.0
:RedirectToFile    ./obs/${WA_prefix}_108564_135.rvt    #Misty
:RedirectToFile    ./obs/${WA_prefix}_1031318_443.rvt   #1031318.0
:RedirectToFile    ./obs/${WA_prefix}_1031964_501.rvt   #1031964.0
:RedirectToFile    ./obs/${WA_prefix}_1035727_57.rvt    #1035727.0
:RedirectToFile    ./obs/${WA_prefix}_1033905_795.rvt   #1033905.0
:RedirectToFile    ./obs/${WA_prefix}_1031261_419.rvt   #1031261.0
:RedirectToFile    ./obs/${WA_prefix}_1033145_902.rvt   #1033145.0
:RedirectToFile    ./obs/${WA_prefix}_1035794_58.rvt    #1035794.0
:RedirectToFile    ./obs/${WA_prefix}_1034212_335.rvt   #1034212.0
:RedirectToFile    ./obs/${WA_prefix}_1032851_610.rvt   #1032851.0
:RedirectToFile    ./obs/${WA_prefix}_1033900_236.rvt   #1033900.0
:RedirectToFile    ./obs/${WA_prefix}_1034741_654.rvt   #1034741.0
:RedirectToFile    ./obs/${WA_prefix}_1032953_582.rvt   #1032953.0
:RedirectToFile    ./obs/${WA_prefix}_1034144_553.rvt   #1034144.0
:RedirectToFile    ./obs/${WA_prefix}_1032844_281.rvt   #Narrowbag
:RedirectToFile    ./obs/${WA_prefix}_1034866_82.rvt    #1034866.0
:RedirectToFile    ./obs/${WA_prefix}_1034854_69.rvt    #1034854.0
:RedirectToFile    ./obs/${WA_prefix}_1033635_273.rvt   #1033635.0
:RedirectToFile    ./obs/${WA_prefix}_108303_919.rvt    #108303.0
:RedirectToFile    ./obs/${WA_prefix}_1032345_666.rvt   #1032345.0
:RedirectToFile    ./obs/${WA_prefix}_1031870_502.rvt   #1031870.0
:RedirectToFile    ./obs/${WA_prefix}_1031683_450.rvt   #1031683.0
:RedirectToFile    ./obs/${WA_prefix}_1034140_227.rvt   #1034140.0
:RedirectToFile    ./obs/${WA_prefix}_108193_875.rvt    #108193.0
:RedirectToFile    ./obs/${WA_prefix}_108015_449.rvt    #Little Cauchon
:RedirectToFile    ./obs/${WA_prefix}_1034409_549.rvt   #1034409.0
:RedirectToFile    ./obs/${WA_prefix}_1032458_580.rvt   #1032458.0
:RedirectToFile    ./obs/${WA_prefix}_1033144_810.rvt   #1033144.0
:RedirectToFile    ./obs/${WA_prefix}_1034597_268.rvt   #1034597.0
:RedirectToFile    ./obs/${WA_prefix}_1032986_692.rvt   #1032986.0
:RedirectToFile    ./obs/${WA_prefix}_1033299_330.rvt   #1033299.0
:RedirectToFile    ./obs/${WA_prefix}_1032795_520.rvt   #1032795.0
:RedirectToFile    ./obs/${WA_prefix}_1033132_495.rvt   #1033132.0
:RedirectToFile    ./obs/${WA_prefix}_1031873_745.rvt   #1031873.0
:RedirectToFile    ./obs/${WA_prefix}_1034695_148.rvt   #1034695.0
:RedirectToFile    ./obs/${WA_prefix}_1031362_500.rvt   #1031362.0
:RedirectToFile    ./obs/${WA_prefix}_1034101_760.rvt   #1034101.0
:RedirectToFile    ./obs/${WA_prefix}_1031919_428.rvt   #1031919.0
:RedirectToFile    ./obs/${WA_prefix}_1031624_442.rvt   #1031624.0
:RedirectToFile    ./obs/${WA_prefix}_1031745_789.rvt   #1031745.0
:RedirectToFile    ./obs/${WA_prefix}_1033557_862.rvt   #1033557.0
:RedirectToFile    ./obs/${WA_prefix}_1033131_376.rvt   #1033131.0
:RedirectToFile    ./obs/${WA_prefix}_1032609_739.rvt   #1032609.0
:RedirectToFile    ./obs/${WA_prefix}_1031283_441.rvt   #1031283.0
:RedirectToFile    ./obs/${WA_prefix}_107949_294.rvt    #107949.0
:RedirectToFile    ./obs/${WA_prefix}_1033211_310.rvt   #1033211.0
:RedirectToFile    ./obs/${WA_prefix}_1032312_587.rvt   #1032312.0
:RedirectToFile    ./obs/${WA_prefix}_108509_215.rvt    #108509.0
:RedirectToFile    ./obs/${WA_prefix}_1034633_659.rvt   #1034633.0
:RedirectToFile    ./obs/${WA_prefix}_108446_77.rvt     #108446.0
:RedirectToFile    ./obs/${WA_prefix}_1034801_71.rvt    #1034801.0
:RedirectToFile    ./obs/${WA_prefix}_1030966_302.rvt   #1030966.0
:RedirectToFile    ./obs/${WA_prefix}_1035858_210.rvt   #1035858.0
:RedirectToFile    ./obs/${WA_prefix}_1034048_143.rvt   #1034048.0
:RedirectToFile    ./obs/${WA_prefix}_108614_47.rvt     #108614.0
:RedirectToFile    ./obs/${WA_prefix}_1034740_221.rvt   #1034740.0
:RedirectToFile    ./obs/${WA_prefix}_1030543_417.rvt   #1030543.0
:RedirectToFile    ./obs/${WA_prefix}_1031538_422.rvt   #1031538.0
:RedirectToFile    ./obs/${WA_prefix}_1031841_808.rvt   #1031841.0
:RedirectToFile    ./obs/${WA_prefix}_1033765_338.rvt   #1033765.0
:RedirectToFile    ./obs/${WA_prefix}_1032210_499.rvt   #1032210.0
:RedirectToFile    ./obs/${WA_prefix}_108347_753.rvt    #Grand
:RedirectToFile    ./obs/${WA_prefix}_1032551_559.rvt   #1032551.0
:RedirectToFile    ./obs/${WA_prefix}_1034612_342.rvt   #1034612.0
:RedirectToFile    ./obs/${WA_prefix}_1034890_83.rvt    #1034890.0
:RedirectToFile    ./obs/${WA_prefix}_1034185_687.rvt   #1034185.0
:RedirectToFile    ./obs/${WA_prefix}_1034662_167.rvt   #1034662.0
:RedirectToFile    ./obs/${WA_prefix}_1034213_547.rvt   #1034213.0
:RedirectToFile    ./obs/${WA_prefix}_1033490_250.rvt   #1033490.0
:RedirectToFile    ./obs/${WA_prefix}_1034585_202.rvt   #1034585.0
:RedirectToFile    ./obs/${WA_prefix}_1034487_165.rvt   #1034487.0
:RedirectToFile    ./obs/${WA_prefix}_1035566_43.rvt    #1035566.0
:RedirectToFile    ./obs/${WA_prefix}_108126_574.rvt    #Radiant
:RedirectToFile    ./obs/${WA_prefix}_1032092_802.rvt   #1032092.0
:RedirectToFile    ./obs/${WA_prefix}_1031002_303.rvt   #1031002.0
:RedirectToFile    ./obs/${WA_prefix}_1033817_235.rvt   #1033817.0
:RedirectToFile    ./obs/${WA_prefix}_1033345_328.rvt   #1033345.0
:RedirectToFile    ./obs/${WA_prefix}_1034389_243.rvt   #1034389.0
:RedirectToFile    ./obs/${WA_prefix}_1034707_67.rvt    #1034707.0
:RedirectToFile    ./obs/${WA_prefix}_1033977_864.rvt   #1033977.0
:RedirectToFile    ./obs/${WA_prefix}_1033509_717.rvt   #1033509.0
:RedirectToFile    ./obs/${WA_prefix}_1032906_283.rvt   #1032906.0
:RedirectToFile    ./obs/${WA_prefix}_1032671_740.rvt   #1032671.0
:RedirectToFile    ./obs/${WA_prefix}_1034033_129.rvt   #1034033.0
:RedirectToFile    ./obs/${WA_prefix}_1033908_229.rvt   #1033908.0
:RedirectToFile    ./obs/${WA_prefix}_1032634_575.rvt   #1032634.0
:RedirectToFile    ./obs/${WA_prefix}_1034632_65.rvt    #1034632.0
:RedirectToFile    ./obs/${WA_prefix}_1033298_278.rvt   #1033298.0
:RedirectToFile    ./obs/${WA_prefix}_1033116_361.rvt   #1033116.0
:RedirectToFile    ./obs/${WA_prefix}_1034436_133.rvt   #1034436.0
:RedirectToFile    ./obs/${WA_prefix}_1034867_204.rvt   #1034867.0
:RedirectToFile    ./obs/${WA_prefix}_1032404_279.rvt   #1032404.0
:RedirectToFile    ./obs/${WA_prefix}_1033077_406.rvt   #1033077.0
:RedirectToFile    ./obs/${WA_prefix}_1034634_203.rvt   #1034634.0
:RedirectToFile    ./obs/${WA_prefix}_8767_326.rvt      #Lavieille
:RedirectToFile    ./obs/${WA_prefix}_1034936_74.rvt    #1034936.0
:RedirectToFile    ./obs/${WA_prefix}_1031452_770.rvt   #1031452.0
:RedirectToFile    ./obs/${WA_prefix}_1031609_462.rvt   #1031609.0
:RedirectToFile    ./obs/${WA_prefix}_1032580_887.rvt   #1032580.0
:RedirectToFile    ./obs/${WA_prefix}_1033643_554.rvt   #1033643.0
:RedirectToFile    ./obs/${WA_prefix}_1034584_201.rvt   #1034584.0
:RedirectToFile    ./obs/${WA_prefix}_1033363_247.rvt   #1033363.0
:RedirectToFile    ./obs/${WA_prefix}_107978_459.rvt    #107978.0
:RedirectToFile    ./obs/${WA_prefix}_1033852_867.rvt   #1033852.0
:RedirectToFile    ./obs/${WA_prefix}_1031410_807.rvt   #1031410.0
:RedirectToFile    ./obs/${WA_prefix}_1034034_230.rvt   #1034034.0
:RedirectToFile    ./obs/${WA_prefix}_1033350_716.rvt   #1033350.0
:RedirectToFile    ./obs/${WA_prefix}_1033491_311.rvt   #1033491.0
:RedirectToFile    ./obs/${WA_prefix}_1032591_481.rvt   #1032591.0
:RedirectToFile    ./obs/${WA_prefix}_1033162_457.rvt   #1033162.0
:RedirectToFile    ./obs/${WA_prefix}_108541_81.rvt     #108541.0
:RedirectToFile    ./obs/${WA_prefix}_1031779_529.rvt   #1031779.0
:RedirectToFile    ./obs/${WA_prefix}_1031889_799.rvt   #1031889.0
:RedirectToFile    ./obs/${WA_prefix}_1034841_214.rvt   #1034841.0
:RedirectToFile    ./obs/${WA_prefix}_8778_322.rvt      #8778.0
:RedirectToFile    ./obs/${WA_prefix}_1031887_424.rvt   #1031887.0
:RedirectToFile    ./obs/${WA_prefix}_108275_246.rvt    #108275.0
:RedirectToFile    ./obs/${WA_prefix}_1030949_301.rvt   #1030949.0
:RedirectToFile    ./obs/${WA_prefix}_108465_200.rvt    #108465.0
:RedirectToFile    ./obs/${WA_prefix}_1034611_124.rvt   #1034611.0
:RedirectToFile    ./obs/${WA_prefix}_1032645_480.rvt   #1032645.0
:RedirectToFile    ./obs/${WA_prefix}_108618_61.rvt     #108618.0
:RedirectToFile    ./obs/${WA_prefix}_1031008_390.rvt   #1031008.0
:RedirectToFile    ./obs/${WA_prefix}_1034453_225.rvt   #1034453.0
:RedirectToFile    ./obs/${WA_prefix}_1036081_51.rvt    #1036081.0
:RedirectToFile    ./obs/${WA_prefix}_1034051_130.rvt   #1034051.0
:RedirectToFile    ./obs/${WA_prefix}_1032421_584.rvt   #1032421.0
:RedirectToFile    ./obs/${WA_prefix}_108404_122.rvt    #Loontail
:RedirectToFile    ./obs/${WA_prefix}_1034755_68.rvt    #1034755.0
:RedirectToFile    ./obs/${WA_prefix}_1035996_211.rvt   #1035996.0
:RedirectToFile    ./obs/${WA_prefix}_1031625_298.rvt   #1031625.0
:RedirectToFile    ./obs/${WA_prefix}_1035399_136.rvt   #1035399.0
:RedirectToFile    ./obs/${WA_prefix}_1033669_253.rvt   #1033669.0
:RedirectToFile    ./obs/${WA_prefix}_1035854_59.rvt    #1035854.0
:RedirectToFile    ./obs/${WA_prefix}_1035235_86.rvt    #1035235.0
:RedirectToFile    ./obs/${WA_prefix}_1033970_540.rvt   #1033970.0
:RedirectToFile    ./obs/${WA_prefix}_1032603_585.rvt   #1032603.0
:RedirectToFile    ./obs/${WA_prefix}_1033546_251.rvt   #1033546.0
:RedirectToFile    ./obs/${WA_prefix}_1033458_538.rvt   #1033458.0
:RedirectToFile    ./obs/${WA_prefix}_1033837_541.rvt   #1033837.0
:RedirectToFile    ./obs/${WA_prefix}_1034552_336.rvt   #1034552.0
:RedirectToFile    ./obs/${WA_prefix}_1034444_120.rvt   #1034444.0
:RedirectToFile    ./obs/${WA_prefix}_1033127_886.rvt   #1033127.0
:RedirectToFile    ./obs/${WA_prefix}_1034705_66.rvt    #1034705.0
:RedirectToFile    ./obs/${WA_prefix}_1032539_280.rvt   #1032539.0
:RedirectToFile    ./obs/${WA_prefix}_1033117_612.rvt   #1033117.0
:RedirectToFile    ./obs/${WA_prefix}_1033678_274.rvt   #1033678.0
:RedirectToFile    ./obs/${WA_prefix}_1034386_548.rvt   #1034386.0
:RedirectToFile    ./obs/${WA_prefix}_1032218_503.rvt   #1032218.0
:RedirectToFile    ./obs/${WA_prefix}_1035622_63.rvt    #1035622.0
:RedirectToFile    ./obs/${WA_prefix}_1033862_128.rvt   #1033862.0
:RedirectToFile    ./obs/${WA_prefix}_8741_528.rvt      #Cedar
:RedirectToFile    ./obs/${WA_prefix}_108298_249.rvt    #108298.0
:RedirectToFile    ./obs/${WA_prefix}_1033916_869.rvt   #1033916.0
:RedirectToFile    ./obs/${WA_prefix}_1031292_420.rvt   #1031292.0
:RedirectToFile    ./obs/${WA_prefix}_1032749_742.rvt   #1032749.0
:RedirectToFile    ./obs/${WA_prefix}_1032083_800.rvt   #1032083.0
:RedirectToFile    ./obs/${WA_prefix}_1031451_460.rvt   #1031451.0
:RedirectToFile    ./obs/${WA_prefix}_1032794_519.rvt   #1032794.0
:RedirectToFile    ./obs/${WA_prefix}_1032390_579.rvt   #1032390.0
:RedirectToFile    ./obs/${WA_prefix}_1036038_117.rvt   #Lilypond
:RedirectToFile    ./obs/${WA_prefix}_1034125_131.rvt   #1034125.0
:RedirectToFile    ./obs/${WA_prefix}_1034305_316.rvt   #1034305.0
:RedirectToFile    ./obs/${WA_prefix}_8781_220.rvt      #Big Trout
:RedirectToFile    ./obs/${WA_prefix}_1031843_465.rvt   #1031843.0
:RedirectToFile    ./obs/${WA_prefix}_1032676_397.rvt   #1032676.0
:RedirectToFile    ./obs/${WA_prefix}_1030917_389.rvt   #1030917.0
:RedirectToFile    ./obs/${WA_prefix}_1032677_398.rvt   #1032677.0
:RedirectToFile    ./obs/${WA_prefix}_1031435_295.rvt   #1031435.0
:RedirectToFile    ./obs/${WA_prefix}_1031042_305.rvt   #1031042.0
:RedirectToFile    ./obs/${WA_prefix}_1031615_466.rvt   #1031615.0
:RedirectToFile    ./obs/${WA_prefix}_1033733_555.rvt   #1033733.0
:RedirectToFile    ./obs/${WA_prefix}_1033035_402.rvt   #1033035.0
:RedirectToFile    ./obs/${WA_prefix}_1035731_45.rvt    #1035731.0
:RedirectToFile    ./obs/${WA_prefix}_1031965_586.rvt   #1031965.0
:RedirectToFile    ./obs/${WA_prefix}_1033133_906.rvt   #1033133.0
:RedirectToFile    ./obs/${WA_prefix}_1031162_363.rvt   #1031162.0
:RedirectToFile    ./obs/${WA_prefix}_8762_291.rvt      #Hogan
:RedirectToFile    ./obs/${WA_prefix}_1033928_865.rvt   #1033928.0
:RedirectToFile    ./obs/${WA_prefix}_108324_552.rvt    #108324.0
:RedirectToFile    ./obs/${WA_prefix}_1035812_48.rvt    #Hambone
:RedirectToFile    ./obs/${WA_prefix}_1031733_464.rvt   #1031733.0
:RedirectToFile    ./obs/${WA_prefix}_1034937_84.rvt    #1034937.0
:RedirectToFile    ./obs/${WA_prefix}_1031714_522.rvt   #1031714.0
:RedirectToFile    ./obs/${WA_prefix}_1032135_353.rvt   #1032135.0
:RedirectToFile    ./obs/${WA_prefix}_108422_231.rvt    #108422.0
:RedirectToFile    ./obs/${WA_prefix}_1034486_35.rvt    #1034486.0
:RedirectToFile    ./obs/${WA_prefix}_1032240_665.rvt   #1032240.0
:RedirectToFile    ./obs/${WA_prefix}_1032437_844.rvt   #1032437.0
:RedirectToFile    ./obs/${WA_prefix}_1033508_248.rvt   #1033508.0
:RedirectToFile    ./obs/${WA_prefix}_1035728_44.rvt    #1035728.0
:RedirectToFile    ./obs/${WA_prefix}_1033670_718.rvt   #1033670.0
:RedirectToFile    ./obs/${WA_prefix}_1034131_132.rvt   #1034131.0
:RedirectToFile    ./obs/${WA_prefix}_1033831_719.rvt   #1033831.0
:RedirectToFile    ./obs/${WA_prefix}_1034660_653.rvt   #1034660.0
:RedirectToFile    ./obs/${WA_prefix}_108004_531.rvt    #108004.0
:RedirectToFile    ./obs/${WA_prefix}_108027_497.rvt    #North Depot
:RedirectToFile    ./obs/${WA_prefix}_1034459_290.rvt   #1034459.0
:RedirectToFile    ./obs/${WA_prefix}_1033680_393.rvt   #1033680.0
:RedirectToFile    ./obs/${WA_prefix}_1035210_85.rvt    #1035210.0
:RedirectToFile    ./obs/${WA_prefix}_108494_652.rvt    #108494.0
:RedirectToFile    ./obs/${WA_prefix}_1030908_388.rvt   #1030908.0
:RedirectToFile    ./obs/${WA_prefix}_1031780_798.rvt   #1031780.0
:RedirectToFile    ./obs/${WA_prefix}_1034198_686.rvt   #1034198.0
:RedirectToFile    ./obs/${WA_prefix}_1031842_423.rvt   #1031842.0
:RedirectToFile    ./obs/${WA_prefix}_1034133_308.rvt   #1034133.0
:RedirectToFile    ./obs/${WA_prefix}_1035821_49.rvt    #1035821.0
:RedirectToFile    ./obs/${WA_prefix}_1032796_598.rvt   #1032796.0
:RedirectToFile    ./obs/${WA_prefix}_1034951_39.rvt    #1034951.0
:RedirectToFile    ./obs/${WA_prefix}_1033587_127.rvt   #1033587.0
:RedirectToFile    ./obs/${WA_prefix}_1032864_597.rvt   #1032864.0
:RedirectToFile    ./obs/${WA_prefix}_1034779_345.rvt   #Animoosh
:RedirectToFile    ./obs/${WA_prefix}_108638_209.rvt    #108638.0
:RedirectToFile    ./obs/${WA_prefix}_1032044_578.rvt   #1032044.0
:RedirectToFile    ./obs/${WA_prefix}_1031603_297.rvt   #1031603.0
:RedirectToFile    ./obs/${WA_prefix}_1033439_381.rvt   #Charles
:RedirectToFile    ./obs/${WA_prefix}_1034989_75.rvt    #1034989.0
:RedirectToFile    ./obs/${WA_prefix}_1033959_880.rvt   #1033959.0
:RedirectToFile    ./obs/${WA_prefix}_1035387_42.rvt    #1035387.0
:RedirectToFile    ./obs/${WA_prefix}_1033280_669.rvt   #1033280.0
:RedirectToFile    ./obs/${WA_prefix}_1032834_401.rvt   #1032834.0
:RedirectToFile    ./obs/${WA_prefix}_1033982_542.rvt   #1033982.0
:RedirectToFile    ./obs/${WA_prefix}_1033935_796.rvt   #1033935.0
:RedirectToFile    ./obs/${WA_prefix}_1033803_758.rvt   #1033803.0
:RedirectToFile    ./obs/${WA_prefix}_108357_334.rvt    #108357.0
:RedirectToFile    ./obs/${WA_prefix}_1032651_649.rvt   #1032651.0
:RedirectToFile    ./obs/${WA_prefix}_1034169_723.rvt   #1034169.0
:RedirectToFile    ./obs/${WA_prefix}_108567_110.rvt    #108567.0
:RedirectToFile    ./obs/${WA_prefix}_1031232_461.rvt   #1031232.0
:RedirectToFile    ./obs/${WA_prefix}_1034859_317.rvt   #1034859.0
:RedirectToFile    ./obs/${WA_prefix}_1034840_38.rvt    #1034840.0
:RedirectToFile    ./obs/${WA_prefix}_1032373_355.rvt   #1032373.0
:RedirectToFile    ./obs/${WA_prefix}_1031409_806.rvt   #1031409.0
:RedirectToFile    ./obs/${WA_prefix}_1033237_616.rvt   #1033237.0
:RedirectToFile    ./obs/${WA_prefix}_1034739_37.rvt    #1034739.0
:RedirectToFile    ./obs/${WA_prefix}_1032217_483.rvt   #1032217.0
:RedirectToFile    ./obs/${WA_prefix}_107912_485.rvt    #107912.0
:RedirectToFile    ./obs/${WA_prefix}_1032652_645.rvt   #1032652.0
:RedirectToFile    ./obs/${WA_prefix}_1033619_378.rvt   #1033619.0
:RedirectToFile    ./obs/${WA_prefix}_1032579_396.rvt   #1032579.0
:RedirectToFile    ./obs/${WA_prefix}_1034121_722.rvt   #1034121.0
:RedirectToFile    ./obs/${WA_prefix}_1033838_793.rvt   #1033838.0
:RedirectToFile    ./obs/${WA_prefix}_1030960_413.rvt   #1030960.0
:RedirectToFile    ./obs/${WA_prefix}_1033971_797.rvt   #1033971.0
:RedirectToFile    ./obs/${WA_prefix}_1033798_752.rvt   #1033798.0
:RedirectToFile    ./obs/${WA_prefix}_1033034_384.rvt   #1033034.0
:RedirectToFile    ./obs/${WA_prefix}_1035581_52.rvt    #1035581.0
:RedirectToFile    ./obs/${WA_prefix}_1035460_88.rvt    #1035460.0
:RedirectToFile    ./obs/${WA_prefix}_1032532_479.rvt   #1032532.0
:RedirectToFile    ./obs/${WA_prefix}_1032963_611.rvt   #1032963.0
:RedirectToFile    ./obs/${WA_prefix}_108041_351.rvt    #108041.0
:RedirectToFile    ./obs/${WA_prefix}_1034663_660.rvt   #1034663.0
:RedirectToFile    ./obs/${WA_prefix}_1033532_272.rvt   #1033532.0
:RedirectToFile    ./obs/${WA_prefix}_1031710_463.rvt   #1031710.0
:RedirectToFile    ./obs/${WA_prefix}_1034345_259.rvt   #1034345.0
:RedirectToFile    ./obs/${WA_prefix}_1033588_252.rvt   #1033588.0
:RedirectToFile    ./obs/${WA_prefix}_1035657_53.rvt    #1035657.0
:RedirectToFile    ./obs/${WA_prefix}_1034361_261.rvt   #1034361.0
:RedirectToFile    ./obs/${WA_prefix}_1034534_651.rvt   #1034534.0
:RedirectToFile    ./obs/${WA_prefix}_1033640_539.rvt   #1033640.0
:RedirectToFile    ./obs/${WA_prefix}_1033500_329.rvt   #1033500.0
:RedirectToFile    ./obs/${WA_prefix}_1031153_440.rvt   #1031153.0
:RedirectToFile    ./obs/${WA_prefix}_1032731_785.rvt   #1032731.0

# Weight to remove winter period [Dec-1 - Apr-1]
:RedirectToFile    ./obs/${WA_prefix}_1035335_41_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108435_315_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034038_142_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033025_277_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032273_747_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032168_803_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033541_327_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034546_36_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108585_116_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108316_126_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031109_415_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034014_307_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033787_138_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033705_861_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032918_405_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033851_794_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035236_113_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032359_843_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032522_737_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033727_313_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035983_50_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035248_217_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035231_112_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031942_352_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035677_207_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033627_921_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108506_78_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032769_399_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033915_720_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031014_304_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032691_646_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034075_544_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108394_258_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108604_111_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032780_596_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034708_344_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108348_754_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034574_321_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108257_704_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031839_452_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033850_543_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034091_536_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033704_379_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034122_859_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108175_276_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035432_87_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032797_650_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031844_427_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035069_216_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108083_767_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032285_354_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031986_430_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031979_429_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034245_267_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034926_319_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033549_847_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108233_377_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108379_228_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031908_623_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033206_496_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031173_391_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108500_73_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031664_299_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033877_140_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031300_421_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034933_655_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108226_901_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032827_786_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033173_615_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033422_407_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034625_658_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034874_205_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108470_164_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032869_876_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034674_343_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034400_341_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032819_282_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108369_241_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035755_46_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032552_667_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034337_123_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108451_260_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032502_738_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034293_147_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032227_504_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034100_237_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033519_751_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031634_451_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034317_724_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033548_312_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032102_673_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031744_426_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032101_525_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033884_863_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035551_62_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034132_144_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033712_792_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031604_744_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033084_375_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034246_657_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035297_218_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033094_403_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108564_135_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031318_443_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031964_501_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035727_57_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033905_795_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031261_419_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033145_902_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035794_58_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034212_335_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032851_610_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033900_236_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034741_654_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032953_582_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034144_553_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032844_281_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034866_82_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034854_69_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033635_273_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108303_919_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032345_666_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031870_502_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031683_450_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034140_227_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108193_875_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108015_449_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034409_549_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032458_580_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033144_810_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034597_268_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032986_692_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033299_330_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032795_520_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033132_495_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031873_745_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034695_148_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031362_500_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034101_760_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031919_428_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031624_442_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031745_789_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033557_862_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033131_376_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032609_739_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031283_441_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_107949_294_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033211_310_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032312_587_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108509_215_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034633_659_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108446_77_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034801_71_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1030966_302_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035858_210_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034048_143_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108614_47_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034740_221_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1030543_417_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031538_422_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031841_808_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033765_338_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032210_499_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108347_753_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032551_559_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034612_342_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034890_83_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034185_687_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034662_167_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034213_547_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033490_250_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034585_202_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034487_165_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035566_43_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108126_574_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032092_802_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031002_303_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033817_235_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033345_328_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034389_243_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034707_67_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033977_864_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033509_717_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032906_283_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032671_740_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034033_129_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033908_229_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032634_575_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034632_65_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033298_278_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033116_361_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034436_133_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034867_204_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032404_279_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033077_406_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034634_203_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_8767_326_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034936_74_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031452_770_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031609_462_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032580_887_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033643_554_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034584_201_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033363_247_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_107978_459_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033852_867_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031410_807_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034034_230_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033350_716_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033491_311_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032591_481_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033162_457_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108541_81_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031779_529_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031889_799_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034841_214_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_8778_322_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031887_424_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108275_246_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1030949_301_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108465_200_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034611_124_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032645_480_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108618_61_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031008_390_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034453_225_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1036081_51_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034051_130_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032421_584_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108404_122_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034755_68_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035996_211_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031625_298_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035399_136_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033669_253_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035854_59_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035235_86_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033970_540_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032603_585_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033546_251_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033458_538_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033837_541_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034552_336_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034444_120_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033127_886_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034705_66_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032539_280_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033117_612_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033678_274_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034386_548_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032218_503_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035622_63_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033862_128_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_8741_528_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108298_249_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033916_869_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031292_420_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032749_742_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032083_800_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031451_460_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032794_519_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032390_579_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1036038_117_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034125_131_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034305_316_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_8781_220_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031843_465_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032676_397_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1030917_389_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032677_398_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031435_295_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031042_305_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031615_466_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033733_555_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033035_402_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035731_45_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031965_586_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033133_906_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031162_363_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_8762_291_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033928_865_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108324_552_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035812_48_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031733_464_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034937_84_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031714_522_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032135_353_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108422_231_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034486_35_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032240_665_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032437_844_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033508_248_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035728_44_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033670_718_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034131_132_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033831_719_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034660_653_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108004_531_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108027_497_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034459_290_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033680_393_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035210_85_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108494_652_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1030908_388_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031780_798_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034198_686_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031842_423_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034133_308_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035821_49_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032796_598_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034951_39_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033587_127_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032864_597_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034779_345_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108638_209_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032044_578_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031603_297_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033439_381_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034989_75_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033959_880_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035387_42_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033280_669_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032834_401_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033982_542_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033935_796_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033803_758_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108357_334_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032651_649_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034169_723_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108567_110_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031232_461_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034859_317_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034840_38_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032373_355_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031409_806_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033237_616_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034739_37_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032217_483_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_107912_485_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032652_645_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033619_378_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032579_396_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034121_722_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033838_793_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1030960_413_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033971_797_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033798_752_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033034_384_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035581_52_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035460_88_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032532_479_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032963_611_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_108041_351_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034663_660_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033532_272_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031710_463_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034345_259_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033588_252_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1035657_53_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034361_261_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1034534_651_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033640_539_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1033500_329_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1031153_440_weight.rvt
:RedirectToFile    ./obs/${WA_prefix}_1032731_785_weight.rvt

EOF
#============================================================
# Run Raven


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