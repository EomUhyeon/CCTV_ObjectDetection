import os
import shutil

# 경로 설정
image_folder = 'hagseong_junghaggyo_dataset/hagseong_junghaggyo_dataset/img'  # 이미지 파일들이 있는 폴더
label_folder = 'hagseong_junghaggyo_dataset/hagseong_junghaggyo_dataset/label'  # 라벨 파일들이 있는 폴더
output_image_folder = 'filtered_images_train'                         # 필터링된 이미지를 저장할 폴더
output_label_folder = 'filtered_labels_train'                         # 필터링된 라벨을 저장할 폴더

# 기준 바운딩 박스 크기 설정 (상대적 값, 예: 0.1 = 이미지 크기의 10%)
min_box_size = 0.5  # 객체의 최대 크기 (너비 * 높이)

# 폴더가 존재하지 않으면 생성
os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

# 모든 라벨 파일 순회
for label_file in os.listdir(label_folder):
    if not label_file.endswith('.txt'):
        continue

    # 라벨 파일 경로
    label_path = os.path.join(label_folder, label_file)

    # 라벨 파일 읽기
    with open(label_path, 'r') as file:
        lines = file.readlines()

    # 객체 크기 확인
    small_object_found = False
    for line in lines:
        # YOLO 라벨 형식: class x_center y_center width height
        parts = line.strip().split()
        if len(parts) != 5:
            continue

        # 바운딩 박스 너비와 높이 추출
        box_width = float(parts[3])
        box_height = float(parts[4])

        # 객체의 크기 계산
        box_size = box_width * box_height

        # 작은 객체가 존재하면 True
        if box_size <= min_box_size:
            small_object_found = True
            break

    # 작은 객체가 포함된 경우, 이미지와 라벨 파일 복사
    if small_object_found:
        image_file = label_file.replace('.txt', '.jpg')  # 이미지 파일 이름은 라벨 파일과 동일한 이름으로 가정
        image_path = os.path.join(image_folder, image_file)

        # 이미지와 라벨 파일이 모두 존재하면 복사
        if os.path.exists(image_path):
            shutil.copy(image_path, os.path.join(output_image_folder, image_file))
            shutil.copy(label_path, os.path.join(output_label_folder, label_file))

print(f"작은 객체가 포함된 이미지와 라벨이 '{output_image_folder}' 폴더에 저장되었습니다.")
