#!/bin/bash
# set -x 
# trap read debug

expname=${1} #'0a'
ens_num=`printf '%02d\n' "${2}"`
trials=${3}
#=====================================
# cd into 
cd ./out/S${expname}_${ens_num}
#
echo "making ostIn.txt"
ProgramType='DDS' #ShuffledComplexEvolution
ObjectiveFunction='GCOP'
RandomSeed=$(od -N 4 -t uL -An /dev/urandom | tr -d " ") ##$RANDOM
MaxIterations=${trials}

# define cost function
CostFunction='NegKG_Q'
if [ ${expname} = "0a" ]; then
    CostFunction='NegKG_Q'
elif [[ ${expname} = "0b" || ${expname} = "0c" || ${expname} = "0d" || ${expname} = "0e" || ${expname} = "0f" || ${expname} = "0g" || ${expname} = "0h" ]]; then
    CostFunction='NegKG_Q_WL'
elif [[ ${expname} = "1a" || ${expname} = "1b" || ${expname} = "1c" || ${expname} = "1d" ||  ${expname} = "1e" ||  ${expname} = "1f" ||  ${expname} = "1g" ||  ${expname} = "1h" ||  ${expname} = "1i" ||  ${expname} = "1j" ||  ${expname} = "1k" ]]; then
    CostFunction='NegKGR2_Q_WA'
elif [ ${expname} = "2a" ]; then
    CostFunction='NegKGR2_Q_WL_WA'
else
    CostFunction='NegKG_Q_WL'
fi
# write ostIn.txt
# ostin=sys.argv[1]
# finalcat_hru_info=sys.argv[2]
# RavenDir=sys.argv[3]
# progType=sys.argv[4]    
# objFunc=sys.argv[5]
# RandomSeed=sys.argv[6]
# MaxIter=sys.argv[7]
# only_lake=int(sys.argv[8]) # True |    False --> only lake    observations or any    observation
# ObsTypes=sys.argv[9::]

ostIn='./ostIn.txt'
final_cat='./finalcat_hru_info_updated.csv'
RavenDir='./RavenInput'
only_lake_obs=1 # use only observations realted to Lake for calibrating lake parameters

python create_ostIn.py $ostIn $final_cat $RavenDir $ProgramType $ObjectiveFunction $RandomSeed $MaxIterations $only_lake_obs

rm -r ${ostIn}
# 0. 
cat >> ${ostIn} << EOF
ProgramType         $ProgramType
ObjectiveFunction   $ObjectiveFunction
ModelExecutable     ./Ost-RAVEN.sh
PreserveBestModel   ./save_best.sh
#OstrichWarmStart   yes

BeginExtraDirs
RavenInput
#best
EndExtraDirs

BeginFilePairs    
Petawawa.rvp.tpl;           Petawawa.rvp
Petawawa.rvh.tpl;           Petawawa.rvh
crest_width_par.csv.tpl;    crest_width_par.csv
Petawawa.rvc.tpl;           Petawawa.rvc

#can be multiple (.rvh, .rvi)
EndFilePairs

EOF

# 1.parameters
cat >> ${ostIn} << EOF
#Parameter Specification
BeginParams
#parameter	               init.	    low	      high	      tx_in	 tx_ost	  tx_out	format

## SOIL
%D_FF%	                   0.1		    0.01	   0.2	        none	none	none # high 
%D_AT%	                   0.1		    0.01	   2	        none	none	none 
%MLT_F_Add%		           random	    0	       6	        none	none	none
%MIN_MLT_F%	               random	    1	       3	        none	none	none
# %HBV_MLT_A_C%	           random	    0.1	       1	        none	none	none
%Rfrez_F%	               random		0 	       4	        none	none	none
%WFPS%		               random	    0.9	       27	        none	none	none
%HydCond_FF%	           random	    10  	   1000	        none	none	none
%FC_FF%		               random	    0.1	       0.7	        none	none	none
%FC_AT%		               random	    0.1	       0.7	        none	none	none
%FC_BT%		               random	    0.5  	   0.99	        none	none	none
%MAX_BASEFLOW_RATE_FF%	   random	    10  	   1000	        none	none	none
%MAX_BASEFLOW_RATE_AT%	   random	    10  	   1000	        none	none	none
%MAX_BASEFLOW_RATE_BT%	   random	    10  	   1000	        none	none	none
%BASEFLOW_N_FF%            random       1.00E-01   4.00E+00     none    none    none
%BASEFLOW_N_AT%            random       1.00E-01   4.00E+00     none    none    none
%BASEFLOW_N_BT%            random       1.00E-01   8.00E+00     none    none    none
%Rain_Snow_T%	           random	    -2	       2	        none	none	none
%Rain_Snow_Delta%          random	    0	       6	        none	none	none
%MAX_PERC_RATE_FF%	       random	    10  	   1000	        none	none	none
%MAX_PERC_RATE_AT%	       random	    10  	   1000	        none	none	none
%MAX_CAP_RISE_RATE%	       random	    10  	   1000	        none	none	none

%MAX_CAPACITY%	           random	    0    	       5	        none	none	none
%MAX_SNOW_CAPACITY%	       random	    0  	           5	        none	none	none
%RAIN_ICEPT_PCT%	       random	    0.01  	       0.2	        none	none	none
%SNOW_ICEPT_PCT%	       random	    0.01  	       0.3	        none	none	none

##PET CORRECTION
%LAKE_PET_CORR%            random   0.5    1.5      none   none     none
%PET_CORRECTION%           random   0.5    1.5      none   none     none

EOF

# 1.1 Routing parameters [for all experiments]
cat >> ${ostIn} << EOF
## ROUTING
n_multi                    random   0.1     10      none   none     none  # manning's n
w_a0                       random   0.1     0.8      none   none     none
w_n0                       random   0.1     0.8      none   none     none

EOF

# 1.2 Routing parameters
if [[ ${expname} = "0b"  || ${expname} = "0d" || ${expname} = "0e" || ${expname} = "0f" || ${expname} = "0g" || ${expname} = "0h" ||  ${expname} = "1a" ]]; then
cat >> ${ostIn} << EOF
w_Cedar	                   random	0.1	100	none	none	none
w_Big_Trout	               random	0.1	100	none	none	none
w_Grand	                   random	0.1	100	none	none	none
w_Lavieille	               random	0.1	100	none	none	none
w_Misty	                   random	0.1	100	none	none	none
w_Animoosh	               random	0.1	100	none	none	none
w_Traverse	               random	0.1	100	none	none	none
w_Burntroot	               random	0.1	100	none	none	none
w_La_Muir	               random	0.1	100	none	none	none
w_Narrowbag	               random	0.1	100	none	none	none
w_Little_Cauchon	       random	0.1	100	none	none	none
w_Hogan	                   random	0.1	100	none	none	none
w_North_Depot	           random	0.1	100	none	none	none
w_Radiant                  random	0.1	100	none	none	none
w_Loontail	               random	0.1	100	none	none	none

EOF
elif [[ ${expname} = "1b" ]]; then
cat >> ${ostIn} << EOF
w_Cedar	                   random	0.1	100	none	none	none
w_Big_Trout	               random	0.1	100	none	none	none
w_Misty	                   random	0.1	100	none	none	none
w_Traverse	               random	0.1	100	none	none	none
w_Narrowbag	               random	0.1	100	none	none	none
w_Radiant                  random	0.1	100	none	none	none

EOF
elif [[ ${expname} = "1d" ]]; then
cat >> ${ostIn} << EOF
w_Cedar	                   random	90	110	none	none	none
w_Big_Trout	               random	25	40	none	none	none
w_Grand	                   random	35	55	none	none	none
w_Lavieille	               random	30	50	none	none	none
w_Misty	                   random	1	10	none	none	none
w_Animoosh	               random	1	25	none	none	none
w_Traverse	               random	30	50	none	none	none
w_Burntroot	               random	20	30	none	none	none
w_La_Muir	               random	1	10	none	none	none
w_Narrowbag	               random	1	20	none	none	none
w_Little_Cauchon	       random	15	35	none	none	none
w_Hogan	                   random	10	30	none	none	none
w_North_Depot	           random	20	30	none	none	none
w_Radiant                  random	30	40	none	none	none
w_Loontail	               random	1	10	none	none	none

EOF
elif [[ ${expname} = "1e" ]]; then
cat >> ${ostIn} << EOF
w_Cedar	                   random	90	110	none	none	none
w_Big_Trout	               random	25	40	none	none	none
w_Grand	                   random	35	55	none	none	none
w_Lavieille	               random	30	50	none	none	none
w_Animoosh	               random	1	25	none	none	none
w_Traverse	               random	30	50	none	none	none
w_Burntroot	               random	20	30	none	none	none
w_La_Muir	               random	1	10	none	none	none
w_Little_Cauchon	       random	15	35	none	none	none
w_Hogan	                   random	10	30	none	none	none
w_Radiant                  random	30	40	none	none	none

EOF
elif [[ ${expname} = "1f" ]]; then
cat >> ${ostIn} << EOF
w_Cedar	                   random	90	110	none	none	none
w_Big_Trout	               random	25	40	none	none	none
w_Grand	                   random	35	55	none	none	none
w_Lavieille	               random	30	50	none	none	none
w_Misty	                   random	1	10	none	none	none
w_Animoosh	               random	1	25	none	none	none
w_Traverse	               random	30	50	none	none	none
w_Burntroot	               random	20	30	none	none	none
w_La_Muir	               random	1	10	none	none	none
w_Little_Cauchon	       random	15	35	none	none	none
w_Hogan	                   random	10	30	none	none	none
w_North_Depot	           random	20	30	none	none	none
w_Radiant                  random	30	40	none	none	none
w_Loontail	               random	1	10	none	none	none

EOF
elif [[ ${expname} = "1g" ]]; then
cat >> ${ostIn} << EOF
w_Traverse	               random	30	50	none	none	none
w_Narrowbag	               random	1	20	none	none	none
w_North_Depot	           random	20	30	none	none	none
w_Burntroot	               random	20	30	none	none	none
w_Radiant                  random	30	40	none	none	none

EOF
elif [[ ${expname} = "1h" ]]; then
cat >> ${ostIn} << EOF
w_Cedar	                   random	90	110	none	none	none
w_Big_Trout	               random	25	40	none	none	none
w_Grand	                   random	35	55	none	none	none
w_Lavieille	               random	30	50	none	none	none
w_Misty	                   random	1	10	none	none	none
w_Traverse	               random	30	50	none	none	none
w_Burntroot	               random	20	30	none	none	none
w_Little_Cauchon	       random	15	35	none	none	none
w_North_Depot	           random	20	30	none	none	none
w_Radiant                  random	30	40	none	none	none
w_Narrowbag	               random	1	20	none	none	none

EOF
elif [[ ${expname} = "1i" ]]; then
cat >> ${ostIn} << EOF
w_Cedar	                   random	90	110	none	none	none
w_Big_Trout	               random	25	40	none	none	none
w_Grand	                   random	35	55	none	none	none
w_Lavieille	               random	30	50	none	none	none
w_Animoosh	               random	1	25	none	none	none
w_Traverse	               random	30	50	none	none	none
w_Burntroot	               random	20	30	none	none	none
w_La_Muir	               random	1	10	none	none	none
w_Little_Cauchon	       random	15	35	none	none	none
w_Hogan	                   random	10	30	none	none	none
w_Radiant                  random	30	40	none	none	none
w_Narrowbag	               random	1	20	none	none	none

EOF
elif [[ ${expname} = "1j" ]]; then
cat >> ${ostIn} << EOF
w_Cedar	                   random	90	110	none	none	none
w_Big_Trout	               random	25	40	none	none	none
w_Grand	                   random	35	55	none	none	none
w_Lavieille	               random	30	50	none	none	none
w_Traverse	               random	30	50	none	none	none
w_Burntroot	               random	20	30	none	none	none
w_Little_Cauchon	       random	15	35	none	none	none
w_Radiant                  random	30	40	none	none	none

EOF
elif [[ ${expname} = "1k" ]]; then
cat >> ${ostIn} << EOF
w_Cedar	                   random	90	110	none	none	none
w_Big_Trout	               random	25	40	none	none	none
w_Grand	                   random	35	55	none	none	none
w_Lavieille	               random	30	50	none	none	none
w_Traverse	               random	30	50	none	none	none
w_Burntroot	               random	20	30	none	none	none
w_Little_Cauchon	       random	15	35	none	none	none
w_Radiant                  random	30	40	none	none	none
w_Narrowbag	               random	1	20	none	none	none

EOF
fi

# additonal variables
if [ ${expname} = "0f" ]; then
cat >> ${ostIn} << EOF
# Runoff
%AvgAnnualRunoff%         random	100	1000	none	none	none

EOF
fi

# additonal variables for Diffusive Wave routing
if [[ ${expname} = "0g" || ${expname} = "0h" ]]; then
cat >> ${ostIn} << EOF
# Runoff
%AvgAnnualRunoff%         random	100	1000	none	none	none

# Routing
c_multi                   random	0.1	10	none	none	none # celerity
d_multi                   random	0.1	10	none	none	none # diffusivity

EOF
fi

cat >> ${ostIn} << EOF
EndParams
EOF

cat >> ${ostIn} << EOF
BeginTiedParams
# Xtied = (c1 * X) + c0
# --> c0 = 0.0
# --> c1 = 1.
#   
#Xtied = (c3 × X1 × X2) + (c2 × X2) + (c1 × X1) + c0
#<c3> <c2> <c1> <c0> <fmt>
%MLT_F%	       2 	%MLT_F_Add%      %MIN_MLT_F%     linear 0 1 1 0  free
%Ininc_Soil2%   1 	%FC_BT%                          linear 600 0  free

EndTiedParams

EOF

cat >> ${ostIn} << EOF
BeginResponseVars
  #name                                                         filename  keyword       line     col     token
  # KGE [Discharge]
  
EOF

cat >> ${ostIn} << EOF
  KG_02KB001                ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL         1       5        ','

EOF

# Experments use in-situ lake stage {S0}
if [[ ${expname} = "0b" ||  ${expname} = "0c" ||  ${expname} = "0d" || ${expname} = "0e" || ${expname} = "0f" || ${expname} = "0g" || ${expname} = "0h" ]]; then  
cat >> ${ostIn} << EOF
  # KGE deviation [Reservoir stages]
  KGD_Animoosh_497          ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL         2       6       ','
  KGD_Big_Trout_353         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL         3       6       ','
  KGD_Burntroot_390         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL         4       6       ','
  KGD_Cedar_857             ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL         5       6       ','
  KGD_Charles_659           ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL         6       6       ','
  KGD_Grand_1179            ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL         7       6       ','
  KGD_Hambone_62            ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL         8       6       ','
  KGD_Hogan_518             ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL         9       6       ','
  KGD_La_Muir_385           ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        10       6       ','
  KGD_Lilypond_44           ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        11       6       ','
  KGD_Little_Cauchon_754    ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        12       6       ','
  KGD_Loontail_136          ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        13       6       ','
  KGD_Misty_233             ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        14       6       ','
  KGD_Narrowbag_467         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        15       6       ','
  KGD_North_Depot_836       ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        16       6       ','
  KGD_Radiant_944           ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        17       6       ','
  KGD_Temberwolf_43         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        18       6       ','
  KGD_Traverse_1209         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        19       6       ','
  KGD_Lavieille_326         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        20       6       ','  

EOF
fi

# Experments use remotely-sensed lake area {S1}
if [[ ${expname} = "1a" ||  ${expname} = "1b" ||  ${expname} = "1c" ||  ${expname} = "1d" ||  ${expname} = "1e" ||  ${expname} = "1f" ||  ${expname} = "1g" ||  ${expname} = "1h" ||  ${expname} = "1i" ||  ${expname} = "1j" ||  ${expname} = "1k" ]]; then
cat >> ${ostIn} << EOF
  # R2 [Reservoir area]
  R2_Animoosh_497           ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        21       7       ','
  R2_Big_Trout_353          ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        22       7       ','
  R2_Burntroot_390          ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        23       7       ','
  R2_Cedar_857              ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        24       7       ','
  R2_Charles_659            ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        25       7       ','
  R2_Grand_1179             ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        26       7       ','
  R2_Hambone_62             ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        27       7       ','
  R2_Hogan_518              ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        28       7       ','
  R2_La_Muir_385            ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        29       7       ','
  R2_Lilypond_44            ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        30       7       ','
  R2_Little_Cauchon_754     ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        31       7       ','
  R2_Loontail_136           ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        32       7       ','
  R2_Misty_233              ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        33       7       ','
  R2_Narrowbag_467          ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        34       7       ','
  R2_North_Depot_836        ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        35       7       ','
  R2_Radiant_944            ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        36       7       ','
  R2_Temberwolf_43          ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        37       7       ','
  R2_Traverse_1209          ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        38       7       ','
  R2_Lavieille_326          ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        39       7       ','  

EOF
fi

cat >> ${ostIn} << EOF
EndResponseVars 

EOF

# 2.objective function
cat >> ${ostIn} << EOF
BeginTiedRespVars
    # <name1> <np1> <pname1,1> <pname1,2> ... <pname1,np1> <type1> <type_data1>
EOF

# Outlet only
cat >> ${ostIn} << EOF
    NegKG_Q              1   KG_02KB001  wsum -1.00
EOF

# Outlet + Lake stage
if [[ ${expname} = "0b" || ${expname} = "0c" || ${expname} = "0d" || ${expname} = "0e" || ${expname} = "0f" || ${expname} = "0g" || ${expname} = "0h" ]]; then
cat >> ${ostIn} << EOF
    NegKGD_LAKE_WL1      7   KGD_Animoosh_497  KGD_Loontail_136  KGD_Narrowbag_467  KGD_Lavieille_326 KGD_Hogan_518  KGD_Big_Trout_353 KGD_Burntroot_390 wsum -1 -1 -1 -1 -1 -1 -1
    NegKGD_LAKE_WL2      8   KGD_Cedar_857 KGD_Grand_1179 KGD_La_Muir_385 KGD_Little_Cauchon_754 KGD_Misty_233 KGD_North_Depot_836 KGD_Radiant_944 KGD_Traverse_1209 wsum -1 -1 -1 -1 -1 -1 -1 -1
    NegKGD_LAKE_WL       2   NegKGD_LAKE_WL1 NegKGD_LAKE_WL2  wsum 1 1

EOF
fi

# Outlet + Lake area [15]
if [[ ${expname} = "1a" || ${expname} = "1c" ||  ${expname} = "1d" ]]; then
cat >> ${ostIn} << EOF
    NegR2_LAKE_WA1      7   R2_Animoosh_497  R2_Loontail_136  R2_Narrowbag_467  R2_Lavieille_326 R2_Hogan_518  R2_Big_Trout_353 R2_Burntroot_390 wsum -1 -1 -1 -1 -1 -1 -1
    NegR2_LAKE_WA2      8   R2_Cedar_857 R2_Grand_1179 R2_La_Muir_385 R2_Little_Cauchon_754 R2_Misty_233 R2_North_Depot_836 R2_Radiant_944 R2_Traverse_1209 wsum -1 -1 -1 -1 -1 -1 -1 -1 -1
    NegR2_LAKE_WA       2   NegR2_LAKE_WA1 NegR2_LAKE_WA2 wsum 1 1

EOF

# Outlet + Lake area [6 {R2> 0.6}]
elif [ ${expname} = "1b" ]; then
cat >> ${ostIn} << EOF
    NegR2_LAKE_WA       6   R2_Narrowbag_467 R2_Grand_1179 R2_Radiant_944 R2_Misty_233 R2_Traverse_1209 R2_Big_Trout_353 wsum -1 -1 -1 -1 -1 -1

EOF

# Outlet + Lake area [11]
elif [ ${expname} = "1e" ]; then
cat >> ${ostIn} << EOF
    NegR2_LAKE_WA1      5   R2_Animoosh_497  R2_Lavieille_326 R2_Hogan_518  R2_Big_Trout_353 R2_Burntroot_390 wsum -1 -1 -1 -1 -1
    NegR2_LAKE_WA2      6   R2_Cedar_857 R2_Grand_1179 R2_La_Muir_385 R2_Little_Cauchon_754 R2_Radiant_944 R2_Traverse_1209 wsum -1 -1 -1 -1 -1 -1
    NegR2_LAKE_WA       2   NegR2_LAKE_WA1 NegR2_LAKE_WA2 wsum 1 1

EOF

# Outlet + Lake area [14]
elif [ ${expname} = "1f" ]; then
cat >> ${ostIn} << EOF
    NegR2_LAKE_WA1      6   R2_Animoosh_497  R2_Loontail_136 R2_Lavieille_326 R2_Hogan_518  R2_Big_Trout_353 R2_Burntroot_390 wsum -1 -1 -1 -1 -1 -1
    NegR2_LAKE_WA2      8   R2_Cedar_857 R2_Grand_1179 R2_La_Muir_385 R2_Little_Cauchon_754 R2_Misty_233 R2_North_Depot_836 R2_Radiant_944 R2_Traverse_1209 wsum -1 -1 -1 -1 -1 -1 -1 -1 -1
    NegR2_LAKE_WA       2   NegR2_LAKE_WA1 NegR2_LAKE_WA2 wsum 1 1

EOF

# Outlet + Lake area [5]
elif [ ${expname} = "1g" ]; then
cat >> ${ostIn} << EOF
    NegR2_LAKE_WA       5   R2_Burntroot_390 R2_Radiant_944 R2_Traverse_1209 R2_Narrowbag_467 R2_North_Depot_836 wsum -1 -1 -1 -1 -1

EOF

# Outlet + Lake area [14]
elif [ ${expname} = "1h" ]; then
cat >> ${ostIn} << EOF
    NegR2_LAKE_WA1      5   R2_Burntroot_390 R2_Radiant_944 R2_Traverse_1209 R2_Narrowbag_467 R2_North_Depot_836 wsum -1 -1 -1 -1 -1 -1
    NegR2_LAKE_WA2      6   R2_Cedar_857 R2_Grand_1179 R2_Little_Cauchon_754 R2_Misty_233 R2_Big_Trout_353 R2_Lavieille_326 wsum -1 -1 -1 -1 -1 -1
    NegR2_LAKE_WA       2   NegR2_LAKE_WA1 NegR2_LAKE_WA2 wsum 1 1

EOF

# Outlet + Lake area [12]
elif [ ${expname} = "1i" ]; then
cat >> ${ostIn} << EOF
    NegR2_LAKE_WA1      6   R2_Animoosh_497  R2_Lavieille_326 R2_Hogan_518  R2_Big_Trout_353 R2_Burntroot_390 R2_Narrowbag_467 wsum -1 -1 -1 -1 -1 -1
    NegR2_LAKE_WA2      6   R2_Cedar_857 R2_Grand_1179 R2_La_Muir_385 R2_Little_Cauchon_754 R2_Radiant_944 R2_Traverse_1209 wsum -1 -1 -1 -1 -1 -1
    NegR2_LAKE_WA       2   NegR2_LAKE_WA1 NegR2_LAKE_WA2 wsum 1 1

EOF

# Outlet + Lake area [9]
elif [ ${expname} = "1j" ]; then
cat >> ${ostIn} << EOF
    NegR2_LAKE_WA1      4   R2_Lavieille_326  R2_Big_Trout_353 R2_Burntroot_390 R2_Narrowbag_467 wsum -1 -1 -1 -1
    NegR2_LAKE_WA2      5   R2_Cedar_857 R2_Grand_1179 R2_Little_Cauchon_754 R2_Radiant_944 R2_Traverse_1209 wsum -1 -1 -1 -1 -1
    NegR2_LAKE_WA       2   NegR2_LAKE_WA1 NegR2_LAKE_WA2 wsum 1 1

EOF

# Outlet + Lake area [10]
elif [ ${expname} = "1k" ]; then
cat >> ${ostIn} << EOF
    NegR2_LAKE_WA1      5   R2_Lavieille_326  R2_Big_Trout_353 R2_Burntroot_390 R2_Narrowbag_467 R2_Narrowbag_467 wsum -1 -1 -1 -1 -1
    NegR2_LAKE_WA2      5   R2_Cedar_857 R2_Grand_1179 R2_Little_Cauchon_754 R2_Radiant_944 R2_Traverse_1209 wsum -1 -1 -1 -1 -1
    NegR2_LAKE_WA       2   NegR2_LAKE_WA1 NegR2_LAKE_WA2 wsum 1 1

EOF
fi

# combination of objective function {Q + WL[15]}
if [[ ${expname} = "0b" || ${expname} = "0c" || ${expname} = "0d" || ${expname} = "0e" || ${expname} = "0f" || ${expname} = "0g" || ${expname} = "0h" ]]; then
cat >> ${ostIn} << EOF  
    # Q + WL(15)
    NegKG_Q_WL           2   NegKG_Q NegKGD_LAKE_WL wsum 1.00 0.066

EOF
# combination of objective function {Q + WA [15]}
elif [[ ${expname} = "1a" || ${expname} = "1c" ||  ${expname} = "1d" ]]; then
cat >> ${ostIn} << EOF  
    # Q + WA(15)
    NegKGR2_Q_WA        2   NegKG_Q NegR2_LAKE_WA wsum 1.00 0.066 

EOF
# combination of objective function {Q + WA [6]}
elif [ ${expname} = "1b" ]; then
cat >> ${ostIn} << EOF  
    # Q + WA(6) 
    NegKGR2_Q_WA        2   NegKG_Q NegR2_LAKE_WA wsum 1.00 0.166 

EOF
# combination of objective function {Q + WA [11]}
elif [ ${expname} = "1e" ]; then
cat >> ${ostIn} << EOF  
    # Q + WA(11) 
    NegKGR2_Q_WA        2   NegKG_Q NegR2_LAKE_WA wsum 1.00 0.090 

EOF
# combination of objective function {Q + WA [14]}
elif [ ${expname} = "1f" ]; then
cat >> ${ostIn} << EOF  
    # Q + WA(14) 
    NegKGR2_Q_WA        2   NegKG_Q NegR2_LAKE_WA wsum 1.00 0.071 
EOF
# combination of objective function {Q + WA [5]}
elif [ ${expname} = "1g" ]; then
cat >> ${ostIn} << EOF  
    # Q + WA(5) 
    NegKGR2_Q_WA        2   NegKG_Q NegR2_LAKE_WA wsum 1.00 0.200
EOF
# combination of objective function {Q + WA [11]}
elif [ ${expname} = "1h" ]; then
cat >> ${ostIn} << EOF  
    # Q + WA(11) 
    NegKGR2_Q_WA        2   NegKG_Q NegR2_LAKE_WA wsum 1.00 0.090  
EOF
# combination of objective function {Q + WA [12]}
elif [ ${expname} = "1i" ]; then
cat >> ${ostIn} << EOF  
    # Q + WA(12) 
    NegKGR2_Q_WA        2   NegKG_Q NegR2_LAKE_WA wsum 1.00 0.083 
EOF
# combination of objective function {Q + WA [8]}
elif [ ${expname} = "1j" ]; then
cat >> ${ostIn} << EOF  
    # Q + WA(8) 
    NegKGR2_Q_WA        2   NegKG_Q NegR2_LAKE_WA wsum 1.00 0.125
EOF
# combination of objective function {Q + WA [9]}
elif [ ${expname} = "1k" ]; then
cat >> ${ostIn} << EOF  
    # Q + WA(9) 
    NegKGR2_Q_WA        2   NegKG_Q NegR2_LAKE_WA wsum 1.00 0.111 
EOF
# combination of objective function {Q + WL + WA}
elif [${expname} = "2a" ]; then
cat >> ${ostIn} << EOF  
    # Q + WL + WA  
    NegKGR2_Q_WL_WA     3   NegKG_Q NegKGD_LAKE_WL NegR2_LAKE_WA wsum 1.00 0.066 0.066

EOF
fi

cat >> ${ostIn} << EOF  
EndTiedRespVars

EOF

cat >> ${ostIn} << EOF
RandomSeed    $RandomSeed 
EOF

cat >> ${ostIn} << EOF
BeginGCOP
    CostFunction  $CostFunction
    PenaltyFunction APM
EndGCOP

EOF

cat >> ${ostIn} << EOF
BeginDDSAlg
    PerturbationValue 0.20
    MaxIterations $MaxIterations
    UseRandomParamValues
#        # UseInitialParamValues
#        # above intializes DDS to parameter values IN the initial model input files
EndDDSAlg

EOF


#'pwd'
echo "Run Ostrich"

# run Ostrich
./Ostrich

#'pwd'

cd ../..

wait