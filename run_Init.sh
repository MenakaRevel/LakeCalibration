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

if [[ ${expname} = "0b"  ||  ${expname} = "1a" || ${expname} = "1d" || ${expname} = "0d" ]]; then  
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
if [ ${expname} = "0e" ]; then
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
# 0. 
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