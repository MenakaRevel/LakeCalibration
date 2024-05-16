#!/bin/bash
# set -x 
# trap read debug

expname=${1} #'0a'
ens_num=`printf '%02d\n' "${2}"`
MaxIteration=${3}
RunType=${4}
CostFunction=${5}
ObsType1=${6} # [Obs_SF_IS, Obs_WL_IS, Obs_WA_RS]
ObsType2=${7} # [Obs_SF_IS, Obs_WL_IS, Obs_WA_RS]
#=====================================
echo $ens_num
# make experiment pertunation directory
echo "making folder --> ./out/${expname}_${ens_num}"
mkdir -p ./out/${expname}_${ens_num}
# cd into 
cd ./out/${expname}_${ens_num}

# copy main Ostrich + Raven model calibation pacakage
cp -r ../../OstrichRaven/* . 

# copy some utility codes
cp -r ../../src/* .

# copy params.py
# cp -r ../../params.py .
#===============================================================
# write the experiment settings
# create param.py
#===============================================================
# For ObsTypes
if [[ -v ObsType2 && -z $ObsType2 ]]; then
    ObsTypeCh="['$ObsType1']"
else
    ObsTypeCh="['$ObsType1','$ObsType2']"
fi
params=./params.py
rm -r $params
echo 'creating.....'`pwd` $params
cat >> ${params} << EOF
import os
import sys
#======================================
# defines the initial parameters for calibration experiments
#======================================
def ProgramType():
    return 'DDS'                            # calibration program type (e.g., DDS, GML as in Ostrich documentation https://usbr.github.io/ostrich/index.html)
#--------------------------------------
def ObjectiveFunction():
    return 'GCOP'                           # e.g., GCOP, wsse
#--------------------------------------
def finalcat_hru_info():
    return 'finalcat_hru_info_updated.csv'  # catchment information --> updated by adding observation columns
#--------------------------------------
def RavenDir():
    return './RavenInput'                   # Raven setup folder
#-------------------------------------- 
def only_lake_obs():
    return 1                                # use only lake observations for CW calibration
#--------------------------------------
def CostFunction():
    return '$CostFunction'
    # return 'NegKG_Q'                        # Q           ** this should be consistent with ObsTypes()
    # return 'NegKG_Q_WL'                     # Q + WL
    # return 'NegKGR2_Q_WA'                   # Q + WA
    # return 'NegKGR2_Q_WL_WA'                # Q + WL + WA
#--------------------------------------
def ObsTypes():
    return $ObsTypeCh
    # return ['Obs_SF_IS']                    # observations types 
    # return ['Obs_SF_IS', 'Obs_WL_IS']
    # return ['Obs_SF_IS', 'Obs_WA_RS1']
    # return ['Obs_SF_IS', 'Obs_WA_RS2']
                                            # SF - stream flow
                                            # WL - water level
                                            # WA - water area
                                            # IS - in situ
                                            # RA - remote sensing
#--------------------------------------
def ExpName():                              # Experiment name
    return '$ExpName'
#--------------------------------------
def MaxIteration():                        # Calibration budget
    return $MaxIteration
#--------------------------------------
def RunType():                             # Run initiaze or restart mode
    return '$RunType'                        # Restart mode {Extend the calibration budget} (OstrichWarmStart)
EOF
#===============================================================

# # # write observations types
# # ObsType=./ObsTypes.txt
# # cat >> ${ObsType} << EOF  
# # $Obs_Type1
# # $Obs_Type2

# # EOF

# observed lake list is written to the final_cat_info_updated.csv
# need to edit this file to add any observation parameter
# need special treatment when multiple observations available in one lake/sub Id ** on going work
#========================
# finalcat_hru_info_updated.csv
#========================
final_cat='finalcat_hru_info_updated.csv'
echo python update_final_cat_info.py
python update_final_cat_info.py #$final_cat # $Obs_Type1 $Obs_Type2

#========================
# rvh.tpl
#========================
rvh_tpl='Petawawa.rvh.tpl'
# only_lake_obs=1 # use only observations realted to Lake for calibrating lake parameters
# Obs_Type='Obs_SF_IS'
echo python update_rvh_tpl.py $rvh_tpl 
python update_rvh_tpl.py $rvh_tpl #$final_cat $only_lake_obs #$Obs_Type1 $Obs_Type2

# #========================
# # crest_width_par.csv.tpl
# #========================
# rvh_tpl='crest_width_par.csv.tpl'
# echo python create_cw_para_tpl.py $rvh_tpl
# python create_cw_para_tpl.py $rvh_tpl #$final_cat

#========================
# Lakes.rvh.tpl
#========================
echo create_lake_rvh_tpl.py 
python create_lake_rvh_tpl.py

#========================
# ./RavenInput/Petawawa.rvt
#========================
python update_rvt.py 'Petawawa'

# go back
cd ../

wait