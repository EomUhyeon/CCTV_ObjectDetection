import os
import cv2

# 이미지와 라벨 경로를 설정하세요.
image_dir = 'dataset/images/val'  # 이미지 파일이 있는 폴더 경로
label_dir = 'dataset/labels/val'  # 라벨 파일이 있는 폴더 경로

# 이미지 파일 확장자 (예: '.jpg', '.png')
image_ext = '.jpg'

# 라벨 파일 확장자 (보통 YOLOv5 형식은 '.txt')
label_ext = '.txt'


# 이미지 파일과 라벨 파일 이름을 비교하는 함수
def check_dataset(image_dir, label_dir, image_ext, label_ext):
    missing_labels = []
    missing_images = []
    mismatched = []

    image_files = [f for f in os.listdir(image_dir) if f.endswith(image_ext)]
    label_files = [f for f in os.listdir(label_dir) if f.endswith(label_ext)]

    # 이미지 파일에서 확장자를 뺀 파일명 추출
    image_basenames = [os.path.splitext(f)[0] for f in image_files]
    label_basenames = [os.path.splitext(f)[0] for f in label_files]

    # 이미지에 대응되는 라벨이 있는지 확인
    for img_name in image_basenames:
        if img_name not in label_basenames:
            missing_labels.append(f"{img_name}{image_ext}")

    # 라벨에 대응되는 이미지가 있는지 확인
    for lbl_name in label_basenames:
        if lbl_name not in image_basenames:
            missing_images.append(f"{lbl_name}{label_ext}")

    # 이미지와 라벨 쌍의 사이즈가 맞는지 확인
    for img_name in image_basenames:
        if img_name in label_basenames:
            image_path = os.path.join(image_dir, f"{img_name}{image_ext}")
            label_path = os.path.join(label_dir, f"{img_name}{label_ext}")

            # 이미지 로드 및 크기 확인
            img = cv2.imread(image_path)
            if img is None:
                print(f"Error loading image: {image_path}")
                continue

            height, width = img.shape[:2]

            # 라벨 파일 내용 확인
            with open(label_path, 'r') as f:
                labels = f.readlines()

            # 라벨의 포맷이 올바른지 확인 (YOLO 형식: class x_center y_center width height)
            for label in labels:
                try:
                    cls, x_center, y_center, w, h = map(float, label.strip().split())
                    if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                        mismatched.append(f"{img_name}{label_ext}")
                except ValueError:
                    mismatched.append(f"{img_name}{label_ext}")

    return missing_labels, missing_images, mismatched


# 데이터셋 검사 실행
missing_labels, missing_images, mismatched = check_dataset(image_dir, label_dir, image_ext, label_ext)

# 결과 출력
if missing_labels:
    print(f"Missing labels for images: {missing_labels}")
else:
    print("All images have corresponding labels.")

if missing_images:
    print(f"Missing images for labels: {missing_images}")
else:
    print("All labels have corresponding images.")

if mismatched:
    print(f"Mismatched label format: {mismatched}")
else:
    print("All labels are correctly formatted.")
