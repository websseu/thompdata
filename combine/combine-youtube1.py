import os
import json

# 병합할 폴더 지정
base_folder = "youtube"

# 최종 JSON 파일 경로
output_folder = "combine"
output_file = os.path.join(output_folder, "combine-youtube.json")

# 중복 제거를 위한 딕셔너리
unique_data = {}

# 🔹 폴더가 없으면 생성
os.makedirs(output_folder, exist_ok=True)

# youtube 폴더 내부의 모든 JSON 파일을 탐색
for root, _, files in os.walk(base_folder):
    for file in files:
        if file.endswith(".json"):  # JSON 파일만 처리
            file_path = os.path.join(root, file)  # 파일 경로 생성
            
            # JSON 파일 열기
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)  # JSON 파일 읽기
                    
                    # JSON 파일이 리스트 형태인지 확인
                    if isinstance(data, list):
                        for item in data:
                            # 필수 필드 확인 (title, artist, image, youtubeID가 없는 경우 제외)
                            if all(key in item for key in ["title", "artist", "image", "youtubeID"]):
                                key = (item["title"].lower(), item["artist"].lower())  # 중복 방지용 키 생성

                                # 새로운 항목을 저장할 딕셔너리
                                entry = {
                                    "title": item["title"],
                                    "artist": item["artist"],
                                    "image": item["image"],
                                    "youtubeID": item["youtubeID"]  # 필수 필드 (무조건 포함)
                                }

                                # 중복되지 않은 경우에만 저장
                                if key not in unique_data:
                                    unique_data[key] = entry
                except json.JSONDecodeError:
                    print(f"⚠️ JSON 파싱 오류 발생: {file_path}")  # JSON 형식이 올바르지 않은 경우 경고 출력

# 중복 제거된 데이터를 리스트로 변환
combined_data = list(unique_data.values())

# 최종 데이터 JSON 파일로 저장
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=2)

# 완료 메시지 출력
print(f"✅ youtube 폴더 데이터를 중복 제거 후 {output_file} 파일로 합쳤습니다! (필드: title, artist, image, youtubeID)")
