#!/bin/bash
# set -x 
# trap read debug

expname=${1} #'0a'
ens_num=`printf '%02d\n' "${2}"`
#=====================================
echo $ens_num
# make experiment pertunation directory
echo "making folder --> ./out/S${expname}_${ens_num}"
mkdir -p ./out/S${expname}_${ens_num}
# cd into 
cd ./out/S${expname}_${ens_num}

# copy main Ostrich + Raven model calibation pacakage
cp -r ../../OstrichRaven/* . 

# create observation lake list
obs_gauge_ini=('Misty' 'Animoosh' 'Traverse' 'Burntroot' 'La Muir' 'Narrowbag' 'Little Cauchon' 'Hogan' 'North Depot' 'Radiant' 'Loontail' 'Cedar' 'Big Trout' 'Grand' 'Lavieille')

if [[ ${expname} = "0b" || ${expname} = "0d" || ${expname} = "0e" || ${expname} = "0f"  ||  ${expname} = "1a" || ${expname} = "1d" ]]; then  
    obs_gauge_ini=('Misty' 'Animoosh' 'Traverse' 'Burntroot' 'La Muir' 'Narrowbag' 'Little Cauchon' 'Hogan' 'North Depot' 'Radiant' 'Loontail' 'Cedar' 'Big Trout' 'Grand' 'Lavieille')
elif [ ${expname} = "1b" ]; then
    obs_gauge_ini=('Misty' 'Traverse' 'Narrowbag' 'Radiant' 'Cedar' 'Big Trout')
elif [ ${expname} = "1e" ]; then
    obs_gauge_ini=('Animoosh' 'Traverse' 'Burntroot' 'La Muir' 'Little Cauchon' 'Hogan' 'Radiant' 'Cedar' 'Big Trout' 'Grand' 'Lavieille')
elif [ ${expname} = "1f" ]; then
    obs_gauge_ini=('Misty' 'Animoosh' 'Traverse' 'Burntroot' 'La Muir' 'Little Cauchon' 'Hogan' 'North Depot' 'Radiant' 'Loontail' 'Cedar' 'Big Trout' 'Grand' 'Lavieille')
elif [ ${expname} = "1g" ]; then
    obs_gauge_ini=('Traverse' 'Burntroot' 'North Depot' 'Radiant' 'Narrowbag')
elif [ ${expname} = "1h" ]; then
    obs_gauge_ini=('Misty' 'Traverse' 'Burntroot' 'Narrowbag' 'Little Cauchon' 'North Depot' 'Radiant' 'Cedar' 'Big Trout' 'Grand' 'Lavieille')
elif [ ${expname} = "1i" ]; then
    obs_gauge_ini=('Animoosh' 'Traverse' 'Burntroot' 'La Muir' 'Little Cauchon' 'Hogan' 'Radiant' 'Cedar' 'Big Trout' 'Grand' 'Lavieille' 'Narrowbag')
elif [ ${expname} = "1j" ]; then
    obs_gauge_ini=('Traverse' 'Burntroot' 'Little Cauchon' 'Radiant' 'Cedar' 'Big Trout' 'Grand' 'Lavieille')
elif [ ${expname} = "1k" ]; then
    obs_gauge_ini=('Traverse' 'Burntroot' 'Little Cauchon' 'Radiant' 'Cedar' 'Big Trout' 'Grand' 'Lavieille' 'Narrowbag')
elif [[ ${expname} = "0a" ||  ${expname} = "0c" ||  ${expname} = "1c" ]]; then
    obs_gauge_ini=('Misty' 'Animoosh' 'Traverse' 'Burntroot' 'La Muir' 'Narrowbag' 'Little Cauchon' 'Hogan' 'North Depot' 'Radiant' 'Loontail' 'Cedar' 'Big Trout' 'Grand' 'Lavieille')
else
    obs_gauge_ini=('Misty' 'Animoosh' 'Traverse' 'Burntroot' 'La Muir' 'Narrowbag' 'Little Cauchon' 'Hogan' 'North Depot' 'Radiant' 'Loontail' 'Cedar' 'Big Trout' 'Grand' 'Lavieille')
fi

# write to csv file
output_file="obs_gauge_ini.csv"
# Write the list to the CSV file
echo "obs_gauge_ini" > "$output_file" # Writing the column header
for item in "${obs_gauge_ini[@]}"; do
    echo "$item" >> "$output_file" # Appending each item to the CSV file
done

# create model_structure.txt
if [[ ${expname} = "0b"  || ${expname} = "0d"  ||  ${expname} = "1a" ||  ${expname} = "1b" || ${expname} = "1d" ||  ${expname} = "1e" ||  ${expname} = "1f" ||  ${expname} = "1g" ||  ${expname} = "1h" ||  ${expname} = "1i" ||  ${expname} = "1j" ||  ${expname} = "1k" ]]; then
    echo "S1" > model_structure.txt
elif [[ ${expname} = "0a" ||  ${expname} = "0c" ||  ${expname} = "1c" ]]; then
    echo "S3" > model_structure.txt
else
    echo "S1" > model_structure.txt
fi

#=================
# Routing method
if [[ ${expname} = "0e" || ${expname} = "0f" ]]; then
    Routing='ROUTE_DIFFUSIVE_WAVE'
else 
    Routing='ROUTE_HYDROLOGIC'
fi

# Catchment Routing method
CatchmentRoute='ROUTE_TRI_CONVOLUTION'

# edit rvi file
cd ./RavenInput
rvi='Petawawa.rvi'
rm -r ${rvi}
# rvi 
cat >> ${rvi} << EOF
# ----------------------------------------------
# Raven Input file
# HBV-EC Petawawa River
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


:Routing                ${Routing}
:CatchmentRoute         ${CatchmentRoute}
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
:SuppressOutput
:SilentMode
:DontWriteWatershedStorage
:EvaluationMetrics NASH_SUTCLIFFE RMSE KLING_GUPTA KLING_GUPTA_DEVIATION R2 SPEARMAN

EOF

# go back
cd ../

# edit .tpl files

#========================
# rvp.tpl
#========================
# AvgAnnualRunoff
if [ ${expname} = "0f" ]; then
    AvgAnnualRunoff='%AvgAnnualRunoff%'
else 
    AvgAnnualRunoff='477'
fi
rvp_tpl='Petawawa.rvp.tpl'
rm -r ${rvp_tpl}
# rvp.tpl
cat >> ${rvp_tpl} << EOF
#-----------------------------------------------------------------
# Raven Properties file Template. Created by Raven v2.9 w/ netCDF
#-----------------------------------------------------------------
# all expressions of format *xxx* need to be specified by the user 
# all parameter values of format ** need to be specified by the user 
# soil, land use, and vegetation classes should be made consistent with user-generated .rvh file 
#-----------------------------------------------------------------
:AvgAnnualRunoff  ${AvgAnnualRunoff}

# -Orographic Corrections-------------------------------------
#:PrecipitationLapseRate %PLapRate%
#:AdiabaticLapseRate %TLapRate%

#-----------------------------------------------------------------
# Soil Classes
#-----------------------------------------------------------------
:SoilClasses          
:Attributes		      SAND	  %CLAY	 %SILT	 %ORGANIC
	:Units			  none	  none	 none	 none
	Forest_Floor,     0.66,   0.1,  0.24,    0.05,    
	Ablation_Till,    0.66,   0.1,  0.24,    0.03,    
	Basal_Till,       0.22,   0.13, 0.65,    0.02,     
:EndSoilClasses

#-----------------------------------------------------------------
# Land Use Classes
#-----------------------------------------------------------------
:LandUseClasses, 
  :Attributes,        IMPERM,          FOREST_COV,    LAKE_PET_CORR,
       :Units,          frac,                frac,             frac,       
  Landuse_Land_HRU,        0,                   1,                1,            
  LAKE,                    0,                   0,  %LAKE_PET_CORR%,     
:EndLandUseClasses

#-----------------------------------------------------------------
# Vegetation Classes
#-----------------------------------------------------------------

:VegetationClasses, 
  :Attributes,        MAX_HT,       MAX_LAI,   MAX_LEAF_COND, 
       :Units,             m,          none,        mm_per_s, 
    Veg_Land_HRU,           15,           7.5,             5.3,     
    LAKE,                    0,             0,               0,          
:EndVegetationClasses  

#-----------------------------------------------------------------
# Soil Profiles
#-----------------------------------------------------------------
:SoilProfiles
         LAKE, 0
   Soil_Land_HRU,      3, Forest_Floor, %D_FF%,  	Ablation_Till,  %D_AT%,   Basal_Till,        3,
:EndSoilProfiles

#-----------------------------------------------------------------
# Global Parameters
#-----------------------------------------------------------------
:GlobalParameter        RAINSNOW_TEMP %Rain_Snow_T%
:GlobalParameter       RAINSNOW_DELTA %Rain_Snow_Delta%
:GlobalParameter     SNOW_TEMPERATURE -2.9
:GlobalParameter             SNOW_SWI 3.332293E-01 #(Raven manual 0.04 - 0.07) 

#-----------------------------------------------------------------
# Soil Parameters
#-----------------------------------------------------------------
###
#POROSITY and FIELD_CAPACITY HYDRAUL_COND for ablation till obtained from (Figure2 Murray2005)
#ALBEDO_WET ALBEDO_DRY obtained from Figure 2 of https://en.wikipedia.org/wiki/Albedo ; https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2008GL036377   
#WETTING_FRONT_PSI table 2 of  https://ascelibrary.org/doi/pdf/10.1061/%28ASCE%290733-9429%281983%29109%3A1%2862%29?casa_token=Db6omitRaNAAAAAA:NJEfRhzP2102wLfyfQ6-niyrgad8YenXl3aAK5eU_FnPN9Aorx6EV31zTiGxUW07XFYGQV_t-ODb
####
:SoilParameterList
  :Parameters,        POROSITY,      ALBEDO_WET,      ALBEDO_DRY,    HYDRAUL_COND,      WETTING_FRONT_PSI,       PET_CORRECTION,   FIELD_CAPACITY,        SAT_WILT,       MAX_PERC_RATE,                 MAX_BASEFLOW_RATE,   BASEFLOW_COEFF,         BASEFLOW_N,    MAX_CAP_RISE_RATE, BASEFLOW_THRESH 
       :Units,            none,            none,            none,            mm/d,                     mm,                    -,                -,               -,                mm/d,                               mm/d,            none,               none,                mm/d,             none 
Forest_Floor,     6.543765E-01,            0.15,            0.15,    %HydCond_FF%,                 %WFPS%,     %PET_CORRECTION%,          %FC_FF%,    1.007189E-02,  %MAX_PERC_RATE_FF%,             %MAX_BASEFLOW_RATE_FF%,             0.0,    %BASEFLOW_N_FF%,                 0.0,          %FC_FF%,  
Ablation_Till,    6.882158E-01,            0.00,            0.00,    %HydCond_FF%,                 %WFPS%,     %PET_CORRECTION%,          %FC_AT%,    5.475422E-02,  %MAX_PERC_RATE_AT%,             %MAX_BASEFLOW_RATE_AT%,    5.168251E-02,    %BASEFLOW_N_AT%,                 0.0,          %FC_AT%,
Basal_Till                0.2,             0.00,            0.00,            9.52,                    0.0,                    0,          %FC_BT%,    5.764653E-03,        7.501124E-01,             %MAX_BASEFLOW_RATE_BT%,       0.9351502,    %BASEFLOW_N_BT%, %MAX_CAP_RISE_RATE%,          %FC_BT%,
:EndSoilParameterList



#-----------------------------------------------------------------
# Land Use Parameters
#-----------------------------------------------------------------
:LandUseParameterList
  :Parameters, FOREST_SPARSENESS,       ROUGHNESS,    REFREEZE_FACTOR,    MELT_FACTOR,   MIN_MELT_FACTOR , HBV_MELT_FOR_CORR, HBV_MELT_ASP_CORR,    CC_DECAY_COEFF,   
       :Units,                 -,                 m,           mm/d/C,        mm/d/K ,             mm/d/K,              none,              none,             1/day,    
   [DEFAULT] ,                 0,               1.9,        %Rfrez_F%,        %MLT_F%,        %MIN_MLT_F%,                 1,                 1,                 0, 
   Landuse_Land_HRU,           0,               1.9,         _DEFAULT,       _DEFAULT,           _DEFAULT,          _DEFAULT,          _DEFAULT,          _DEFAULT,
   LAKE,                       1,                 0,         _DEFAULT,       _DEFAULT,           _DEFAULT,          _DEFAULT,          _DEFAULT,          _DEFAULT,
:EndLandUseParameterList


#-----------------------------------------------------------------
# Vegetation Parameters
#-----------------------------------------------------------------
## SAI_HT_RATIO did not find any information. use zero to make ignore the SAI, the canopy interception only 
## determined by LAI
:VegetationParameterList
  :Parameters,      MAX_HEIGHT,   MAX_LEAF_COND,       ALBEDO,  SVF_EXTINCTION,    SAI_HT_RATIO,         RAIN_ICEPT_PCT,    SNOW_ICEPT_PCT,     MAX_CAPACITY,    MAX_SNOW_CAPACITY, 
       :Units,               m,        mm_per_s,            -,               -,               -,                      -,                 -,               mm,                   mm, 
    Veg_Land_HRU              15,             5.3,         0.15,              0.5,            0.0,       %RAIN_ICEPT_PCT%,   %SNOW_ICEPT_PCT%,   %MAX_CAPACITY%,  %MAX_SNOW_CAPACITY%, 
    LAKE,                      0,             0.0,         0.06,              0.5,            0.0,                  0.0,               0.0,                0,                    0,  
:EndVegetationParameterList

:SeasonalRelativeLAI
  Veg_Land_HRU, 0.2,0.2,0.2,0.4,0.8,1,1,0.7,0.6,0.0.3,0.0.2,0.0.2
  LAKE, 0,0,0,0,0,0,0,0,0,0,0,0
:EndSeasonalRelativeLAI

:SeasonalRelativeHeight
  Veg_Land_HRU, 1,1,1,1,1,1,1,1,1,1,1,1
  LAKE, 0,0.0,0.0,0,0,0,0,0,0,0,0,0
:EndSeasonalRelativeHeight

:RedirectToFile channel_properties.rvp

EOF


#========================
# rvh.tpl
#========================

rvh_tpl='Petawawa.rvh.tpl'
rm -r ${rvh_tpl}
# rvp.tpl
cat >> ${rvh_tpl} << EOF
:SubBasins
  :Attributes   NAME  DOWNSTREAM_ID       PROFILE REACH_LENGTH  GAUGED
  :Units        none           none          none           km    none
  202     sub202     220     Chn_202     ZERO-     0
  41     sub41     42     Chn_41     ZERO-     0
  315     sub315     322     Chn_315     ZERO-     0
  142     sub142     141     Chn_142     ZERO-     0
  277     sub277     276     Chn_277     ZERO-     0
  747     sub747     743     Chn_747     ZERO-     0
  803     sub803     801     Chn_803     ZERO-     0
  542     sub542     551     Chn_542     ZERO-     0
  327     sub327     326     Chn_327     ZERO-     0
  36     sub36     34     Chn_36     ZERO-     0
  688     sub688     753     Chn_688         0.4563     0
  450     sub450     455     Chn_450     ZERO-     0
  720     sub720     719     Chn_720     ZERO-     0
  460     sub460     468     Chn_460     ZERO-     0
  402     sub402     400     Chn_402     ZERO-     0
  657     sub657     656     Chn_657     ZERO-     0
  519     sub519     528     Chn_519     ZERO-     0
  464     sub464     463     Chn_464     ZERO-     0
  548     sub548     547     Chn_548     ZERO-     0
  652     sub652     655     Chn_652     ZERO-     0
  116     sub116     118     Chn_116     ZERO-     1
  299     sub299     297     Chn_299     ZERO-     0
  887     sub887     888     Chn_887     ZERO-     0
  126     sub126     125     Chn_126     ZERO-     0
  415     sub415     414     Chn_415     ZERO-     0
  307     sub307     306     Chn_307     ZERO-     0
  331     sub331     494     Chn_331         0.9447     0
  746     sub746     743     Chn_746     ZERO-     0
  165     sub165     164     Chn_165     ZERO-     0
  138     sub138     139     Chn_138     ZERO-     0
  861     sub861     868     Chn_861     ZERO-     0
  405     sub405     406     Chn_405     ZERO-     0
  132     sub132     131     Chn_132     ZERO-     0
  794     sub794     792     Chn_794     ZERO-     0
  113     sub113     110     Chn_113     ZERO-     0
  424     sub424     423     Chn_424     ZERO-     0
  419     sub419     449     Chn_419     ZERO-     0
  843     sub843     842     Chn_843     ZERO-     0
  66     sub66     78     Chn_66     ZERO-     0
  146     sub146     231     Chn_146         9.2893     0
  355     sub355     351     Chn_355     ZERO-     0
  737     sub737     748     Chn_737     ZERO-     0
  313     sub313     312     Chn_313     ZERO-     0
  363     sub363     362     Chn_363     ZERO-     0
  82     sub82     83     Chn_82     ZERO-     0
  577     sub577     575     Chn_577         3.0486     0
  463     sub463     460     Chn_463     ZERO-     0
  254     sub254     276     Chn_254         3.6616     0
  50     sub50     47     Chn_50     ZERO-     0
  217     sub217     215     Chn_217     ZERO-     0
  504     sub504     506     Chn_504     ZERO-     0
  112     sub112     110     Chn_112     ZERO-     0
  396     sub396     398     Chn_396     ZERO-     0
  461     sub461     460     Chn_461     ZERO-     0
  135     sub135     136     Chn_135     ZERO-     1
  808     sub808     805     Chn_808     ZERO-     0
  352     sub352     351     Chn_352     ZERO-     0
  426     sub426     425     Chn_426     ZERO-     0
  383     sub383     412     Chn_383         3.0433     0
  207     sub207     215     Chn_207     ZERO-     0
  246     sub246     254     Chn_246     ZERO-     0
  921     sub921     -1     Chn_921     ZERO-     1
  864     sub864     863     Chn_864     ZERO-     0
  78     sub78     80     Chn_78     ZERO-     0
  262     sub262     326     Chn_262        10.1500     0
  215     sub215     219     Chn_215     ZERO-     0
  114     sub114     220     Chn_114         5.1269     0
  399     sub399     398     Chn_399     ZERO-     0
  304     sub304     301     Chn_304     ZERO-     0
  345     sub345     340     Chn_345     ZERO-     1
  375     sub375     377     Chn_375     ZERO-     0
  646     sub646     644     Chn_646     ZERO-     0
  544     sub544     545     Chn_544     ZERO-     0
  258     sub258     265     Chn_258     ZERO-     0
  111     sub111     110     Chn_111     ZERO-     0
  596     sub596     600     Chn_596     ZERO-     0
  69     sub69     78     Chn_69     ZERO-     0
  344     sub344     340     Chn_344     ZERO-     0
  752     sub752     750     Chn_752     ZERO-     0
  397     sub397     396     Chn_397     ZERO-     0
  754     sub754     757     Chn_754     ZERO-     0
  538     sub538     537     Chn_538     ZERO-     0
  321     sub321     326     Chn_321     ZERO-     0
  294     sub294     296     Chn_294     ZERO-     0
  704     sub704     706     Chn_704     ZERO-     0
  452     sub452     450     Chn_452     ZERO-     0
  225     sub225     231     Chn_225     ZERO-     0
  862     sub862     861     Chn_862     ZERO-     0
  230     sub230     228     Chn_230     ZERO-     0
  340     sub340     336     Chn_340         0.8143     0
  543     sub543     542     Chn_543     ZERO-     0
  553     sub553     552     Chn_553     ZERO-     0
  536     sub536     535     Chn_536     ZERO-     0
  658     sub658     656     Chn_658     ZERO-     0
  379     sub379     377     Chn_379     ZERO-     0
  750     sub750     846     Chn_750        13.4356     0
  559     sub559     558     Chn_559     ZERO-     0
  859     sub859     858     Chn_859     ZERO-     0
  276     sub276     287     Chn_276     ZERO-     0
  400     sub400     395     Chn_400         7.3595     1
  650     sub650     648     Chn_650     ZERO-     0
  531     sub531     532     Chn_531     ZERO-     0
  767     sub767     768     Chn_767     ZERO-     1
  545     sub545     689     Chn_545         8.7384     0
  622     sub622     764     Chn_622         9.9410     0
  501     sub501     508     Chn_501     ZERO-     0
  87     sub87     80     Chn_87     ZERO-     0
  508     sub508     503     Chn_508         1.4982     0
  110     sub110     114     Chn_110     ZERO-     0
  589     sub589     596     Chn_589         1.6042     0
  427     sub427     425     Chn_427     ZERO-     0
  216     sub216     215     Chn_216     ZERO-     0
  451     sub451     450     Chn_451     ZERO-     0
  274     sub274     276     Chn_274     ZERO-     0
  354     sub354     351     Chn_354     ZERO-     0
  539     sub539     537     Chn_539     ZERO-     0
  613     sub613     764     Chn_613         0.5934     0
  430     sub430     429     Chn_430     ZERO-     0
  429     sub429     425     Chn_429     ZERO-     0
  267     sub267     269     Chn_267     ZERO-     0
  326     sub326     333     Chn_326     ZERO-     1
  319     sub319     322     Chn_319     ZERO-     0
  847     sub847     846     Chn_847     ZERO-     0
  391     sub391     390     Chn_391     ZERO-     0
  484     sub484     481     Chn_484         2.7782     0
  377     sub377     382     Chn_377     ZERO-     0
  228     sub228     232     Chn_228     ZERO-     1
  466     sub466     467     Chn_466     ZERO-     0
  623     sub623     622     Chn_623     ZERO-     0
  673     sub673     671     Chn_673     ZERO-     0
  599     sub599     617     Chn_599         0.8037     0
  251     sub251     250     Chn_251     ZERO-     0
  73     sub73     74     Chn_73     ZERO-     0
  575     sub575     581     Chn_575     ZERO-     0
  496     sub496     495     Chn_496     ZERO-     0
  131     sub131     125     Chn_131     ZERO-     0
  525     sub525     528     Chn_525     ZERO-     0
  164     sub164     166     Chn_164     ZERO-     0
  716     sub716     753     Chn_716     ZERO-     0
  800     sub800     801     Chn_800     ZERO-     0
  129     sub129     125     Chn_129     ZERO-     0
  239     sub239     260     Chn_239         1.4592     0
  270     sub270     404     Chn_270         8.5972     0
  144     sub144     142     Chn_144     ZERO-     0
  140     sub140     139     Chn_140     ZERO-     0
  421     sub421     449     Chn_421     ZERO-     0
  362     sub362     386     Chn_362         5.2355     0
  655     sub655     654     Chn_655     ZERO-     0
  343     sub343     340     Chn_343     ZERO-     0
  901     sub901     903     Chn_901     ZERO-     0
  786     sub786     784     Chn_786     ZERO-     0
  615     sub615     614     Chn_615     ZERO-     0
  407     sub407     404     Chn_407     ZERO-     0
  665     sub665     664     Chn_665     ZERO-     0
  205     sub205     200     Chn_205     ZERO-     0
  244     sub244     291     Chn_244         2.2203     0
  249     sub249     255     Chn_249     ZERO-     0
  876     sub876     875     Chn_876     ZERO-     0
  229     sub229     230     Chn_229     ZERO-     0
  341     sub341     340     Chn_341     ZERO-     0
  293     sub293     377     Chn_293         4.3853     0
  282     sub282     281     Chn_282     ZERO-     0
  656     sub656     689     Chn_656         8.8163     0
  241     sub241     244     Chn_241     ZERO-     1
  659     sub659     658     Chn_659     ZERO-     0
  869     sub869     868     Chn_869     ZERO-     0
  46     sub46     135     Chn_46     ZERO-     0
  749     sub749     740     Chn_749         0.7531     0
  667     sub667     664     Chn_667     ZERO-     0
  123     sub123     121     Chn_123     ZERO-     0
  260     sub260     264     Chn_260     ZERO-     0
  738     sub738     737     Chn_738     ZERO-     0
  403     sub403     402     Chn_403     ZERO-     0
  147     sub147     146     Chn_147     ZERO-     0
  47     sub47     56     Chn_47     ZERO-     0
  499     sub499     574     Chn_499     ZERO-     0
  756     sub756     754     Chn_756         0.9295     0
  237     sub237     249     Chn_237     ZERO-     0
  751     sub751     750     Chn_751     ZERO-     0
  227     sub227     249     Chn_227     ZERO-     0
  118     sub118     135     Chn_118         0.1412     0
  724     sub724     723     Chn_724     ZERO-     0
  617     sub617     611     Chn_617         2.8431     0
  505     sub505     497     Chn_505         0.1538     0
  312     sub312     326     Chn_312     ZERO-     0
  268     sub268     267     Chn_268     ZERO-     0
  420     sub420     421     Chn_420     ZERO-     0
  281     sub281     288     Chn_281     ZERO-     1
  863     sub863     870     Chn_863     ZERO-     0
  62     sub62     61     Chn_62     ZERO-     0
  483     sub483     482     Chn_483     ZERO-     0
  844     sub844     842     Chn_844     ZERO-     0
  529     sub529     528     Chn_529     ZERO-     0
  481     sub481     482     Chn_481     ZERO-     0
  537     sub537     691     Chn_537         6.3044     0
  85     sub85     80     Chn_85     ZERO-     0
  649     sub649     650     Chn_649     ZERO-     0
  792     sub792     793     Chn_792     ZERO-     0
  744     sub744     743     Chn_744     ZERO-     0
  482     sub482     528     Chn_482         5.9986     0
  587     sub587     585     Chn_587     ZERO-     0
  317     sub317     322     Chn_317     ZERO-     0
  218     sub218     215     Chn_218     ZERO-     0
  297     sub297     296     Chn_297     ZERO-     0
  136     sub136     137     Chn_136     ZERO-     0
  259     sub259     258     Chn_259     ZERO-     0
  768     sub768     771     Chn_768         4.3645     0
  888     sub888     901     Chn_888         0.4047     0
  264     sub264     261     Chn_264         3.9684     0
  130     sub130     125     Chn_130     ZERO-     0
  443     sub443     442     Chn_443     ZERO-     0
  220     sub220     223     Chn_220     ZERO-     1
  57     sub57     56     Chn_57     ZERO-     0
  298     sub298     296     Chn_298     ZERO-     0
  574     sub574     583     Chn_574     ZERO-     1
  795     sub795     791     Chn_795     ZERO-     0
  462     sub462     460     Chn_462     ZERO-     0
  252     sub252     253     Chn_252     ZERO-     0
  71     sub71     78     Chn_71     ZERO-     0
  300     sub300     294     Chn_300         5.0341     0
  459     sub459     469     Chn_459     ZERO-     0
  668     sub668     691     Chn_668         8.9061     0
  59     sub59     58     Chn_59     ZERO-     0
  902     sub902     901     Chn_902     ZERO-     0
  58     sub58     57     Chn_58     ZERO-     0
  382     sub382     380     Chn_382         1.6563     0
  308     sub308     307     Chn_308     ZERO-     0
  301     sub301     303     Chn_301     ZERO-     0
  335     sub335     334     Chn_335     ZERO-     0
  610     sub610     613     Chn_610     ZERO-     0
  236     sub236     249     Chn_236     ZERO-     0
  758     sub758     761     Chn_758     ZERO-     0
  654     sub654     653     Chn_654     ZERO-     0
  582     sub582     581     Chn_582     ZERO-     0
  291     sub291     293     Chn_291     ZERO-     1
  788     sub788     798     Chn_788         0.8722     0
  875     sub875     878     Chn_875     ZERO-     0
  42     sub42     135     Chn_42     ZERO-     0
  273     sub273     274     Chn_273     ZERO-     0
  919     sub919     923     Chn_919     ZERO-     0
  666     sub666     664     Chn_666     ZERO-     0
  211     sub211     209     Chn_211     ZERO-     0
  739     sub739     749     Chn_739     ZERO-     0
  250     sub250     249     Chn_250     ZERO-     0
  502     sub502     501     Chn_502     ZERO-     0
  549     sub549     547     Chn_549     ZERO-     0
  669     sub669     668     Chn_669     ZERO-     0
  290     sub290     291     Chn_290     ZERO-     0
  503     sub503     509     Chn_503     ZERO-     0
  449     sub449     454     Chn_449     ZERO-     1
  580     sub580     577     Chn_580     ZERO-     0
  810     sub810     809     Chn_810     ZERO-     0
  692     sub692     691     Chn_692     ZERO-     0
  500     sub500     505     Chn_500     ZERO-     0
  330     sub330     329     Chn_330     ZERO-     0
  742     sub742     741     Chn_742     ZERO-     0
  497     sub497     507     Chn_497     ZERO-     1
  219     sub219     220     Chn_219         0.7807     0
  520     sub520     528     Chn_520     ZERO-     0
  389     sub389     387     Chn_389     ZERO-     0
  495     sub495     494     Chn_495     ZERO-     0
  745     sub745     743     Chn_745     ZERO-     0
  523     sub523     528     Chn_523         0.4122     0
  148     sub148     146     Chn_148     ZERO-     0
  653     sub653     651     Chn_653     ZERO-     0
  586     sub586     585     Chn_586     ZERO-     0
  84     sub84     83     Chn_84     ZERO-     0
  166     sub166     260     Chn_166         3.7524     0
  723     sub723     760     Chn_723     ZERO-     0
  760     sub760     762     Chn_760     ZERO-     0
  353     sub353     351     Chn_353     ZERO-     0
  428     sub428     425     Chn_428     ZERO-     0
  414     sub414     445     Chn_414         1.0333     0
  279     sub279     284     Chn_279     ZERO-     0
  442     sub442     448     Chn_442     ZERO-     0
  285     sub285     279     Chn_285         0.4469     0
  789     sub789     788     Chn_789     ZERO-     0
  445     sub445     440     Chn_445         0.8341     0
  798     sub798     804     Chn_798     ZERO-     0
  376     sub376     375     Chn_376     ZERO-     0
  441     sub441     447     Chn_441     ZERO-     0
  310     sub310     312     Chn_310     ZERO-     0
  137     sub137     215     Chn_137         7.5919     0
  63     sub63     61     Chn_63     ZERO-     0
  295     sub295     294     Chn_295     ZERO-     0
  243     sub243     241     Chn_243     ZERO-     0
  456     sub456     484     Chn_456         0.3469     0
  611     sub611     614     Chn_611     ZERO-     0
  232     sub232     249     Chn_232         1.6088     0
  278     sub278     276     Chn_278     ZERO-     0
  77     sub77     79     Chn_77     ZERO-     0
  127     sub127     125     Chn_127     ZERO-     0
  302     sub302     303     Chn_302     ZERO-     0
  210     sub210     209     Chn_210     ZERO-     0
  143     sub143     144     Chn_143     ZERO-     0
  248     sub248     246     Chn_248     ZERO-     0
  221     sub221     220     Chn_221     ZERO-     0
  417     sub417     416     Chn_417     ZERO-     0
  125     sub125     270     Chn_125        29.8906     0
  53     sub53     52     Chn_53     ZERO-     0
  422     sub422     449     Chn_422     ZERO-     0
  581     sub581     596     Chn_581         1.9603     0
  664     sub664     889     Chn_664        10.9143     0
  51     sub51     47     Chn_51     ZERO-     0
  540     sub540     550     Chn_540     ZERO-     0
  48     sub48     47     Chn_48     ZERO-     1
  338     sub338     337     Chn_338     ZERO-     0
  753     sub753     756     Chn_753     ZERO-     1
  38     sub38     34     Chn_38     ZERO-     0
  342     sub342     340     Chn_342     ZERO-     0
  83     sub83     80     Chn_83     ZERO-     0
  288     sub288     286     Chn_288         0.3159     1
  687     sub687     686     Chn_687     ZERO-     0
  167     sub167     166     Chn_167     ZERO-     0
  547     sub547     546     Chn_547     ZERO-     0
  43     sub43     135     Chn_43     ZERO-     0
  203     sub203     220     Chn_203     ZERO-     0
  72     sub72     78     Chn_72         4.8764     0
  870     sub870     865     Chn_870         0.2846     0
  846     sub846     861     Chn_846         6.5827     0
  557     sub557     554     Chn_557         1.4705     0
  802     sub802     803     Chn_802     ZERO-     0
  411     sub411     484     Chn_411         1.8591     0
  37     sub37     34     Chn_37     ZERO-     0
  88     sub88     86     Chn_88     ZERO-     0
  303     sub303     300     Chn_303     ZERO-     0
  722     sub722     723     Chn_722     ZERO-     0
  401     sub401     400     Chn_401     ZERO-     0
  494     sub494     617     Chn_494         6.8053     0
  532     sub532     771     Chn_532         5.9869     0
  235     sub235     249     Chn_235     ZERO-     0
  616     sub616     615     Chn_616     ZERO-     0
  506     sub506     574     Chn_506         0.4782     0
  328     sub328     331     Chn_328     ZERO-     0
  67     sub67     69     Chn_67     ZERO-     0
  395     sub395     574     Chn_395         2.7258     0
  809     sub809     905     Chn_809        14.5162     0
  717     sub717     718     Chn_717     ZERO-     0
  283     sub283     281     Chn_283     ZERO-     0
  316     sub316     315     Chn_316     ZERO-     0
  387     sub387     445     Chn_387         4.6624     0
  740     sub740     741     Chn_740     ZERO-     0
  584     sub584     577     Chn_584     ZERO-     0
  706     sub706     753     Chn_706         0.5408     0
  329     sub329     332     Chn_329     ZERO-     0
  455     sub455     522     Chn_455         0.3919     0
  598     sub598     599     Chn_598     ZERO-     0
  253     sub253     251     Chn_253     ZERO-     0
  467     sub467     528     Chn_467         4.0932     0
  380     sub380     400     Chn_380         2.7551     0
  801     sub801     889     Chn_801         2.8590     0
  65     sub65     67     Chn_65     ZERO-     0
  796     sub796     791     Chn_796     ZERO-     0
  305     sub305     304     Chn_305     ZERO-     0
  804     sub804     799     Chn_804         3.5274     0
  361     sub361     360     Chn_361     ZERO-     0
  378     sub378     377     Chn_378     ZERO-     0
  133     sub133     125     Chn_133     ZERO-     0
  204     sub204     200     Chn_204     ZERO-     0
  261     sub261     263     Chn_261     ZERO-     0
  209     sub209     208     Chn_209     ZERO-     0
  406     sub406     404     Chn_406     ZERO-     0
  60     sub60     55     Chn_60         0.0900     0
  52     sub52     54     Chn_52     ZERO-     0
  306     sub306     488     Chn_306         4.8483     0
  339     sub339     334     Chn_339         2.5236     0
  74     sub74     72     Chn_74     ZERO-     0
  770     sub770     798     Chn_770     ZERO-     0
  554     sub554     556     Chn_554     ZERO-     0
  287     sub287     281     Chn_287         0.1513     0
  201     sub201     203     Chn_201     ZERO-     0
  785     sub785     786     Chn_785     ZERO-     0
  759     sub759     758     Chn_759     ZERO-     0
  247     sub247     246     Chn_247     ZERO-     0
  867     sub867     866     Chn_867     ZERO-     0
  807     sub807     805     Chn_807     ZERO-     0
  771     sub771     798     Chn_771         7.7078     0
  34     sub34     125     Chn_34        16.3020     0
  743     sub743     737     Chn_743        13.3275     0
  61     sub61     60     Chn_61     ZERO-     0
  311     sub311     312     Chn_311     ZERO-     0
  868     sub868     863     Chn_868         2.5850     0
  660     sub660     656     Chn_660     ZERO-     0
  530     sub530     561     Chn_530         4.7767     0
  457     sub457     456     Chn_457     ZERO-     0
  81     sub81     87     Chn_81     ZERO-     0
  35     sub35     36     Chn_35     ZERO-     0
  200     sub200     220     Chn_200     ZERO-     0
  799     sub799     805     Chn_799     ZERO-     0
  214     sub214     220     Chn_214     ZERO-     0
  644     sub644     753     Chn_644         8.3749     0
  322     sub322     323     Chn_322     ZERO-     0
  842     sub842     875     Chn_842         2.7258     0
  86     sub86     80     Chn_86     ZERO-     0
  600     sub600     598     Chn_600         0.0900     0
  124     sub124     121     Chn_124     ZERO-     0
  79     sub79     231     Chn_79         1.6981     0
  480     sub480     479     Chn_480     ZERO-     0
  392     sub392     400     Chn_392         1.1192     0
  390     sub390     387     Chn_390     ZERO-     0
  323     sub323     326     Chn_323         0.0900     0
  393     sub393     392     Chn_393     ZERO-     0
  908     sub908     919     Chn_908         7.4042     0
  469     sub469     466     Chn_469         0.4866     0
  122     sub122     121     Chn_122     ZERO-     1
  68     sub68     69     Chn_68     ZERO-     0
  265     sub265     262     Chn_265         4.3504     1
  805     sub805     800     Chn_805         4.2222     0
  242     sub242     241     Chn_242     ZERO-     0
  923     sub923     921     Chn_923         1.0259     0
  552     sub552     557     Chn_552     ZERO-     0
  296     sub296     386     Chn_296         4.2825     0
  886     sub886     901     Chn_886     ZERO-     0
  337     sub337     488     Chn_337         3.9831     0
  55     sub55     47     Chn_55         0.2386     0
  585     sub585     589     Chn_585     ZERO-     0
  541     sub541     540     Chn_541     ZERO-     0
  336     sub336     339     Chn_336     ZERO-     0
  120     sub120     119     Chn_120     ZERO-     0
  54     sub54     135     Chn_54         1.2795     0
  121     sub121     119     Chn_121         0.0900     0
  757     sub757     760     Chn_757         0.0900     0
  280     sub280     285     Chn_280     ZERO-     0
  561     sub561     574     Chn_561         5.4493     0
  612     sub612     611     Chn_612     ZERO-     0
  49     sub49     47     Chn_49     ZERO-     0
  535     sub535     668     Chn_535         3.4997     0
  509     sub509     504     Chn_509         0.1118     0
  272     sub272     276     Chn_272     ZERO-     0
  128     sub128     125     Chn_128     ZERO-     0
  44     sub44     135     Chn_44     ZERO-     0
  528     sub528     530     Chn_528     ZERO-     1
  440     sub440     446     Chn_440     ZERO-     0
  117     sub117     116     Chn_117     ZERO-     1
  416     sub416     413     Chn_416         0.3279     0
  579     sub579     580     Chn_579     ZERO-     0
  748     sub748     739     Chn_748         0.6310     0
  865     sub865     866     Chn_865     ZERO-     0
  487     sub487     500     Chn_487         0.1681     0
  651     sub651     656     Chn_651     ZERO-     0
  465     sub465     463     Chn_465     ZERO-     0
  691     sub691     767     Chn_691         2.2317     0
  286     sub286     280     Chn_286         3.5452     0
  386     sub386     500     Chn_386         3.4078     0
  446     sub446     441     Chn_446         0.2005     0
  360     sub360     404     Chn_360         2.4734     0
  398     sub398     395     Chn_398     ZERO-     0
  139     sub139     270     Chn_139         4.3077     0
  233     sub233     228     Chn_233         2.8428     0
  263     sub263     258     Chn_263         0.7791     0
  806     sub806     805     Chn_806     ZERO-     0
  672     sub672     671     Chn_672     ZERO-     0
  425     sub425     561     Chn_425         1.7677     0
  255     sub255     246     Chn_255         0.0972     0
  879     sub879     908     Chn_879         2.9016     0
  878     sub878     901     Chn_878         0.7798     0
  741     sub741     875     Chn_741         1.7201     0
  555     sub555     554     Chn_555     ZERO-     0
  45     sub45     44     Chn_45     ZERO-     0
  905     sub905     919     Chn_905        15.8108     0
  906     sub906     905     Chn_906     ZERO-     0
  791     sub791     861     Chn_791         2.8333     0
  447     sub447     442     Chn_447         1.4041     0
  351     sub351     356     Chn_351     ZERO-     0
  223     sub223     231     Chn_223         0.6699     0
  764     sub764     767     Chn_764         0.0900     0
  332     sub332     328     Chn_332         1.6424     0
  522     sub522     523     Chn_522     ZERO-     0
  56     sub56     52     Chn_56         4.6886     0
  546     sub546     540     Chn_546         5.0918     0
  231     sub231     233     Chn_231     ZERO-     0
  80     sub80     77     Chn_80        28.9599     0
  404     sub404     412     Chn_404         8.3329     0
  448     sub448     522     Chn_448         0.4682     0
  718     sub718     753     Chn_718     ZERO-     0
  507     sub507     501     Chn_507         1.0837     0
  454     sub454     450     Chn_454         0.4648     0
  719     sub719     753     Chn_719     ZERO-     0
  412     sub412     411     Chn_412         9.8688     1
  388     sub388     387     Chn_388     ZERO-     0
  686     sub686     688     Chn_686     ZERO-     0
  413     sub413     414     Chn_413     ZERO-     0
  671     sub671     767     Chn_671         2.6269     0
  866     sub866     919     Chn_866         8.8051     0
  797     sub797     795     Chn_797     ZERO-     0
  423     sub423     449     Chn_423     ZERO-     0
  381     sub381     380     Chn_381     ZERO-     1
  356     sub356     449     Chn_356         1.0700     0
  284     sub284     528     Chn_284         0.5122     0
  384     sub384     383     Chn_384     ZERO-     0
  889     sub889     887     Chn_889         1.8326     0
  39     sub39     38     Chn_39     ZERO-     0
  614     sub614     610     Chn_614         5.8295     0
  597     sub597     596     Chn_597     ZERO-     0
  578     sub578     580     Chn_578     ZERO-     0
  558     sub558     809     Chn_558        22.4367     0
  880     sub880     879     Chn_880     ZERO-     0
  784     sub784     809     Chn_784         2.6287     0
  75     sub75     74     Chn_75     ZERO-     0
  208     sub208     215     Chn_208         0.4465     0
  334     sub334     337     Chn_334     ZERO-     0
  762     sub762     758     Chn_762         0.5009     0
  551     sub551     544     Chn_551         0.3515     0
  761     sub761     846     Chn_761         2.1287     0
  689     sub689     686     Chn_689         1.7608     0
  550     sub550     542     Chn_550         2.5102     0
  485     sub485     487     Chn_485     ZERO-     0
  488     sub488     494     Chn_488         8.3629     0
  333     sub333     329     Chn_333         1.0978     0
  645     sub645     646     Chn_645     ZERO-     0
  858     sub858     908     Chn_858         7.9751     0
  793     sub793     795     Chn_793     ZERO-     0
  583     sub583     577     Chn_583         0.2670     0
  468     sub468     459     Chn_468         0.7439     0
  479     sub479     528     Chn_479     ZERO-     0
  648     sub648     767     Chn_648         8.5904     0
  269     sub269     326     Chn_269         1.8524     0
  556     sub556     668     Chn_556         2.6200     0
  903     sub903     905     Chn_903         1.5581     0
  141     sub141     138     Chn_141         6.3328     0
  119     sub119     125     Chn_119         5.3786     0
:EndSubBasins


:HRUs
  :Attributes AREA ELEVATION  LATITUDE  LONGITUDE   BASIN_ID  LAND_USE_CLASS  VEG_CLASS   SOIL_PROFILE  AQUIFER_PROFILE   TERRAIN_CLASS   SLOPE   ASPECT
  :Units       km2         m       deg        deg       none            none       none           none             none            none     deg      deg
  1         1.1796       450.6630        45.7947       -78.5451     202     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.514000       127.1790     
  2         0.5244       446.2420        45.7165       -78.8206     41     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.387000       100.6160     
  3         1.2137       411.3400        45.8036       -78.1690     315     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.551000       101.7350     
  4         0.6894       440.8570        45.8530       -78.8228     142     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.201000       102.7780     
  5         0.4809       415.7210        45.9467       -78.5847     277     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.619000       114.7790     
  6         0.2268       223.6940        46.0121       -77.6213     747     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.963000        94.2240     
  7         0.1446       252.4000        46.0194       -77.7229     803     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.608000        94.8670     
  8         3.2339       294.0370        45.8525       -77.8421     542     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.740000        96.2080     
  9         0.1606       410.2480        45.8980       -78.2091     327     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.380000        93.8460     
  10         0.3548       468.9180        45.8001       -79.0548     36     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.859000       118.8460     
  11         1.7405       314.6170        45.8379       -77.7633     688     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.241000       108.1360     
  12         4.7245       367.4800        46.0605       -78.6131     450     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.131000        87.5450     
  13         2.5890       240.6070        45.8681       -77.7320     720     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.470000       117.3450     
  14        14.7576       386.1500        46.0852       -78.4621     460     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.899000        93.1600     
  15         3.9019       401.8460        45.9414       -78.3162     402     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.468000        81.8340     
  16         1.5927       302.0130        45.8316       -77.7597     657     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.834000       147.9890     
  17         6.6166       413.2330        45.9550       -78.4524     519     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.903000        79.1060     
  18         0.7810       409.4670        46.0586       -78.4500     464     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.584000       110.6710     
  19         2.7357       326.8830        45.8125       -77.9237     548     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.825000        95.2030     
  20         2.8425       297.6240        45.7616       -77.7357     652     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.031000       102.3420     
  21         1.7692       447.6720        45.6819       -78.8014     116     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.591000        95.8250     
  22         3.5849       413.8960        46.0583       -78.3404     299     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.718000        78.9570     
  23        17.1442       218.8120        45.9990       -77.6988     887     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.418000        83.6400     
  24         1.6859       423.0030        45.8793       -78.9209     126     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.859000       102.8120     
  25         0.3793       397.5850        46.1108       -78.6901     415     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.641000        86.3120     
  26         0.1889       400.5940        45.8489       -78.1680     307     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.164000        92.9840     
  27         0.4352       358.4500        45.9166       -78.1584     331     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.526000        88.4200     
  28         0.1142       257.1620        46.0188       -77.6750     746     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.486000        97.7830     
  29         1.2860       459.1850        45.8008       -78.5249     165     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.357000        52.5710     
  30         0.9708       433.0930        45.8725       -78.7786     138     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.219000        96.8660     
  31         0.4132       224.0930        45.8823       -77.5938     861     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.186000        83.9260     
  32         0.2065       464.1960        45.9536       -78.7625     405     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.537000       133.1130     
  33         1.8330       449.3440        45.8404       -78.8641     132     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.178000       107.6900     
  34         0.1298       282.8320        45.8665       -77.6691     794     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.304000        80.7640     
  35         0.1856       440.9480        45.7279       -78.5369     113     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.412000       132.4740     
  36         3.9822       375.8520        46.0387       -78.6514     424     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.092000        77.1480     
  37         1.7864       420.2910        46.1073       -78.7224     419     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.317000       116.8590     
  38         0.2580       233.8250        46.0024       -77.5564     843     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.171000        93.8930     
  39         1.5012       481.3940        45.7792       -78.8674     66     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.029000       122.1760     
  40        55.8985       440.0660        45.8116       -78.7620     146     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.649000        98.5690     
  41         2.1932       413.2120        46.0058       -78.5679     355     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.540000       120.1930     
  42         0.1336       230.4070        45.9912       -77.6209     737     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.961000        72.6880     
  43         0.1276       411.1300        45.8797       -78.3122     313     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.668000       101.8040     
  44         2.7894       396.4100        46.1108       -78.3861     363     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.454000       100.2230     
  45         1.7015       490.1200        45.7649       -78.7973     82     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.681000        97.8160     
  46        12.7075       350.7900        45.9658       -78.2703     577     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.195000        57.6360     
  47         1.4677       395.2480        46.0548       -78.4603     463     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.260000        82.7560     
  48         5.2818       410.6290        45.9070       -78.5759     254     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.884000       100.9430     
  49         0.4819       485.4030        45.6503       -78.9807     50     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.998000        96.9420     
  50         0.2375       434.1360        45.7274       -78.7328     217     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.631000        91.6640     
  51         1.6578       323.6100        46.0201       -78.2930     504     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.669000       152.0540     
  52         0.1023       461.9010        45.7292       -78.5797     112     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.617000        98.4190     
  53         3.6776       407.0770        45.9841       -78.3814     396     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.613000        90.2850     
  54         5.3165       447.1240        46.1090       -78.5084     461     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.614000        85.5970     
  55        12.3863       438.5500        45.7006       -78.8206     135     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.803000       106.9540     
  56         2.1489       282.7550        46.0499       -77.7739     808     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.193000        95.4420     
  57         0.1759       416.0160        46.0391       -78.5968     352     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.451000       102.2110     
  58         0.9477       413.6330        46.0583       -78.3642     426     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.663000       100.2440     
  59        24.9186       417.1860        45.9716       -78.7055     383     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.863000       106.0200     
  60         0.3201       432.8490        45.6842       -78.7134     207     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.392000        80.2400     
  61        17.9472       425.6020        45.8858       -78.6180     246     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.958000        92.1870     
  62         0.5479       151.5370        45.8827       -77.3266     921     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.429000       116.9660     
  63         1.8297       242.4800        45.8531       -77.5372     864     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.981000        49.4840     
  64         3.0788       455.6580        45.7592       -78.9072     78     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.738000       112.1130     
  65        43.7490       418.2800        45.8557       -78.3584     262     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.130000        91.5850     
  66        42.6454       427.9560        45.7084       -78.6920     215     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.029000        97.4680     
  67         8.6311       443.4940        45.7199       -78.6164     114     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.041000        96.9750     
  68         0.1511       414.3750        45.9669       -78.3698     399     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.123000        81.5710     
  69         0.4227       240.6070        45.8621       -77.7379     720     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.470000       117.3450     
  70         0.1771       419.6440        46.1212       -78.4839     304     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.684000       103.7960     
  71         2.6620       420.8930        45.7716       -78.1428     345     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.745000        80.7910     
  72         1.0757       429.4870        45.9363       -78.4560     375     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.202000       104.5440     
  73         0.2049       291.3360        45.9760       -77.9022     646     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.151000        96.5780     
  74         0.2276       304.2930        45.8468       -77.8237     544     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.808000       108.5580     
  75         4.2215       423.9510        45.8325       -78.4375     258     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.339000        95.8020     
  76         1.2742       443.9710        45.6835       -78.5971     111     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.223000        97.3410     
  77         0.6931       313.0740        45.9666       -78.2045     596     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.067000        60.3980     
  78         4.3395       470.3080        45.7701       -78.8168     69     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.395000        93.1240     
  79         0.1238       399.6360        45.7791       -78.1351     344     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.168000       102.3660     
  80         3.9070       241.5210        45.8630       -77.7131     752     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.354000        79.7040     
  81         0.6116       426.4570        45.9730       -78.3939     397     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.820000        68.0420     
  82         1.8822       288.5740        45.8502       -77.7204     754     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.113000        69.1660     
  83         1.9552       390.6260        45.9047       -78.0955     538     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.339000        82.2180     
  84         0.2344       457.3100        45.7921       -78.2526     321     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.310000        70.6950     
  85        14.4879       385.7420        46.0898       -78.4015     294     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.615000        90.6560     
  86         1.0618       290.1530        45.9083       -77.9088     704     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.467000        91.5330     
  87         0.1517       436.6540        46.0482       -78.5874     452     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.370000        80.5490     
  88         0.7249       420.3650        45.8014       -78.6514     225     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.617000        68.6510     
  89         3.4178       199.2050        45.8892       -77.5691     862     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.385000        93.9730     
  90         3.0145       453.3370        45.8543       -78.6129     230     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.351000        94.8400     
  91         9.8507       403.3310        45.7840       -78.1205     340     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.495000        95.5990     
  92         0.1079       369.8570        45.8672       -77.8299     543     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.719000        76.7090     
  93         3.8760       365.9620        45.8404       -78.0101     553     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.788000        88.0930     
  94         0.1741       398.1230        45.8425       -78.0490     536     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.184000        80.3880     
  95         0.3388       278.6980        45.7898       -77.7495     658     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.484000        84.1230     
  96         0.1674       445.5340        45.8803       -78.4303     379     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.511000        69.1060     
  97        56.9305       252.9250        45.9225       -77.7675     750     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.314000        88.6320     
  98         0.8736       259.4750        45.9920       -77.7969     559     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       1.751000       102.8710     
  99         0.1126       212.2450        45.8403       -77.4207     859     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.649000       133.1680     
  100         8.4063       417.2770        45.9312       -78.5520     276     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.126000       103.4630     
  101        12.7495       375.7500        45.9482       -78.3473     400     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.292000        95.8740     
  102        16.4512       286.9750        45.9573       -77.9552     650     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.117000       105.6090     
  103        18.9879       337.6650        46.0617       -78.0659     531     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.852000        74.2490     
  104        31.3746       282.7870        46.0004       -78.0403     767     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.044000       103.7700     
  105        30.3465       297.5850        45.8137       -77.8223     545     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.021000        61.7700     
  106        43.9770       291.1850        45.9952       -78.1286     622     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.960000        94.7860     
  107         2.3613       372.3330        46.0383       -78.2749     501     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.118000        80.5800     
  108         0.8399       457.8930        45.7143       -78.8795     87     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.834000        98.7910     
  109         2.4320       367.5650        46.0291       -78.2748     508     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.990000       101.2360     
  110        15.7826       446.9330        45.7134       -78.5812     110     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.453000       103.9030     
  111         0.1713       286.9750        45.9630       -77.9693     650     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.117000       105.6090     
  112         1.8141       292.7470        45.9760       -78.2007     589     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.560000       119.1650     
  113         0.1907       394.8640        46.0468       -78.3712     427     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.957000        96.8270     
  114         0.1849       441.4230        45.7457       -78.6965     216     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.105000       112.9880     
  115         6.1730       282.7870        45.9797       -78.0428     767     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.044000       103.7700     
  116         2.3794       405.0560        46.0725       -78.6415     451     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.316000       125.4390     
  117         5.2037       430.5500        45.8810       -78.5721     274     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.922000       102.7540     
  118         0.1775       488.9960        46.0097       -78.6279     354     LAKE     LAKE     LAKE     [NONE]     [NONE]       1.571000       102.5560     
  119         1.3126       385.8260        45.8838       -78.0815     539     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.590000        81.3090     
  120         0.0822       221.9260        45.9608       -78.0686     613     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.096000        87.7010     
  121         0.2748       396.6770        46.0332       -78.3071     430     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.851000       101.3750     
  122         0.8958       389.1400        46.0325       -78.3337     429     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.977000       111.2440     
  123         0.7711       435.1380        45.8178       -78.2869     267     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.088000        84.3080     
  124        52.2821       395.1470        45.8566       -78.2517     326     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.615000        96.6490     
  125         0.3558       439.2440        45.7583       -78.2514     319     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.163000        91.1780     
  126         0.1143       254.2720        45.8962       -77.6346     847     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.776000       117.1110     
  127         4.1012       463.7270        46.1064       -78.5566     391     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.122000       100.7680     
  128         3.0070       346.0380        45.9790       -78.5960     484     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.172000       137.9110     
  129         1.9172       395.4300        45.9227       -78.4057     377     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.239000       104.6210     
  130         2.4827       421.8160        45.8308       -78.6527     228     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.617000       104.0350     
  131         2.9219       366.5840        46.0811       -78.5152     466     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.049000       121.6850     
  132         0.1319       378.3380        46.0405       -78.1343     623     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.746000       103.6480     
  133         4.8376       384.3520        46.0341       -78.1004     673     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.508000       101.0960     
  134         1.0827       295.3250        45.9678       -78.1851     599     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.536000       118.6330     
  135         1.1568       424.8190        45.8940       -78.6883     251     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.339000       117.9480     
  136        11.3928       471.2480        45.7472       -79.0612     73     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.194000       105.1630     
  137         1.8898       295.0950        45.9817       -78.2411     575     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.333000        92.4120     
  138         0.1485       386.4020        45.9269       -78.2109     496     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.577000        80.7730     
  139         1.3560       443.8250        45.8400       -78.8835     131     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.659000       100.9940     
  140         1.3155       449.7770        46.0288       -78.5689     525     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.188000       112.5800     
  141        18.8267       439.1560        45.7801       -78.4884     164     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.829000        92.1740     
  142         4.3229       291.7910        45.9137       -77.8036     716     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.445000       101.6290     
  143         8.5331       221.1600        46.0274       -77.7777     800     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.873000        64.2350     
  144         0.1023       463.7270        46.1063       -78.5701     391     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.122000       100.7680     
  145         2.6089       446.0700        45.8494       -78.8873     129     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.062000        95.8120     
  146         1.8809       471.2480        45.7511       -79.0299     73     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.194000       105.1630     
  147         0.4204       413.8960        46.0644       -78.3429     299     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.718000        78.9570     
  148        25.9088       445.9970        45.7971       -78.3655     239     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.306000        96.2540     
  149        20.5814       412.2310        45.8941       -78.7519     270     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.194000       105.0970     
  150         1.5438       446.4130        45.8407       -78.8452     144     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.286000        71.0240     
  151         0.1739       429.3440        45.8617       -78.7466     140     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.943000        84.0580     
  152         0.1128       424.9070        46.0967       -78.7363     421     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.329000        80.6400     
  153        28.3289       378.7110        46.1265       -78.3717     362     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.239000       100.9980     
  154         0.1200       288.6960        45.7562       -77.7215     655     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.993000        92.9820     
  155         1.3626       419.0400        45.7895       -78.1429     343     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.215000        91.7190     
  156         8.3012       443.9710        45.6855       -78.5821     111     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.223000        97.3410     
  157         3.0436       202.3180        45.9528       -77.6165     901     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.749000        87.9800     
  158        28.6267       202.3180        45.9576       -77.6336     901     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.749000        87.9800     
  159         0.2347       224.5200        45.9664       -77.7009     786     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.858000        88.2580     
  160         0.2891       329.8240        45.9300       -78.1137     615     LAKE     LAKE     LAKE     [NONE]     [NONE]       8.319000        79.2160     
  161         0.1051       430.7040        45.9067       -78.7726     407     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.221000        84.5360     
  162        16.7812       273.2210        46.0069       -77.8460     665     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       1.960000        74.7190     
  163         0.1586       278.6980        45.7891       -77.7476     658     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.484000        84.1230     
  164         0.2949       450.9080        45.7614       -78.5163     205     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.721000       102.0800     
  165         3.0518       439.1560        45.7696       -78.4715     164     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.829000        92.1740     
  166         1.8832       408.5160        45.8477       -78.5484     244     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.186000        94.7340     
  167        22.8444       414.3150        45.8600       -78.6880     249     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.809000       103.9790     
  168         2.8152       410.2480        45.9022       -78.2184     327     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.380000        93.8460     
  169         0.1050       223.2910        45.9596       -77.5257     876     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.436000       130.2130     
  170         3.1406       304.2930        45.8502       -77.8237     544     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.808000       108.5580     
  171         0.3064       419.0400        45.7856       -78.1370     343     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.215000        91.7190     
  172         2.3995       454.9500        45.8662       -78.6179     229     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.774000       105.4950     
  173         0.1161       436.6220        45.8103       -78.1270     341     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.436000       121.1400     
  174         4.3519       397.0160        45.9188       -78.4400     293     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.959000       118.2740     
  175         0.1542       401.9990        45.9648       -78.5266     282     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.975000       143.3110     
  176        25.4724       290.5670        45.8060       -77.7468     656     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.253000        96.7770     
  177         1.1098       461.9010        45.7283       -78.5848     112     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.617000        98.4190     
  178         7.5074       425.9680        45.8248       -78.5989     241     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.501000        96.8590     
  179         6.6187       298.1030        45.7736       -77.7546     659     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.295000        76.5740     
  180         3.9799       272.7930        45.8547       -77.5682     869     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.135000        63.1260     
  181         0.2855       468.4540        45.6752       -78.8627     46     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.174000        82.8380     
  182         0.9807       222.3330        45.9797       -77.6014     749     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.706000        95.0270     
  183         0.1088       222.2390        45.9870       -77.7443     667     LAKE     LAKE     LAKE     [NONE]     [NONE]       1.330000        83.7710     
  184         0.1103       437.1180        45.8180       -78.8720     123     LAKE     LAKE     LAKE     [NONE]     [NONE]       1.938000       109.1060     
  185         3.8366       422.2900        45.7773       -78.4001     260     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.895000        89.8560     
  186         0.1155       259.6510        45.9915       -77.6686     738     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.934000       120.0090     
  187         3.9903       413.4010        45.9330       -78.3010     403     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.177000        90.1680     
  188         0.1107       431.5580        45.8227       -78.8225     147     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.083000        93.5780     
  189         9.9499       471.6540        45.6562       -78.9518     47     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.654000        81.3030     
  190         5.4271       358.2310        46.0211       -78.3296     499     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.785000       130.0530     
  191         0.9470       290.2130        45.8497       -77.7572     756     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.597000        36.5760     
  192         0.2612       323.6100        46.0144       -78.2904     504     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.669000       152.0540     
  193         2.8312       398.1230        45.8387       -78.0429     536     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.184000        80.3880     
  194         0.2561       437.4830        45.8420       -78.7255     237     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.080000        96.4720     
  195         0.0992       263.8250        45.8978       -77.6952     751     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.371000       112.7530     
  196         0.4637       405.0560        46.0664       -78.6377     451     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.316000       125.4390     
  197         0.2060       212.2450        45.8406       -77.4210     859     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.649000       133.1680     
  198         0.3478       403.6550        45.8356       -78.6759     227     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.867000        78.6960     
  199         0.0713       430.4710        45.6993       -78.7901     118     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.699000        79.8240     
  200         0.0984       332.3160        45.8177       -77.6545     724     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.413000        54.4320     
  201         1.9585       286.2030        45.9591       -78.1696     617     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.575000        99.9770     
  202         0.0984       329.6930        46.0868       -78.2765     505     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.406000        87.7750     
  203         0.6598       410.2070        45.8913       -78.2892     312     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.619000       106.4360     
  204         0.9544       444.5190        45.7913       -78.3278     268     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.745000        86.8870     
  205         0.6125       426.4430        46.0961       -78.7618     420     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.573000        79.6360     
  206         0.2576       384.3520        46.0273       -78.0967     673     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.508000       101.0960     
  207         0.1730       413.6330        46.0556       -78.3656     426     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.663000       100.2440     
  208         4.0314       407.4070        45.9547       -78.5138     281     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.752000       104.0340     
  209         0.2504       449.7770        46.0250       -78.5685     525     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.188000       112.5800     
  210         0.3421       209.8630        45.8657       -77.5367     863     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.483000        85.0080     
  211         0.1211       490.5940        45.6969       -78.9812     62     LAKE     LAKE     LAKE     [NONE]     [NONE]       8.215000       115.9860     
  212         7.3007       411.3400        45.8114       -78.1663     315     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.551000       101.7350     
  213         1.1134       432.1990        46.0174       -78.5645     483     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.078000        78.5720     
  214         2.8937       232.0290        45.9971       -77.5841     844     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.135000       104.6030     
  215         3.5737       420.6150        46.0630       -78.4313     529     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.100000        75.1710     
  216         0.1037       446.4130        45.8387       -78.8394     144     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.286000        71.0240     
  217         5.0246       371.6330        45.9890       -78.5837     481     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.387000       120.5500     
  218        28.3753       328.6850        45.9042       -78.0580     537     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.237000        63.1320     
  219         1.2178       489.2120        45.7329       -78.9783     85     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.153000       118.9770     
  220         3.0229       306.6410        45.9778       -77.9435     649     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.373000        98.5460     
  221         0.2559       248.9600        45.8773       -77.6619     792     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.966000        66.0010     
  222         0.2052       254.1190        46.0685       -77.7067     744     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.352000        93.7030     
  223        14.0772       378.5060        45.9953       -78.5473     482     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.945000       110.4520     
  224         0.3392       429.4870        45.9364       -78.4511     375     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.202000       104.5440     
  225         5.9047       361.9380        46.0217       -78.2073     587     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.842000       127.5760     
  226         0.1334       302.0130        45.8253       -77.7648     657     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.834000       147.9890     
  227         1.1795       470.8130        45.7586       -78.1789     317     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.575000        78.2610     
  228         0.4283       459.9710        45.7175       -78.6411     218     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.692000        83.0970     
  229         0.4807       408.7640        46.0687       -78.3533     297     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.394000        90.3390     
  230         0.4434       436.6540        46.0469       -78.5851     452     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.370000        80.5490     
  231         4.2359       438.5110        45.7094       -78.7657     136     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.673000       110.7950     
  232         2.7499       467.2710        45.8111       -78.4100     259     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.875000        72.7490     
  233         8.7373       301.2010        46.0335       -78.0020     768     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.974000        96.5500     
  234         1.3121       220.6580        45.9865       -77.6826     888     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.584000       111.9730     
  235         7.1060       435.7400        45.8000       -78.4341     264     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.494000        88.5410     
  236         0.1749       413.4010        45.9378       -78.3028     403     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.177000        90.1680     
  237         0.5498       458.1620        45.8503       -78.8687     130     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.851000        99.9420     
  238         3.4853       438.5500        45.6980       -78.8179     135     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.803000       106.9540     
  239         0.1140       454.7330        46.0953       -78.5901     443     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.585000        90.9440     
  240         0.4446       464.1960        45.9548       -78.7642     405     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.537000       133.1130     
  241        37.6716       421.2990        45.7646       -78.5978     220     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.486000        97.7920     
  242         0.1285       372.3330        46.0375       -78.2794     501     LAKE     LAKE     LAKE     [NONE]     [NONE]       8.118000        80.5800     
  243         0.1168       456.2460        45.6789       -78.8872     57     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.503000        69.9770     
  244         0.5885       413.8400        46.0651       -78.3632     298     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.413000        61.9380     
  245        13.0679       316.3680        45.9829       -78.2975     574     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.234000        78.6640     
  246         1.5757       429.3440        45.8584       -78.7447     140     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.943000        84.0580     
  247         0.1394       252.3660        45.8616       -77.6325     795     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.775000        87.3910     
  248         0.7216       409.4430        46.0668       -78.4513     462     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.779000        82.3650     
  249         0.1094       420.2910        46.1016       -78.7197     419     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.317000       116.8590     
  250         0.3253       426.0340        45.8909       -78.7081     252     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.181000       105.7150     
  251         1.0225       455.9780        45.7736       -78.9269     71     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.467000       105.3420     
  252        12.1851       394.2600        46.1067       -78.4346     300     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.440000        94.7930     
  253         9.8128       369.7440        46.0736       -78.4920     459     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.267000        92.3140     
  254        33.3643       277.3530        45.9144       -78.0044     668     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.054000        75.4220     
  255         3.9617       481.2010        45.6545       -78.8620     59     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.694000        93.4730     
  256         0.3776       191.9520        45.9297       -77.5319     902     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.393000       102.0380     
  257         0.3534       466.6970        45.6685       -78.8763     58     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.620000        84.5120     
  258         2.0956       373.3320        45.9183       -78.3863     382     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.553000        95.6130     
  259         8.4172       404.0640        45.8353       -78.1879     308     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.016000        83.9050     
  260         3.1088       417.4990        46.1222       -78.4950     301     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.102000        86.4950     
  261         0.4106       412.0420        45.8269       -78.1331     335     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.394000        88.8510     
  262         0.1088       230.8190        45.9593       -78.0758     610     LAKE     LAKE     LAKE     [NONE]     [NONE]       1.854000        92.4060     
  263         0.1580       429.9090        45.8634       -78.7141     236     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.315000       113.9220     
  264         3.0178       229.8670        45.8674       -77.6795     758     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.060000        91.9350     
  265        19.4105       435.1380        45.8039       -78.2997     267     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.088000        84.3080     
  266         0.1183       273.7110        45.7710       -77.7084     654     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.035000        88.9310     
  267         0.2148       403.3650        45.9473       -78.2632     582     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.156000        71.6900     
  268         0.6288       365.9620        45.8389       -77.9964     553     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.788000        88.0930     
  269        63.5569       410.0910        45.8575       -78.5013     291     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.616000       104.0070     
  270         1.6736       386.4020        45.9223       -78.2083     496     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.577000        80.7730     
  271         0.6089       407.4070        45.9600       -78.5172     281     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.752000       104.0340     
  272         0.1038       490.1200        45.7645       -78.7911     82     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.681000        97.8160     
  273        14.6307       273.4810        46.0299       -77.9148     788     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.019000        55.7610     
  274         3.7516       454.7330        46.0942       -78.5827     443     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.585000        90.9440     
  275         0.1800       470.3080        45.7688       -78.8307     69     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.395000        93.1240     
  276        13.5298       203.2180        45.9567       -77.5611     875     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.760000        94.4450     
  277         0.7566       438.2590        45.7129       -78.8113     42     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.165000       101.2290     
  278         1.0960       191.9520        45.9291       -77.5287     902     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.393000       102.0380     
  279         0.3298       416.3360        45.8845       -78.5773     273     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.568000       115.8370     
  280         1.9610       169.9550        45.8809       -77.3866     919     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.576000        92.0110     
  281         0.1081       231.0990        46.0054       -77.7707     666     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.459000        41.6880     
  282         3.5221       445.4900        45.6427       -78.7676     211     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.759000        75.7290     
  283         1.7343       228.2800        45.9822       -77.6114     739     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.939000        56.9420     
  284         0.6492       421.4150        45.9024       -78.6653     250     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.327000       114.6210     
  285         0.2162       406.1520        46.0443       -78.2586     502     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.995000        90.0250     
  286         1.1768       346.2090        45.8033       -77.8847     549     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.733000        64.2280     
  287         1.5328       270.8340        45.9206       -77.9569     669     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.096000       119.8850     
  288         7.8561       378.3380        46.0496       -78.1217     623     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.746000       103.6480     
  289         1.4373       446.3450        45.8005       -78.5537     290     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.299000        94.7120     
  290         0.6238       367.4800        46.0626       -78.6118     450     LAKE     LAKE     LAKE     [NONE]     [NONE]       8.131000        87.5450     
  291         2.4865       439.2440        45.7558       -78.2473     319     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.163000        91.1780     
  292         0.1478       403.6550        45.8373       -78.6750     227     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.867000        78.6960     
  293         1.1456       317.8430        46.0207       -78.2781     503     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.881000       131.7980     
  294         2.7622       203.2180        45.9560       -77.5691     875     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.760000        94.4450     
  295         4.9043       372.6590        46.0589       -78.6872     449     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.222000       105.3440     
  296         0.2133       346.2090        45.8069       -77.8862     549     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.733000        64.2280     
  297         0.8837       288.6960        45.7545       -77.7246     655     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.993000        92.9820     
  298         0.5742       223.6940        46.0120       -77.6183     747     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.963000        94.2240     
  299         0.4995       330.0500        45.9975       -78.2489     580     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.693000       137.3320     
  300         0.1054       193.8230        45.9328       -77.6321     810     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.694000       112.1500     
  301         0.1134       444.5190        45.7904       -78.3248     268     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.745000        86.8870     
  302         0.1234       303.9360        45.9481       -78.0634     692     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.017000        48.7920     
  303        11.6300       355.7840        46.1001       -78.2698     500     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.257000        96.5340     
  304         0.1888       399.9730        45.9171       -78.2166     330     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.635000        85.4450     
  305         1.9021       209.0640        45.9745       -77.5552     742     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.421000       113.5310     
  306        24.0204       375.2910        46.0702       -78.2905     497     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.117000        89.8940     
  307         0.2952       420.2260        45.7557       -78.6591     219     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]      10.800000       109.1200     
  308         2.8409       332.3160        45.8178       -77.6697     724     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.413000        54.4320     
  309         0.1038       403.2560        45.9635       -78.4172     520     LAKE     LAKE     LAKE     [NONE]     [NONE]       9.522000        94.6470     
  310         1.0979       388.3200        46.1341       -78.6370     389     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.012000       103.5890     
  311         0.2181       381.6320        45.9362       -78.2086     495     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.227000        87.2510     
  312         0.1070       304.4090        46.0438       -77.7581     745     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.257000        78.4900     
  313         3.9588       406.1520        46.0411       -78.2498     502     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.995000        90.0250     
  314         0.2556       368.0350        46.0542       -78.5848     523     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]      10.538000       359.1390     
  315         9.1701       397.5850        46.0985       -78.6794     415     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.641000        86.3120     
  316         0.1540       473.1000        45.7796       -78.7564     148     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.478000       109.7950     
  317         3.4113       285.0380        45.7788       -77.7199     653     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.370000        72.2660     
  318         0.4543       421.5110        46.0345       -78.1966     586     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.346000        83.4640     
  319         0.3812       440.9480        45.7299       -78.5352     113     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.412000       132.4740     
  320         1.9509       463.4850        45.7567       -78.7933     84     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.770000       111.3760     
  321         4.6677       430.9370        45.7840       -78.4424     166     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.829000       101.1010     
  322        10.1072       273.5950        45.8269       -77.6596     723     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.692000        96.8170     
  323         0.8864       355.7840        46.1004       -78.2820     500     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.257000        96.5340     
  324         0.8841       263.7400        45.8436       -77.6884     760     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.519000        61.0510     
  325         8.5512       410.2070        45.9050       -78.2873     312     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.619000       106.4360     
  326         0.6468       430.3320        46.0212       -78.5782     353     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.109000       121.4980     
  327         0.0948       402.9650        46.0395       -78.3795     428     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.995000        80.8420     
  328         2.7557       381.7650        46.1136       -78.6711     414     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.093000        89.7430     
  329         1.4481       355.1990        45.9981       -78.4803     279     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.694000        67.4940     
  330         0.5450       388.6180        46.0780       -78.6165     442     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.595000        97.8340     
  331         0.1553       349.1140        45.9929       -78.4772     285     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.580000        70.4400     
  332         0.0950       252.0120        46.0555       -77.9214     789     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.300000        62.9210     
  333         0.3181       199.2050        45.8911       -77.5813     862     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.385000        93.9730     
  334         1.0306       387.4320        46.1138       -78.6592     445     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       9.440000        35.7830     
  335         9.9306       268.6790        46.0691       -77.8883     798     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.561000       102.0420     
  336         0.3117       450.3550        45.9308       -78.4506     376     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.521000       128.5650     
  337         0.1069       228.2800        45.9845       -77.6099     739     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.939000        56.9420     
  338         0.1697       395.5550        46.0996       -78.6365     441     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.452000        72.8000     
  339         2.4059       385.7420        46.0871       -78.3906     294     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.615000        90.6560     
  340         0.3719       434.6110        45.9281       -78.2754     310     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.975000        79.0990     
  341         8.4297       427.7040        45.7164       -78.7261     137     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.599000       102.8970     
  342         4.3024       481.6480        45.6895       -78.9995     63     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.613000       119.1200     
  343         0.4268       399.6360        45.7796       -78.1357     344     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.168000       102.3660     
  344         0.4530       437.1180        45.8191       -78.8732     123     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       1.938000       109.1060     
  345         5.8749       391.3260        46.0702       -78.3815     295     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.815000        74.2790     
  346         2.8336       425.1570        45.8051       -78.5686     243     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.031000        93.5170     
  347        15.7971       386.0740        45.9529       -78.6034     456     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.309000        90.2950     
  348        16.1961       303.6190        45.9634       -78.1522     611     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.007000        92.0250     
  349         0.1883       361.9380        46.0096       -78.2057     587     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.842000       127.5760     
  350        17.4412       423.9510        45.8440       -78.4375     258     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.339000        95.8020     
  351         7.5517       427.9560        45.7244       -78.6818     215     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.029000        97.4680     
  352         0.7005       402.1750        45.8430       -78.6593     232     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.249000        93.7350     
  353         2.5158       400.5940        45.8464       -78.1694     307     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.164000        92.9840     
  354         0.8043       223.2910        45.9610       -77.5275     876     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.436000       130.2130     
  355         0.5212       417.7750        45.9191       -78.5324     278     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.975000       105.9660     
  356         0.5384       298.1030        45.7797       -77.7472     659     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.295000        76.5740     
  357         1.6673       425.7800        45.7808       -78.6982     77     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.695000        84.9890     
  358         4.3903       440.3680        45.8973       -78.8371     127     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.535000        91.5340     
  359         0.1239       455.9780        45.7705       -78.9301     71     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.467000       105.3420     
  360         0.1042       405.1810        46.1249       -78.4281     302     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.461000        98.6410     
  361         0.1005       459.9990        45.6644       -78.7485     210     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.127000        95.0330     
  362         0.0999       458.9390        45.8477       -78.8502     143     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.052000       126.6160     
  363         2.2234       429.0550        45.9042       -78.6370     248     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.958000       121.3290     
  364         1.3179       471.6540        45.6626       -78.9462     47     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.654000        81.3030     
  365         0.4399       426.6880        45.7732       -78.6791     221     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.992000       114.4410     
  366         0.1832       370.2590        46.1623       -78.6535     417     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.305000       121.2290     
  367        69.8577       432.2610        45.8503       -78.9045     125     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.566000       101.1870     
  368         0.7952       457.6260        45.6849       -78.8691     53     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.954000        78.8350     
  369         0.1816       389.5000        46.0746       -78.6796     422     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.948000       130.8180     
  370         0.1323       282.7550        46.0475       -77.7773     808     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.193000        95.4420     
  371         3.0204       263.7400        45.8403       -77.6880     760     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.519000        61.0510     
  372         6.6468       336.0890        45.9655       -78.2389     581     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.933000        74.9480     
  373        15.8157       231.5780        46.0021       -77.7752     664     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.962000        57.2240     
  374         1.5524       493.6380        45.6363       -78.9461     51     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.955000        93.5510     
  375        11.4330       318.8100        45.8618       -77.8766     540     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.326000        92.5500     
  376         0.4601       304.4090        46.0429       -77.7577     745     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.257000        78.4900     
  377         1.2317       461.4980        45.6757       -78.9759     48     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.475000       117.9350     
  378         0.1170       398.5330        45.8747       -78.1011     338     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.386000       118.0690     
  379         0.4428       358.2310        46.0165       -78.3153     499     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.785000       130.0530     
  380         2.6282       426.6880        45.7740       -78.6820     221     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.992000       114.4410     
  381         7.7604       274.7070        45.8764       -77.8065     753     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.329000        93.3790     
  382         1.4238       468.4540        45.6741       -78.8602     46     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.174000        82.8380     
  383         0.3437       259.4750        45.9889       -77.7959     559     LAKE     LAKE     LAKE     [NONE]     [NONE]       1.751000       102.8710     
  384         2.9651       467.4130        45.7629       -79.0428     38     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.917000       110.1830     
  385         0.0968       415.7120        45.7899       -78.1305     342     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.638000        72.9700     
  386         0.1596       462.1820        45.7632       -78.7688     83     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.334000       117.0370     
  387         0.3079       399.9630        45.9668       -78.5040     288     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.286000       123.5400     
  388         0.2624       265.1180        45.8322       -77.7960     687     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.811000       114.9920     
  389         0.3337       460.3090        45.7865       -78.4643     167     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.060000       120.4960     
  390        10.2191       421.8160        45.8390       -78.6449     228     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.617000       104.0350     
  391         0.3942       338.9380        45.8243       -77.9047     547     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.968000        92.8210     
  392         0.2617       421.4150        45.9026       -78.6643     250     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.327000       114.6210     
  393         6.7488       395.5550        46.1044       -78.6289     441     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.452000        72.8000     
  394         0.1067       450.6630        45.7926       -78.5497     202     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.514000       127.1790     
  395         0.1556       459.1850        45.8013       -78.5167     165     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.357000        52.5710     
  396         0.1610       437.1570        45.6952       -78.7993     43     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.006000       114.1350     
  397         0.3219       405.4260        45.7885       -78.5726     203     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.440000        93.2580     
  398         7.7923       465.2980        45.7582       -78.9690     72     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.349000       106.6970     
  399         4.1060       209.6760        45.8747       -77.5150     870     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.554000       116.0010     
  400         6.3647       316.3680        45.9929       -78.2912     574     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.234000        78.6640     
  401        11.6323       241.1340        45.8922       -77.6526     846     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.595000       103.8650     
  402         1.0211       294.2280        45.8709       -77.9458     557     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.002000        50.3350     
  403         0.1270       273.1330        46.0268       -77.7223     802     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.688000        87.4940     
  404         1.1666       335.9340        45.9674       -78.6089     411     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.506000        97.2090     
  405         4.8361       464.5980        45.7663       -79.0825     37     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.310000       101.3970     
  406         2.7909       488.7470        45.7067       -78.9615     88     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.758000       128.2860     
  407         0.7914       401.3410        46.1272       -78.4553     303     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.394000        90.9550     
  408         3.4707       262.7680        45.8387       -77.6360     722     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.936000       107.1330     
  409         1.2479       407.6960        45.9630       -78.3537     401     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.522000       116.1520     
  410        13.7180       339.6170        45.9335       -78.1803     494     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.515000        66.3370     
  411        17.1069       330.0300        46.0571       -78.0083     532     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.733000        86.0550     
  412         0.1240       419.4080        45.8704       -78.6997     235     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.506000        95.7290     
  413         1.3103       364.8760        45.9208       -78.1180     616     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.591000        82.2480     
  414         6.3428       425.7800        45.7756       -78.7031     77     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.695000        84.9890     
  415         0.8272       299.6630        46.0088       -78.2904     506     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.301000        97.7490     
  416         2.3027       291.3360        45.9782       -77.9035     646     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.151000        96.5780     
  417         0.1783       368.3630        45.9120       -78.1667     328     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.899000        79.6350     
  418         0.1824       425.1570        45.8106       -78.5708     243     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.031000        93.5170     
  419         0.3174       488.9960        46.0098       -78.6305     354     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       1.571000       102.5560     
  420         0.5719       466.8330        45.7810       -78.7946     67     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.632000        94.1060     
  421        11.3886       348.9250        45.9803       -78.3371     395     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.540000        62.7820     
  422        33.8906       205.8310        45.9134       -77.6031     809     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.686000        85.4690     
  423         1.4239       473.1000        45.7763       -78.7630     148     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.478000       109.7950     
  424         1.2294       416.3360        45.8854       -78.5795     273     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.568000       115.8370     
  425         0.1095       242.4800        45.8567       -77.5322     864     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.981000        49.4840     
  426         0.4015       288.5410        45.8989       -77.7967     717     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.073000       107.3900     
  427         0.1764       453.3970        45.9555       -78.4898     283     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.017000        85.7250     
  428         0.7956       429.0450        45.8139       -78.1447     316     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.516000        88.6250     
  429        14.2849       383.6970        46.1380       -78.6101     387     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.968000        95.9670     
  430         0.0969       204.4020        45.9756       -77.5967     740     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.464000        72.9000     
  431         1.3601       248.9600        45.8738       -77.6613     792     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.966000        66.0010     
  432         0.2159       446.0700        45.8486       -78.8939     129     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.062000        95.8120     
  433         4.2473       389.1400        46.0360       -78.3274     429     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.977000       111.2440     
  434         9.6504       403.3650        45.9318       -78.2537     582     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.156000        71.6900     
  435         1.6885       295.1110        46.0071       -78.2680     584     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.248000       100.1750     
  436         4.3501       277.1130        45.9119       -77.8916     706     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.144000       103.5160     
  437         0.1346       454.9500        45.8623       -78.6196     229     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.774000       105.4950     
  438         0.9502       398.5330        45.8761       -78.0972     338     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.386000       118.0690     
  439         3.5404       288.5410        45.9021       -77.7848     717     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.073000       107.3900     
  440         4.4128       395.3000        45.8996       -78.1923     329     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.856000        91.6000     
  441         0.0741       311.9330        46.0637       -78.5999     455     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.051000       114.3810     
  442         3.7138       457.3100        45.7899       -78.2578     321     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.310000        70.6950     
  443         0.4304       281.2780        45.9634       -78.1909     598     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.483000       133.4900     
  444         1.0454       423.4350        45.8844       -78.7098     253     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.869000       116.8590     
  445         0.3072       295.0950        45.9815       -78.2431     575     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.333000        92.4120     
  446         1.4340       252.4000        46.0196       -77.7176     803     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.608000        94.8670     
  447        20.6947       399.3510        46.0731       -78.5314     467     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.319000       100.2350     
  448         3.0427       375.0610        45.9150       -78.3768     380     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.861000        87.9000     
  449         5.0517       214.5590        46.0184       -77.7481     801     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.887000        87.6520     
  450         0.1321       484.9540        45.7890       -78.8219     65     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.981000       100.7630     
  451         0.3661       271.3540        45.8587       -77.5930     796     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.939000       106.6660     
  452         0.4569       419.6700        46.1203       -78.4651     305     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.760000       108.6080     
  453         2.7130       453.3970        45.9522       -78.4882     283     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.017000        85.7250     
  454         0.0955       417.7750        45.9184       -78.5341     278     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.975000       105.9660     
  455        10.2726       261.2530        46.0369       -77.8815     804     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.731000        69.9300     
  456         0.1693       402.0920        45.9344       -78.6488     361     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.122000       111.0210     
  457         4.6725       252.3660        45.8568       -77.6464     795     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.775000        87.3910     
  458         0.8690       417.6840        45.8835       -78.4093     378     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.800000        75.3380     
  459         0.1046       462.5490        45.8070       -78.9777     133     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.495000        89.4950     
  460         0.1383       455.5590        45.7642       -78.5533     204     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.873000        64.9460     
  461         0.2099       355.1990        45.9984       -78.4815     279     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.694000        67.4940     
  462         9.0993       429.1150        45.8173       -78.4711     261     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.283000        96.7450     
  463         2.6088       459.9710        45.7135       -78.6435     218     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.692000        83.0970     
  464         5.5574       433.0930        45.8677       -78.7834     138     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.219000        96.8660     
  465         9.1770       445.0180        45.6673       -78.7718     209     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.822000        87.7220     
  466         0.7291       432.9750        45.9405       -78.7640     406     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.124000        98.1700     
  467        27.8122       425.9680        45.8271       -78.6024     241     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.501000        96.8590     
  468         0.8158       459.2430        45.6756       -78.9487     60     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.148000        72.4740     
  469         5.4352       457.0450        45.6946       -78.8796     52     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.412000       111.0870     
  470        16.3741       387.5810        45.8660       -78.1641     306     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.469000        88.7630     
  471         3.8699       395.5180        45.8052       -78.0948     339     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.041000        63.5910     
  472         0.1214       405.4260        45.7887       -78.5756     203     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.440000        93.2580     
  473        25.5094       395.1470        45.8608       -78.2529     326     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.615000        96.6490     
  474         0.3560       458.2700        45.7582       -79.0003     74     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.231000       115.9700     
  475         0.1418       322.6310        46.0818       -77.8794     770     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.518000        96.2840     
  476         1.4638       434.1360        45.7266       -78.7361     217     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.631000        91.6640     
  477         0.1969       409.4430        46.0675       -78.4525     462     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.779000        82.3650     
  478         0.8820       218.8120        45.9912       -77.7022     887     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.418000        83.6400     
  479         0.6463       330.1140        45.8768       -77.9437     554     LAKE     LAKE     LAKE     [NONE]     [NONE]       8.272000       122.6490     
  480         0.0352       395.9600        45.9569       -78.5355     287     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.017000       125.1450     
  481         0.4021       423.5160        45.7953       -78.5805     201     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.214000        79.4050     
  482         4.7850       240.2910        45.9763       -77.7608     785     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.950000        66.1730     
  483         0.3587       283.7240        45.8546       -77.6762     759     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.243000        81.9030     
  484         7.2211       224.0930        45.8789       -77.5923     861     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.186000        83.9260     
  485         0.3057       424.5120        45.9111       -78.6013     247     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.273000       113.3780     
  486         1.6716       369.7440        46.0781       -78.4940     459     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.267000        92.3140     
  487         0.1629       206.9210        45.8650       -77.4164     867     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.577000        98.0070     
  488         0.2013       265.5810        46.0837       -77.7987     807     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.551000        63.3020     
  489        36.3593       282.6930        46.0527       -77.9585     771     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.501000        90.8770     
  490        42.2670       274.7070        45.8806       -77.8143     753     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.329000        93.3790     
  491        32.8007       372.6590        46.0671       -78.6931     449     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.222000       105.3440     
  492         0.1822       453.3370        45.8525       -78.6205     230     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.351000        94.8400     
  493        35.9486       451.8960        45.7859       -79.0133     34     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.382000       105.7820     
  494         8.7349       230.4070        45.9926       -77.6398     737     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.961000        72.6880     
  495        51.4375       240.4000        46.0409       -77.6950     743     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.825000        92.3520     
  496         0.1527       291.7910        45.9118       -77.8156     716     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.445000       101.6290     
  497         9.7725       303.9360        45.9292       -78.0846     692     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.017000        48.7920     
  498         8.0068       459.0460        45.6964       -78.9438     61     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.086000       100.4690     
  499         0.3296       400.2780        45.9007       -78.2975     311     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.884000        89.0390     
  500         0.1695       371.6330        45.9844       -78.5736     481     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.387000       120.5500     
  501         1.6330       462.1820        45.7629       -78.7744     83     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.334000       117.0370     
  502         3.7440       204.8630        45.8748       -77.5648     868     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.051000        92.1780     
  503         0.5072       317.5640        45.7805       -77.7311     660     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.121000        86.7010     
  504         0.3562       437.1570        45.6956       -78.7991     43     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.006000       114.1350     
  505         9.1569       351.8030        46.0095       -78.3795     530     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.522000        83.8060     
  506         0.8477       427.2880        45.9239       -78.6284     457     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.242000        90.9580     
  507         1.2841       465.5690        45.7178       -78.9017     81     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.879000       107.1810     
  508         5.5482       486.2480        45.8063       -79.0773     35     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.157000       116.5940     
  509         5.3634       443.8980        45.7771       -78.5322     200     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.452000        95.7600     
  510         0.2141       420.6150        46.0583       -78.4224     529     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.100000        75.1710     
  511         0.5970       256.8410        46.0471       -77.8365     799     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.846000       106.2220     
  512         0.1005       424.1180        45.7666       -78.6683     214     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.359000       106.0790     
  513        27.7523       280.5240        45.9392       -77.8808     644     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.883000        95.7360     
  514        24.1232       290.1530        45.9118       -77.9295     704     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.467000        91.5330     
  515        10.1289       415.6850        45.7912       -78.1989     322     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.432000        87.0960     
  516        11.9890       207.5220        45.9794       -77.5442     842     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.990000        93.9790     
  517         0.6922       375.8520        46.0427       -78.6537     424     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.092000        77.1480     
  518         0.8877       389.5000        46.0780       -78.6839     422     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.948000       130.8180     
  519         1.6101       425.6020        45.8863       -78.6268     246     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.958000        92.1870     
  520         0.9620       206.9210        45.8654       -77.4120     867     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.577000        98.0070     
  521         4.2871       475.9600        45.7206       -78.9500     86     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.628000       104.8790     
  522         0.0045       267.0650        45.9610       -78.1953     600     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.618000       110.2720     
  523         0.1582       417.4990        46.1269       -78.4849     301     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.102000        86.4950     
  524         5.2198       233.8250        46.0082       -77.5818     843     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.171000        93.8930     
  525         2.8573       430.7040        45.9110       -78.7746     407     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.221000        84.5360     
  526         0.4774       204.4020        45.9743       -77.5959     740     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.464000        72.9000     
  527         4.5486       443.8980        45.7712       -78.5328     200     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.452000        95.7600     
  528         1.4749       411.1300        45.8788       -78.3120     313     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.668000       101.8040     
  529         1.3403       273.7110        45.7682       -77.7097     654     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.035000        88.9310     
  530         1.4873       394.8640        46.0522       -78.3734     427     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.957000        96.8270     
  531         0.2159       484.2270        45.7895       -78.8407     124     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.714000        94.6400     
  532         1.0986       418.0880        45.7912       -78.6786     79     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.553000       106.6270     
  533         0.2194       399.7290        45.9796       -78.5285     480     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.940000       101.6730     
  534        14.6434       455.6580        45.7651       -78.8791     78     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.738000       112.1130     
  535        10.9037       422.2900        45.7790       -78.4022     260     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.895000        89.8560     
  536        27.0401       398.0060        45.9070       -78.3402     392     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.429000        88.7490     
  537         4.6545       459.0460        45.6940       -78.9447     61     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.086000       100.4690     
  538         0.3347       416.4220        46.1192       -78.6191     390     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.658000        86.7090     
  539         0.3078       420.3650        45.7997       -78.6497     225     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.617000        68.6510     
  540         0.0090       379.7660        45.8190       -78.2126     323     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.086000       346.6860     
  541        34.5201       415.6850        45.7775       -78.2074     322     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.432000        87.0960     
  542         0.7346       398.1170        45.8808       -78.3509     393     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.545000       102.4080     
  543         0.1549       493.6380        45.6391       -78.9395     51     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.955000        93.5510     
  544        42.0286       417.2770        45.9196       -78.5373     276     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.126000       103.4630     
  545         5.5391       313.0740        45.9579       -78.2058     596     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.067000        60.3980     
  546         1.4773       458.9390        45.8501       -78.8574     143     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.052000       126.6160     
  547         0.1083       458.1620        45.8512       -78.8694     130     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.851000        99.9420     
  548         5.1065       432.9750        45.9395       -78.7697     406     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.124000        98.1700     
  549         9.8469       171.3560        45.8700       -77.3590     908     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.042000        79.4570     
  550         0.4263       333.1980        46.0788       -78.5073     469     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.516000       170.1040     
  551         0.1311       295.1110        45.9997       -78.2627     584     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.248000       100.1750     
  552         1.0063       444.1680        45.8285       -78.8764     122     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.909000       100.3740     
  553         3.2483       402.0920        45.9369       -78.6482     361     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.122000       111.0210     
  554         0.2371       467.8390        45.7760       -78.8082     68     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.855000       125.0350     
  555         9.9132       424.7340        45.8388       -78.4005     265     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.938000        96.4750     
  556         3.3478       450.3550        45.9309       -78.4694     376     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.521000       128.5650     
  557        25.7549       258.4600        46.0513       -77.8155     805     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.471000        80.5710     
  558         0.3241       465.2810        45.8495       -78.6008     242     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.030000       116.6350     
  559         0.1606       445.4900        45.6496       -78.7636     211     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.759000        75.7290     
  560         0.1060       413.8400        46.0668       -78.3642     298     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.413000        61.9380     
  561         0.9480       155.2150        45.8806       -77.3455     923     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.275000        98.1700     
  562        16.4014       328.5400        45.8500       -77.9693     552     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.926000        86.8700     
  563        11.4061       376.7450        46.0885       -78.3389     296     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.317000        81.3960     
  564         6.6546       179.2970        45.9313       -77.5961     886     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.327000        93.4030     
  565         0.6983       438.5110        45.7111       -78.7695     136     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.673000       110.7950     
  566         2.3257       399.9730        45.9182       -78.2259     330     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.635000        85.4450     
  567         2.4587       484.2270        45.7881       -78.8451     124     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.714000        94.6400     
  568         0.3539       423.4350        45.8839       -78.7077     253     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.869000       116.8590     
  569        10.4580       363.0290        45.8621       -78.0938     337     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.201000       100.5500     
  570         0.3853       481.2010        45.6607       -78.8627     59     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.694000        93.4730     
  571        10.4249       401.3410        46.1302       -78.4626     303     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.394000        90.9550     
  572         0.8115       475.9600        45.7190       -78.9487     86     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.628000       104.8790     
  573         0.8351       318.8100        45.8604       -77.8776     540     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.326000        92.5500     
  574         0.1245       450.9750        45.6705       -78.9450     55     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.763000        95.4780     
  575         1.4380       273.1330        46.0277       -77.7276     802     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.688000        87.4940     
  576         4.0283       485.4030        45.6424       -78.9878     50     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.998000        96.9420     
  577         0.1774       315.3980        45.9838       -78.2039     585     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.373000       106.8050     
  578         0.6670       424.8190        45.8945       -78.6852     251     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.339000       117.9480     
  579         0.8426       419.6440        46.1203       -78.4801     304     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.684000       103.7960     
  580         0.1205       390.6260        45.9031       -78.0905     538     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.339000        82.2180     
  581         0.1233       307.5650        45.8667       -77.9098     541     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.966000        91.1010     
  582         0.1133       396.5810        45.7968       -78.0990     336     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.101000        89.2410     
  583         0.1014       435.3360        45.8065       -78.9120     120     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.431000        97.9760     
  584         1.2301       454.2420        45.6916       -78.8547     54     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.473000        87.9570     
  585         1.1744       441.4230        45.7468       -78.7036     216     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.105000       112.9880     
  586         2.8963       231.0990        46.0090       -77.7835     666     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.459000        41.6880     
  587        10.2601       452.2270        45.8071       -78.8626     121     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.959000        99.6840     
  588         0.4135       179.2970        45.9308       -77.6112     886     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.327000        93.4030     
  589         0.1344       481.3940        45.7788       -78.8637     66     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.029000       122.1760     
  590         0.0054       220.8760        45.8432       -77.6940     757     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.384000        52.1370     
  591         0.3689       371.1880        45.9861       -78.4824     280     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.647000        88.4000     
  592         1.8730       419.4080        45.8746       -78.7039     235     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.506000        95.7290     
  593         7.6911       326.2350        46.0049       -78.3379     561     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.329000        89.6480     
  594         0.2012       336.6940        45.9349       -78.1387     612     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.927000        70.8630     
  595         0.5451       469.7400        45.6690       -78.9630     49     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.994000       125.6250     
  596        21.2465       353.3970        45.8652       -78.0219     535     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.654000        83.6060     
  597         0.4348       257.1620        46.0181       -77.6729     746     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.486000        97.7830     
  598         0.5374       430.5500        45.8888       -78.5577     274     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.922000       102.7540     
  599         0.2352       326.8830        45.8142       -77.9155     548     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.825000        95.2030     
  600         0.3300       317.8430        46.0171       -78.2810     503     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.881000       131.7980     
  601         0.1018       481.6480        45.6903       -78.9772     63     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.613000       119.1200     
  602         5.2604       423.0030        45.8788       -78.9127     126     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.859000       102.8120     
  603         0.0135       285.7840        46.0155       -78.2851     509     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.366000       137.5080     
  604         1.6331       461.5830        45.8960       -78.5118     272     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.937000       127.3570     
  605         0.2296       436.9190        45.8690       -78.9636     128     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.817000       119.0660     
  606         1.1478       473.3240        45.6768       -78.8371     44     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.469000        69.7950     
  607         4.2544       468.9180        45.8058       -79.0483     36     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.859000       118.8460     
  608         0.4874       405.1810        46.1254       -78.4273     302     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.461000        98.6410     
  609        25.9962       353.5150        46.0198       -78.4645     528     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.531000        94.1360     
  610         9.3501       414.3150        45.8611       -78.6761     249     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.809000       103.9790     
  611         0.7862       358.1380        46.1129       -78.6495     440     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]      11.522000        68.2490     
  612         0.3553       272.7930        45.8611       -77.5609     869     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.135000        63.1260     
  613         5.6260       480.2810        45.6473       -78.8437     117     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.242000        87.4790     
  614         0.1967       426.4430        46.0955       -78.7604     420     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.573000        79.6360     
  615        10.1002       288.5740        45.8452       -77.7219     754     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.113000        69.1660     
  616         2.0830       455.5590        45.7574       -78.5536     204     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.873000        64.9460     
  617         0.5649       209.0640        45.9720       -77.5581     742     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.421000       113.5310     
  618         3.6032       265.1180        45.8387       -77.8025     687     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.811000       114.9920     
  619         1.2196       414.3750        45.9670       -78.3734     399     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.123000        81.5710     
  620         0.1825       221.1600        46.0290       -77.7650     800     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.873000        64.2350     
  621         4.4026       371.1880        45.9835       -78.4830     280     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.647000        88.4000     
  622         0.6233       386.1500        46.0812       -78.4719     460     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.899000        93.1600     
  623        17.8324       381.1320        46.1540       -78.6535     416     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.851000        89.7400     
  624         0.4021       413.2330        45.9616       -78.4360     519     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.903000        79.1060     
  625         0.2271       293.1990        45.9997       -78.2226     579     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.129000        94.2300     
  626         3.1786       237.2950        45.9974       -77.6044     748     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.263000       120.0450     
  627         0.1946       480.2810        45.6481       -78.8294     117     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.242000        87.4790     
  628         2.9439       227.2520        45.8507       -77.5243     865     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.067000        92.3840     
  629         1.9321       329.8240        45.9286       -78.1138     615     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.319000        79.2160     
  630         0.8208       282.8320        45.8624       -77.6693     794     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.304000        80.7640     
  631         0.0199       315.6360        46.1114       -78.2838     487     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.710000       166.1590     
  632         0.1263       443.8250        45.8393       -78.8855     131     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.659000       100.9940     
  633         0.0981       429.0450        45.8173       -78.1501     316     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.516000        88.6250     
  634        11.0450       416.4220        46.1190       -78.5945     390     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.658000        86.7090     
  635         3.2645       424.1180        45.7609       -78.6832     214     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.359000       106.0790     
  636         9.4096       330.4340        45.8106       -77.6992     651     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.727000       106.6990     
  637         2.7895       460.3090        45.7913       -78.4688     167     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.060000       120.4960     
  638        15.7125       421.2990        45.7634       -78.6242     220     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.486000        97.7920     
  639        13.9862       330.0500        46.0128       -78.2408     580     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.693000       137.3320     
  640         0.1175       403.0450        46.0472       -78.4575     465     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.695000        76.4060     
  641         1.7047       234.3320        45.9470       -78.0534     691     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.634000        69.3730     
  642         4.8481       391.1520        45.9729       -78.5060     286     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.160000        98.4220     
  643         0.0954       426.4570        45.9730       -78.3943     397     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.820000        68.0420     
  644         0.1143       388.3200        46.1302       -78.6336     389     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.012000       103.5890     
  645         2.4034       354.3420        46.1003       -78.3029     386     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.979000        86.0900     
  646         0.1301       360.6180        46.1087       -78.6446     446     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]      11.673000        57.4460     
  647        20.3078       393.7410        45.9169       -78.6796     360     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.268000       108.2820     
  648         0.4989       402.2000        45.9723       -78.3621     398     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.601000        77.7960     
  649         6.1870       417.0950        45.8766       -78.7540     139     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.663000        95.3310     
  650         1.9724       413.4790        45.8173       -78.6683     233     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.446000        86.9250     
  651         2.2841       412.0420        45.8235       -78.1373     335     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.394000        88.8510     
  652         0.3828       408.9880        45.8180       -78.4456     263     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.197000        86.9250     
  653         0.5627       391.3260        46.0790       -78.3806     295     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.815000        74.2790     
  654         0.6653       292.9380        46.0843       -77.8292     806     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.221000        72.9430     
  655         0.2044       370.2540        46.0271       -78.1214     672     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.780000       105.4660     
  656         8.0546       377.8270        46.0379       -78.3576     425     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.622000       115.5540     
  657         0.1256       419.6700        46.1199       -78.4642     305     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.760000       108.6080     
  658         0.3593       366.5840        46.0720       -78.5095     466     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.049000       121.6850     
  659         0.0063       393.1820        45.8878       -78.6552     255     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.370000        96.3830     
  660        22.9194       182.7850        45.8438       -77.3166     879     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.898000        92.2680     
  661         0.5381       195.4140        45.9433       -77.5670     878     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.723000        81.6080     
  662         2.3733       368.3630        45.9138       -78.1719     328     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.899000        79.6350     
  663         4.0599       484.9540        45.7882       -78.8220     65     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.981000       100.7630     
  664         5.0224       219.6490        45.9785       -77.5791     741     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.510000       123.1160     
  665         0.2940       313.9740        45.8779       -77.9713     555     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.849000        78.4820     
  666         0.2525       401.8460        45.9445       -78.3184     402     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.468000        81.8340     
  667         0.1218       466.1810        45.6788       -78.8473     45     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.093000        86.0130     
  668        48.9757       186.9920        45.9099       -77.4788     905     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.968000        92.4830     
  669         0.9220       403.0450        46.0473       -78.4621     465     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.695000        76.4060     
  670         0.0966       421.5110        46.0347       -78.1951     586     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.346000        83.4640     
  671         0.1162       205.0920        45.9334       -77.5263     906     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.223000       106.6390     
  672        12.1805       246.9830        45.8608       -77.6133     791     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.575000        84.9020     
  673         4.1140       390.1780        46.0910       -78.6333     447     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.937000        81.2720     
  674         0.2896       396.4100        46.1085       -78.3730     363     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.454000       100.2230     
  675        18.6016       404.4600        46.0167       -78.6152     351     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.881000        76.4770     
  676        13.4991       410.0910        45.8710       -78.4988     291     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.616000       104.0070     
  677         0.5707       432.8490        45.6824       -78.7155     207     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.392000        80.2400     
  678         0.6445       412.1850        45.7889       -78.6513     223     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.592000       122.6850     
  679         0.1120       227.2520        45.8602       -77.5164     865     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.067000        92.3840     
  680         1.7381       328.5400        45.8592       -77.9602     552     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.926000        86.8700     
  681        18.5678       169.9550        45.8889       -77.4075     919     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.576000        92.0110     
  682         0.5649       490.5940        45.6979       -78.9822     62     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.215000       115.9860     
  683         3.8920       444.1680        45.8281       -78.8873     122     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.909000       100.3740     
  684         0.4198       461.4980        45.6725       -78.9767     48     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.475000       117.9350     
  685         8.3585       330.1140        45.8800       -77.9310     554     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.272000       122.6490     
  686         0.1438       409.4670        46.0572       -78.4555     464     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.584000       110.6710     
  687         0.2072       463.4850        45.7578       -78.7875     84     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.770000       111.3760     
  688         0.5782       369.8570        45.8658       -77.8298     543     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.719000        76.7090     
  689         0.0036       212.9820        45.9611       -78.0649     764     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       1.627000       150.3830     
  690         1.2035       392.1690        45.9067       -78.1800     332     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.704000        90.0950     
  691         0.2094       416.2630        46.0620       -78.5919     522     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.524000       125.3890     
  692         9.8019       465.2110        45.6851       -78.9144     56     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.782000       104.9840     
  693        20.9692       317.2390        45.8386       -77.9112     546     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.638000        77.4370     
  694         0.1145       430.3320        46.0213       -78.5799     353     LAKE     LAKE     LAKE     [NONE]     [NONE]       8.109000       121.4980     
  695        69.1899       353.5150        46.0134       -78.4664     528     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.531000        94.1360     
  696         1.4632       412.5900        45.7970       -78.6683     231     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.784000        88.4220     
  697         0.2209       486.2480        45.8010       -79.0655     35     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.157000       116.5940     
  698         0.5851       273.2210        46.0103       -77.8323     665     LAKE     LAKE     LAKE     [NONE]     [NONE]       1.960000        74.7190     
  699         0.7707       370.2590        46.1656       -78.6526     417     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.305000       121.2290     
  700         0.7903       259.6510        45.9926       -77.6663     738     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.934000       120.0090     
  701        80.8776       448.6230        45.7437       -78.8262     80     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.025000       107.3390     
  702        11.3327       440.8570        45.8422       -78.8254     142     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.201000       102.7780     
  703        19.5841       387.5110        45.9281       -78.7336     404     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.686000       106.4170     
  704         0.1893       232.0290        45.9965       -77.5726     844     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.135000       104.6030     
  705         0.8504       429.9090        45.8658       -78.7141     236     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.315000       113.9220     
  706         0.3585       353.6000        46.0692       -78.5964     448     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.262000       110.5400     
  707         0.7434       429.0550        45.9014       -78.6371     248     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.958000       121.3290     
  708         0.3737       466.1810        45.6779       -78.8477     45     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.093000        86.0130     
  709         7.0298       254.1190        46.0705       -77.6976     744     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.352000        93.7030     
  710         0.1066       473.3240        45.6808       -78.8339     44     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.469000        69.7950     
  711         0.1138       266.1410        45.8826       -77.7970     718     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.756000       123.9160     
  712         2.2966       372.3940        46.0457       -78.2903     507     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.683000        75.5290     
  713         8.3438       256.8410        46.0510       -77.8367     799     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.846000       106.2220     
  714         0.1680       343.9270        46.0564       -78.6205     454     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.982000       111.3970     
  715         2.2195       336.6940        45.9311       -78.1397     612     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.927000        70.8630     
  716         0.1766       449.3440        45.8394       -78.8725     132     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.178000       107.6900     
  717         2.0235       446.2420        45.7157       -78.8236     41     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.387000       100.6160     
  718         0.7007       450.9080        45.7632       -78.5127     205     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.721000       102.0800     
  719         0.2537       262.0260        45.8697       -77.7441     719     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.086000       107.2560     
  720        26.5439       386.3150        45.9685       -78.6496     412     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.191000       122.7670     
  721         1.8131       378.7410        46.1369       -78.6575     388     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.762000       133.3530     
  722         2.4178       262.0260        45.8807       -77.7397     719     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.086000       107.2560     
  723         0.2579       285.0380        45.7838       -77.7141     653     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.370000        72.2660     
  724         1.1780       337.6650        46.0663       -78.0383     531     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.852000        74.2490     
  725         1.2431       375.2910        46.0716       -78.2813     497     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.117000        89.8940     
  726         1.0239       249.6050        45.8292       -77.7872     686     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.634000        96.3880     
  727         0.6330       403.2560        45.9625       -78.4151     520     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       9.522000        94.6470     
  728         0.2426       446.3450        45.8011       -78.5507     290     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.299000        94.7120     
  729        13.1684       315.3980        45.9991       -78.1962     585     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.373000       106.8050     
  730        11.6361       447.6720        45.6750       -78.8121     116     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.591000        95.8250     
  731         0.1420       398.1170        45.8813       -78.3562     393     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.545000       102.4080     
  732         0.9116       293.1990        46.0006       -78.2211     579     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.129000        94.2300     
  733         9.3521       416.2630        46.0705       -78.5726     522     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.524000       125.3890     
  734         0.0975       465.2810        45.8489       -78.5994     242     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.030000       116.6350     
  735         5.4261       360.8680        46.1305       -78.6794     413     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.872000        71.8700     
  736        18.6206       299.4880        46.0063       -78.0843     671     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.263000       113.8650     
  737         0.9050       193.8230        45.9368       -77.6334     810     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.694000       112.1500     
  738         0.1541       489.2120        45.7303       -78.9727     85     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.153000       118.9770     
  739         1.1606       297.6240        45.7594       -77.7340     652     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.031000       102.3420     
  740         2.7253       396.6770        46.0397       -78.3059     430     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.851000       101.3750     
  741         0.4438       230.8190        45.9585       -78.0761     610     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       1.854000        92.4060     
  742         0.1388       378.7410        46.1305       -78.6572     388     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.762000       133.3530     
  743         9.7919       224.5200        45.9674       -77.7263     786     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.858000        88.2580     
  744        30.3778       208.5020        45.8552       -77.4708     866     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.766000        85.6170     
  745         1.6040       436.9190        45.8723       -78.9682     128     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.817000       119.0660     
  746         0.7295       462.5490        45.8058       -78.9738     133     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.495000        89.4950     
  747         0.2487       268.6790        46.0564       -77.8999     798     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.561000       102.0420     
  748         0.2698       249.6050        45.8297       -77.7850     686     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.634000        96.3880     
  749         0.5221       287.5570        45.8575       -77.6654     797     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.925000       115.0120     
  750         0.1431       367.2850        46.0465       -78.6682     423     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.469000        67.4100     
  751         1.0197       413.5100        45.9033       -78.4001     381     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.469000        96.1820     
  752         0.9934       392.4930        46.0498       -78.6153     356     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       9.365000        76.8230     
  753         0.9362       404.0640        45.8289       -78.1855     308     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.016000        83.9050     
  754         6.0837       263.8250        45.9112       -77.6884     751     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.371000       112.7530     
  755         0.4037       343.9780        46.0055       -78.4803     284     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.131000        61.5560     
  756         0.1814       469.7400        45.6684       -78.9594     49     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.994000       125.6250     
  757         1.7842       441.7940        45.9485       -78.7306     384     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.255000       117.2460     
  758         0.1403       281.2780        45.9627       -78.1904     598     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.483000       133.4900     
  759         1.4972       211.5630        46.0087       -77.7214     889     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.445000       119.7800     
  760         0.1754       466.4070        45.7577       -79.0409     39     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.034000       104.8930     
  761         8.8650       279.6120        45.9454       -78.1053     614     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.430000        77.9410     
  762         0.1999       440.3680        45.8907       -78.8324     127     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.535000        91.5340     
  763         5.5796       412.5900        45.7984       -78.6724     231     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.784000        88.4220     
  764         0.1222       370.4150        45.9569       -78.2270     597     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.848000        86.5220     
  765         1.9526       415.7210        45.9505       -78.5805     277     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.619000       114.7790     
  766         4.3792       416.0160        46.0347       -78.5874     352     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.451000       102.2110     
  767         0.7101       435.3360        45.8081       -78.9045     120     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.431000        97.9760     
  768         0.6254       420.8930        45.7717       -78.1384     345     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.745000        80.7910     
  769         3.3301       445.0180        45.6720       -78.7701     209     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.822000        87.7220     
  770         0.1585       410.5940        46.0309       -78.2517     578     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.485000       101.0140     
  771         0.0955       408.7640        46.0692       -78.3534     297     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.394000        90.3390     
  772         1.0296       205.0920        45.9378       -77.5297     906     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.223000       106.6390     
  773        66.0425       272.9540        45.9746       -77.8345     558     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.525000        89.8120     
  774         5.8068       424.5120        45.9161       -78.6062     247     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.273000       113.3780     
  775         6.9200       162.3890        45.8489       -77.2733     880     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       1.475000        78.3250     
  776         4.6635       466.8330        45.7810       -78.7871     67     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.632000        94.1060     
  777         0.1188       413.5100        45.9048       -78.3969     381     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.469000        96.1820     
  778         1.1658       436.6220        45.8132       -78.1275     341     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.436000       121.1400     
  779         8.9401       220.5970        45.9523       -77.7039     784     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.663000        87.6350     
  780         0.3507       459.9990        45.6629       -78.7463     210     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.127000        95.0330     
  781         0.1438       475.6260        45.7521       -79.0075     75     LAKE     LAKE     LAKE     [NONE]     [NONE]       9.851000        84.1640     
  782         0.1929       162.3890        45.8552       -77.2769     880     LAKE     LAKE     LAKE     [NONE]     [NONE]       1.475000        78.3250     
  783         0.1170       438.2590        45.7142       -78.8077     42     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.165000       101.2290     
  784         0.3226       270.8340        45.9193       -77.9567     669     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.096000       119.8850     
  785         0.1084       407.6960        45.9615       -78.3514     401     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.522000       116.1520     
  786         0.8975       456.2460        45.6793       -78.8894     57     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.503000        69.9770     
  787         5.2731       254.2720        45.9038       -77.6379     847     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.776000       117.1110     
  788         0.2229       294.0370        45.8542       -77.8400     542     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.740000        96.2080     
  789         1.6931       399.7290        45.9739       -78.5345     480     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.940000       101.6730     
  790         0.1205       271.3540        45.8577       -77.5935     796     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.939000       106.6660     
  791         5.8130       447.7730        45.6921       -78.7543     208     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.826000       113.3970     
  792         0.1962       229.8670        45.8672       -77.6831     758     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.060000        91.9350     
  793         0.8642       437.4830        45.8415       -78.7308     237     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.080000        96.4720     
  794         5.8561       381.2620        45.8357       -78.1099     334     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.788000        85.9670     
  795         0.1114       306.6410        45.9782       -77.9473     649     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.373000        98.5460     
  796         9.8380       338.9380        45.8115       -77.8959     547     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.968000        92.8210     
  797         0.2246       273.5950        45.8314       -77.6698     723     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.692000        96.8170     
  798         3.1336       446.9330        45.7056       -78.5896     110     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.453000       103.9030     
  799         0.1055       447.1240        46.1031       -78.4858     461     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.614000        85.5970     
  800         0.1210       224.5210        45.8582       -77.6872     762     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       9.219000        60.6180     
  801         0.1643       258.0030        45.8501       -77.8358     551     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.463000        29.8670     
  802         0.0977       470.8130        45.7626       -78.1789     317     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.575000        78.2610     
  803         0.2311       467.4130        45.7650       -79.0398     38     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.917000       110.1830     
  804         2.5306       218.3880        45.8760       -77.6874     761     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.111000        56.7860     
  805        17.2416       381.2620        45.8331       -78.1182     334     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.788000        85.9670     
  806         0.2820       413.2120        46.0025       -78.5738     355     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.540000       120.1930     
  807         4.0810       307.5650        45.8645       -77.9157     541     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.966000        91.1010     
  808         0.9406       238.5220        45.8259       -77.7768     689     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.041000        96.6340     
  809         0.1629       292.9380        46.0856       -77.8282     806     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.221000        72.9430     
  810         2.0982       400.2780        45.9042       -78.2982     311     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.884000        89.0390     
  811         2.0985       427.2880        45.9221       -78.6285     457     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.242000        90.9580     
  812         1.2007       367.2850        46.0447       -78.6724     423     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.469000        67.4100     
  813         3.1336       293.1450        45.8619       -77.8588     550     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.267000       117.3290     
  814         7.5931       424.9070        46.0931       -78.7417     421     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.329000        80.6400     
  815         5.0879       457.8930        45.7104       -78.8778     87     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.834000        98.7910     
  816        18.2882       353.9990        46.1336       -78.3010     485     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.777000        87.3670     
  817         0.0955       364.8760        45.9233       -78.1260     616     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.591000        82.2480     
  818         0.1117       283.7240        45.8569       -77.6756     759     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.243000        81.9030     
  819         4.5094       465.5690        45.7211       -78.9054     81     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.879000       107.1810     
  820         0.5454       464.5980        45.7727       -79.0692     37     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.310000       101.3970     
  821        26.5141       366.0700        45.8957       -78.1368     488     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.146000        91.5100     
  822         0.2015       432.1990        46.0159       -78.5629     483     LAKE     LAKE     LAKE     [NONE]     [NONE]       8.078000        78.5720     
  823         1.1782       389.7700        45.8952       -78.1976     333     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.828000       117.7000     
  824         1.6364       353.9990        46.1316       -78.2901     485     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.777000        87.3670     
  825         0.3750       301.5920        45.9779       -77.9171     645     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.440000        89.9730     
  826         4.8046       301.5920        45.9750       -77.9246     645     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.440000        89.9730     
  827         2.1712       402.2000        45.9737       -78.3643     398     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.601000        77.7960     
  828         0.1837       417.6840        45.8851       -78.4097     378     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.800000        75.3380     
  829         1.3684       265.5810        46.0823       -77.8043     807     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.551000        63.3020     
  830         5.8983       402.9650        46.0537       -78.3980     428     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.995000        80.8420     
  831        34.3766       202.1400        45.8471       -77.3948     858     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.268000        91.2340     
  832         0.8076       475.6260        45.7509       -79.0033     75     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       9.851000        84.1640     
  833         0.2234       407.0770        45.9851       -78.3685     396     LAKE     LAKE     LAKE     [NONE]     [NONE]       3.613000        90.2850     
  834         0.6378       262.7680        45.8390       -77.6455     722     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.936000       107.1330     
  835         1.6054       434.6110        45.9260       -78.2730     310     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.975000        79.0990     
  836         1.1756       467.8390        45.7773       -78.8124     68     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.855000       125.0350     
  837         0.2296       246.0840        45.8682       -77.6419     793     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.783000        79.4250     
  838         0.3786       431.5580        45.8230       -78.8240     147     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.083000        93.5780     
  839         0.2742       360.8680        46.1342       -78.6780     413     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.872000        71.8700     
  840         0.1126       287.5570        45.8567       -77.6650     797     LAKE     LAKE     LAKE     [NONE]     [NONE]       7.925000       115.0120     
  841         0.0379       280.0390        45.9971       -78.2637     583     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       2.782000       111.9780     
  842         0.1204       241.5210        45.8713       -77.7150     752     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.354000        79.7040     
  843         0.5522       410.5940        46.0324       -78.2531     578     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.485000       101.0140     
  844         1.2960       401.9990        45.9652       -78.5316     282     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.975000       143.3110     
  845         1.7463       396.5810        45.7974       -78.1009     336     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.101000        89.2410     
  846         0.4452       441.7940        45.9471       -78.7274     384     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.255000       117.2460     
  847        35.0859       395.4300        45.9306       -78.4128     377     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.239000       104.6210     
  848         0.2830       457.0450        45.6935       -78.8687     52     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.412000       111.0870     
  849         0.3977       488.7470        45.7069       -78.9570     88     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.758000       128.2860     
  850         0.8736       222.2390        45.9855       -77.7457     667     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       1.330000        83.7710     
  851         0.3224       331.4200        46.0802       -78.4823     468     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.018000        84.4030     
  852         0.2182       388.3590        45.9885       -78.5245     479     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.515000        99.1860     
  853         3.3767       370.4150        45.9518       -78.2275     597     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.848000        86.5220     
  854         0.3681       370.2540        46.0281       -78.1195     672     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.780000       105.4660     
  855         0.2478       303.6190        45.9505       -78.1445     611     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.007000        92.0250     
  856         3.7625       404.4600        46.0147       -78.6025     351     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.881000        76.4770     
  857         2.3826       458.2700        45.7615       -79.0021     74     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.231000       115.9700     
  858         2.4188       151.5370        45.8815       -77.3258     921     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.429000       116.9660     
  859         5.8159       209.8630        45.8651       -77.5424     863     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       6.483000        85.0080     
  860         0.1779       317.5640        45.7800       -77.7310     660     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.121000        86.7010     
  861        22.3172       270.8350        45.9731       -77.9980     648     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.074000        99.0100     
  862         4.0597       409.2280        45.8333       -78.2923     269     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.293000        78.7620     
  863         2.5727       246.0840        45.8712       -77.6461     793     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.783000        79.4250     
  864         6.1041       266.1410        45.8914       -77.7983     718     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.756000       123.9160     
  865         0.1220       461.5830        45.8955       -78.5150     272     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.937000       127.3570     
  866         5.6605       252.0120        46.0477       -77.9345     789     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.300000        62.9210     
  867         2.4497       415.7120        45.7984       -78.1413     342     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.638000        72.9700     
  868         0.8039       466.4070        45.7579       -79.0404     39     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.034000       104.8930     
  869         0.2175       395.2480        46.0584       -78.4627     463     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.260000        82.7560     
  870         2.8291       445.5340        45.8768       -78.4283     379     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.511000        69.1060     
  871         3.1184       308.9060        45.8902       -77.9707     556     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       8.886000        81.4620     
  872         0.1117       467.2710        45.8143       -78.4001     259     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.875000        72.7490     
  873         2.6164       423.5160        45.7975       -78.5835     201     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.214000        79.4050     
  874         0.1009       426.0340        45.8905       -78.7078     252     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.181000       105.7150     
  875         4.0054       466.6970        45.6673       -78.8820     58     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.620000        84.5120     
  876         0.1199       457.6260        45.6871       -78.8675     53     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.954000        78.8350     
  877         0.7367       429.1150        45.8135       -78.4524     261     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.283000        96.7450     
  878         0.4479       330.4340        45.7984       -77.7022     651     LAKE     LAKE     LAKE     [NONE]     [NONE]       6.727000       106.6990     
  879         3.8697       388.3590        45.9852       -78.5234     479     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.515000        99.1860     
  880         5.6364       381.6320        45.9367       -78.2240     495     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.227000        87.2510     
  881         0.1663       385.8260        45.8852       -78.0775     539     LAKE     LAKE     LAKE     [NONE]     [NONE]       5.590000        81.3090     
  882         0.5934       322.6310        46.0829       -77.8798     770     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.518000        96.2840     
  883         0.1719       395.3000        45.8984       -78.1882     329     LAKE     LAKE     LAKE     [NONE]     [NONE]       4.856000        91.6000     
  884         2.5597       174.6800        45.9242       -77.5454     903     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       3.955000        84.1770     
  885         2.3359       313.9740        45.8746       -77.9747     555     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       4.849000        78.4820     
  886         0.1549       358.1380        46.1143       -78.6501     440     LAKE     LAKE     LAKE     [NONE]     [NONE]      11.522000        68.2490     
  887        15.0510       436.6560        45.8458       -78.7794     141     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.064000        92.8830     
  888         7.7487       388.6180        46.0828       -78.6090     442     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       7.595000        97.8340     
  889        22.0475       444.4380        45.7848       -78.9201     119     Landuse_Land_HRU     Veg_Land_HRU     Soil_Land_HRU     [NONE]     [NONE]       5.366000       100.3310     
  890         0.1237       240.2910        45.9731       -77.7414     785     LAKE     LAKE     LAKE     [NONE]     [NONE]       2.950000        66.1730     
:EndHRUs
:PopulateHRUGroup Lake_HRUs With LANDUSE EQUALS LAKE     
:RedirectToFile Lakes.rvh
:SubBasinGroup   Allsubbasins
       127   451   211   751   440   148   559   548   290   863
       281   214   250   537   462   297   43   51   381   86
       529   446   406   144   671   450   544   457   341   252
       722   420   138   808   554   82   720   487   251   426
       56   577   126   330   63   136   803   461   307   166
       338   480   220   363   795   864   122   282   258   59
       146   73   789   484   501   133   343   398   532   452
       140   806   210   742   217   574   340   610   229   69
       535   277   42   50   379   586   85   528   759   443
       303   253   919   543   336   62   794   667   506   301
       580   202   316   377   417   847   81   921   746   247
       244   802   786   596   581   110   623   645   584   313
       459   400   165   508   287   499   753   760   456   923
       112   754   482   649   665   793   585   355   500   207
       463   71   397   427   129   279   296   119   45   322
       801   878   243   799   41   49   38   383   36   390
       558   687   716   880   291   505   321   205   859   719
       870   228   428   599   261   652   389   792   361   269
       88   414   164   612   278   204   396   465   552   249
       752   430   738   657   549   209   441   47   764   132
       664   295   613   655   354   538   268   393   407   241
       272   236   58   87   74   523   235   35   329   46
       557   669   310   869   658   78   449   424   614   843
       239   131   67   502   464   622   274   113   660   522
       412   706   216   686   810   650   447   219   77   305
       615   886   737   403   494   750   230   142   375   862
       125   545   485   225   259   353   302   651   771   267
       333   503   345   479   583   328   762   692   276   469
       284   299   616   504   617   311   611   809   68   844
       130   65   887   317   749   327   248   659   798   137
       118   342   724   578   807   653   579   352   141   673
       280   800   221   326   387   382   312   237   265   332
       542   646   744   466   232   55   547   143   467   319
       135   481   587   555   718   483   323   421   842   704
       298   263   556   111   846   723   391   509   672   308
       561   717   117   215   335   203   785   351   758   304
       867   331   422   889   315   519   246   858   541   743
       218   530   167   888   656   413   861   388   745   460
       288   445   72   536   39   419   380   906   902   405
       908   442   739   551   116   84   597   334   575   589
       415   147   582   768   200   525   654   306   401   201
       121   691   378   255   797   75   124   550   805   507
       546   384   54   598   770   454   905   80   399   767
       416   876   61   262   362   273   83   740   644   879
       48   53   788   429   423   227   294   784   648   128
       395   231   540   791   260   120   242   689   553   448
       531   804   139   496   666   339   668   60   757   411
       114   34   756   123   497   404   376   37   223   286
       688   455   747   539   285   66   865   796   901   337
       283   868   270   57   208   748   761   360   520   254
       344   233   866   44   468   52   300   903   293   402
       79   425   392   495   600   875   741   488   356   386
       264
:EndSubBasinGroup   
# :SBGroupPropertyOverride Allsubbasins   MANNINGS_N 0.001
:SBGroupPropertyMultiplier Allsubbasins  MANNINGS_N n_multi
EOF
# AvgAnnualRunoff
if [ ${expname} = "0g" ]; then
cat >> ${rvh_tpl} << EOF
:SBGroupPropertyMultiplier Allsubbasins  CELERITY c_multi
:SBGroupPropertyMultiplier Allsubbasins  DIFFUSIVITY d_multi
EOF
fi

wait