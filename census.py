'''
census.py

    Scrapes the URL "https://www.census.gov/programs-surveys/popest.html" and extracts all the unique external URL's

Created by Angelo Walsh
November 17, 2018
'''

import requests
from bs4 import BeautifulSoup
import csv

census_url = "https://www.census.gov/programs-surveys/popest.html"
relative_census_url = "/popest.html"

# get plain html from census website
r_obj = requests.get(census_url)
census_html = r_obj.text

# convert to BeautifulSoup object
census_soup = BeautifulSoup(census_html, "html.parser")

# collect all tags that are html links
census_links = census_soup.find_all('a', href=True)

# empty set stores urls that link to pages other than home; removes duplicates
external_census_urls = set()

# get only urls from the collection of census links that don't
# use the absolute or relative address of the search url
for i in census_links:
    link_url = i['href']     # extracts the url only in string format
    if link_url != census_url and link_url != relative_census_url:
        # remove last '/' from urls if present and add to set of external urls
        if link_url[-1] == '/':
            link_url = link_url[:-1]
        external_census_urls.add(link_url)

# convert all relative links to absolute links in set and store in list
list_external_census_urls = []
for i in external_census_urls:
    absolute_path = "https://www.census.gov/programs-surveys/popest"
    # if links in set begin with '/', add absolute path
    # and save in list_external_census_url
    if i[0] == '/':
        full_path = absolute_path + i
        list_external_census_urls.append(full_path)
    else:
        list_external_census_urls.append(i)

# sort set of external links
list_external_census_urls.sort()

# check if  https://www.census.gov and https://www.census.gov/en.html both are in list.
# If they are remove one
if 'https://www.census.gov/en.html' in list_external_census_urls and \
    'https://www.census.gov' in list_external_census_urls:
        list_external_census_urls.remove('https://www.census.gov/en.html')

# remove non links that made into the list
for i in list_external_census_urls:
    if 'http' not in i:
        list_external_census_urls.remove(i)

# export list to a csv file
with open('/Users/angelo/Desktop/WGU/Data Mining/external_census_links.csv', 'w') as csvFile:
    file_writer = csv.writer(csvFile)
    file_writer.writerow(list_external_census_urls)
csvFile.close()

print("Total number of external links: {}".format(len(list_external_census_urls)))