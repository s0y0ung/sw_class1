import json
import os
import sys
from pathlib import Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.getcwd()
print(INDEX_DIR)

if(os.path.isfile(os.path.join(BASE_DIR, 'news_latest_one.json'))):
  os.remove(os.path.join('docs', 'index.md'))

  with open(os.path.join(BASE_DIR, 'news_latest_one.json'),'r',encoding='utf-8') as f:
    content=json.load(f)
    for item in content:
      title=item['name']
      url=item['url']
      imageurl=item['imgurl']
      sec=item['sec']

      readme = open(os.path.join('docs', 'index.md'), "a")
      readme.write("### section : " + sec+"\n")
      readme.write("📝 뉴스 제목 : " + title+"\n")
      readme.write("![image]("+ imageurl+")" +"        ")
      readme.write("🔗 [link]("+ url + ")\n")
      readme.close()
