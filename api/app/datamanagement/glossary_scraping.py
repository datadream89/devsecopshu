import requests
import pandas as pd

import itertools
from more_itertools import one
import json

from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
url = "https://www.crissieinsurance.com/insurance-toolbox/glossary-insurance-terms"
r = requests.get(url, headers=headers)


soup = BeautifulSoup(r.content, "html.parser")
tables = soup.find_all('table')

#pagination table
page_table = [td.text for table in soup.find_all("div",{"class":"tabular"}) 
                for subtable in table.find_all('table')
                for tbody in subtable.find_all('tbody')
                for tr in tbody.find_all('tr')
                for td in tr.find_all('td')]

#ignore pagination table by selecting only the tables with class name 'wpb_wrapper'
parents = [one(table.parent['class']) for table in tables]
parent_class_list = ['wpb_wrapper']

rows = [table.find_all('tr') for table in tables if one(table.parent['class']) in parent_class_list]
rows_flatten = list(itertools.chain.from_iterable(rows))
row_dict = dict()

for tr in rows_flatten:
    td = tr.find_all('td')
    row = [i.text for i in td]
    row_dict[row[0]] = row[1]

#save the file
with open('glossary.json', 'w') as fp:
    json.dump(row_dict, fp)


# with open('glossary.json') as fp:
#     d = json.load(fp)
    
# print(d['ABANDONMENT'])