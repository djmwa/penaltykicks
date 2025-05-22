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

<details>
  <summary>FBRef Python Script (EPL)</summary>
  
  ```p
  import httpx
  import os
  import pandas as pd
  import time
  from bs4 import BeautifulSoup, Comment
  from collections import defaultdict
  from io import StringIO
  
  def scrape_and_save_fbref_table(url):
      # Standard anti-bot headers
      headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
          'Referer': 'https://www.google.com',
          'Accept-Language': 'en-US,en;q=0.9',
      }
  
      grouped_tables = defaultdict(dict)
  
      with httpx.Client(headers=headers) as client:
          r = client.get(url, timeout=10)
          r.raise_for_status()
  
          soup = BeautifulSoup(r.text, 'lxml')
  
          # Capture both visible and commented-out tables
          comments = soup.find_all(string=lambda text: isinstance(text, Comment))
          tables = soup.find_all('table')
          for comment in comments:
              tables += BeautifulSoup(comment, 'lxml').find_all('table')
  
          for table in tables:
              caption = table.find('caption')
              base_title = caption.text.strip() if caption else table.get('id') or 'UnnamedTable'
  
              try:
                  # Read multi-indexed HTML tables
                  df = pd.read_html(StringIO(str(table)), header=[0, 1])[0]
  
                  # Flatten column headers if necessary
                  if isinstance(df.columns, pd.MultiIndex):
                      df.columns = [' '.join(col).strip() for col in df.columns.values]
  
                  # Suffix to differentiate table variants under same title
                  if len(grouped_tables[base_title]) == 0:
                      sub_title = ''
                  elif 'Squad' in base_title:
                      sub_title = '_against'
                  elif 'Table' in base_title:
                      sub_title = '_home_away'
                  else:
                      sub_title = f'_p{len(grouped_tables[base_title]) + 1}'
  
                  grouped_tables[base_title][sub_title] = df
                  print(f'✅ Parsed: {base_title}{sub_title} ({len(df)} rows)')
  
              except Exception as e:
                  print(f'❌ Skipped {base_title}: {e}')
  
      # Output path uses the global `yr` from calling context
      output_dir = f'premier_league_tables_{yr}'
      os.makedirs(output_dir, exist_ok=True)
  
      # Save to CSV with sanitized, length-limited filenames
      for base_title, sub_tables in grouped_tables.items():
          safe_base = ''.join(c if c.isalnum() else '_' for c in base_title)[:50]
          for sub_title, df in sub_tables.items():
              safe_sub = ''.join(c if c.isalnum() else '_' for c in sub_title)[:30]
              csv_path = os.path.join(output_dir, f'{safe_base}{safe_sub}.csv')
              df.to_csv(csv_path, index=False)
              print(f'📄 Saved CSV: {csv_path}')
  
  
  # Year range: Premier League history from 1888 to 2025
  # 1888 was the inception of the English football league system
  # Premier League came into existence in 1992
  # Due to the World Wars, the league was not active from 1915-1918 or 1939-1945
  start_years = list(range(1888, 1915)) + list(range(1919, 1939)) + list(range(1946, 2026))
  seasons = [str(yr) + '-' + str(yr + 1) for yr in start_years]
  
  # Season-specific stats page
  base_url = 'https://fbref.com/en/comps/9/{0}/{0}-Premier-League-Stats'
  
  # Sequential scrape with throttling to avoid rate-limiting
  for yr in seasons:
      url = base_url.format(yr)
      print(f'🔍 Scraping: {url}')
      scrape_and_save_fbref_table(url)
      time.sleep(5)
  
  print('✅ Completed All Seasons')
  ```
</details>

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

<details>
  <summary>Football-Data Python Script</summary>
  
  ```p
  import requests 
  from bs4 import BeautifulSoup 
  
  ''' 
  With 32 seasons of data for each of the 10 European league (US and Mexico
  have only a single combined .csv file), manually downloading them would be
  extremely tedious. This script is to automate that process.
  '''
  
  # Base URL for the site; all pages use the same structure with only the
  # name of the country changed
  base_url = 'https://www.football-data.co.uk/{0}m.php'
  
  # List of league pages to iterate through
  league_pages = ['england',
                  'france',
                  'germany',
                  'italy',
                  'spain']
  
  failed_downloads = [] ## null list to hold failed links for manual clean-up later
  
  def get_csv_links(url): 
      
      # create response object 
      r = requests.get(url, timeout = 30) 
      
      # create beautiful-soup object 
      soup = BeautifulSoup(r.content,'html5lib') 
      
      # find all links on web-page 
      links = soup.find_all('a') 
  
      # filter the link sending with .csv 
      csv_links = ['https://www.football-data.co.uk/' + link['href'] for link in links if link['href'].endswith('csv')] 
  
      return csv_links 
  
  
  def download_csv_links(csv_links):
  
      for link in csv_links: 
  
          # iterate through all links in csv_links         
          # obtain filename by splitting url and getting 
          # last 2 strings
          try:
              league = (link.split('/')[-1]).split('.')[-2]   ## Isolate league code
              season = link.split('/')[-2]                    ## Isolate season code
              file_name = league + '_' + season + '.csv'      ## Name file with league & season
  
              print( 'Downloading file:%s'%file_name) 
              
              # create response object 
              r = requests.get(link, timeout = 30) 
              
              # download started 
              with open(file_name, 'wb') as f:
                  f.write(r.content) 
              
              print('%s downloaded!'%file_name )
          except:
              print('!! Failed to download %s!!'%file_name )
              failed_downloads.append(link)
  
      print ('csv files completed for country')
      return
  
  
  for country in league_pages:
      # getting all csv links
      url = base_url.format(country)
      csv_links = get_csv_links(url)
  
      # download all csv files
      download_csv_links(csv_links)
  
  print(failed_downloads)
  ```
</details>

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

<details>
  <summary>EPL Review Python Script</summary>

  ```p
  import pandas as pd
  import requests
  from bs4 import BeautifulSoup
  
  base_url = 'https://www.eplreview.com/statistics-penalty_epl20{0}.htm'
  
  for yr in range(12,20):
      season = str(yr) + '-' + str(yr + 1)
      url = base_url.format(season)
      
      response = requests.get(url)
      response.raise_for_status()
  
      soup = BeautifulSoup(response.text, 'html.parser')
      tables = soup.find_all('table')
  
      # Select the largest table (the main data table)
      main_table = max(tables, key=lambda t: len(t.find_all('tr')))
  
      rows = main_table.find_all('tr')
  
      # Extract header from the first row — no <th> tags, only <td>
      header = [cell.get_text(strip=True) for cell in rows[0].find_all('td')]
  
      # Extract data from remaining rows
      data = []
      for row in rows[1:]:
          cols = [col.get_text(strip=True) for col in row.find_all('td')]
          # Only include rows that have the same number of columns as header
          if len(cols) == len(header):
              data.append(cols)
  
      # Create DataFrame
      df = pd.DataFrame(data, columns=header)
  
      # Save to CSV
      csv_filename = 'epl_penalty_stats_20' + season + '.csv'
      df.to_csv(csv_filename, index=False)
  
      print(f'✅ Data successfully saved to: {csv_filename}')
  
  print('✅ Seasons complete!')
  ```
</details>

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
