import cv2
import time

# 학성 중학교 hagseong junghaggyo
video_url_01 = 'http://211.34.248.240:1935/live/T065.stream/playlist.m3u8'

# 서부역 입구 삼거리 seobuyeog ibgu samgeoli
video_url_02 = 'https://wowza.cheonan.go.kr/live/cctv002.stream/playlist.m3u8'

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_url_01)

if not cap.isOpened():
    print("스트리밍 소스를 열 수 없습니다.")
    exit()

# FPS 계산을 위한 변수 초기화
frame_count = 0
start_time = time.time()

# 스트리밍이 계속되는 동안 프레임을 실시간으로 처리
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("스트리밍이 중단되었습니다.")
        break

    # 프레임 카운트 증가
    frame_count += 1

    # 1초마다 FPS 계산
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time >= 1.0:  # 1초마다 계산
        fps = frame_count / elapsed_time
        print(f"실시간 FPS: {fps:.2f}")

        # 변수 초기화
        frame_count = 0
        start_time = current_time

# 자원 해제
cap.release()
cv2.destroyAllWindows()
