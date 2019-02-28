import pandas as pd
import numpy as np
import glob

##########################################################
# Construct main dataframe
##########################################################

main_files = glob.glob('./data/raw/E0_*.csv')

print(main_files)

dataframes = []

for file in main_files:
    df = pd.read_csv(file, sep=',', index_col=None, header=0, error_bad_lines=False, parse_dates=[1], dayfirst=True)

    dataframes.append(df)

main_df = pd.concat(dataframes, sort=False)

##########################################################
# Merge Additional Dataset X
##########################################################

# <---- Add your code here to modify main_df


print(main_df.head(10))
