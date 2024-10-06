import os

# 라벨 파일들이 저장된 디렉터리 경로 설정
label_dir = 'path_to_your_label_directory'

# 라벨 디렉토리 내의 모든 파일들을 처리
for filename in os.listdir(label_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(label_dir, filename)

        # 파일 열기
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 모든 라인의 class_id를 0으로 변경
        new_lines = []
        for line in lines:
            parts = line.split()
            parts[0] = '0'  # class_id를 0으로 설정
            new_lines.append(' '.join(parts) + '\n')

        # 변경된 내용을 파일에 다시 쓰기
        with open(file_path, 'w') as file:
            file.writelines(new_lines)

print("모든 라벨 파일의 클래스가 0으로 변경되었습니다.")
