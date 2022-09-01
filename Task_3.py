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
        movie_release[i]=movie_release[i][1:5]
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
            
    return(movie_dict)
        


dec_arg=by_year(scrapped)

def by_decade(movies):
    movie_dec={}
    list1=[]
    
    for index in movies:
        index=int(index)
        Mod=index%10
        decade=index-Mod
        
        if decade not in list1:
            list1.append(decade)
    
    list1.sort()
    for i in list1:
        movie_dec[i]=[]
    for i in movie_dec:
        dec10=i+9
        for x in movies:
            if int(x)<=dec10 and int(x)>=i:
                for v in movies[x]:
                    movie_dec[i].append(v)
    
    str=json.dumps(movie_dec, indent=4)
    f=open("Task_3",'w')
    w_f=f.write(str)
    f.close()
    
    return(movie_dec)
 
print(by_decade(dec_arg))     
    

