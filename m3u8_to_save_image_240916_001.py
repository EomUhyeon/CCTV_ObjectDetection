import cv2
import os
from datetime import datetime, timedelta


# .m3u8 파일 URL

# video_url = 'https://strm2.spatic.go.kr/live/152.stream/playlist.m3u8'

# 서부역 입구 삼거리 seobuyeog ibgu samgeoli
video_url = 'https://wowza.cheonan.go.kr/live/cctv002.stream/playlist.m3u8'

video_name = 'seobuyeog ibgu samgeoli'

# 프레임 저장 간격
save_interval = 15


def m3u8_to_save_img(video, name, frame_interval):
    current_time = datetime.now().replace(microsecond=1)
    frame_count = 0
    saved_count = 0

    # 프레임 저장 폴더
    save_dir = f'./{name}'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(name, '저장 폴더 생성')

    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        print("스트리밍 소스를 열 수 없습니다.")
        exit()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("스트리밍이 중단되었습니다.")
            break

        if frame_count % frame_interval == 0:
            formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S-%f")
            frame_filename = os.path.join(save_dir, f'{formatted_time}.jpg')
            cv2.imwrite(frame_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            print(f'Saved {frame_filename}')
            saved_count += 1
            current_time = current_time + timedelta(seconds=0.5)

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    m3u8_to_save_img(video_url, video_name, save_interval)
    