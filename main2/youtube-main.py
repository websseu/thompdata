import os
import json
from datetime import datetime

# youtube 나라마다 1위~20위까지 추출하여 정리

# 🎯 기본 설정 (폴더 경로 맞추기)
base_folder = "main2"  # 실행되는 폴더
youtube_folder = "youtube"  # "youtube" 폴더는 main2과 같은 레벨에 존재
platforms = [
    "argentina", "australia", "austria", "belgium", "bolivia", "brazil", "canada", "chile",
    "colombia", "costa-rica", "czechia", "denmark", "dominican_republic", "ecuador", "egypt",
    "el-salvador", "estonia", "finland", "france", "germany", "guatemala", "honduras", "hungary",
    "iceland", "india", "indonesia", "israel", "italy", "japan", "kenya", "luxembourg", "mexico",
    "netherlands", "new-zealand", "nicaragua", "nigeria", "norway", "panama", "paraguay", "peru",
    "poland", "portugal", "romania", "russia", "saudi-arabia", "serbia", "south-africa",
    "south-korea", "spain", "sweden", "switzerland", "tanzania", "turkey", "uganda", "ukraine",
    "united-arab-emirates", "united-kingdom", "united-states", "uruguay", "zimbabwe"
]

# 📅 오늘 날짜 가져오기 (YYYY-MM-DD 형식)
today = datetime.today().strftime("%Y-%m-%d")
# today = "2025-03-20"

# 🔹 날짜별 JSON 파일을 처리하는 함수
def process_date(date_str):
    combined_data = {}  # 날짜별 데이터 저장

    for platform in platforms:
        platform_folder = os.path.join(youtube_folder, platform)  # 플랫폼 폴더 경로
        json_file = os.path.join(platform_folder, f"{platform}Top100_{date_str}.json")

        # JSON 파일이 존재하는지 확인
        if not os.path.exists(json_file):
            print(f"⚠️ {platform} - {date_str} 데이터가 없습니다. 건너뜁니다.")
            continue

        # JSON 파일 로드
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                # 상위 20개 곡만 가져오기
                top_20 = data[:20]

                # 필요한 정보만 필터링
                filtered_top_20 = []
                for item in top_20:
                    filtered_item = {
                        "title": item.get("title", ""),
                        "artist": item.get("artist", ""),
                        "image": item.get("image", ""),
                        "youtubeID": item.get("youtubeID", "")
                    }
                    filtered_top_20.append(filtered_item)

                combined_data[platform] = filtered_top_20
            else:
                print(f"⚠️ {platform} - {date_str} JSON 형식이 잘못되었습니다.")

        except json.JSONDecodeError:
            print(f"❌ {platform} - {date_str} JSON 파싱 오류 발생!")

    # 결과 저장
    output_file = os.path.join(base_folder, f"youtube-main_{date_str}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)

    print(f"✅ {output_file} 생성 완료!")

# 📌 실행
process_date(today)
