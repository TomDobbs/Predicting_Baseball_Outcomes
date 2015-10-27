
## FEEL FREE TO WRITE NOTES YOU HAVE OR ADD ANY ADDITIONAL CODE YOU THINK WOULD BE HELPFUL
# LOAD IN PACKAGES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import collections as c
%matplotlib inline

# CLEANING BASEBALL DATA 
with open('atbat_table.csv','r') as in_file, open('edited_atbat_table.csv','w') as out_file:
    seen = set()
    for line in in_file:
        if line in seen: continue 

        seen.add(line)
        out_file.write(line)
        
with open('pitch_table.csv','r') as in_file, open('edited_pitch_table.csv','w') as out_file:
    seen = set()
    for line in in_file:
        if line in seen: continue 

        seen.add(line)
        out_file.write(line)
        
# LOAD IN DATA FROM CSV
    bat = pd.read_csv('edited_atbat_table.csv')
    pitch = pd.read_csv('edited_pitch_table.csv')

# Drop NA Rows
    # Gets rid of rows w/ null values
    pitch = pitch[pd.notnull(pitch['pitch_type'])]
    # Drops columns w/ insignificant pitch types (pitch_out, eephus, intent, etc.)
    pp = ['AB','EP','UN','IN']
    #pitch[pitch.pitch_type not in pp] 

# Include Full Pitch Name column (naming conventions are slighlty different across stadiums)
    pitch_dict = {'FF': 'fastball', 'SL': 'slider', 'FT': 'fastball', 'CH': 'changeup', 'CB': 'curveball', 'CU': 'curveball', 'SI': 'sinker', 'FC': 'cutter', 'SF': 'split-finger', 
                  'KC': 'knuckle-curve', 'FS': 'fastball', 'IN': 'pitch_out', 'KN': 'knuckleball', 'PO': 'pitch_out', 'FO': 'pitch_out', 'EP': 'eephus', 'UN': 'unidentified', 'AB': 'unidentified'}
                  
# OVERVIEW OF TABLES
    bat.info()
    bat.describe()
    pitch.info()
    pitch.describe()
    bat.start_bases_cd.describe()
    pitch.end_speed.describe()

# EXPLORING PITCH TABLE
    # Distinct pitch_types    
    set(pitch.pitch_type)    
    # Count of Pitches    
    c.Counter(pitch['pitch_type'])
    # Pitch Type %
    pitch.pitch_type.value_counts()/pitch.pitch_type.count()
    
    pitch.groupby(['pitch_type']).start_speed.mean()
    pitch.groupby('pitch_type')[['spin_dir','spin_rate']].mean()
    pitch[['pitch_type','start_speed','end_speed']].sort_index(by='end_speed', ascending = True).tail(20)

# EXPLORING BATTING TABLE
    # Distinct pitch_types    
    set(bat.event_tx)    
    # Count of Pitches    
    c.Counter(bat.event_tx)
    # Pitch Type %
    bat.event_tx.value_counts()/bat.event_tx.count()

# seaborn pairplot (under construction)
sns.set()
pitch_pair = sns.load_dataset("pitch")
sns.pairplot(pitch_pair , hue="species")

# Plot of the strike zone w/ pitch location
# Want to break out plots to each distinct pitch type along w/ trajectory of the average pitch
x = pitch.x
y = pitch.y
plt.scatter(x, y, alpha=0.4)