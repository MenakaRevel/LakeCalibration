import pandas as pd
import os
#===============================================================================================
def mk_dir(folder_path):
  """
  Creates a folder at the specified path.

  Args:
    folder_path: The path of the folder to create.
  """

  try:
    os.makedirs(folder_path)
    print(f"\n\t            Folder created successfully at {folder_path}")
  except FileExistsError:
    print(f"\n\t            Folder already exists at {folder_path}")
#===============================================================================================
# Main Code
#===============================================================================================
#=====================
odir='/scratch/menaka/LakeCalibration/out'
#=====================
lexp=["E0a","E0b"]
ens_num=10
combined_df = pd.DataFrame()
for expname in lexp:
    for num in range(1,ens_num+1):
        expfile = odir+"/"+expname+"_"+"%02d"%(num)+"/best/RavenInput/output/Petawawa_Diagnostics.csv"
        
        # Read the data
        df = pd.read_csv(expfile)
        
        # Add 'Expname' column
        df['Expname'] = expname

        # Add 'Number' column
        df['Number'] = num
        
        # Append to combined dataframe
        combined_df = pd.concat([combined_df, df], ignore_index=True)

# make folder
mk_dir('../output')

# Save the combined dataframe to a new CSV file
combined_df.to_csv('../output/combined_output_all_cedar.csv', index=False)

print(combined_df.head())