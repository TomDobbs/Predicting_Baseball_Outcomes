GOAL:
I want to predict baseball game outcomes.

WHY:
I chose this topic for a number of reasons...
1. I love baseball and they have a LOT of data for a sport
2. The type of data being logged is very new
3. Data munging will be very important & will be a complex challenge for me
4. If my model is good enough, betting on baseball games could become a side hobby ;)

TARGET:
Win or Lose

FEATURES:
- Pitcher (Pitch repoirtoire)(Bucket types of pitchers)
- Batters (Lineup)(Bucket types of batters)

DATA: 
Daily baseball data and historical data exists going back to 2008, PitchFX data is the most common place to retrieve data from. Will require scraping the information from the MLB website. 

What I have done to date:
1. Scraped detailed baseball data from the MLB.com website.
    1. Scraper iterates through daily baseball statistics through pages such as this...http://gd2.mlb.com/components/game/mlb/year_2009/month_10/day_06/gid_2009_10_06_detmlb_minmlb_1/
    2. Scraper goes through individual innings per game
2. High level EDA
    1. Most common pitch types
    2. Most common plate appearance results


Next Steps:
    1. Alter parser to include actual player names
    2. Use batter information & pitcher information to create pitcher/batter categories using K-Means clustering
    3. Use the categories to feed lineup and pitcher categories into a Logistic Regression to predict game outcomes
    4. Build out more interesting visualizations - as they apply to project goal
