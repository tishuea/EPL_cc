# EPL Data Analysis for 2024-2025 Season    

## Our Data and Context
- Legend File: legend_EPL.txt (txt file containing description of EPL_24_25.csv columns )
- Data File: EPL_24_25.csv (our data, containing each match played, teams and dates the results, goals, yellow/red cards, stats, and betting odds etx)
- NOTE: likely to be some missing data. We are also unlikely to use every column.

## High level Overview
1. EDA: missing values, summary statistics, outliers etc.
2. Visualizations: distributions, interesting correlations, etc.  save figures as PDFs to a /figures folder
3. Modeling and Inference: both basic statstical modeling (match result as random independent variable) as well as ML-oriented analyses.

## Project Specifics
1a. Standings Table: Build a standings table at season end. In the EPL, winners get 3 pts, losers get 0, and draws give 1 to each team. Goal differential breaks ties; if there is a still a tie, just sort alphabetically.
1b. Home team advantage analysis - does it exist? Are home teams more likely to win, or receive fewer yellow/red cards?
1c. Team profiles. Attack/defense scatter plots, and conversion rates (shots vs goals).
1d. Referees. Analysis of yellow cards given by each ref, and if any ref statistically benefits home or away team. Only include refs with enough games refereed (10+). 

2a. Half time -> Full time result analysis. Represent as 3x3 matrix (e.g. an item is how many games ended with that specific combination of HT-FT result, e.g. draw at HT but H team win at FT.) How does HT result compare to FT results?
2b. Form analysis. What are the teams on the best hot streak, in a given match week? This will be defined as average points per game (3 for wins, 1 for draws, 0 for losses) won over the last five games that team has played. So you need to start this only after a team as played 5 games. For given match week, what are the three best and worst form teams? Also, show line graph depicting this 'form' metric as a function of match week.
2c. Corners. Corners per game for and against by each team. Do corners correlate with match results?

3a. Match result predication. Take the BET365 odds, convert them to implied probabilities, and renormalize them to sum to 100percent to account for the bookmaker margin. Predict the team with the highest renormalized probability. Compare the accuracy of this model compared to pure random chance (e.g. assuming H,D,A are equally 1/3 probably )
3b.


## Methods
- Use Python and the python scientific computing stack (pandas, scipy, stats, numpy, matplotlib). Carry out and save your work within a python notebook.
- Save the outputs and figures to disk.
- Save an executive summary in a summary.md file, updating as you go. 