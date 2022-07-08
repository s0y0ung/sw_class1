import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from pathlib import Path
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

# data = {}
data=list()
i=1
for title,title_photo in zip(datas,datas_photo): 
    if title_photo.select_one('a') is not None:
        imgurl=title_photo.select_one('a').find("img")['src']
    else:
        imgurl='none'
    name = title.text.strip()
    url = title['href']
    print('{0}번째 뉴스\n name: {1} \n url: {2} \n imgurl: {3}'.format(i,name,url,imgurl))
    # data[i]=[[name, url,imgurl]]
    data.append(dict({'name':name, 'url':url,'imgurl': imgurl}))
    i=i+1
print('뉴스기사 스크래핑 끝')

if(os.path.isfile(os.path.join(BASE_DIR, 'news.json'))):
    print('새롭게 업데이트 되었는지 체크 합니다 ✅')
    news_title_oldest=[]
    news_title_latest=[]
    news_latest={}
    # print(os.path.join(BASE_DIR, 'news.json'))

    with open(os.path.join(BASE_DIR, 'news_latest.json'), 'w+',encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii = False, indent='\t')
    with open(os.path.join(BASE_DIR, 'news.json'),'r',encoding='utf-8') as f:
        old_content=json.load(f)
        print('* 기존의 뉴스')
        for item in old_content:
            # print(list(item.values())[0])
            news_title_oldest.append(list(item.values())[0])
        print(news_title_oldest)
        print(len(news_title_oldest))
        with open(os.path.join(BASE_DIR, 'news_latest.json'),'r',encoding='utf-8') as f2:
            latest_content=json.load(f2)
            print('* 최신의 뉴스')
            for item in latest_content:
                # print(list(item.values())[0])
                news_title_latest.append(list(item.values())[0])
            print(news_title_latest)
            print(len(news_title_latest))

            if(news_title_latest[0]!=news_title_oldest[0]):
                print('새롭게 업데이트된 뉴스가 있습니다')
                print(latest_content[0])
                news_latest=latest_content[0]
                with open(os.path.join(BASE_DIR, 'news_latest_one.json'), 'w+',encoding='utf-8') as json_file2:
                    json.dump(news_latest, json_file2, ensure_ascii = False, indent='\t')
            else:
                print('업데이트 되지 않았습니다')

            #news.json을 news_latest.json으로 변환하는 작업
            data_file=Path(os.path.join(BASE_DIR, 'news_latest.json'))
            os.remove(os.path.join(BASE_DIR, 'news.json'))
            data_file.rename('news.json')


else: 
    with open(os.path.join(BASE_DIR, 'news.json'), 'w+',encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii = False, indent='\t')

