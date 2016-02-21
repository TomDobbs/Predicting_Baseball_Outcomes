'''
Move this code into your OWN SF_DAT_15_WORK repo

Please complete each question using 100% python code

If you have any questions, ask a peer or one of the instructors!

When you are done, add, commit, and push up to your repo

This is due 7/1/2015
'''

killings.info()

import pandas as pd
import seaborn as sns
# pd.set_option('max_colwidth', 50)
# set this if you need to

killings = pd.read_csv('C:\Users\eymbszk\DataScience\SF_DAT_17_WORK\data\police-killings.csv')
killings.head()

# 1. Make the following changed to column names:
# lawenforcementagency -> agency
# raceethnicity        -> race

killings.rename(columns={'lawenforcementagency': 'agency', 'raceethnicity':'race'}, inplace = True)

# 2. Show the count of missing values in each column

killings.isnull().sum()

# 3. replace each null value in the dataframe with the string "Unknown"

killings.fillna(value='Unknown', inplace = True)

# 4. How many killings were there so far in 2015?

killings[(killings.year == 2015)].groupby('year').year.count()

# 5. Of all killings, how many were male and how many female?

killings.groupby('gender').gender.count()

# 6. How many killings were of unarmed people?

killings.groupby('armed').year.count()
killings[(killings.armed == 'No')].groupby('armed').armed.count()

# 7. What percentage of all killings were unarmed?

killings[(killings.armed == 'No')].groupby('armed').armed.count()/len(killings)

# 8. What are the 5 states with the most killings?

killings.state.value_counts().head(5)

# 9. Show a value counts of deaths for each race

killings.groupby('race').race.count()

# 10. Display a histogram of ages of all killings

killings.age.hist()

# 11. Show 6 histograms of ages by race

killings.age.hist(by = killings.race)

# 12. What is the average age of death by race?

killings.groupby('race').age.mean()

# 13. Show a bar chart with counts of deaths every month
killings.groupby('month').month.count().plot(kind = 'bar')


###################
### Less Morbid ###
###################
import pandas as pd
majors = pd.read_csv('C:/Users/eymbszk/DataScience/SF_DAT_17/hw/data/college-majors.csv')
majors.head()

# 1. Delete the columns (employed_full_time_year_round, major_code)

majors.drop(['Major_code', 'Employed_full_time_year_round'], axis = 1, inplace = True)

# 2. Show the cout of missing values in each column

majors.isnull().sum()

# 3. What are the top 10 highest paying majors?

majors[['Median', 'Major']].sort(columns = ['Median', 'Major'], ascending = [0, 1]).head(10)

# 4. Plot the data from the last question in a bar chart, include proper title, and labels!

majors[['Median', 'Major']].sort(columns = ['Median', 'Major'], 
ascending = [0, 1]).head(10).plot(kind = 'barh', title = 'Median Salaries by Major',
x = 'Major', y = 'Median')


# 5. What is the average median salary for each major category?

majors.groupby('Major_category').Median.mean()

# 6. Show only the top 5 paying major categories

majors[['Median', 'Major_category']].groupby('Major_category', 
as_index = False).Median.mean().sort_index(by = 'Median', 
ascending = False).head()

# 7. Plot a histogram of the distribution of median salaries

majors.Median.hist(bins = 10)

# 8. Plot a histogram of the distribution of median salaries by major category

majors.groupby('Major_category').Median.mean().hist(bins = 10)


# 9. What are the top 10 most UNemployed majors?
# What are the unemployment rates?

majors[['Unemployment_rate', 'Major']].sort(columns = ['Unemployment_rate',
 'Major'], ascending = [0,1]).head(10)

# 10. What are the top 10 most UNemployed majors CATEGORIES? Use the mean for each category
# What are the unemployment rates?

majors[['Unemployment_rate', 'Major_category']].groupby('Major_category', 
as_index = False).Unemployment_rate.mean().sort_index(by = 'Unemployment_rate', 
ascending = False)

# 11. the total and employed column refer to the people that were surveyed.
# Create a new column showing the emlpoyment rate of the people surveyed 
# for each major; call it "sample_employment_rate"
# Example the first row has total: 128148 and employed: 90245. it's 
# sample_employment_rate should be 90245.0 / 128148.0 = .7042

majors['sample_employment_rate'] = majors.Employed/majors.Total
majors.head(5)

# 12. Create a "sample_unemployment_rate" colun
# this column should be 1 - "sample_employment_rate"

majors['sample_unemployment_rate'] = 1 - majors.sample_employment_rate

majors[['Major', 'Employed', 'Total', 'sample_unemployment_rate', 'Unemployment_rate']].head()
