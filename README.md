# EPL analysis with Agents

## This is a personal project for a) toying around with EPL data from the 24-25 season, and b) having fun with agents (here I used Claude Code, but use whatever you like).

## Data source: https://www.football-data.co.uk/englandm.php ['Season 2024/2025' -> 'Premier League']. (Corresponding legend is from the same source: https://www.football-data.co.uk/notes.txt).

## Agent mandates are defined in instructions.md. The agent is instructed to carry out the analysis in python, save the script and results to disk, store the plots in /figures, and record a summary of the findings in summary.md. 

## Just spin up your agent and tell it to carry out the analysis using instructions.md, e.g. 
###  ```claude```
### ```Read instructions.md, then load EPL_24_25.csv and begin the full analysis. Document your findings in summary.md as you go.```


## For posterity and comparison, the outputs from my own agent's analysis are saved in this repo in /Results_AJT.
## I chose to request analysis about home team advantage, referrees, form, corners, betting odds reliability, etc. 
## Later: comparing human findings (my own) to that of the agent. 
## Could also be interesting to compare others's results when using indentical instructions (some instructions have been left intentionally vague, to see what the agent comes up with). 
## Modify instructions.md if you want a different analysis.




