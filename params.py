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
    # return 'NegKG_Q'                        # Q           ** this should be consistent with ObsTypes()
    # return 'NegKG_Q_WL'                     # Q + WL
    return 'NegKGR2_Q_WA'                   # Q + WA
    # return 'NegKGR2_Q_WL_WA'                # Q + WL + WA
#--------------------------------------
def ObsTypes():
    # return ['Obs_SF_IS', 'Obs_WL_IS']       # observations types 
    return ['Obs_SF_IS', 'Obs_WA_RS1']
                                            # SF - stream flow
                                            # WL - water level
                                            # WA - water area
                                            # IS - in situ
                                            # RA - remote sensing
#--------------------------------------
def ExpName():                              # Experiment name
    return 'S1a'
    # return 'E0b'
#--------------------------------------
def MaxIteration():                        # Calibration budget
    return 1000
#--------------------------------------
def RunType():
    return 'Init'
    # return 'Restart'