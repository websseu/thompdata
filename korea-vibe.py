from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from bs4 import BeautifulSoup
import os
import json
import time

# 현재 날짜를 문자열로 저장
current_date = datetime.now().strftime("%Y-%m-%d")

# 파일 이름 설정
folder_path = "korea/vibe"
file_name = f"{folder_path}/vibeTop100_{current_date}.json"

# 폴더가 없으면 생성
os.makedirs(folder_path, exist_ok=True)

# 웹드라이버 설정 및 페이지 로드
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
browser.get("https://vibe.naver.com/chart/total")

# 웹드라이버 설정(로컬)
# browser = webdriver.Chrome()
# browser.get("https://vibe.naver.com/chart/total")

# 페이지가 완전히 로드될 때까지 대기
try:
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tracklist"))
    )
    print("페이지가 완전히 로드되었습니다.")
    time.sleep(3)
except TimeoutException:
    print("요소를 찾는 데 실패했습니다. 페이지가 완전히 로드되지 않았습니다.")
    browser.quit()
    exit()

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# print(html_source_updated)

# 차트 정보를 저장할 리스트
chart_data = []

# 데이터 추출
tracks = soup.select(".tracklist table tbody tr")

for track in tracks:
    # 순위, 제목, 아티스트, 앨범 정보 추출
    ranking = track.select_one(".rank .text").text.strip() if track.select_one(".rank .text") else None
    title = track.select_one(".song .link_text span").text.strip() if track.select_one(".song .link_text span") else None
    artist = track.select_one(".artist .text").text.strip() if track.select_one(".artist .text") else None
    album = track.select_one(".album .link").text.strip() if track.select_one(".album .link") else None
    image = track.select_one(".thumb img")['src'] if track.select_one(".thumb img") else None
    
    # 수집된 정보를 딕셔너리에 저장
    chart_data.append({
        "ranking": ranking,
        "title": title,
        "artist": artist,
        "album": album,
        "image": image
    })

# 추출된 데이터를 JSON 파일로 저장
with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(chart_data, f, ensure_ascii=False, indent=4)
    print(f"데이터가 '{file_name}' 파일에 저장되었습니다.")
  
# 브라우저 종료
browser.quit()
