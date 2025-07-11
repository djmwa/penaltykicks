---
title: Penalty Kicks in Professional Soccer
description: Daniel Moser<br>May 21, 2025
---

**Document Type:** Code & Analysis  
**Purpose:** Data acquisition and initial exploration

***

## Data Acquisition Strategy
As with most data-driven projects, the first step—after framing the research question (see Introduction)—is acquiring appropriate and sufficient data. I began by targeting data for the English Premier League (EPL), under the assumption that it's the most followed and well-documented league, increasing the likelihood of accessible, structured historical data.

My hope was that a reliable EPL data source would also contain data for other leagues of interest. The [official Premier League]( website does offer detailed match-level data, but unfortunately, penalty kick (PK) information is embedded only on individual match pages—nearly 400 per season—making scraping this data impractical as a first approach.

After surveying multiple sources, I identified three primary sites that collectively offer:

* Season-level statistics for all 12 leagues across 15–30 seasons
* Match-level data with limited PK information (8 seasons of EPL matches)
* Match-level data with information on shots, goals, fouls, cards, and more

While the match-level PK dataset is limited, it provides a good foundation for initial analysis. I will continue seeking more comprehensive PK data, but this gives us a sufficient base to begin quantifying game-level PK impact and determine how well predictions from season-level PK statistics match with those from game-level PK stats.

## Data Sources and Scripts
### 1. FBRef
**Site:** [FBRef EPL Stats (2024–25)](https://fbref.com/en/comps/9/Premier-League-Stats)  
**Data:** Season-level team and player statistics for all 12 leagues, including shooting, scoring, goalkeeping, passing, fouls, cards, and more.

**Key Challenges:**
* Data is spread across separate pages per league and season
* Team stats are tabbed into ‘For’ and ‘Against’ views
* Leaderboards are partially collapsed in HTML
* Season URL formats vary (e.g. split vs. single-year formats)

**Solutions:**
* Iterated over seasons using a for loop to handle league URLs
* Used `httpx` for requests and `BeautifulSoup` (`bs4`) for HTML parsing
* Navigated tabbed/secondary tables using `bs4` to pull from HTML comments and collapsed sections
* Chose to maintain separate scripts per league due to variability in URL structure and data availability

[FBRef Python Script (EPL)](data_collection/fbref_EPL.md)

**Note:** The biggest lift was handling ambiguous or non-unique table identifiers due to the tabbed layout and commented HTML. Once parsed correctly, looping through seasons and exporting structured data became straightforward.

### 2. Football-Data.co.uk
**Site:** [Football-Data.co.uk](https://www.football-data.co.uk/englandm.php)  
**Data:** Match-level results for nearly 30 years, including goals, half-time scores, shots, fouls, and cards. Available for all 12 leagues.

**Key Challenges:**
* Each country is hosted on a separate page
* One CSV per league-season, except MLS and Liga MX (combined)
* Occasional download failures due to unstable connections

**Solutions:**
* Constructed a master list of country URLs and looped through each using consistent URL patterns
* Parsed page content using `BeautifulSoup.find_all()` to extract links to .csv files
* Wrapped the download logic in `try/except` blocks to capture and log failures for manual review

[Football-Data Python Script](data_collection/football-data.py)

**Note:** Adding fault tolerance to the download function was crucial—initial runs failed silently or halted mid-script. Logging errors to a list allowed me to reattempt or manually complete downloads efficiently.

### 3. EPL Review
**Site:** [EPL Review](https://www.eplreview.com/statistics-penalty_epl2019-20.htm)  
**Data:** Game-level penalty kick data (attempts and conversions) for 8 EPL seasons

**Key Challenges:**
* No HTML tags identifying relevant tables
* Matches without PKs are not listed, creating gaps in coverage
* Each PK appears as a separate entry, requiring match consolidation

**Solutions:**
* Pulled all tables per page and filtered for the one with the most rows (generally the PK data)
* Date and team info can be used to align with match data from Football-Data for consolidation

[EPL Review Python Script](data_collection/EPL_review.py)

**Note:** This site presented the most brittle structure—lacking predictable HTML tags or consistent formats. A row-count heuristic worked for now but will need re-evaluation if the site structure changes.

## Final Thoughts
This first pass at data collection prioritized completeness and reproducibility over elegance. Where site structure allowed, I leaned on reusable scripts and common patterns; where it didn’t, I opted for pragmatic one-off solutions.

Next steps will include:
* Structuring and cleaning the merged datasets
* Defining metrics for penalty kick influence at both the match and season levels
* Building exploratory visualizations to identify patterns and potential modeling targets

I expect the next update will focus on initial trends identified during the EDA process.

***

[Home](/penaltykicks)  
[Previous: Background](background.md)  
[Next: Data Cleaning](data_cleaning.md)
