import cv2
import os

# .m3u8 파일 URL (또는 로컬 파일 경로)
video_url = 'https://strm2.spatic.go.kr/live/152.stream/playlist.m3u8'

# 프레임을 저장할 디렉토리
output_dir = '../img'

# 디렉토리가 없으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_url)

# 동영상의 초당 프레임 수(FPS) 가져오기
video_fps = cap.get(cv2.CAP_PROP_FPS)

# 초당 2프레임을 저장하도록 설정
desired_fps = 2
frame_interval = int(video_fps / desired_fps)  # FPS 비율로 프레임 간격 계산

frame_count = 0
saved_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 특정 간격의 프레임을 저장
    if frame_count % frame_interval == 0:
        # 프레임 파일명을 './img' 디렉토리에 저장
        frame_filename = os.path.join(output_dir, f'frame_{saved_count:04d}.png')
        cv2.imwrite(frame_filename, frame)
        print(f'Saved {frame_filename}')
        saved_count += 1

    frame_count += 1

cap.release()
cv2.destroyAllWindows()
