import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

# 현재 날짜를 문자열로 저장
current_date = datetime.now().strftime("%Y-%m-%d")

# 파일 이름 설정
folder_path = "korea/genie"
file_name = f"{folder_path}/genieTop100_{current_date}.json"

# 폴더가 없으면 생성
os.makedirs(folder_path, exist_ok=True)

# 웹 페이지로부터 데이터 요청 및 수신(웹 서버가 자동 스크립트를 막아놓은 경우 우회할 때 사용)
head = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

# 두 개의 페이지 URL 리스트
urls = [
    "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20241105&hh=10&rtm=Y&pg=1",
    "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20241105&hh=10&rtm=Y&pg=2"
]

# 전체 차트 데이터를 저장할 리스트
chart_data = []

# 각 페이지에서 데이터 수집
for url in urls:
    res = requests.get(url, headers=head)
    soup = BeautifulSoup(res.text, "lxml")

    # 데이터 선택
    rows = soup.select("tr.list")
    for row in rows:
        # 데이터를 추출하여 변수에 저장
        ranking = row.select_one("td.number").contents[0].strip()
        image = row.select_one("td a.cover img").get('src').replace('//', 'https://')
        title = row.select_one("td.info a.title.ellipsis").text.strip()
        artist = row.select_one("td.info a.artist.ellipsis").text.strip()
        album = row.select_one("td.info a.albumtitle.ellipsis").text.strip()

        # 한 곡의 데이터를 dictionary 형태로 저장
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