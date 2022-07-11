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
    new_content=json.load(f)
  with open(os.path.join(BASE_DIR, 'news_prev_one.json'),'r',encoding='utf-8') as f2:
    prev_content=json.load(f2)

  for i in range(len(prev_content)):    
    readme = open(os.path.join('docs', 'index.md'), "a")
    new_item = new_content[i]
    prev_item = prev_content[i]
    prev_title=prev_item['name']
    prev_url=prev_item['url']
    prev_sec=prev_item['sec']
    readme.write('<div style="border: 2px solid #34a1eb; padding:10px;">\n\n')
    readme.write("## section : " + prev_sec+"\n\n")
    # 업데이트 되었는지 확인
    if 'name' in new_item:
      new_title=new_item['name']
      new_url=new_item['url']
      new_imageurl=new_item['imgurl']

      readme.write("📝 뉴스 제목 : " + new_title+"\n\n")
      # readme.write("![image]("+ new_imageurl+")")
      readme.write('<img src = "' + new_imageurl + '" width="40%" height="40%"/>')
      readme.write("🔗 [link]("+ new_url + ")\n\n")
    else:
      readme.write("새롭게 업데이트 된 뉴스가 없습니다.\n\n")
      
    readme.write("이전 뉴스 : [" + prev_title + "]("+ prev_url + ")\n\n")
    readme.write("</div>")
    readme.write("\n\n\n\n")
    readme.close()
