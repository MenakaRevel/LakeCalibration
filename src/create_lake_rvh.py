'''
create_lake_rvh.py: create Lakes.rvh using w_{Hylakid} for observed lakes and CW=a*DA**n
--> in basin basinmaker: 
    BkfWidth=max(7.2 * q ** 0.5,min_bkf_width)
    q=k*DA**c

'''
import pandas as pd 
import numpy as np 
import os
import params as pm

def WriteStringToFile(Out_String, File_Path, WriteMethod):
    """Write String to a file

    Function that used to write Out_String to a file located at the File_Path.

    Parameters
    ----------
    Out_String            : string
        The string that will be writed to the file located at File_Path
    File_Path             : string
        Path and filename of file that will be modified or created
    WriteMethod           : {'a','w'}
        If WriteMethod = "w", a new file will be created at the File_Path
        If WriteMethod = "a", the Out_String will be added to exist file

    Notes
    ------
        The file located at the File_Path will be modified or created

    Returns
    -------
        None

    Examples
    --------
    >>> from WriteRavenInputs import WriteStringToFile
    >>> Out_String = 'sometest at line 1\n some test at line 2\n some test at line 3\n'
    >>> File_Path  = 'C:/Path_to_the_Flie_with_file_name'
    >>> WriteStringToFile(Out_String = Out_String,File_Path = File_Path,WriteMethod = 'w')

    """

    if os.path.exists(
        File_Path
    ):  ### if file exist, we can either modify or overwrite it
        with open(File_Path, WriteMethod) as f:
            f.write(Out_String)
    else:  ## create a new file anyway, since file did not exist
        with open(File_Path, "w") as f:
            f.write(Out_String)



def Generate_Raven_Lake_rvh_String(catinfo, Raveinputsfolder, Model_Name,lake_out_flow_method,lake_par_info,obs_gauge,model_structure):
    """Generate string of raven lake rvh input

    Function that used to generate the content for
    Raven lake definition Model_Name_Lake.rvh input file.

    Parameters
    ----------
    catinfo              : DataFrame
        A dataframe includes all attribute for each HRU
        read from polygon shpfile generated by the toolbox
    Raveinputsfolder     : string
        Folder path and name that save outputs

    Notes
    ------
    None

    See Also
    --------
    None

    Returns
    -------
    Lake_rvh_string       : string
        It is the string that contains the content that will be used to
        to define lake parameters for all lakes in
        Raven lake rvh input file format.
    Lake_rvh_file_path    : string
        It is the string that define the path of
        the raven channel rvp input file.

    Examples
    --------
    >>> from WriteRavenInputs import Generate_Raven_Lake_rvh_String
    >>> outFolderraven    = 'c:/path_to_the_raven_input_folder/'
    >>> DataFolder = "C:/Path_to_foldr_of_example_dataset_provided_in_Github_wiki/"
    >>> Model_Folder     = os.path.join(DataFolder,'Model')
    >>> Raveinputsfolder = os.path.join(Model_Folder,'RavenInput')
    >>> finalcatchpath = os.path.join(DataFolder,'finalcat_hru_info.shp')
    >>> tempinfo = Dbf5(finalcatchpath[:-3] + "dbf")
    >>> ncatinfo = tempinfo.to_dataframe()
    >>> Model_Name = 'test'
    >>> ncatinfo2 = ncatinfo.drop_duplicates('HRU_ID', keep='first')
    >>> Lake_rvh_string, Lake_rvh_file_path= Generate_Raven_Lake_rvh_String(ncatinfo2,Raveinputsfolder,lenThres,Model_Name)

    """
    Lake_rvh_file_path = os.path.join(Raveinputsfolder, "Lakes.rvh")
    Lake_rvh_string_list = []
    Lake_rvh_string_list.append("#----------------------------------------------")
    Lake_rvh_string_list.append("# This is a Raven lake rvh file generated")
    Lake_rvh_string_list.append("# by BasinMaker v2.0")
    Lake_rvh_string_list.append("#----------------------------------------------")

    for i in range(0, len(catinfo.index)):
        if catinfo.iloc[i]["HRU_IsLake"] > 0:  ## lake hru
            lakeid = int(catinfo.iloc[i]["HyLakeId"])
            catid = catinfo.iloc[i]["SubId"]
            A = catinfo.iloc[i]["HRU_Area"]  ### in meters
            h0 = catinfo.iloc[i]["LakeDepth"]  ## m
            WeirCoe = 0.6
            hruid = int(catinfo.iloc[i]["HRU_ID"])
            
            has_obs = catinfo.iloc[i]["Has_Gauge"]  ##3 m
            da_km = catinfo.iloc[i]["DrainArea"]/1000/1000
            # w_a = lake_par_info['a'].values[0]
            # w_n = lake_par_info['n'].values[0]
            # Crewd = w_a*(da_km**w_n)
            # obs_nm = catinfo.iloc[i]["Obs_NM"]

            # updated by Menaka@UWaterloo on 2024/04/30
            # according to the BasinMaker software to get the CWi
            # # w_a = 7.2
            # # w_n = 0.5
            # # q = catinfo.iloc[i]["Q_mean"]
            
            Crewd = catinfo.iloc[i]["BkfWidth"]

            obs_nm = catinfo.iloc[i]["HyLakeId"]
            
            # updated by Menaka@UWaterloo on 2024/04/30
            # no longer model_structure is needed
            if obs_nm in obs_gauge:
                Crewd = lake_par_info[obs_nm].values[0]

            # if model_structure == 'S1':

            #     if obs_nm in obs_gauge:
            #         Crewd = lake_par_info[obs_nm].values[0]
            #     # if catid == 921:
            #     #     Crewd = lake_par_info['02KB001'].values[0]

            # elif model_structure == 'S2':
            #     dep1 = lake_par_info['depth1'].values[0]
            #     dep2 = dep1 + lake_par_info['depadd'].values[0]
                
            #     if h0 <= dep1:
            #         w_a1 = lake_par_info['a'].values[0]
            #         w_n1 = lake_par_info['n'].values[0]  
            #         Crewd = w_a1*(da_km**w_n1)
            #     elif h0 > dep1 and h0 <= dep2:
            #         w_a2 = lake_par_info['a2'].values[0]
            #         w_n2 = lake_par_info['n2'].values[0]  
            #         Crewd = w_a2*(da_km**w_n2)
            #     if h0 > dep2:
            #         w_a3 = lake_par_info['a3'].values[0]
            #         w_n3 = lake_par_info['n3'].values[0]  
            #         Crewd = w_a3*(da_km**w_n3)     
                
            if has_obs < 1 or lake_out_flow_method == 'broad_crest':
                Lake_rvh_string_list.append(
                    "#############################################"
                )  # f2.write("#############################################"+"\n")
                Lake_rvh_string_list.append(
                    "# New Lake starts"
                )  # f2.write("###New Lake starts"+"\n")
                Lake_rvh_string_list.append(
                    "#############################################"
                )  # f2.write("#############################################"+"\n")
                ######write lake information to file
                Lake_rvh_string_list.append(
                    ":Reservoir" + "   Lake_" + str(int(lakeid))
                )  # f2.write(":Reservoir"+ "   Lake_"+ str(int(lakeid))+ "   ######## " +"\n")
                Lake_rvh_string_list.append(
                    "  :SubBasinID  " + str(int(catid))
                )  # f2.write("  :SubBasinID  "+str(int(catid))+ "\n")
                Lake_rvh_string_list.append(
                    "  :HRUID   " + str(int(hruid))
                )  # f2.write("  :HRUID   "+str(int(hruid))+ "\n")
                Lake_rvh_string_list.append(
                    "  :Type RESROUTE_STANDARD   "
                )  # f2.write("  :Type RESROUTE_STANDARD   "+"\n")
                Lake_rvh_string_list.append(
                    "  :WeirCoefficient  " + str(WeirCoe)
                )  # f2.write("  :WeirCoefficient  "+str(WeirCoe)+ "\n")
                Lake_rvh_string_list.append(
                    "  :CrestWidth " + '{:>10.4f}'.format(Crewd) #"{:.4f}".format(Crewd) #str(Crewd)
                )  # f2.write("  :CrestWidth "+str(Crewd)+ "\n")
                Lake_rvh_string_list.append(
                    "  :MaxDepth " + str(h0)
                )  # f2.write("  :MaxDepth "+str(h0)+ "\n")
                Lake_rvh_string_list.append(
                    "  :LakeArea    " + str(A)
                )  # f2.write("  :LakeArea    "+str(A)+ "\n")

                Lake_rvh_string_list.append(
                    "  :SeepageParameters   0   0 "
                )  # f2.write("  :LakeArea    "+str(A)+ "\n")            
                
                Lake_rvh_string_list.append(
                    ":EndReservoir   "
                )  # f2.write(":EndReservoir   "+"\n")
            elif has_obs >= 1 and lake_out_flow_method == 'power_law':
                Lake_rvh_string_list.append(
                    "#############################################"
                )  # f2.write("#############################################"+"\n")
                Lake_rvh_string_list.append(
                    "# New Lake starts"
                )  # f2.write("###New Lake starts"+"\n")
                Lake_rvh_string_list.append(
                    "#############################################"
                )  # f2.write("#############################################"+"\n")
                ######write lake information to file
                Lake_rvh_string_list.append(
                    ":Reservoir" + "   Lake_" + str(int(lakeid))
                )  # f2.write(":Reservoir"+ "   Lake_"+ str(int(lakeid))+ "   ######## " +"\n")
                Lake_rvh_string_list.append(
                    "  :SubBasinID  " + str(int(catid))
                )  # f2.write("  :SubBasinID  "+str(int(catid))+ "\n")
                Lake_rvh_string_list.append(
                    "  :HRUID   " + str(int(hruid))
                )  # f2.write("  :HRUID   "+str(int(hruid))+ "\n")
                Lake_rvh_string_list.append(
                    "  :Type RESROUTE_STANDARD   "
                )  # f2.write("  :Type RESROUTE_STANDARD   "+"\n")
                Lake_rvh_string_list.append(
                    "  :MaxDepth " + str(h0)
                )  # f2.write("  :MaxDepth "+str(h0)+ "\n")
                Lake_rvh_string_list.append(
                    "  :SeepageParameters   0   0 "
                )  # f2.write("  :LakeArea    "+str(A)+ "\n")            

                Lake_rvh_string_list.append(
                    "  :OutflowStageRelation POWER_LAW "
                )           

                Lake_rvh_string_list.append(
                    "  %s   %s " %(str(Crewd*2/3*(9.80616**(0.5))),str(1.5))
                ) 
                
                Lake_rvh_string_list.append(
                    "  :EndOutflowStageRelation "
                ) 
                            

                Lake_rvh_string_list.append(
                    "  :VolumeStageRelation POWER_LAW "
                )           

                Lake_rvh_string_list.append(
                    "  %s   %s " %(str(A),str(1))
                ) 
                
                Lake_rvh_string_list.append(
                    "  :EndVolumeStageRelation "
                ) 
                
                
                Lake_rvh_string_list.append(
                    "  :AreaStageRelation POWER_LAW "
                )           

                Lake_rvh_string_list.append(
                    "  %s   %s " %(str(A),str(0))
                ) 
                
                Lake_rvh_string_list.append(
                    "  :EndAreaStageRelation "
                ) 
                            
                            
                Lake_rvh_string_list.append(
                    ":EndReservoir   "
                )  # f2.write(":EndReservoir   "+"\n")
                
    Lake_rvh_string = "\n".join(Lake_rvh_string_list)
    return Lake_rvh_string, Lake_rvh_file_path

ObsTypes=pm.ObsTypes()

hru_info = pd.read_csv(os.path.join(os.getcwd(),'finalcat_hru_info_updated.csv'))

if len(ObsTypes) == 1 and ObsTypes[0]=='Obs_SF_IS':
    lake_par_info = []
    obs_gauge = []
else:
    lake_par_info = pd.read_csv(os.path.join(os.getcwd(),'crest_width_par.csv'))
    obs_gauge = lake_par_info.columns

hru_info = hru_info.drop_duplicates("HRU_ID", keep="first")
hru_info = hru_info.loc[(hru_info["HRU_ID"] > 0) & (hru_info["SubId"] > 0)]
 

 
# obs_gauge_ini = ['Misty','Animoosh','Traverse','Burntroot',
#              'La Muir','Narrowbag','Little Cauchon','Hogan','North Depot',
#              'Radiant','Loontail','Cedar','Big Trout','Grand','Lavieille']
# Lake_Nms = lake_par_info['Lake_Nms'].values[0]

# ## read list observated lakes
# df_gauge = pd.read_csv('obs_gauge_ini.csv')
# obs_gauge_ini = df_gauge['obs_gauge_ini'].values
# # obs_gauge_ini=hru_info[Obs_Types].eq(1)['Hyla']s

# # model structure : method for calibrated river width
# # S1 = use individual creset width if observations available
# # S2 = use depth1 , etc ==> need confirmation from Ming
# # S3 = use power low only ==> calibration to outlet gauage only

# model_structure = 'S1'
# ## method to read model_structure
# with open('model_structure.txt','r') as f:
#     model_structure = f.read().split('\n')[0]

# if model_structure == 'S1':
#     if Lake_Nms == 'ALL':
#         obs_gauge = obs_gauge_ini
#     else:
#         for i in range(0,len(obs_gauge_ini)):
#             if obs_gauge_ini[i] == Lake_Nms:
#                 obs_gauge = [Lake_Nms]
# else:

# obs_gauge = obs_gauge_ini    
model_structure='S1'

Lake_rvh_string, Lake_rvh_file_path = Generate_Raven_Lake_rvh_String(
    hru_info, os.getcwd(), 'test','broad_crest',lake_par_info,obs_gauge,model_structure
)

WriteStringToFile(Lake_rvh_string, Lake_rvh_file_path, "w")

