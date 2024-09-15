import cv2
import os

# .m3u8 파일 URL (또는 로컬 파일 경로)
video_url = 'https://strm2.spatic.go.kr/live/152.stream/playlist.m3u8'

# 프레임을 저장할 디렉토리
output_dir = './img'

# 디렉토리가 없으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_url)

# 초당 2 프레임을 저장하도록 설정
fps = 2
frame_interval = int(1 / fps * 1000)  # 프레임 간격(밀리초)

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임을 초당 2번 저장
    if frame_count % (int(cap.get(cv2.CAP_PROP_FPS) / fps)) == 0:
        # 프레임 파일명을 './img' 디렉토리에 저장
        frame_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.png')
        cv2.imwrite(frame_filename, frame)
        print(f'Saved {frame_filename}')

    frame_count += 1

cap.release()
cv2.destroyAllWindows()
