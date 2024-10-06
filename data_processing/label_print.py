import os

# 라벨 파일들이 저장된 디렉터리 경로 설정
label_dir = 'data/240921_001/dataset/labels/val'
cnt = 0

# 라벨 디렉토리 내의 모든 파일들을 처리
for filename in os.listdir(label_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(label_dir, filename)

        # 파일 열기
        # print(f"\n{filename} 파일의 내용:")
        with open(file_path, 'r') as file:
            cnt = cnt + 1
            lines = file.readlines()
            for line in lines:
                print(cnt, line.strip())  # 각 라인을 출력
