import requests
from bs4 import BeautifulSoup
import json
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_request(section):
    custom_header = {
        'referer' : 'https://www.naver.com/',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    
    url = "https://news.naver.com/main/list.naver"

    sections = {
        "정치" : 100,
        "경제" : 101,
        "사회" : 102,
        "생활" : 103,
        "세계" : 104,
        "과학" : 105
    }
    para={
        'mode':'LS2D',
        'mid':'shm',
        'sid1':sections[section],
    }

    req = requests.get(url, headers = custom_header, params=para)
    print(url)
    return req


# get category and url
section = input('"정치, 경제, 사회, 생활, 세계, 과학" 중 하나를 입력하세요.\n')
req = get_request(section)
req.encoding= None
html = req.content
soup = BeautifulSoup(html, 'html.parser')


# start scraping
datas = soup.select(
    'div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:not(.photo) > a'
    )
datas_photo= soup.select(
    'div.list_body.newsflash_body > ul.type06_headline > li > dl > dt.photo'
    )
print(datas)
print(datas_photo)
data = {}
i=1
for title,title_photo in zip(datas,datas_photo): 
    if title_photo.select_one('a') is not None:
        imgurl=title_photo.select_one('a').find("img")['src']
        print(imgurl)
    else:
        imgurl='none'
    name = title.text.strip()
    url = title['href']
    print('{0}번째 뉴스\n name: {1} \n url: {2} \n imgurl: {3}'.format(i,name,url,imgurl))
    data[name]=[url,imgurl]
    i=i+1
    

with open(os.path.join(BASE_DIR, 'news.json'), 'w+',encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii = False, indent='\t')

print('뉴스기사 스크래핑 끝')


    

    

