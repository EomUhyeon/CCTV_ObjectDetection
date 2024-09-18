import cv2
import os
import time
from datetime import datetime, timedelta


# test
# video_url = 'https://strm2.spatic.go.kr/live/152.stream/playlist.m3u8'
# video_name = 'test'
# save_interval = 15
# save_quality = 80

# 서부역 입구 삼거리 seobuyeog ibgu samgeoli
# video_url = 'https://wowza.cheonan.go.kr/live/cctv002.stream/playlist.m3u8'
# video_name = 'seobuyeog_ibgu_samgeoli'
# save_interval = 15
# save_quality = 90

# 학성 중학교 hagseong junghaggyo
video_url = 'http://211.34.248.240:1935/live/T065.stream/playlist.m3u8'
video_name = 'hagseong_junghaggyo'
save_interval = 10
save_quality = 90


def m3u8_to_save_img(video, name, interval, quality):
    frame_count = 0
    current_day = None

    while True:
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

                # 현재 날짜 확인
                now = datetime.now()
                today = now.strftime("%Y-%m-%d")

                # 날짜 변경 폴더 생성
                if current_day != today:
                    current_day = today
                    save_dir = f'./{name}/{current_day}'
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                        print(f'{save_dir} 저장 폴더 생성')

                # 15프레임마다 한 장 저장
                if frame_count % interval == 0:
                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S_%f")
                    frame_filename = os.path.join(save_dir, f'{formatted_time}.jpg')
                    cv2.imwrite(frame_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                    print(f'Saved {frame_filename}')
                    frame_count = frame_count - interval

                frame_count += 1

            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"에러 발생: {e}, 5초 후 다시 시도합니다...")
            time.sleep(5)  # 5초 대기 후 다시 시도


if __name__ == "__main__":
    m3u8_to_save_img(video_url, video_name, save_interval, save_quality)

