
# LOAD IN REQUIRED PACKAGES
import pandas as pd
import numpy as np
import seaborn as sns

# LOAD IN DATA FROM CSV
cd desktop/my_python/data_science/SF_DAT_17_WORK
pwd
ls
bat = pd.read_csv('atbat_table.csv')
pitch = pd.read_csv('pitch_table.csv')

# EDA 
bat.info()
bat.describe()
pitch.info()
pitch.describe()