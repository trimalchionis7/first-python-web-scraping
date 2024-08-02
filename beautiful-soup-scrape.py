from bs4 import BeautifulSoup
import requests
import pandas as pd

# request url
url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_Kingdom"
page = requests.get(url)

# use BeautifulSoup to parse web-page as HTML
soup = BeautifulSoup(page.text, 'html')

# retrieve HTML for table
table = soup.find_all('table')[0]

world_titles = table.find_all('th')

# pull out column headers from table
world_tables_titles = [title.text.strip() for title in world_titles]

# set up empty dataframe with column headers
df = pd.DataFrame(columns = world_tables_titles)

column_row = table.find_all('tr')

# enter records into dataframe
for row in column_row[1:]:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]

    length = len(df)
    df.loc[length] = individual_row_data

# store to CSV file & remove ID column
df.to_csv(r'/absolutepath', Index=False)