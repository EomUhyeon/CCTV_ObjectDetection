import os


# jpg 파일 확장자를 가진 파일의 개수를 세는 함수
def count_jpg_files(folder_path):
    # 폴더 안의 파일 목록 불러오기
    files = os.listdir(folder_path)

    # jpg 확장자를 가진 파일 개수 세기
    jpg_count = len([file for file in files if file.lower().endswith('.jpg')])

    print(f"폴더 '{folder_path}' 안의 .jpg 파일 개수: {jpg_count}")


if __name__ == "__main__":
    # 이미지가 있는 폴더 경로 설정
    folder_path = "output_images1"  # 여기에 폴더 경로 설정

    # jpg 파일 개수 출력
    count_jpg_files(folder_path)
