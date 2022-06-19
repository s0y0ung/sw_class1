#!/bin/bash

FILE=song-lyrics.md

if [[ -f "$FILE" ]]; then
	rm $FILE
fi

touch $FILE

echo "# 제목 나비야" >> $FILE

git add $FILE && git commit -m "타이틀"

echo "![나비야 그림](./butterfly.png)" >> $FILE

git add $FILE && git commit -m "그림"

echo "나비야, 나비야 이리 날아오너라" >> $FILE

git add $FILE && git commit -m "첫 나비야 노래"

echo "노랑나비, 흰 나비 춤을 추며 오너라" >> $FILE

git add $FILE && git commit -m "두번쨰 나비야 노래 줄"

echo "봄바람에 꽃잎도 방긋방긋 웃으며" >> $FILE

git add $FILE && git commit -m "세번쨰 나비야 노래 줄"

echo "참새도 짹짹짹 노래하며 춤춘다" >> $FILE

git add $FILE && git commit -m "네번쨰 나비야 노래 줄"

echo "봄바람에 꽃잎도 방긋방긋 웃으며" >> $FILE

git add $FILE && git commit -m "다섯번쨰 나비야 노래 줄"