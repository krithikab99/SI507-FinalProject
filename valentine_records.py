from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

page = 1
titles = []
while page != 10:
    url = f"https://www.imdb.com/search/keyword/?keywords=boyfriend-girlfriend-relationship%2Ckiss%2Clove&mode=detail&page={page}&ref_=kw_nxt&sourceid=chrome&ie=UTF-8&sort=moviemeter,asc"
    print(url)
    response = requests.get(url)
    html = response.content
    soup = bs(html, "lxml")
    for h3 in soup.find_all('a'):
        titles.append(h3.get_text(strip=True))
    page = page + 1
    myfile = open('xyz.txt', 'w')
    for title in titles:
        var1=title
        myfile.write("%s\n" % var1)
        
    myfile.close()
# with open('xyz.txt', 'r') as f:
#     for line in f:
#         if line.strip() == "":
#             iter_line=iter(line)
#             next(iter_line)
#             (next(iter_line))
v_file = open('valentines.csv', 'w')
file = open("xyz.txt",  "r")
print()
search = "  "
print()   
counter = 0

for line in file:
    if counter > 0 and line!="Get the IMDb App":
        counter -= 1
        v_file.write("%s\n" % line)
    if line.strip() == "": 
        counter = 1     

v_file.close()
from more_itertools import unique_everseen
with open('valentines.json', 'r') as f, open('valentine.json', 'w') as out_file:
    out_file.writelines(unique_everseen(f))