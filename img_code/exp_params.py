def get_final_cat_colname():
    colname={
        "E0a":"Obs_SF_IS",
        "E0b":"Obs_WL_IS",
        "S0a":"Obs_WL_IS",
        "S0b":"Obs_WL_IS",
        "S0c":"Obs_SF_IS",
        "S1d":"Obs_WA_RS3",
        "S1f":"Obs_WA_RS4",
        "S1h":"Obs_WA_RS5",
        "S1i":"Obs_WA_RS4",
        "S1z":"Obs_WA_RS4",
        "V0a":"Obs_SF_SY",
        "V1a":"Obs_WA_SY1",
        "V1b":"Obs_WA_SY1",
        "V1c":"Obs_WA_SY1",
        "V1d":"Obs_WA_SY1",
        "V1e":"Obs_WA_SY0",
        "V2a":"Obs_WA_SY1",
        "V2b":"Obs_WA_SY1",
        "V2c":"Obs_WA_SY1",
        "V2d":"Obs_WA_SY1",
        "V2e":"Obs_WA_SY0",
        "V3d":"Obs_WA_SY1",
        "V4d":"Obs_WA_SY1",
        "V4e":"Obs_WA_SY0",
    }
    return colname

def get_exp_explain():
    char_explain={
        "E0a":"($Q$ [$KGE$])",
        "E0b":"($Q$ [$KGE$])+ $WL$ [$KGED$])",
        "S0a":"($Q$ [$KGE$] + $WSA$ [$KGED$])",
        "S0b":"($Q$ [$KGE$] + $WSA$ [$KGED$])",
        "S0c":"($Q$ [$KGE$] + $WSA$ [$KGED$])",
        "S1d":"($Q$ [$KGE$] + $WSA$ [$KGED$])",
        "S1f":"($Q$ [$KGE$] + $WSA$ [$KGED$])",
        "S1h":"($Q$ [$KGE$] + $WSA$ [$KGED$])",
        "S1i":"($Q$ [$KGE$] + $WSA$ [$KGED$])",
        "S1z":"($Q$ [$KGE$] + $WSA$ [$KGED$])",
        "V0a":"($vQ$ [$KGE$])",
        "V1a":"($vQ$ [$KGE$] + $w/o$ $error$ $vWSA$[$18$ $Lakes$] ($daily$) [$KGED$])",
        "V1b":"($vQ$ [$KGE$] + $w/o$ $error$ $vWSA$[$18$ $Lakes$] ($per$ $16-day$) [$KGED$])",
        "V1c":"($vQ$ [$KGE$] + $w/$ $error$ $vWSA$[$18$ $Lakes$] ($daily$) [$KGED$])",
        "V1d":"($vQ$ [$KGE$] + $w/$ $error$ $vWSA$[$18$ $Lakes$] ($per$ $16-day$) [$KGED$])",
        "V1e":"($vQ$ [$KGE$] + $w/$ $error$ $vWSA$[$All$ $Lakes$] ($per$ $16-day$) [$KGED$])",
        "V2a":"($w/o$ $error$ $vWSA$[$18$ $Lakes$] ($daily$) [$KGED$])",
        "V2b":"($w/o$ $error$ $vWSA$[$18$ $Lakes$] ($per$ $16-day$) [$KGED$])",
        "V2c":"($w/$ $error$ $vWSA$[$18$ $Lakes$] ($daily$) [$KGED$])",
        "V2d":"($w/$ $error$ $vWSA$[$18$ $Lakes$] ($per$ $16-day$) [$KGED$])",
        "V2e":"($w/$ $error$ $vWSA$[$All$ $Lakes$] ($per$ $16-day$) [$KGED$])",
        "V3d":"($w/$ $error$ $vWSA$[$18$ $Lakes$] ($per$ $16-day$) [$KGED$]+Q-constrain)",
        "V4d":"($w/$ $error$ $vWSA$[$18$ $Lakes$] ($per$ $16-day$) [$KGE$])",
        "V4e":"($w/$ $error$ $vWSA$[$All$ $Lakes$] ($per$ $16-day$) [$KGE$])",
    }
    return char_explain
def get_paraList():
    para_list={
        'vegitation_para': ['%RAIN_ICEPT_PCT%','%SNOW_ICEPT_PCT%','%MAX_CAPACITY%',
        '%MAX_SNOW_CAPACITY%'],
        'landuse_para': ['%Rfrez_F%','%MLT_F_Add%','%MIN_MLT_F%'],
        'soil_para': ['%HydCond_FF%','%WFPS%','%PET_CORRECTION%','%FC_FF%','%FC_AT%','%FC_BT%'],
        'baseflow_para': ['%MAX_PERC_RATE_FF%','%MAX_PERC_RATE_AT%','%MAX_BASEFLOW_RATE_FF%',
        '%MAX_BASEFLOW_RATE_AT%','%MAX_BASEFLOW_RATE_BT%','%MAX_CAP_RISE_RATE%',
        '%BASEFLOW_N_FF%','%BASEFLOW_N_AT%','%BASEFLOW_N_BT%','%FC_FF%','%FC_AT%','%FC_BT%'],
        'routing_para': ['n_multi', 'q_multi', 'k_multi']
    }
    return para_list