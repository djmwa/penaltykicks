---
title: Penalty Kicks in Professional Soccer
description: Daniel Moser<br>July 10, 2025
---

**Document Type:** Code & Analysis  
**Purpose:** Data dictionary and cleaning

***

## Phase 1: Initial Misstep - Overengineering the Data Pipeline

### The Wrong Approach
Despite having a clear research question about penalty kick impact on game outcomes, I made the strategic error of attempting to clean and process the entire available dataset first. This meant working with 79 separate files with stat leaders (each with 1 stat, and limited to 10 players), plus 474 features (many duplicated or irrelevant) across 24 files for team-level stats.

**What I Did Wrong:**
- Started with comprehensive data cataloguing instead of identifying minimum viable data
- Spent time creating detailed data dictionaries for irrelevant datasets
- Attempted to solve complex data structure problems that weren't necessary for my research question
- Got distracted by the "completeness" of having all possible data rather than focusing on what I actually needed

**Problems This Identified:**
- Individual stat files had no column headers
- Player and team names were combined in single columns  
- First and second rows of data were merged into single rows
- Character encoding issues with international player names
- Inconsistent patterns made automated parsing difficult

**The Real Issue:** I was solving interesting technical problems that had no bearing on my actual research question.

Even with the failure of this phase to produce data relevant to my question, I identified several challenges (and ways to tackle them) that will be helpful if there are further questions of interest to explore. I also gained valuable experience writing and debugging code for dataframe import and manipulation. 

## Phase 2: Course Correction and Learning

### Strategic Reset - What I Should Have Done From the Start
After recognizing this was a dead end, I stepped back and properly scoped the project around my original research question.

**Key Realization:** I had clear research objectives but got allowed myself to get lost in the complexity and volume of available data and attempting to wrangle it into a usable form. This is a classic case of letting the data drive the analysis rather than letting the research question drive the data collection.

**What I Learned:** Always start with your research question and work backwards to identify the minimum data needed. Data exploration should be targeted and purposeful, not exhaustive.

**Refined Approach:**
- Focused on match-level outcomes (points per game) rather than individual player statistics
- Limited analysis to the 8 seasons of English Premier League (EPL) games for which I have full penalty kick data
- Identified minimum viable dataset: game results + penalty kick occurrences and outcomes

**Data Requirements Identified:**
1. Teams involved (home vs away)
2. Match outcome (win/draw/loss)
3. Final scores
4. Penalty kick occurrences and outcomes for each team
5. Unique game identifier for joining datasets

## Phase 3: Data Integration Challenges

### Challenge 1: Inconsistent Data Formats
**EPL Penalty Data Issues:**
- No column headers in CSV files
- Character encoding problems (accented characters displayed incorrectly)
- Inconsistent formatting of white space when identifying teams 
- Match identification format: "TeamA vs TeamB" with unclear home/away designation

**football-data Issues:**
- Non-intuitive file naming convention (E0_1213.csv = English Premier League 2012-13)
- Multiple column names for same data (FTHG/HG for home goals)
- Inconsistent column presence across different seasons

### Challenge 2: Creating Unique Match Identifiers
**Problem:** Neither dataset had explicit match IDs, requiring creation of composite keys.

**Solution:** Used combination of season + home team + away team as unique identifier, leveraging the round-robin league structure where each team plays every other team exactly twice (home and away).

**Validation:** Cross-referenced team name formats between datasets to ensure proper matching.

## Phase 4: Data Processing and Technical Problem-Solving

### Problem 1: Missing Column Headers
**Issue:** Penalty kick data CSVs had no headers, causing pandas to treat first row as column names.

**Solution:** Used column indexes instead of names, then manually assigned appropriate column names after data loading.

### Problem 2: Data Quality Issues
**Issue:** One CSV file had incorrect format due to web scraping error.

**Solution:** Manual verification of each file, followed by copy-paste correction of the problematic file while maintaining structural consistency.  
   \* Manual verification was viable because only 8 files required verification

### Problem 3: Character Encoding Errors
**Issue:** `UnicodeDecodeError` when processing files with international player names.

**Solution:** Implemented fallback encoding strategy using Latin-1 encoding with Windows-1252 as backup.

### Problem 4: Data Type Inconsistencies
**Issue:** `TypeError` when processing match strings - missing values were being read as floats instead of strings.

**Root Cause:** Extra null rows in 2012-13 season data.

**Solution:** Added robust null value handling to prevent processing errors, rather than just fixing the single problematic file. This improved code resilience for future use.

### Problem 5: Multiple Penalties Per Game
**Issue:** Simple joins resulted in duplicate rows for games with multiple penalty kicks.

**Solution:** Aggregated penalty data before joining, creating separate columns for:
- Home team penalties scored/awarded
- Away team penalties scored/awarded

## Technical Implementation

### Data Processing Pipeline
1. **Data Loading:** Custom functions with encoding fallbacks
2. **Data Cleaning:** Null value handling and format standardization  
3. **Data Aggregation:** Penalty kick summaries by game
4. **Data Integration:** Merging on composite keys (season + home team + away team)

### Final Dataset Structure
Created 8 season-specific files with standardized columns:
- `Season`: EPL Season identifier
- `HomeTeam`: Home team name
- `AwayTeam`: Away team name  
- `HomeGoals`: Total goals scored by home team
- `AwayGoals`: Total goals scored by away team
- `Result`: Game outcome (H/A/D)
- `home_pk_scored`: Penalties scored by home team
- `home_pk_awarded`: Penalties awarded to home team
- `away_pk_scored`: Penalties scored by away team
- `away_pk_awarded`: Penalties awarded to away team

The Python script and 2019-2020 data used to create these files can be found [here](data_cleaning/README.md), along with the 2019-2020 output file.

## Key Learnings

1. **Start with the Research Question:** The biggest lesson was that I should have worked backwards from my research question to identify the minimum viable dataset. Getting distracted by comprehensive data cleaning was a significant time sink that didn't advance my actual goals.

2. **Data Exploration Should Be Targeted:** While understanding your data is important, exploration should be purposeful and bounded by your analytical objectives, not driven by curiosity about everything that's available.

3. **Minimum Viable Data First:** For future projects, I would identify the smallest dataset that can answer my core research question, prove the analysis works, then expand scope if needed.

4. **Data Quality Assessment:** Always verify data integrity before processing. The time spent on manual verification prevented downstream analytical errors.

5. **Robust Error Handling:** Building resilient code that handles edge cases (like encoding errors and null values) is more valuable than quick fixes.

6. **Beware of Interesting Side Problems:** Complex data structure problems can be intellectually engaging but may not be relevant to your research objectives. Stay focused on what matters for your analysis.

## Remaining Tasks

1. **Exploratory Data Analysis:** 
   - Distribution of penalty kicks across seasons
   - Correlation between penalties and match outcomes
   - Home field advantage in penalty situations

2. **Statistical Analysis:**
   - Quantify penalty kick impact on points per game
   - Assess statistical significance of findings
   - Depending on the above, consider whether other statistics would help improve the results

3. **Future Enhancements:**
   - Incorporate timing of penalty kicks (early vs late in match)
   - Analyze penalty kick conversion rates by team/player
   - Expand to other leagues for comparative analysis

## Next Steps

1. Begin EDA with focus on penalty kick frequency and distribution
2. Develop statistical models to quantify penalty impact on match outcomes
3. Create visualizations to communicate findings effectively
4. Document analytical methodology and conclusions

[Home](/penaltykicks)  
[Previous: Data Collection](data_collection.md)
