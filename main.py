import requests
from bs4 import BeautifulSoup
def crawler(): 
    
    url = 'https://pcmap.place.naver.com/restaurant/2'
    html = requests.get(url)
    soup = BeautifulSoup(html.content,'html.parser',from_encoding='utf-8')
    print(html.text.find('_3ocDE">')) # -1 = 없는 것임.
    select_point = soup.select('span._3ocDE')[0].text
    print(select_point)
    #select_string = select_point.split('_3ocDE">')[1].split('</')[0]
    #print(select_string)
  

crawler()
