import os
import json
from datetime import datetime

# korea 서비스마다 1위~10위까지 추출하여 정리

# 🎯 기본 설정 (폴더 경로 맞추기)
base_folder = "main"  # 실행되는 폴더
korea_folder = "korea"  # "korea" 폴더는 main과 같은 레벨에 존재
platforms = ["bugs", "flo", "genie", "melon", "vibe"]  # 지원하는 플랫폼

# 📅 오늘 날짜 가져오기 (YYYY-MM-DD 형식)
today = datetime.today().strftime("%Y-%m-%d") 
# today = "2025-03-26"

# 🔹 날짜별 JSON 파일을 처리하는 함수
def process_date(date_str):
    combined_data = {}  # 날짜별 데이터 저장

    for platform in platforms:
        platform_folder = os.path.join(korea_folder, platform)  # 플랫폼 폴더 경로
        json_file = os.path.join(platform_folder, f"{platform}Top100_{date_str}.json")

        # JSON 파일이 존재하는지 확인
        if not os.path.exists(json_file):
            print(f"⚠️ {platform} - {date_str} 데이터가 없습니다. 건너뜁니다.")
            continue  # 해당 날짜의 플랫폼 데이터가 없으면 건너뛰기

        # JSON 파일 로드
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 리스트 형태인지 확인 후 TOP 10 추출
            if isinstance(data, list):
                top_10 = data[:10]  # 상위 10개 곡만 저장
                # 각 곡에서 원하는 키만 추출
                filtered_top_10 = []
                for item in top_10:
                    filtered_item = {
                        "title": item.get("title", ""),
                        "artist": item.get("artist", ""),
                        "image": item.get("image", ""),
                        "youtubeID": item.get("youtubeID", "")
                    }
                    filtered_top_10.append(filtered_item)
                combined_data[platform] = filtered_top_10
            else:
                print(f"⚠️ {platform} - {date_str} JSON 형식이 잘못되었습니다.")

        except json.JSONDecodeError:
            print(f"❌ {platform} - {date_str} JSON 파싱 오류 발생!")

    # 결과 파일 저장 (main 폴더에 korea-main_YYYY-MM-DD.json 생성)
    output_file = os.path.join(base_folder, f"korea-main_{date_str}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)

    print(f"✅ {output_file} 생성 완료!")

# 📌 실행 (오늘 날짜 데이터 처리)
process_date(today)
