from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import os

# 현재 날짜를 문자열로 저장
current_date = datetime.now().strftime("%Y-%m-%d")

# 파일 이름 설정
folder_path = "korea/flo"
file_name = f"{folder_path}/floTop100_{current_date}.json"

# 폴더가 없으면 생성
os.makedirs(folder_path, exist_ok=True)

# 웹드라이버 설정 및 페이지 로드
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
browser.get("https://www.music-flo.com/browse")

# 웹드라이버 설정(로컬)
# browser = webdriver.Chrome()
# browser.get("https://www.music-flo.com/browse")

# 페이지가 완전히 로드될 때까지 대기
try:
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "chart_lst"))
    )
    print("페이지가 완전히 로드되었습니다.")
except TimeoutException:
    print("요소를 찾는 데 실패했습니다. 페이지가 완전히 로드되지 않았습니다.")
    browser.quit()
    exit()

# '더 보기' 버튼 클릭하여 추가 데이터 로드
try:
    more_button = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn_list_more"))
    )
    if more_button:
        browser.execute_script("arguments[0].click();", more_button)
        print("더보기 버튼을 클릭했습니다.")
        time.sleep(3)
except Exception as e:
    print("더보기 버튼 클릭 에러 : ", e)


# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# print(html_source_updated[:500])

# 데이터 추출
chart_data = []

tracks = soup.select(".chart_lst .track_list_table tbody tr")
for track in tracks:
    ranking = track.select_one(".num").text.strip()
    title = track.select_one(".tit__text").text.strip()
    artist = track.select_one(".artist__link").text.strip()
    album = track.select_one(".album").text.strip()
    image = track.select_one(".thumb img").get('data-src')

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

# 브라우저 종료
browser.quit()
