import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

# 현재 날짜를 문자열로 저장
current_date = datetime.now().strftime("%Y-%m-%d")

# 파일 이름 설정
folder_path = "korea/bugs"
file_name = f"{folder_path}/bugsTop100_{current_date}.json"

# 폴더가 없으면 생성
os.makedirs(folder_path, exist_ok=True)

# 웹 페이지로부터 데이터 요청 및 수신
res = requests.get("https://music.bugs.co.kr/chart")
soup = BeautifulSoup(res.text, "lxml")

# print(res.text)
# print(res.status_code) 

# 데이터 저장
ranking = [ranking.text.strip() for ranking in soup.select("#CHARTrealtime > table > tbody > tr > td:nth-child(4) > div > strong")]
title = [title.text.strip() for title in soup.select("#CHARTrealtime > table > tbody > tr > th > p > a")]
artist = [artist.text.strip() for artist in soup.select("#CHARTrealtime > table > tbody > tr > td:nth-child(8) > p > a:nth-child(1)")]
image = [img['src'].strip() for img in soup.select("#CHARTrealtime > table > tbody > tr > td:nth-child(5) > a > img")]
album = [album.text.strip() for album in soup.select("#CHARTrealtime > table > tbody > tr > td:nth-child(9) > a")]

# print(len(image))

# 데이터 프레임 생성
chart_data = []
for ranking, title, artist, image, album in zip(ranking, title, artist, image, album):
    chart_data.append({
        "ranking": ranking,
        "title": title,
        "artist": artist,
        "image": image,
        "album": album
    })

# 추출된 데이터를 JSON 파일로 저장
with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(chart_data, f, ensure_ascii=False, indent=4)
    print(f"데이터가 '{file_name}' 파일에 저장되었습니다.")