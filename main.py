import pandas
import requests
from datetime import datetime
import csv
import os
import random
import io
import plotly.express as px
from csv import DictReader

festiveDates = {}
festiveDates['christmas'] = {}
festiveDates['christmas']['month'] = 12
festiveDates['christmas']['day'] = 23
festiveDates['haloween'] = {}
festiveDates['haloween']['month'] = 11
festiveDates['haloween']['day'] = 30
festiveDates['valentine'] = {}
festiveDates['valentine']['month'] = 2
festiveDates['valentine']['day'] = 14

cachedMovies = set()
def isFestiveRelease(releaseDate):
    releaseDate = datetime.strptime(releaseDate, '%Y-%m-%d %H:%M:%S')
    # change based on input accepted in program
    input = 'christmas'
    monthBeforeValidated = festiveDates[input]['month'] - 1
    if(monthBeforeValidated == 0):
        monthBeforeValidated = 12
    monthBefore = datetime(releaseDate.year, monthBeforeValidated, festiveDates[input]['day'])
    festiveDate = datetime(releaseDate.year, festiveDates[input]['month'], festiveDates[input]['day'])
    if (releaseDate >= monthBefore and releaseDate <= festiveDate):
        return True
    return False
#
def getImdbRating(rating):
    if (rating):
        for i in rating:
            if (i.get("Source") and i.get("Source") == 'Internet Movie Database'):
                return i.get("Value").split('/')[0]
    return -1
#
def processMovie(moviename):
    response = requests.get('https://www.omdbapi.com', params = {'t': moviename,'apikey': 'e70fc0a9'}).json()
    #print(response)

    if (response and response.get('Response') == 'True'):
        #print(response)
        movieName = response.get('Title')
        releaseDate = response.get('Released')
        boxOffice = response.get('BoxOffice')
        title = response.get('Title')

        if (releaseDate and releaseDate != 'N/A' and boxOffice and boxOffice != 'N/A' and title.lower() not in cachedMovies):
            attributesToExtract = { 'Title', 'Year', 'Genre', 'Language', 'BoxOffice' }
            responseObject = { key:value for key,value in response.items() if key in attributesToExtract}
            responseObject['ReleasedDate'] = datetime.strptime(releaseDate, '%d %b %Y')
            responseObject['imdbRating'] = getImdbRating(response.get('Ratings'))
            return responseObject
        else:
            print('Movie from input source not found in OMDB API : ' + movieName)
    #rating=response.get('Ratings')
    #   response = requests.get('https://www.omdbapi.com', params = {'t':"home+alone",'apikey: 63ba843})
recordsToWrite = []
counter = 0

#
# # # Read cached files
directory = os.path.join("C:\\","Users\\krith\\OneDrive\\Desktop\\SI 507\\Final_Project\\cache")
for root, dirs, files in os.walk(directory):
    for file in files:
        print(file)
        if file.endswith(".csv"):
            with open(directory + '/' + file, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        cachedMovieName = row[0]
                        # cachedMovieName = row[0].split(',')[0];
                        if(cachedMovieName not in cachedMovies):
                            cachedMovies.add(cachedMovieName)
                        line_count += 1
cachedMovies = set(i.lower() for i in cachedMovies)
print('Cached data:')
print(len(cachedMovies))
print(cachedMovies)

#
# # # Process Input source with cache
sourceFile = open('christmas.csv', encoding="utf-8")
inputData = pandas.read_csv(sourceFile, encoding='utf-8', delimiter=',')
print('InputData count: ' + str(len(inputData.values)))
for inputRecord in inputData.values:
    if (counter > 100):
        break
    movieName = inputRecord[2]
    lowerMovieName = movieName.lower()
    if lowerMovieName in cachedMovies:
        print("Movie in cache.. skipping. Name: " + movieName)
    else:
        print("Movie not in cache.. making API call to OMDB: " + movieName)
        recordToWrite = processMovie(movieName)
        if (recordToWrite):
            counter = counter + 1
            recordsToWrite.append(recordToWrite)
#
# # # Write new items from API to cache
fieldNames = ['Title', 'Year', 'Genre', 'Language', 'BoxOffice', 'ReleasedDate', 'imdbRating']
randomNumber = random.random()
fileName = 'cache\\cacheFile_' + str(randomNumber) + '.csv'
with open(fileName, 'w', newline='') as csvFile:
    csvwriter = csv.DictWriter(csvFile, fieldNames)
    csvwriter.writeheader()
    csvwriter.writerows(recordsToWrite)
print('Done writing new cache file')


# Read updated cache files and prepare datasets along with tree structure


holiday=input("Which holiday do you want movie recommendations for ? Christmas, Halloween or Valentine's Day :   ")
if holiday=="christmas":
    old_new=input("Do you want to watch old movies or new movies?")
    rating=input("What imdbRating do you prefer? Good or Bad?")   
    if old_new=="old":
        directory = os.path.join("C:\\", "Users\\krith\\OneDrive\\Desktop\\SI 507\\Final_Project\\cache")
        df = pandas.read_csv(directory +'/cacheFile_0.909260870295638.csv')
        out = df.to_json(orient='records')[1:-1].replace('},{', '} {')
        with open(directory + '/tree_records.json', 'w') as f:
            f.write(out)
        with open(directory + '/cacheFile_0.909260870295638.csv' , 'r') as f:
            dict_reader = DictReader(f)
            list_of_dict = list(dict_reader)
            expectedResult = [d for d in list_of_dict if (d['Year'] < '2003')]

 
    else:
        directory = os.path.join("C:\\", "Users\\krith\\OneDrive\\Desktop\\SI 507\\Final_Project\\cache")
        df = pandas.read_csv(directory +'/cacheFile_0.909260870295638.csv')
        with open(directory + '/cacheFile_0.909260870295638.csv' , 'r') as f:
            dict_reader = DictReader(f)
            list_of_dict = list(dict_reader)
            expectedResult = [d for d in list_of_dict if d['Year'] > '2003'] 
 
        
    print("Top movies based on your suggestion:") 
    for i in expectedResult:
        print(i['Title'])  
featureMovieSet = set()
festiveRecords = []
nonFestiveRecords = []
directory = os.path.join("C:\\", "Users\\krith\\OneDrive\\Desktop\\SI 507\\Final_Project\\cache")
for root, dirs, files in os.walk(directory):
    for file in files:
        # print(file)
        if file.endswith(".csv"):
            with open(directory + '/' + file, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        featureMovieName = row[0]
                        featureYear = row[1]
                        featureBoxOffice = row[4].replace('$', '')
                        featureBoxOffice = featureBoxOffice.replace(',', '')
                        featureReleaseDate = row[5]

                        # print(featureReleaseDate)
                        featureRating = row[6]
                        tuple = (featureMovieName,featureYear, featureBoxOffice,featureReleaseDate, featureRating)
                        if(featureMovieName not in featureMovieSet):
                            featureMovieSet.add(featureMovieName)
                            if(isFestiveRelease(featureReleaseDate)):
                                festiveRecords.append(tuple)
                            else:
                                nonFestiveRecords.append(tuple)
                        line_count += 1
# print(festiveRecords)
# print(nonFestiveRecords)
fieldNames = ['Title', 'Year','BoxOffice','ReleaseDate', 'imdbRating','Genre']
directory = os.path.join("C:\\", "Users\\krith\\OneDrive\\Desktop\\SI 507\\Final_Project")
with open(directory + '/festive_data_set.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(fieldNames)
    for row in festiveRecords:
        csv_out.writerow(row)
with open(directory + '/non_festive_data_set.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(fieldNames)
    for row in nonFestiveRecords:
        csv_out.writerow(row)
festive_df = pandas.read_csv(directory+'/festive_data_set.csv')
print('Correlation in movie data set released on festive dates')
print(festive_df.corr())
non_festive_df = pandas.read_csv(directory+'/non_festive_data_set.csv')
print('Correlation in movie data set released on non-festive dates')
print(non_festive_df.corr())


trend1= input("Do you want to know the difference in how the imdb ratings rank against the box office collection for both festive and non-festive movies?")
if trend1=="yes":

    non_festive_fig = px.bar(non_festive_df, x="imdbRating", y="BoxOffice", title="Non Festive movie scatterplot")
    non_festive_fig.show()

    festive_fig = px.bar(festive_df, x="imdbRating", y="BoxOffice", title="Festive movie scatterplot")
    festive_fig.show()
else:
    print("No problem , we have a few more trends to show you!")


trend2= input("Want to see how the box office collection ranks against the year of release for both festive and non-festive movies?")
if trend2=="yes":
    nf_year_fig= px.scatter(non_festive_df, x="BoxOffice", y="Year", title="Non Festive movie scatterplot with box office and year of release")
    nf_year_fig.show()

    f_year_fig= px.scatter(festive_df, x="BoxOffice", y="Year", title="Festive movie scatterplot with box office and year of release")
    f_year_fig.show()
else:
    print("No problem , we have a few more trends to show you!")

trend3= input("Youll be surprised in how the Year ranks against the imdbRating for both festive and non-festive movies?")
if trend3=="yes":

    nf_bo_fig= px.scatter(non_festive_df, x="Year", y="imdbRating", title="Non Festive movie line graph where Year ranks against the imdbRating")
    nf_bo_fig.show()

    f_bo_fig= px.scatter(festive_df, x="Year", y="imdbRating", title="Festive movie line graph where Year ranks against the imdbRating")
    f_bo_fig.show()

else:
    print("No problem , we have a few more trends to show you!")


trend4= input("Do you want to know the difference in how the Box Office revenue ranks against the year of release wrt to the imdbRating for both festive and non-festive movies?")
if trend3=="yes":
    nf_genre_fig= px.scatter(non_festive_df, x="Year", y="BoxOffice",color="imdbRating", title="Non Festive movie scatterplot with revenue and year of release")
    nf_genre_fig.show()


    f_genre_fig= px.scatter(festive_df, x="Year", y="BoxOffice",color="imdbRating", title="Festive movie scatterplot with revenue and year of release")
    f_genre_fig.show()

else:
    print("This is the end of the graphs!")
