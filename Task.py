import requests
from bs4 import BeautifulSoup
url="https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
page=requests.get(url)

a=page.content
soup= BeautifulSoup(a,'html.parser')

scrab_movies=soup.find_all('td',class_='titleColumn')
# print(scrab_movies)


movies=[]
for movie in scrab_movies:
    movie=movie.get_text().replace('\n','')
    movie=movie.strip()
    movies.append(movie)
    
# print(movies)

scrap_year=soup.find_all('span',class_="secondaryInfo")
# print(scrap_year)


years=[]
for year in scrap_year:
    year=year.get_text().replace('\n','')
    year=year.strip()
    years.append(year)
# print(years)


scrap_rating=soup.find_all('td', class_='ratingColumn imdbRating')
# print(scrap_rating)


ratings=[]
for rating in scrap_rating:
    rating=rating.get_text().replace('\n','')
    rating=rating.strip()
    ratings.append(rating)
# print(ratings)