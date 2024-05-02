#!/bin/bash
# set -x 
# trap read debug

expname=${1} #'0a'
ens_num=`printf '%02d\n' "${2}"`
# Obs_Type1=${3} # [Obs_SF_IS, Obs_WL_IS, Obs_WA_RS]
# Obs_Type2=${4} # [Obs_SF_IS, Obs_WL_IS, Obs_WA_RS]
#=====================================
echo $ens_num
# make experiment pertunation directory
echo "making folder --> ./out/${expname}_${ens_num}"
mkdir -p ./out/${expname}_${ens_num}
# cd into 
cd ./out/${expname}_${ens_num}

# copy params.py
cp -r ../../params.py .

# copy main Ostrich + Raven model calibation pacakage
cp -r ../../OstrichRaven/* . 

# copy some utility codes
cp -r ../../src/* .

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

#========================
# crest_width_par.csv.tpl
#========================
rvh_tpl='crest_width_par.csv.tpl'
echo python create_cw_para_tpl.py $rvh_tpl
python create_cw_para_tpl.py $rvh_tpl #$final_cat

#========================
# ./RavenInput/Petawawa.rvt
#========================
python update_rvt.py 'Petawawa'

# go back
cd ../

wait