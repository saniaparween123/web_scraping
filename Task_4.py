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
    # print(tbody)
    for tr in trs:
        position = tr.find('td',class_='titleColumn').get_text().strip()
        # print(position)

        rank=' '
        for i in position:
            # print(i)
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
       

        
scrap=movie_list

def scrap_movie_details(movie_url):
    page=requests.get(movie_url)
    soup= BeautifulSoup(page.text, 'html.parser')
    
    #now scrap movie name
    title_div=soup.find('div', class_='sc-80d4314-1 fbQftq').h1.get_text()
    runtime=soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-none ipc-metadata-list--compact ipc-metadata-list--base").li.div.get_text()

    hours=int(runtime[0])*60
    
    if 'minutes' in runtime:
        run_min=int(runtime[8:].strip('minutes'))
        movie_runtime=hours+run_min
    else:
        movie_runtime=hours  
        
    #now scrap movie gener
    gener_scrap=soup.find('div',class_="ipc-chip-list__scroller")
    s=gener_scrap.find_all('span')
    
    
    gener=[]
    for i in s:
        gener.append(i.get_text())
        
    
    sumary=soup.find('div',class_="sc-16ede01-7 hrgVKw").get_text()
    dir=soup.find('li',class_='ipc-metadata-list__item').div.get_text()
    director=list(dir.split(" "))
    
    
    movie_poster=soup.find('div',class_="ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width sc-d383958-0 gvOdLN celwidget ipc-sub-grid-item ipc-sub-grid-item--span-2").a['href']
    poster_link="http://www.imdb.com"+movie_poster
    
    movie_details={"Name":"","Director":"","Runtime":"","Gener":"","Poster_image":"","Bio":""}
    
    
    movie_details["Name"]= title_div
    movie_details["Director"]=director
    movie_details["Bio"]=sumary
    movie_details["Runtime"]=movie_runtime
    movie_details["Gener"]=gener
    movie_details["Poster_image"]=poster_link
    
    
    a=json.dumps(movie_details, indent=4)
    file=open('Details_of_movie','w')
    write=file.write(a)
    return(movie_details)
            
            
url1="https://www.imdb.com/title/tt9263550/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=690bec67-3bd7-45a1-9ab4-4f274a72e602&pf_rd_r=C6M3SMFF3SJ2TDM51P6B&pf_rd_s=center-4&pf_rd_t=60601&pf_rd_i=india.top-rated-indian-movies&ref_=fea_india_ss_toprated_tt_1"
print(scrap_movie_details(url1))
  