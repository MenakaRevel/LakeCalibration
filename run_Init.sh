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

wait