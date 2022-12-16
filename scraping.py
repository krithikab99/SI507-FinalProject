import requests
from bs4 import BeautifulSoup
response = requests.get("https://www.timeout.com/film/the-100-best-romantic-movies")

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.h3)

# blog_titles = soup.findAll('h3', attrs={"class":"_h3_cuogz_1"})
# for title in blog_titles:
#     title1=title.text
#     print(title1)
    # start = title1.index(".")
    # end = title1.index("(",start+1)
    # substring = title1[start+1:end]
    # print(f"Start: {start}, End: {end}")
    # print(substring)

response = requests.get("https://www.theconfusedmillennial.com/list-movies-watch-valentines-day/")
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)

blog_titles = soup.findAll('li')
for title in blog_titles:
    title1=title.text
    print(title1)

response = requests.get("https://www.imdb.com/search/keyword/?keywords=valentine%27s-day")
soup1 = BeautifulSoup(response.text, 'html.parser')
# print(soup1)

blog_titles = soup1.findAll('a')
for title in blog_titles:
    title1=title.text
    print(title1)