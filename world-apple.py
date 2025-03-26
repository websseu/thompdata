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

# 국가별 URL 및 폴더 설정
countries = {
    "global": "https://music.apple.com/us/playlist/top-100-global/pl.d25f5d1181894928af76c85c967f8f31",
    "antigua-and-barbuda": "https://music.apple.com/us/playlist/top-100-antigua-and-barbuda/pl.cca0d50798424e4e871820a03719e841",
    "argentina": "https://music.apple.com/us/playlist/top-100-argentina/pl.7ae8594e422f44658e58212d876d9323",
    "armenia": "https://music.apple.com/us/playlist/top-100-armenia/pl.42abb2144d594137a8fb4d37a9f35b42",
    "australia": "https://music.apple.com/us/playlist/top-100-australia/pl.18be1cf04dfd4ffb9b6b0453e8fae8f1",
    "austria": "https://music.apple.com/us/playlist/top-100-austria/pl.f34430d010a843128337927bba98048b",
    "azerbaijan": "https://music.apple.com/us/playlist/top-100-azerbaijan/pl.ccc31c81303c405baddaaf0f5328b7f3",
    "bahrain": "https://music.apple.com/us/playlist/top-100-bahrain/pl.02a8276fa4ca40b19ac248fda4725fbb",
    "barbados": "https://music.apple.com/us/playlist/top-100-barbados/pl.13743dcd86174ea5b4cb6b2534637e23",
    "belarus": "https://music.apple.com/us/playlist/top-100-belarus/pl.50c1747c37404a9aa07acc39316f6873",
    "belgium": "https://music.apple.com/us/playlist/top-100-belgium/pl.cefe84f7916b4cae8b21b0a78e948380",
    "belize": "https://music.apple.com/us/playlist/top-100-belize/pl.c6d8b5dcf6814168a4b0262628d3a317",
    "bolivia": "https://music.apple.com/us/playlist/top-100-bolivia/pl.cfcd547b034d47648a16fb8e2df0623f",
    "botswana": "https://music.apple.com/us/playlist/top-100-botswana/pl.73bb3593281444fb8ab21d58ccab4600",
    "brazil": "https://music.apple.com/us/playlist/top-100-brazil/pl.11ac7cc7d09741c5822e8c66e5c7edbb",
    "bulgaria": "https://music.apple.com/us/playlist/top-100-bulgaria/pl.040cf0b4c7e9467eb9eed2d33e7a29d6",
    "cambodia": "https://music.apple.com/us/playlist/top-100-cambodia/pl.9d9ee12c7734402ab5ab0dc81911822c",
    "cape-verde": "https://music.apple.com/us/playlist/top-100-cape-verde/pl.917f294713a34cdeb46e67ad2a137067",
    "chile": "https://music.apple.com/us/playlist/top-100-chile/pl.81015bbbefdd46758b2c8c7065f0863e",
    "china": "https://music.apple.com/us/playlist/top-100-china/pl.fde851dc95ce4ffbb74028dfd254ced5",
    "colombia": "https://music.apple.com/us/playlist/top-100-colombia/pl.d116fa6286734b74acff3d38a740fe0d",
    "costa-rica": "https://music.apple.com/us/playlist/top-100-costa-rica/pl.7771c20fc0354f64a723ae9c11a4d5f5",
    "cyprus": "https://music.apple.com/us/playlist/top-100-cyprus/pl.a5ae21745d1d45edacb68971746d31ae",
    "czechia": "https://music.apple.com/us/playlist/top-100-czechia/pl.e447d9ba54254130a76143bf6fdfa65c",
    "denmark": "https://music.apple.com/us/playlist/top-100-denmark/pl.d08496850bc840a4874e877177a69f9f",
    "dominica": "https://music.apple.com/us/playlist/top-100-dominica/pl.68e6ad675521400487ea78463b39899d",
    "dominican-republic": "https://music.apple.com/us/playlist/top-100-dominican-republic/pl.deec8b036583481782c40a2a05554b0b",
    "ecuador": "https://music.apple.com/us/playlist/top-100-ecuador/pl.41b0d399afea495699dbc7660994a96c",
    "egypt": "https://music.apple.com/us/playlist/top-100-egypt/pl.a0b3d0b9a2764646b59ccacdf82e3544",
    "el-salvador": "https://music.apple.com/us/playlist/top-100-el-salvador/pl.9a175d1e9b1e4c81bfa7c63f28c1a79e",
    "estonia": "https://music.apple.com/us/playlist/top-100-estonia/pl.054734b06c7742a985805f45a283bcb4",
    "micronesia": "https://music.apple.com/us/playlist/top-100-micronesia/pl.bee910bc105b43c28eed7d20e4e09a8c",
    "fiji": "https://music.apple.com/us/playlist/top-100-fiji/pl.1e2c1286034c49b78139d2b4ff499a94",
    "finland": "https://music.apple.com/us/playlist/top-100-finland/pl.acea41a017664a8ebcd5aa1622aecc88",
    "france": "https://music.apple.com/us/playlist/top-100-france/pl.6e8cfd81d51042648fa36c9df5236b8d",
    "gambia": "https://music.apple.com/us/playlist/top-100-gambia/pl.62e12ecd522d47858321846adcaac43d",
    "germany": "https://music.apple.com/us/playlist/top-100-germany/pl.c10a2c113db14685a0b09fa5834d8e8b",
    "ghana": "https://music.apple.com/us/playlist/top-100-ghana/pl.78f1974e882d4952b26ebfb8e017c933",
    "greece": "https://music.apple.com/us/playlist/top-100-greece/pl.0f15f3a8ba014979b9fdd7a0ef906dca",
    "grenada": "https://music.apple.com/us/playlist/top-100-grenada/pl.b14c0257c1744d2686f88d05ab1efb4c",
    "guatemala": "https://music.apple.com/us/playlist/top-100-guatemala/pl.7235b4236ee241f083f8026d372cc2d8",
    "guinea-bissau": "https://music.apple.com/us/playlist/top-100-guinea-bissau/pl.ac455234996b468b9f58e573752ab05c",
    "honduras": "https://music.apple.com/us/playlist/top-100-honduras/pl.ec6d493f976349dfb0cba8f6c2f7e937",
    "hong-kong": "https://music.apple.com/us/playlist/top-100-hong-kong/pl.7f35cffa10b54b91aab128ccc547f6ef",
    "hungary": "https://music.apple.com/us/playlist/top-100-hungary/pl.cee165c3a51e466481bde5de75d6dee3",
    "india": "https://music.apple.com/us/playlist/top-100-india/pl.c0e98d2423e54c39b3df955c24df3cc5",
    "indonesia": "https://music.apple.com/us/playlist/top-100-indonesia/pl.2b7e089dc9ef4dd7a18429df9c6e26a3",
    "israel": "https://music.apple.com/us/playlist/top-100-israel/pl.0c9765e5330048af96c2336fa7bc3525",
    "italy": "https://music.apple.com/us/playlist/top-100-italy/pl.737e067787df485a8062e2c4927d94db",
    "japan": "https://music.apple.com/us/playlist/top-100-japan/pl.043a2c9876114d95a4659988497567be",
    "jordan": "https://music.apple.com/us/playlist/top-100-jordan/pl.5adf310412994d9483918fcd8e091fc5",
    "kazakhstan": "https://music.apple.com/us/playlist/top-100-kazakhstan/pl.27d3c4d63b0e41f29f79c98bb5a090e1",
    "kenya": "https://music.apple.com/us/playlist/top-100-kenya/pl.0b36ea82865d4adeb9d1d62207aab172",
    "kyrgyzstan": "https://music.apple.com/us/playlist/top-100-kyrgyzstan/pl.5318aa72adb84bcfac803ecaf6156325",
    "laos": "https://music.apple.com/us/playlist/top-100-laos/pl.42b3fe9c75a947ab84a80019e7bcd704",
    "latvia": "https://music.apple.com/us/playlist/top-100-latvia/pl.5ac047a9ada144aebb9b2f16f5bc8c1d",
    "lebanon": "https://music.apple.com/us/playlist/top-100-lebanon/pl.838a4daba8924c42969ca7162fdc74da",
    "lithuania": "https://music.apple.com/us/playlist/top-100-lithuania/pl.e96de57d836e42dca30f7da24c64bbea",
    "luxembourg": "https://music.apple.com/us/playlist/top-100-luxembourg/pl.2f85377267d74a13be02a53882a5b488",
    "malaysia": "https://music.apple.com/us/playlist/top-100-malaysia/pl.a165defeeccb4b17a59bb5c85637b9b7",
    "malta": "https://music.apple.com/us/playlist/top-100-malta/pl.06ab782ba2324ae49317d6bde84eef56",
    "mauritius": "https://music.apple.com/us/playlist/top-100-mauritius/pl.5e6efed969354b378770c2ea6f2fed6b",
    "mexico": "https://music.apple.com/us/playlist/top-100-mexico/pl.df3f10ca27b1479087de2cd3f9f6716b",
    "mongolia": "https://music.apple.com/us/playlist/top-100-mongolia/pl.71c450d15a9e4440ac5d24c174958225",
    "nepal": "https://music.apple.com/us/playlist/top-100-nepal/pl.9032e70a644e442688f120a829c636cd",
    "netherlands": "https://music.apple.com/us/playlist/top-100-netherlands/pl.26fb1998d54a4b3192be548529a97f8e",
    "new-zealand": "https://music.apple.com/us/playlist/top-100-new-zealand/pl.d8742df90f43402ba5e708eefd6d949a",
    "nicaragua": "https://music.apple.com/us/playlist/top-100-nicaragua/pl.2249e0cc6edb46f4ae64de2c937a4f41",
    "niger": "https://music.apple.com/us/playlist/top-100-niger/pl.cd4a09b0acde49cda246819d9421b26b",
    "nigeria": "https://music.apple.com/us/playlist/top-100-nigeria/pl.2fc68f6d68004ae993dadfe99de83877",
    "norway": "https://music.apple.com/us/playlist/top-100-norway/pl.05a67957c3974729aac67c01247e55b6",
    "oman": "https://music.apple.com/us/playlist/top-100-oman/pl.d4ca5698caf04a9f873861c3659aeeca",
    "panama": "https://music.apple.com/us/playlist/top-100-panama/pl.9d5ee7c72f804dbab97163616c7a8399",
    "papua-new-guinea": "https://music.apple.com/us/playlist/top-100-papua-new-guinea/pl.30fbe54afbf846edabdbe00e90095d04",
    "paraguay": "https://music.apple.com/us/playlist/top-100-paraguay/pl.0843e61953c1430287162e5a36dff52b",
    "peru": "https://music.apple.com/us/playlist/top-100-peru/pl.569a0034bcc64db68bb13afa8171a687",
    "philippines": "https://music.apple.com/us/playlist/top-100-philippines/pl.b9eb00f9d195440e8b0bdf19b8db7f34",
    "poland": "https://music.apple.com/us/playlist/top-100-poland/pl.8c91cbb0ef4e48308dbbba4238135eaf",
    "portugal": "https://music.apple.com/us/playlist/top-100-portugal/pl.5437c1490ac74e9e9505fc7d1f201655",
    "moldova": "https://music.apple.com/us/playlist/top-100-moldova/pl.e4dcd4663130419bb03b80216dee9f57",
    "romania": "https://music.apple.com/us/playlist/top-100-romania/pl.0c6bea611ad54c79b854299bc515a5a6",
    "saudi-arabia": "https://music.apple.com/us/playlist/top-100-saudi-arabia/pl.a5365fa3b6ec4a34994339ca100801ae",
    "singapore": "https://music.apple.com/us/playlist/top-100-singapore/pl.4d763fa1cf15433b9994a14be6a46164",
    "slovakia": "https://music.apple.com/us/playlist/top-100-slovakia/pl.2e50996a5bf44ab78cbb5c34b1992701",
    "slovenia": "https://music.apple.com/us/playlist/top-100-slovenia/pl.e7374de32aec446c92136234d5bcae2f",
    "south-africa": "https://music.apple.com/us/playlist/top-100-south-africa/pl.447bd05172824b89bd745628f7f54c18",
    "south-korea": "https://music.apple.com/us/playlist/top-100-south-korea/pl.d3d10c32fbc540b38e266367dc8cb00c",
    "spain": "https://music.apple.com/us/playlist/top-100-spain/pl.0d656d7feae64198bc5fb1b02786ed75",
    "sri-lanka": "https://music.apple.com/us/playlist/top-100-sri-lanka/pl.cd9b6c35086b43b193ecc3d32882a41e",
    "st-kitts-and-nevis": "https://music.apple.com/us/playlist/top-100-st-kitts-and-nevis/pl.be7b2d63abaf4d25918ef41187f88be4",
    "eswatini": "https://music.apple.com/us/playlist/top-100-eswatini/pl.046c3e297666475aa84c12159a954596",
    "sweden": "https://music.apple.com/us/playlist/top-100-sweden/pl.5876877c387b4ffb8860ac3ea2c244c3",
    "switzerland": "https://music.apple.com/us/playlist/top-100-switzerland/pl.bb1f5218a0f04de3877c4f9ccd63d260",
    "taiwan": "https://music.apple.com/us/playlist/top-100-taiwan/pl.741ff34016704547853b953ec5181d83",
    "tajikistan": "https://music.apple.com/us/playlist/top-100-tajikistan/pl.ea75568dc0524a479b818d551a7b3c35",
    "thailand": "https://music.apple.com/us/playlist/top-100-thailand/pl.c509137d97214632a087129ece060a3d",
    "trinidad-and-tobago": "https://music.apple.com/us/playlist/top-100-trinidad-and-tobago/pl.f1495be1a9774341ab8a1eceb7011579",
    "turkmenistan": "https://music.apple.com/us/playlist/top-100-turkmenistan/pl.f783d8aec4df401583434a2454adbc3d",
    "uganda": "https://music.apple.com/us/playlist/top-100-uganda/pl.b9e553253ed24c2a829c9c08209e5f67",
    "uk": "https://music.apple.com/us/playlist/top-100-uk/pl.c2273b7e89b44121b3093f67228918e7",
    "usa": "https://music.apple.com/us/playlist/top-100-usa/pl.606afcbb70264d2eb2b51d8dbcfa6a12",
    "ukraine": "https://music.apple.com/us/playlist/top-100-ukraine/pl.815f78effb3844909a8259d759ecbddb",
    "united-arab-emirates": "https://music.apple.com/us/playlist/top-100-united-arab-emirates/pl.7b5e51f09aee4733958e23ea97dda459",
    "uzbekistan": "https://music.apple.com/us/playlist/top-100-uzbekistan/pl.90ad69a600ed4d10b00d158eea68cad7",
    "venezuela": "https://music.apple.com/us/playlist/top-100-venezuela/pl.617da0e0bbb74461b607cad435b1e941",
    "vietnam": "https://music.apple.com/us/playlist/top-100-vietnam/pl.550110ec6feb4ae0aff364bcde6d1372",
    "zimbabwe": "https://music.apple.com/us/playlist/top-100-zimbabwe/pl.ad37160bb16c4c70a1d83d3670e96c1a"
}

# 웹드라이버 설정
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

# 최상위 apple 폴더 생성
base_folder_path = "apple"
os.makedirs(base_folder_path, exist_ok=True)

for country, url in countries.items():
    print(f"{country} 데이터를 처리하고 있습니다.")

    # 나라별 하위 폴더 생성
    country_folder_path = os.path.join(base_folder_path, country)
    os.makedirs(country_folder_path, exist_ok=True)

    # 파일 이름 설정
    file_name = f"{country_folder_path}/{country}Top100_{current_date}.json"

    # 페이지 로드
    browser.get(url)

    # 페이지가 완전히 로드될 때까지 대기
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "songs-list"))
        )
        print(f"{country} 페이지가 완전히 로드되었습니다.")
        time.sleep(10)
    except TimeoutException:
        print(f"{country} 페이지가 완전히 로드되지 않았습니다.")
        continue  # 다음 나라로 넘어가기

    # BeautifulSoup으로 페이지 소스 파싱
    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')

    # 차트 정보를 저장할 리스트
    chart_data = []

    # 데이터 추출
    tracks = soup.select(".songs-list-row")

    for track in tracks:
        # 순위, 제목, 아티스트, 앨범 정보 추출
        ranking = track.select_one(".songs-list-row__rank").text.strip() if track.select_one(".songs-list-row__rank") else None
        title = track.select_one(".songs-list-row__song-name").text.strip() if track.select_one(".songs-list-row__song-name") else None
        artist = track.select_one(".songs-list__col--secondary div span a").text.strip() if track.select_one(".songs-list__col--secondary div span a") else None
        image = track.select_one(".artwork-component source")["srcset"].split(",")[1].strip().split(" ")[0] if track.select_one(".artwork-component source") else None
        appleID = (
            track.find("a", {"class": "click-action"})["href"].split("song/")[-1]
            if track.find("a", {"class": "click-action"})
            else None
        )

        # 수집된 정보를 딕셔너리에 저장
        chart_data.append({
            "ranking": ranking,
            "title": title,
            "artist": artist,
            "image": image,
            "appleID": appleID
        })

    # 추출된 데이터를 JSON 파일로 저장
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(chart_data, f, ensure_ascii=False, indent=4)
        print(f"{country} 데이터가 '{file_name}' 파일에 저장되었습니다.")

# 브라우저 종료
browser.quit()
