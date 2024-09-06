#!/usr/python
'''
plot boxplot compare all
'''
import warnings
warnings.filterwarnings("ignore")
import os
import numpy as np
import scipy
import re
import datetime
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
import matplotlib.colors
mpl.use('Agg')
#===============================================================================================
def mk_dir(dir):
    # Create the download directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)
#===============================================================================================
# Function to extract the required part from the filename
def extract_code(filename):
    # Split the filename by underscores
    parts = filename.split('_')
    
    # Extract the relevant parts: SF/WL and the code before the last underscore
    if len(parts) > 3:
        return f"{parts[0][-2::]}_{parts[2]}"
    
    return None
#===============================================================================================
# read the combine files
odir='../output'
lserName=['cedar','graham']
combined_df = pd.DataFrame()
for serName in lserName:
    fname=odir+"/combined_output_all_"+serName+".csv"
    # Read the data
    df = pd.read_csv(fname)
    # Add 'Expname' column
    df['boxName'] = [expName+"_"+serName for expName in df['Expname']]
    df['xLabel'] = df['filename'].apply(extract_code)
    # Append to combined dataframe
    combined_df = pd.concat([combined_df, df], ignore_index=True)
    # print (combined_df)

# boxplot
df_out=combined_df[(combined_df['observed_data_series']=='HYDROGRAPH_CALIBRATION[921]') | 
(((combined_df['filename'].str.contains('WL_IS'))) & (combined_df['observed_data_series'].str.contains('RESERVOIR_STAGE_CALIBRATION')))]

print ("df_out:")
print (df_out.head())

# colors = [plt.cm.tab20(0),plt.cm.tab20c(4),plt.cm.tab20c(8),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]
colors = [plt.cm.tab20(4),plt.cm.tab20(5),plt.cm.tab20(2),plt.cm.tab20(3),plt.cm.tab20c(9),plt.cm.tab20c(10),plt.cm.tab20c(11)]

fig, ax = plt.subplots(figsize=(16, 8))
ax=sns.boxplot(data=df_out,x='xLabel', y='DIAG_KLING_GUPTA_DEVIATION',hue='boxName',palette=colors, boxprops=dict(alpha=0.9)) #order=['obj.function','02KB001','mean_Lake','Narrowbag','Crow','LM','NC']

# Lines between each columns of boxes
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
#
ax.xaxis.grid(True, which='minor', color='grey', lw=1, ls="--")
ax.set_ylabel("$Metric$ $($$KGE$/$KGED$$)$") #/$R^2$$

ax.set_xlabel(" ")
ax.set_xticklabels(df_out['xLabel'].unique(), rotation = 90, ha="center")
# ax.set_ylim(ymin=-0.75,ymax=1.1)
# ax.set_ylim(ymin=-2.2,ymax=1.1)
# plt.savefig('../figures/paper/fs1-KGE_boxplot_S0_CalBugdet_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.tight_layout()
print ('../figures/paper/fs10-KGE_boxplot_combine_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')
plt.savefig('../figures/paper/fs10-KGE_boxplot_combine_'+datetime.datetime.now().strftime("%Y%m%d")+'.jpg')