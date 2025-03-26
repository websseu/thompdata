import os
import json
import re

# 파일 경로 설정
youtube_file = "combine/combine-youtube.json"
korea_folder = "korea"

# 제목에서 () 내용 제거 및 소문자로 변환하는 함수
def clean_text(text):
    return re.sub(r"\s*\([^)]*\)", "", text).strip().lower()

# combine-youtube.json 파일 확인
if not os.path.exists(youtube_file):
    print(f"❌ 오류: {youtube_file} 파일이 존재하지 않습니다. 먼저 combine-youtube1.py를 실행하세요!")
    exit(1)  # 스크립트 종료

# Step 1: combine-youtube.json 데이터 로드
try:
    with open(youtube_file, "r", encoding="utf-8") as f:
        youtube_data = json.load(f)
except json.JSONDecodeError:
    print(f"❌ 오류: {youtube_file} 파일이 올바른 JSON 형식이 아닙니다!")
    exit(1)

# youtube 데이터에서 (title, artist) -> youtubeID 매핑 딕셔너리 생성
youtube_dict = {
    (clean_text(item["title"]), clean_text(item["artist"])): item["youtubeID"]
    for item in youtube_data
    if "title" in item and "artist" in item and "youtubeID" in item  # 필수 필드 확인
}

# Step 2: korea 폴더 내부의 JSON 파일을 수정
if not os.path.exists(korea_folder):
    print(f"❌ 오류: {korea_folder} 폴더가 존재하지 않습니다!")
    exit(1)

for root, _, files in os.walk(korea_folder):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)

            # korea 폴더 JSON 데이터 로드
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ JSON 파싱 오류 발생: {file_path}")
                continue  # 다음 파일로 이동

            # 데이터가 리스트 형태인지 확인
            if not isinstance(data, list):
                print(f"⚠️ 경고: {file_path} 파일이 리스트 형식이 아닙니다. 건너뜁니다.")
                continue  # JSON 파일이 리스트가 아니면 패스

            updated = False  # 파일 업데이트 여부 확인

            for item in data:
                if "title" in item and "artist" in item:
                    key = (clean_text(item["title"]), clean_text(item["artist"]))

                    # youtube 데이터에 있는 경우 youtubeID 추가
                    if key in youtube_dict and "youtubeID" not in item:
                        item["youtubeID"] = youtube_dict[key]
                        updated = True  # 업데이트 플래그 설정

            # 파일이 업데이트된 경우 다시 저장
            if updated:
                with open(file_path, "w", encoding="utf-8") as f_out:
                    json.dump(data, f_out, ensure_ascii=False, indent=2)

                print(f"✅ {file} - youtubeID 추가됨")

print("🎉 모든 korea 폴더의 파일을 업데이트 완료!")
