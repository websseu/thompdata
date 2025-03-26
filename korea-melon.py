from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import time

# 현재 날짜를 문자열로 저장
current_date = datetime.now().strftime("%Y-%m-%d")

# 파일 이름 설정
folder_path = "korea/melon"
file_name = f"{folder_path}/melonTop100_{current_date}.json"

# 폴더가 없으면 생성
os.makedirs(folder_path, exist_ok=True)

# 웹드라이버 설정
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# Selenium 웹드라이버로 멜론 차트 페이지 열기
browser = webdriver.Chrome(options=options)
url = "https://www.melon.com/chart/index.htm"
browser.get(url)

# JavaScript 실행 후 페이지가 로드될 시간을 대기
time.sleep(3)

# BeautifulSoup 객체 생성
html = browser.page_source
soup = BeautifulSoup(html, "lxml")

# 데이터 선택
rows = soup.select("tbody tr[data-song-no]")  # 곡 데이터를 포함한 행 선택

# 데이터 저장
chart_data = []

# 데이터 추출
for row in rows:
    # 순위
    ranking = row.select_one(".wrap.t_center > .rank").text.strip()

    # 제목
    title = row.select_one(".wrap_song_info .ellipsis.rank01 span > a").text.strip()

    # 아티스트
    artist = row.select_one(".wrap_song_info .ellipsis.rank02 span > a").text.strip()

    # 이미지 URL
    image = row.select_one(".image_typeAll img").get("src")

    # 앨범
    album = row.select_one(".wrap_song_info .ellipsis.rank03 > a").text.strip()

    # 좋아요 개수 (숫자만 추출, 쉼표 제거)
    like_text = row.select_one("td:nth-child(8) span.cnt").text.strip()
    like_count = ''.join(filter(str.isdigit, like_text))

    # 멜론 아이디
    melon_id = row.get("data-song-no")

    # 데이터 저장
    chart_data.append({
        "ranking": ranking,
        "title": title,
        "artist": artist,
        "image": image,
        "album": album,
        "likes": like_count,
        "melonID": melon_id
    })

# 추출된 데이터를 JSON 파일로 저장
with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(chart_data, f, ensure_ascii=False, indent=4)
    print(f"데이터가 '{file_name}' 파일에 저장되었습니다.")

# 브라우저 닫기
browser.quit()
