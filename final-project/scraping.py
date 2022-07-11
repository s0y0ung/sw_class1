from selectors import BaseSelector
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
        "polictics" : 100,
        "economy" : 101,
        "society" : 102,
        "life" : 103,
        "world" : 104,
        "science" : 105
    }
    para={
        'mode':'LS2D',
        'mid':'shm',
        'sid1':sections[section],
    }

    req = requests.get(url, headers = custom_header, params=para)
    print(url)
    return req

def category():
    section=['polictics','economy','society','life','world','science']
    for sec in section:
        req = get_request(sec)
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
        file_name_news='news_'+sec+'.json'
        file_name_news_prev='news_prev_'+sec+'.json'
        file_name_news_latest='news_latest_'+sec+'.json'
        file_name_news_oldest='news_oldest_'+sec+'.json'
        file_name_news_latest_one='news_latest_one_'+sec+'.json'
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
            print(sec+ '의 {0}번째 뉴스\n name: {1} \n url: {2} \n imgurl: {3}'.format(i,name,url,imgurl))
            # data[i]=[[name, url,imgurl]]
            data.append(dict({'name':name, 'url':url,'imgurl': imgurl}))
            i=i+1
        print('뉴스기사 스크래핑 끝')

        if(os.path.isfile(os.path.join(BASE_DIR, file_name_news))):
            print('새롭게 업데이트 되었는지 체크 합니다 ✅')
            news_title_oldest=[]
            news_title_latest=[]
            news_latest={}
            # print(os.path.join(BASE_DIR, 'file_name_news'))

            with open(os.path.join(BASE_DIR, file_name_news_latest), 'w+',encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii = False, indent='\t')
            with open(os.path.join(BASE_DIR, file_name_news),'r',encoding='utf-8') as f:
                old_content=json.load(f)
                with open(os.path.join(BASE_DIR, file_name_news_prev), 'w+',encoding='utf-8') as f:
                    json.dump(old_content,f, ensure_ascii = False, indent='\t')
                print('* 기존의 뉴스')
                for item in old_content:
                    # print(list(item.values())[0])
                    news_title_oldest.append(list(item.values())[0])
                print(news_title_oldest)
                print(len(news_title_oldest))
                with open(os.path.join(BASE_DIR, file_name_news_latest),'r',encoding='utf-8') as f:
                    latest_content=json.load(f)
                    print('* 최신의 뉴스')
                    for item in latest_content:
                        # print(list(item.values())[0])
                        news_title_latest.append(list(item.values())[0])
                    print(news_title_latest)
                    print(len(news_title_latest))

                    if(news_title_latest[0]!=news_title_oldest[0]):
                        print('* 새롭게 업데이트된'+sec+' 분야의 뉴스가 있습니다')
                        print(latest_content[0])
                        news_latest=latest_content[0]
                        with open(os.path.join(BASE_DIR, file_name_news_latest_one), 'w+',encoding='utf-8') as f:
                            json.dump(news_latest, f, ensure_ascii = False, indent='\t')
                    else:
                        str={'업데이트':'x'}
                        print('* 업데이트 되지 않았습니다.')
                        with open(os.path.join(BASE_DIR, file_name_news_latest_one), 'w+',encoding='utf-8') as f:
                            json.dump(str, f, ensure_ascii = False, indent='\t')
                        

                    #news_latest.json을 file_name_news으로 변환하는 작업
                    data_file=Path(os.path.join(BASE_DIR, file_name_news_latest))
                    os.remove(os.path.join(BASE_DIR, file_name_news))
                    data_file.rename(os.path.join(BASE_DIR, file_name_news))


        else: 
            with open(os.path.join(BASE_DIR, file_name_news), 'w+',encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii = False, indent='\t')

def combine_news_latest():
    news_list=[]
    news_latest_list=['news_latest_one_polictics','news_latest_one_economy','news_latest_one_science','news_latest_one_society','news_latest_one_life','news_latest_one_world']
    for file_name in news_latest_list:
        with open(os.path.join(BASE_DIR, file_name+'.json'), 'r',encoding='utf-8') as f:
            content=json.load(f)
            news_list.append(content)
    with open(os.path.join(BASE_DIR,'news_latest_one.json'),'w+',encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii = False, indent='\t')
    
if __name__ == "__main__" :
  category()
  combine_news_latest()