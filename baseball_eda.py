
## FEEL FREE TO WRITE NOTES YOU HAVE OR ADD ANY ADDITIONAL CODE YOU THINK WOULD BE HELPFUL
# LOAD IN PACKAGES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import collections as c
%matplotlib inline
import itertools
from collections import Counter
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
logreg = LogisticRegression()

cd SF_DAT_17_WORK
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

    bat = bat[['retro_game_id','regseason_fl','game_id','home_team_id','away_team_id', 
    'bat_home_id','pit_mlbid','pit_hand_cd','bat_mlbid','bat_hand_cd', 
    'event_outs_ct','event_tx','event_cd','battedball_cd']]
    
    pa = list(bat.event_tx)
    uniq_plate_outcome = set(pa)

def pa_outcomes(pa_outcomes, outcome):
   return outcome in pa_outcomes

for i in uniq_plate_outcome:
   bat[i] = bat.event_tx.apply(lambda x: pa_outcomes(x, i))

bat
# Drop NA Rows
    # Gets rid of rows w/ null values
    pitch = pitch[pd.notnull(pitch['pitch_type'])]
    # Drops columns w/ insignificant pitch types (pitch_out, eephus, intent, etc.)
    pitch = pitch[pitch.pitch_type != 'AB']
    pitch = pitch[pitch.pitch_type != 'EP']
    pitch = pitch[pitch.pitch_type != 'UN']
    pitch = pitch[pitch.pitch_type != 'IN']
# Include Full Pitch Name column (naming conventions are slighlty different across stadiums)
    pitch_dict = {'FF': 'fastball', 'SL': 'slider', 'FT': 'fastball', 'CH': 'changeup', 'CB': 'curveball', 'CU': 'curveball', 'SI': 'sinker', 'FC': 'cutter', 'SF': 'split-finger', 
                  'KC': 'knuckle-curve', 'FS': 'fastball', 'IN': 'pitch_out', 'KN': 'knuckleball', 'PO': 'pitch_out', 'FO': 'pitch_out', 'EP': 'eephus', 'UN': 'unidentified', 'AB': 'unidentified'}

def new_col(pitch):
    for i in pitch.pitch_type:
        return pitch_dict[i]

pitch['pitch_name'] = pitch.apply(new_col,axis=1)



# OVERVIEW OF TABLES
    bat.info()
    bat.describe()
    bat.head()
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