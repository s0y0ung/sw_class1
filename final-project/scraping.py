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

    req = requests.get(url, headers = custom_header, params={"sid1": sections[section]})
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
    'div.list_body.newsflash_body > ul.type06_headline > li > dl > dt'
    )

data = {}

for title in datas:   
    name = title.find_all('a')[0].text
    url = 'http:'+title.find('a')['href']
    data[name] = url

with open(os.path.join(BASE_DIR, 'news.json'), 'w+',encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii = False, indent='\t')

print('뉴스기사 스크래핑 끝')