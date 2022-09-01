import requests
import json
from bs4 import BeautifulSoup


url="https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
page=requests.get(url)

a=page.content
soup= BeautifulSoup(a,'html.parser')


Top_movies=[]
def movie_list():
    main_div=soup.find('div',class_='lister')
    tbody=main_div.find('tbody',class_='lister-list')
    trs=tbody.find_all('tr')
    
    movie_ranks=[]
    movie_name=[]
    movie_release=[]
    movie_url=[]
    movie_rating=[]

    for tr in trs:
        position = tr.find('td',class_='titleColumn').get_text().strip()

        rank=' '
        for i in position:
            if '.' not in i:
                rank+=i
            else:
                break
        movie_ranks.append(rank)
        
        title=tr.find('td',class_='titleColumn').a.get_text()
        movie_name.append(title)
        
        year=tr.find('td',class_='titleColumn').span.get_text()
        movie_release.append(year)
            
        rate=tr.find('td',class_='ratingColumn imdbRating').strong.get_text()
        movie_rating.append(rate)
        
        link=tr.find('td',class_='titleColumn').a['href']
        movie_link="https://www.imdb.com"+link
        movie_url.append(movie_link)
        
        
    Details={"Position":" ","Name":" ","Year":" ","Rating":" ","URL":" "}
    for i in range(0,len(movie_ranks)):
        
        Details['Position']=int(movie_ranks[i])
        Details['Name']=str(movie_name[i])
        Details['Year']=(movie_release[i])
        Details['Rating']=float(movie_rating[i])
        Details['URL']=(movie_url[i])
        
        
        Top_movies.append(Details.copy())
        # Detail={"Position":" ","Name":" ","Year":" ","Rating":" ","URL":" "}
    return(Top_movies)
       

        
scrapped=movie_list()

movie_dict={}
def by_year(movies):
    years=[]
    for i in movies:
        year=i['Year']
        if year not in years:
            years.append(year)
            
    movie_dict={i:[]for i in years}
    for i in movies:
        year=i["Year"]
        
        for x in movie_dict:
            if str(x)==str(year):
                movie_dict[x].append(i)
                
    file=json.dumps(movie_dict, indent=4)
    file_open=open('Task_2','w')
    file_write=file_open.write(file)
    file_open.close()
            
    return(movie_dict)
        
print(by_year(scrapped))

