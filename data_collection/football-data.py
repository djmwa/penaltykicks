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
