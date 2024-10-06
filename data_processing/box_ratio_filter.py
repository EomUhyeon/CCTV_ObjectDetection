import os
import shutil
import cv2  # OpenCV를 사용하여 이미지 크기를 불러오기 위해 필요

# 경로 설정
image_folder = 'h/object_detection/CCTV_img'  # 이미지 파일들이 있는 폴더
label_folder = 'h/object_detection/kickboard_label'  # 라벨 파일들이 있는 폴더
output_image_folder = 'filtered_reimages'                         # 필터링된 이미지를 저장할 폴더
output_label_folder = 'filtered_relabels'                         # 필터링된 라벨을 저장할 폴더

# 기준: 이미지 크기 대비 가로 45% 이하, 세로 55% 이하
max_width_ratio = 0.15
max_height_ratio = 0.30

# 폴더가 존재하지 않으면 생성
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

# 모든 라벨 파일 순회
for label_file in os.listdir(label_folder):
    if not label_file.endswith('.txt'):
        continue

    # 라벨 파일 경로
    label_path = os.path.join(label_folder, label_file)

    # 라벨 파일과 일치하는 이미지 파일 경로
    image_file = label_file.replace('.txt', '.jpg')  # 이미지 파일 이름은 라벨 파일과 동일한 이름으로 가정
    image_path = os.path.join(image_folder, image_file)

    # 이미지 파일이 존재하는지 확인
    if not os.path.exists(image_path):
        print(f"이미지 파일을 찾을 수 없습니다: {image_file}")
        continue

    # 이미지 크기 불러오기 (cv2를 사용하여 이미지 열기)
    image = cv2.imread(image_path)
    img_height, img_width = image.shape[:2]

    # 라벨 파일 읽기
    with open(label_path, 'r') as file:
        lines = file.readlines()

    # 작은 객체를 찾기 위한 변수
    valid_object_found = False

    # 라벨 파일에 있는 모든 객체 순회
    for line in lines:
        # YOLO 라벨 형식: class x_center y_center width height
        parts = line.strip().split()
        if len(parts) != 5:
            continue

        # 바운딩 박스 너비와 높이 추출 (상대적 값)
        box_width = float(parts[3])
        box_height = float(parts[4])

        # 바운딩 박스가 기준을 만족하는지 확인
        if box_width * img_width < img_width * max_width_ratio and box_height * img_height < img_height * max_height_ratio:
            valid_object_found = True
            break

    # 기준을 만족하는 객체가 있으면 이미지와 라벨 파일을 출력 폴더로 복사
    if valid_object_found:
        shutil.copy(image_path, os.path.join(output_image_folder, image_file))
        shutil.copy(label_path, os.path.join(output_label_folder, label_file))

print(f"필터링된 이미지와 라벨이 '{output_image_folder}' 및 '{output_label_folder}' 폴더에 저장되었습니다.")
