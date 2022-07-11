import json
import os
import sys
from pathlib import Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.getcwd()
# print(INDEX_DIR)

if(os.path.isfile(os.path.join(BASE_DIR, 'news_latest_one.json'))):

  with open(os.path.join(BASE_DIR, 'news_latest_one.json'),'r',encoding='utf-8') as f:
    content=json.load(f)
    title=content['name']
    url=content['url']
    imageurl=content['imgurl']

  readme = open(os.path.join('docs', 'index.md'), "w")
  readme.write("📝 뉴스 제목 : " + title+"\n")
  readme.write("![ 뉴스 이미지] ("+ imageurl+")" +"\n")
  readme.write(" 🔗 뉴스 링크 : "+ url)
  readme.close()
