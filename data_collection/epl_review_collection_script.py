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
