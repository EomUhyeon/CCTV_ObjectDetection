import os
import shutil

# 이미지와 라벨을 찾아 아웃풋 폴더에 저장하는 함수
def match_and_save_images_labels(image_dir, label_dir, output_image_dir, output_label_dir, image_ext=".jpg", label_ext=".txt"):
    # 출력 디렉토리가 없으면 생성
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    # 이미지 파일 목록 불러오기
    image_files = sorted(os.listdir(image_dir))

    for image_file in image_files:
        # 이미지 파일 확장자가 맞는지 확인
        if image_file.endswith(image_ext):
            # 이미지 파일명에서 확장자를 제거하고 라벨 파일명 생성
            base_name = os.path.splitext(image_file)[0]
            label_file = f"{base_name}{label_ext}"

            # 라벨 파일 경로
            label_path = os.path.join(label_dir, label_file)

            # 라벨 파일이 존재하는지 확인
            if os.path.exists(label_path):
                # 이미지와 라벨을 아웃풋 폴더로 복사
                shutil.copy(os.path.join(image_dir, image_file), os.path.join(output_image_dir, image_file))
                shutil.copy(label_path, os.path.join(output_label_dir, label_file))
            else:
                print(f"라벨 파일을 찾을 수 없습니다: {label_file}")

    print(f"처리가 완료되었습니다. 결과는 {output_image_dir} 및 {output_label_dir}에 저장되었습니다.")

if __name__ == "__main__":
    # 입력 이미지와 라벨 폴더 경로
    input_image_dir = "dataset/images/val"  # 여기에 입력 이미지 폴더 경로 설정
    input_label_dir = "labels/val"  # 여기에 입력 라벨 폴더 경로 설정

    # 출력 폴더 경로
    output_image_dir = "val_test_images"  # 출력 이미지 저장 폴더 경로 설정
    output_label_dir = "val_test_labels"  # 출력 라벨 저장 폴더 경로 설정

    # 이미지와 라벨 처리 및 저장
    match_and_save_images_labels(input_image_dir, input_label_dir, output_image_dir, output_label_dir)
