import cv2
import os
import time
from datetime import datetime


def cctv_save(video_url, video_name, save_interval, save_quality, cctv_img_queue, cctv_to_yolo_queue):
    frame_count = 0
    current_day = None

    while True:
        try:
            cap = cv2.VideoCapture(video_url)
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
                    save_dir = f'./{video_name}/CCTV/{current_day}'
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                        print(f'{save_dir} 저장 폴더 생성')

                # 프레임 저장 및 GUI에 이미지 경로 전달
                if frame_count % save_interval == 0:
                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S_%f")
                    frame_filename = os.path.join(save_dir, f'{formatted_time}.jpg')
                    cv2.imwrite(frame_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), save_quality])
                    print(f'Saved {frame_filename}')
                    cctv_img_queue.put(frame_filename)
                    cctv_to_yolo_queue.put(frame_filename)
                    frame_count = frame_count - save_interval

                frame_count += 1

            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"에러 발생: {e}, 5초 후 다시 시도합니다...")
            time.sleep(5)
