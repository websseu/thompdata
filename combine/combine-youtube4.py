import os
import json
import re

# 4. main에 korea-main 파일에 youtubeID 추가

def clean_text(text):
    return re.sub(r"\s*\([^)]*\)", "", text).strip().lower()

youtube_file = "combine/combine-youtube.json"
main_folder = "main"

# 1) youtube 데이터 로드
with open(youtube_file, "r", encoding="utf-8") as f:
    youtube_data = json.load(f)

# 2) (title, artist) -> youtubeID 매핑 딕셔너리 생성
youtube_dict = {}
for item in youtube_data:
    if "title" in item and "artist" in item and "youtubeID" in item:
        key = (clean_text(item["title"]), clean_text(item["artist"]))
        youtube_dict[key] = item["youtubeID"]

# 3) main 폴더 내부의 JSON 파일들 순회
for root, _, files in os.walk(main_folder):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            
            # JSON 로드
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ JSON 파싱 오류 발생: {file_path}")
                continue

            updated = False  # 업데이트 플래그

            # (A) 최상위가 딕셔너리일 경우
            if isinstance(data, dict):
                # 딕셔너리 내부의 모든 key에 대해 검사
                for key, item_list in data.items():
                    # item_list가 리스트인지 확인
                    if isinstance(item_list, list):
                        # 리스트 안의 각 item(곡 정보)을 순회
                        for item in item_list:
                            if "title" in item and "artist" in item:
                                clean_key = (clean_text(item["title"]), clean_text(item["artist"]))
                                # youtube_dict에 해당 key가 있고, 아직 youtubeID가 없으면 추가
                                if clean_key in youtube_dict and "youtubeID" not in item:
                                    item["youtubeID"] = youtube_dict[clean_key]
                                    updated = True
                    else:
                        # 혹은 item_list가 리스트가 아닌 경우 필요에 따라 처리
                        pass

            # (B) 혹시 최상위가 리스트인 경우(다른 파일 구조)
            elif isinstance(data, list):
                for item in data:
                    if "title" in item and "artist" in item:
                        clean_key = (clean_text(item["title"]), clean_text(item["artist"]))
                        if clean_key in youtube_dict and "youtubeID" not in item:
                            item["youtubeID"] = youtube_dict[clean_key]
                            updated = True

            else:
                print(f"⚠️ 경고: {file_path} - 지원하지 않는 JSON 구조입니다. 건너뜁니다.")
                continue
            
            # 업데이트가 일어났으면 저장
            if updated:
                with open(file_path, "w", encoding="utf-8") as f_out:
                    json.dump(data, f_out, ensure_ascii=False, indent=2)
                print(f"✅ {file} - youtubeID 추가됨")

print("🎉 모든 main 폴더의 파일을 업데이트 완료!")
