from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json
import time

# 현재 날짜를 문자열로 저장
current_date = datetime.now().strftime("%Y-%m-%d")

# 국가별 URL 설정
countries = {
    "global": "https://charts.youtube.com/charts/TopSongs/global/weekly",
    "argentina": "https://charts.youtube.com/charts/TopSongs/ar/weekly",
    "australia": "https://charts.youtube.com/charts/TopSongs/au/weekly",
    "austria": "https://charts.youtube.com/charts/TopSongs/at/weekly",
    "belgium": "https://charts.youtube.com/charts/TopSongs/be/weekly",
    "bolivia": "https://charts.youtube.com/charts/TopSongs/bo/weekly",
    "brazil": "https://charts.youtube.com/charts/TopSongs/br/weekly",
    "canada": "https://charts.youtube.com/charts/TopSongs/ca/weekly",
    "chile": "https://charts.youtube.com/charts/TopSongs/cl/weekly",
    "colombia": "https://charts.youtube.com/charts/TopSongs/co/weekly",
    "costa-rica": "https://charts.youtube.com/charts/TopSongs/cr/weekly",
    "czechia": "https://charts.youtube.com/charts/TopSongs/cz/weekly",
    "denmark": "https://charts.youtube.com/charts/TopSongs/dk/weekly",
    "dominican_republic": "https://charts.youtube.com/charts/TopSongs/do/weekly",
    "ecuador": "https://charts.youtube.com/charts/TopSongs/ec/weekly",
    "egypt": "https://charts.youtube.com/charts/TopSongs/eg/weekly",
    "el-salvador": "https://charts.youtube.com/charts/TopSongs/sv/weekly",
    "estonia": "https://charts.youtube.com/charts/TopSongs/ee/weekly",
    "finland": "https://charts.youtube.com/charts/TopSongs/fi/weekly",
    "france": "https://charts.youtube.com/charts/TopSongs/fr/weekly",
    "germany": "https://charts.youtube.com/charts/TopSongs/de/weekly",
    "guatemala": "https://charts.youtube.com/charts/TopSongs/gt/weekly",
    "honduras": "https://charts.youtube.com/charts/TopSongs/hn/weekly",
    "hungary": "https://charts.youtube.com/charts/TopSongs/hu/weekly",
    "iceland": "https://charts.youtube.com/charts/TopSongs/is/weekly",
    "india": "https://charts.youtube.com/charts/TopSongs/in/weekly",
    "indonesia": "https://charts.youtube.com/charts/TopSongs/id/weekly",
    "israel": "https://charts.youtube.com/charts/TopSongs/il/weekly",
    "italy": "https://charts.youtube.com/charts/TopSongs/it/weekly",
    "japan": "https://charts.youtube.com/charts/TopSongs/jp/weekly",
    "kenya": "https://charts.youtube.com/charts/TopSongs/ke/weekly",
    "luxembourg": "https://charts.youtube.com/charts/TopSongs/lu/weekly",
    "mexico": "https://charts.youtube.com/charts/TopSongs/mx/weekly",
    "netherlands": "https://charts.youtube.com/charts/TopSongs/nl/weekly",
    "new-zealand": "https://charts.youtube.com/charts/TopSongs/nz/weekly",
    "nicaragua": "https://charts.youtube.com/charts/TopSongs/ni/weekly",
    "nigeria": "https://charts.youtube.com/charts/TopSongs/ng/weekly",
    "norway": "https://charts.youtube.com/charts/TopSongs/no/weekly",
    "panama": "https://charts.youtube.com/charts/TopSongs/pa/weekly",
    "paraguay": "https://charts.youtube.com/charts/TopSongs/py/weekly",
    "peru": "https://charts.youtube.com/charts/TopSongs/pe/weekly",
    "poland": "https://charts.youtube.com/charts/TopSongs/pl/weekly",
    "portugal": "https://charts.youtube.com/charts/TopSongs/pt/weekly",
    "romania": "https://charts.youtube.com/charts/TopSongs/ro/weekly",
    "russia": "https://charts.youtube.com/charts/TopSongs/ru/weekly",
    "saudi-arabia": "https://charts.youtube.com/charts/TopSongs/sa/weekly",
    "serbia": "https://charts.youtube.com/charts/TopSongs/rs/weekly",
    "south-africa": "https://charts.youtube.com/charts/TopSongs/za/weekly",
    "south-korea": "https://charts.youtube.com/charts/TopSongs/kr/weekly",
    "spain": "https://charts.youtube.com/charts/TopSongs/es/weekly",
    "sweden": "https://charts.youtube.com/charts/TopSongs/se/weekly",
    "switzerland": "https://charts.youtube.com/charts/TopSongs/ch/weekly",
    "tanzania": "https://charts.youtube.com/charts/TopSongs/tz/weekly",
    "turkey": "https://charts.youtube.com/charts/TopSongs/tr/weekly",
    "uganda": "https://charts.youtube.com/charts/TopSongs/ug/weekly",
    "ukraine": "https://charts.youtube.com/charts/TopSongs/ua/weekly",
    "united-arab-emirates": "https://charts.youtube.com/charts/TopSongs/ae/weekly",
    "united-kingdom": "https://charts.youtube.com/charts/TopSongs/gb/weekly",
    "united-states": "https://charts.youtube.com/charts/TopSongs/us/weekly",
    "uruguay": "https://charts.youtube.com/charts/TopSongs/uy/weekly",
    "zimbabwe": "https://charts.youtube.com/charts/TopSongs/zw/weekly"
}

# 파일 이름 설정
folder_path = "youtube"
os.makedirs(folder_path, exist_ok=True) 

# 웹드라이버 설정 및 페이지 로드
options = ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("prefs", {"intl.accept_languages": "en-US,en"})
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
browser = webdriver.Chrome(options=options)


# 나라별 데이터 수집
for country, url in countries.items():
    print(f"Processing {country}...")

    # 국가별 폴더 생성
    country_folder = os.path.join(folder_path, country)
    os.makedirs(country_folder, exist_ok=True)

    # 브라우저로 URL 열기
    browser.get(url)
    time.sleep(10)  # 페이지 로드 대기

    # HTML 데이터 파싱
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # 데이터 추출
    data = []
    rows = soup.find_all('ytmc-entry-row')  # 각 row를 선택

    for row in rows:
        # 랭킹 추출
        rank_element = row.find('span', {'id': 'rank'})
        ranking = rank_element.text.strip() if rank_element else None

        # 제목 추출
        title_element = row.find('div', {'id': 'entity-title'})
        title = title_element.text.strip() if title_element else None

        # 가수 추출
        artist_element = row.select_one("div#artist-names > span[hidden]")
        artist = artist_element.text.strip() if artist_element else None

        # 이미지 URL 추출
        img_element = row.select_one("div.thumbnail-container > img#thumbnail")
        image = img_element['src'] if img_element else None

        # 지난주 랭킹 추출
        prev_element = row.select_one("div.data-table-container > div:nth-child(4)")
        prev = prev_element.text.strip() if prev_element else None

        # 지속 기간 추출
        streak_element = row.select_one("div.data-table-container > div:nth-child(5)")
        streak = streak_element.text.strip() if streak_element else None

        # 주간 조회수 추출
        streams_element = row.select_one("div.data-table-container > div:nth-child(6)")
        streams = streams_element.text.strip() if streams_element else None

        # YouTube ID 추출
        youtube_element = row.select_one("div.thumbnail-container > img#thumbnail")

        if youtube_element and "endpoint" in youtube_element.attrs:
            # endpoint 속성에서 URL을 추출
            endpoint = youtube_element["endpoint"]
            # watch?v= 이후의 값을 추출
            youtubeID = endpoint.split("watch?v=")[-1].split('"')[0] if "watch?v=" in endpoint else None
        else:
            youtubeID = None

        # 데이터 저장
        data.append({
            "ranking": ranking,
            "title": title,
            "artist": artist,
            "image": image,
            "prev": prev,
            "streak": streak,
            "streams": streams,
            "youtubeID": youtubeID,
        })

    # 국가별 JSON 파일 경로 설정
    json_file_name = os.path.join(country_folder, f"{country}Top100_{current_date}.json")

    # JSON 파일로 저장
    with open(json_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    # JSON 저장 완료 메시지
    print(f"Data for {country} saved in {json_file_name}")

# 브라우저 닫기
browser.quit()