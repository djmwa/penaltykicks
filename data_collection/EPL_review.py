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
