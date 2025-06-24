import glob
import os
import pandas as pd

# Path pattern to match all *_01/ExperimentalSettings.log files
log_files = glob.glob("/home/menaka/scratch/LakeCalibration/out/V*_01/ExperimentalSettings.log")

# Only keep these keys (cleaned and ordered)
target_keys = [
    "Experiment Name",
    "Observation Types",
    "Maximum Iterations",
    "Calibration Method",
    "Cost Function",
    "Metric SF",
    "Metric WL",
    "Metric WA",
    "Calibrate Individual Creset Width",
    "Observation Folder",
    "Hypsometric Curve",
    "Constrains"
]

# Function to parse each log file and return a dictionary of settings
def parse_log_file(filepath):
    settings = {}
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if ':' in line and not line.startswith("#="):
                key, value = line.lstrip('#').split(':', 1)
                settings[key.strip()] = value.strip()

    # Extract the full experiment folder name (e.g., V7e_01)
    folder_name = os.path.basename(os.path.dirname(filepath))
    # Extract the base experiment name (e.g., V7e)
    base_name = folder_name.split('_')[0]
    settings['Experiment Name'] = base_name
    settings['ExperimentFolder'] = folder_name
    return settings

# Parse all log files
all_settings = [parse_log_file(f) for f in log_files]

# Convert to DataFrame
df_settings = pd.DataFrame(all_settings)

# Put columns in order with 'Experiment Name' and 'ExperimentFolder' first
cols = ['Experiment Name', 'ExperimentFolder'] + [c for c in df_settings.columns if c not in ['Experiment Name', 'ExperimentFolder']]
df_settings = df_settings[cols]

# Reorder columns as specified
df_settings = df_settings[target_keys]

# Output the result
print(df_settings)

print (df_settings[['Experiment Name','Observation Types']])

# Optionally save to CSV
df_settings.to_csv("../figures/all_experimental_settings.csv", index=False)