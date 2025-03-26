import os
import json

# 병합할 폴더 리스트
base_folders = ["korea", "youtube"]
output_file = "combine-data.json"

# 중복 제거를 위한 딕셔너리
unique_data = {}

# 지정된 폴더들을 모두 탐색
for base_folder in base_folders:
    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        if isinstance(data, list):  # 리스트 형태일 경우 추가
                            for item in data:
                                # 필수 필드 확인
                                if "title" in item and "artist" in item:
                                    key = (item["title"].lower(), item["artist"].lower())  # 소문자로 변환하여 중복 방지
                                    
                                    # 선택적 필드는 있으면 추가
                                    entry = {
                                        "title": item["title"],
                                        "artist": item["artist"]
                                    }
                                    if "youtubeID" in item:
                                        entry["youtubeID"] = item["youtubeID"]
                                    if "appleID" in item:
                                        entry["appleID"] = item["appleID"]
                                    if "spotifyID" in item:
                                        entry["spotifyID"] = item["spotifyID"]

                                    # 기존에 없으면 추가 (중복 제거)
                                    if key not in unique_data:
                                        unique_data[key] = entry
                    except json.JSONDecodeError:
                        print(f"⚠️ JSON 파싱 오류: {file_path}")

# 중복 제거된 데이터 리스트로 변환
combined_data = list(unique_data.values())

# 최종 데이터 저장
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=2)

print(f"✅ 모든 데이터를 중복 제거 후 {output_file} 파일로 합쳤습니다!")
