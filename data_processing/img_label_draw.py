import os
import cv2

# 입력 이미지와 라벨 폴더 경로
input_image_dir = "kickboard_241007_001/dataset/images/val"  # 여기에 입력 이미지 폴더 경로 설정
input_label_dir = "kickboard_241007_001/dataset/labels/val"  # 여기에 입력 라벨 폴더 경로 설정
output_image_dir = "val_test_images"  # 출력 이미지 저장 폴더 경로


# YOLO 형식의 라벨을 실제 이미지 좌표로 변환하여 그리는 함수
def draw_labels(image, label_path):
    h, w, _ = image.shape
    with open(label_path, 'r') as label_file:
        for line in label_file:
            # YOLO 형식의 라벨 데이터 읽기
            class_id, x_center, y_center, width, height = map(float, line.strip().split())

            # 정규화된 좌표를 실제 이미지 크기로 변환
            x_center *= w
            y_center *= h
            width *= w
            height *= h

            # 좌상단(x1, y1)과 우하단(x2, y2) 좌표 계산
            x1 = int(x_center - width / 2)
            y1 = int(y_center - height / 2)
            x2 = int(x_center + width / 2)
            y2 = int(y_center + height / 2)

            # 이미지 위에 라벨 사각형 그리기 (녹색 박스, 두께 2)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

            # 클래스 ID를 텍스트로 표시 (좌상단 모서리 근처)
            cv2.putText(image, f'Class {int(class_id)}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return image

# 이미지와 라벨 처리 및 저장 함수
def process_and_save_images(input_image_dir, input_label_dir, output_image_dir):
    # 출력 디렉토리가 없으면 생성
    os.makedirs(output_image_dir, exist_ok=True)

    # 이미지와 라벨 파일 목록 불러오기
    image_files = sorted(os.listdir(input_image_dir))
    label_files = sorted(os.listdir(input_label_dir))

    # 이미지와 라벨을 순차적으로 처리
    for image_file, label_file in zip(image_files, label_files):
        image_path = os.path.join(input_image_dir, image_file)
        label_path = os.path.join(input_label_dir, label_file)

        # 이미지 읽기
        image = cv2.imread(image_path)

        # 라벨을 이미지 위에 그리기
        image_with_labels = draw_labels(image, label_path)

        # 결과 이미지를 출력 폴더에 저장
        output_path = os.path.join(output_image_dir, image_file)
        cv2.imwrite(output_path, image_with_labels)

    print(f"처리가 완료되었습니다. 결과는 {output_image_dir}에 저장되었습니다.")

if __name__ == "__main__":
    # 이미지와 라벨 처리 및 저장 실행
    process_and_save_images(input_image_dir, input_label_dir, output_image_dir)
