# SI507-FinalProject
Final project in python for course SI 507

**Special Requirements:** 
A valid API key has been added since earlier ones used in previous verisons have exhausted after fetching over 1000 records.

**Required packages :**
pandas
requests
datetime
csv
os
random
plotly

**Code to import required packages:**
import pandas
import requests
from datetime import datetime
import csv
import os
import random
import plotly.express as px

**Instructions on how to interact with the program:**
1) The first choice given to the user is to identify which holiday season thay are looking for a movie under. Question asked to user is "Which holiday do you want movie recommendations for ? Christmas, Halloween or Valentine's Day"
2) The second question is to understand the year range they want. Old movies are below 2003 and new movies are greater than the year 2003. Question asked is "Do you want to watch old movies or new movies?"
3) The third question asked to the user is to understand if they are looking for good rated movies or poorly rated movies. Question asked is "What imdbRating do you prefer? Good or Bad?"

Once the user provides a response to this, they will be able to view the correlation statistics between the fields "Year", "BoxOffice",  "imdbRating",  "Genre"

Some interesting trends were identified that can be viewed by the user if they want to.The questions include :
1) Do you want to know the difference in how the imdb ratings rank against the box office collection for both festive and non-festive movies?
2) Want to see how the box office collection ranks against the year of release for both festive and non-festive movies?
3) Youll be surprised in how the Year ranks against the imdbRating for both festive and non-festive movies?
4) Do you want to know the difference in how the Box Office revenue ranks against the year of release wrt to the imdbRating for both festive and non-festive movies?
