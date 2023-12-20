#!/bin/bash

expname=${1} #'0a'
ens_num=`printf '%02d\n' "${2}"`
trials=${3}
#=====================================
echo $ens_num
# make experiment pertunation directory
echo "making folder --> ./out/S${expname}_${ens_num}"
mkdir -p ./out/S${expname}_${ens_num}
# cd into 
cd ./out/S${expname}_${ens_num}

# copy main Ostrich + Raven model calibation pacakage
cp -r ../../OstrichRaven/* . 

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
elif [ ${expname} = "0b" ]; then
    CostFunction='NegKG_Q_WL'
elif [ ${expname} = "1a" ]; then
    CostFunction='NegKGSRC_Q_WA'
elif [ ${expname} = "2a" ]; then
    CostFunction='NegKGSRC_Q_WL_WA'
fi
# write ostIn.txt
ostIn='ostIn.txt'
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
#parameter	               init.	low	high	tx_in	tx_ost	tx_out	format

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

# 1.1 Routing parameters
cat >> ${ostIn} << EOF
## ROUTING
n_multi                    random   0.1     10      none   none     none
w_a0                       random   0.1     0.8      none   none     none
w_n0                       random   0.1     0.8      none   none     none

EOF

# 1.2 Routing parameters
if [[ ${expname} = "0b"  ||  ${expname} = "1a" ]]; then
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


BeginResponseVars
  #name                                                         filename  keyword       line     col     token
  # KGE [Discharge]
  KG                        ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL         1       5        ','
  
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

  # Spearman Ranked Correlation [Reservoir area]
  SRC_Animoosh_497          ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        21       8       ','
  SRC_Big_Trout_353         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        22       8       ','
  SRC_Burntroot_390         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        23       8       ','
  SRC_Cedar_857             ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        24       8       ','
  SRC_Charles_659           ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        25       8       ','
  SRC_Grand_1179            ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        26       8       ','
  SRC_Hambone_62            ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        27       8       ','
  SRC_Hogan_518             ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        28       8       ','
  SRC_La_Muir_385           ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        29       8       ','
  SRC_Lilypond_44           ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        30       8       ','
  SRC_Little_Cauchon_754    ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        31       8       ','
  SRC_Loontail_136          ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        32       8       ','
  SRC_Misty_233             ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        33       8       ','
  SRC_Narrowbag_467         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        34       8       ','
  SRC_North_Depot_836       ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        35       8       ','
  SRC_Radiant_944           ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        36       8       ','
  SRC_Temberwolf_43         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        37       8       ','
  SRC_Traverse_1209         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        38       8       ','
  SRC_Lavieille_326         ./RavenInput/output/Petawawa_Diagnostics.csv; OST_NULL        39       8       ','  

EndResponseVars 

BeginTiedRespVars
    # <name1> <np1> <pname1,1> <pname1,2> ... <pname1,np1> <type1> <type_data1>
    NegKG_Q              1   KG  wsum -1.00

    NegKGD_LAKE_WL1      7   KGD_Animoosh_497  KGD_Loontail_136  KGD_Narrowbag_467  KGD_Lavieille_326 KGD_Hogan_518  KGD_Big_Trout_353 KGD_Burntroot_390 wsum -1 -1 -1 -1 -1 -1 -1
    NegKGD_LAKE_WL2      8   KGD_Cedar_857 KGD_Grand_1179 KGD_La_Muir_385 KGD_Little_Cauchon_754 KGD_Misty_233 KGD_North_Depot_836 KGD_Radiant_944 KGD_Traverse_1209 wsum -1 -1 -1 -1 -1 -1 -1 -1
    
    NegSRC_LAKE_WA1      7   SRC_Animoosh_497  SRC_Loontail_136  SRC_Narrowbag_467  SRC_Lavieille_326 SRC_Hogan_518  SRC_Big_Trout_353 SRC_Burntroot_390 wsum -1 -1 -1 -1 -1 -1 -1
    NegSRC_LAKE_WA2      8   SRC_Cedar_857 SRC_Grand_1179 SRC_La_Muir_385 SRC_Little_Cauchon_754 SRC_Misty_233 SRC_North_Depot_836 SRC_Radiant_944 SRC_Traverse_1209 wsum -1 -1 -1 -1 -1 -1 -1 -1 -1
  
    NegKGD_LAKE_WL       2   NegKGD_LAKE_WL1 NegKGD_LAKE_WL2  wsum 1 1

    NegSRC_LAKE_WA       2   NegSRC_LAKE_WA1 NegSRC_LAKE_WA2 wsum 1 1

    # Q + WL
    NegKG_Q_WL           2   NegKG_Q NegKGD_LAKE_WL wsum 1.00 0.066

    # Q + WA 
    NegKGSRC_Q_WA        2   NegKG_Q NegSRC_LAKE_WA wsum 1.00 0.066 

    # Q + WL + WA  
    NegKGSRC_Q_WL_WA     3   NegKG_Q NegKGD_LAKE_WL NegSRC_LAKE_WA wsum 1.00 0.066 0.066
EndTiedRespVars

RandomSeed    $RandomSeed 

BeginGCOP
    CostFunction  $CostFunction
    PenaltyFunction APM
EndGCOP




BeginDDSAlg
    PerturbationValue 0.20
    MaxIterations $MaxIterations
    UseRandomParamValues
#        # UseInitialParamValues
#        # above intializes DDS to parameter values IN the initial model input files
EndDDSAlg
EOF

# run Ostrich
./Ostrich

'pwd'

cd ../..

wait 