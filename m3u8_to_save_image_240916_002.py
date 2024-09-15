import cv2
import os
import time
from datetime import datetime, timedelta


# .m3u8 파일 URL

# video_url = 'https://strm2.spatic.go.kr/live/152.stream/playlist.m3u8'

# 서부역 입구 삼거리 seobuyeog ibgu samgeoli
video_url = 'https://wowza.cheonan.go.kr/live/cctv002.stream/playlist.m3u8'

video_name = 'seobuyeog ibgu samgeoli'

# 프레임 저장 간격
save_interval = 15


def m3u8_to_save_img(video, name, frame_interval):
    frame_count = 0
    saved_count = 0

    # 프레임 저장 폴더
    save_dir = f'./{name}'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(name, '저장 폴더 생성')

    while True:
        current_time = datetime.now().replace(microsecond=0)
        try:
            cap = cv2.VideoCapture(video)
            if not cap.isOpened():
                print("스트리밍 소스를 열 수 없습니다. 다시 시도합니다...")
                time.sleep(1)
                continue

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("스트리밍이 중단되었습니다. 다시 시작합니다...")
                    break

                # 15프레임마다 한 장 저장
                if frame_count % frame_interval == 0:
                    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S-%f")
                    frame_filename = os.path.join(save_dir, f'{formatted_time}.jpg')
                    cv2.imwrite(frame_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                    print(f'Saved {frame_filename}')
                    saved_count += 1
                    current_time = current_time + timedelta(seconds=0.500001)

                frame_count += 1

            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"에러 발생: {e}, 5초 후 다시 시도합니다...")
            time.sleep(5)  # 5초 대기 후 다시 시도


if __name__ == "__main__":
    m3u8_to_save_img(video_url, video_name, save_interval)
    