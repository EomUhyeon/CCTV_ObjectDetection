import os
import cv2
import shutil

# 경로 설정
input_image_dir = "dataset/images/train"  # 입력 이미지 폴더 경로
input_label_dir = "dataset/labels/train"  # 입력 라벨 폴더 경로
output_image_dir = "train_images"  # 출력 이미지 저장 폴더 경로
output_label_dir = "train_labels"  # 출력 라벨 저장 폴더 경로

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
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 클래스 ID를 텍스트로 표시 (좌상단 모서리 근처)
            cv2.putText(image, f'Class {int(class_id)}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return image


# 이미지와 라벨 처리 함수
def process_data(image_path, label_path):
    image = cv2.imread(image_path)

    # 이미지 위에 라벨을 표시
    image_with_labels = draw_labels(image, label_path)

    # 이미지를 화면에 표시
    cv2.imshow("Image with Labels", image_with_labels)

    # 0 = 패스, 1 = 저장
    key = cv2.waitKey(0)
    if key == ord('1'):
        return True  # 저장
    elif key == ord('0'):
        return False  # 패스


# main 함수
def main():
    # 출력 디렉토리가 없으면 생성
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    # 이미지와 라벨 파일 목록 불러오기
    image_files = sorted(os.listdir(input_image_dir))
    label_files = sorted(os.listdir(input_label_dir))

    # 이미지와 라벨을 순차적으로 처리
    for image_file, label_file in zip(image_files, label_files):
        image_path = os.path.join(input_image_dir, image_file)
        label_path = os.path.join(input_label_dir, label_file)

        # 이미지와 라벨을 처리하고 저장할지 여부를 결정
        if process_data(image_path, label_path):
            # 이미지와 라벨을 출력 폴더에 복사
            shutil.copy(image_path, os.path.join(output_image_dir, image_file))
            shutil.copy(label_path, os.path.join(output_label_dir, label_file))

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
