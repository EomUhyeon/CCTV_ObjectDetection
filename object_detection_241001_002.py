import os
import cv2
from ultralytics import YOLO


def yolo_process(video_name, batch_size, yolo_img_queue, cctv_to_yolo_queue):
    # YOLOv8 모델 불러오기
    model = YOLO('runs/detect/train/weights/best.pt')

    image_batch = []
    image_paths = []

    while True:
        if not cctv_to_yolo_queue.empty():
            frame_filename = cctv_to_yolo_queue.get()

            img = cv2.imread(frame_filename)
            if img is None:
                print(f"이미지를 읽을 수 없습니다: {frame_filename}")
                continue

            image_batch.append(img)
            image_paths.append(frame_filename)

            if len(image_batch) == batch_size:
                process_batch(model, video_name, image_batch, image_paths, yolo_img_queue)
                image_batch = []
                image_paths = []


def process_batch(model, video_name, image_batch, image_paths, yolo_img_queue):
    results = model(image_batch)

    output_folder = f'./{video_name}/object_detection/kickboard_img'
    label_folder = f'./{video_name}/object_detection/kickboard_label'
    original_folder = f'./{video_name}/object_detection/CCTV_img'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(label_folder):
        os.makedirs(label_folder)
    if not os.path.exists(original_folder):
        os.makedirs(original_folder)

    for i, result in enumerate(results):
        img_height, img_width, _ = image_batch[i].shape
        img_file = image_paths[i]

        # 검출된 객체가 있는지 확인
        objects_detected = False

        if result.boxes is not None and len(result.boxes) > 0:
            objects_detected = True

            # 원본 이미지 저장
            original_img_path = os.path.join(original_folder, os.path.basename(img_file))
            cv2.imwrite(original_img_path, image_batch[i])
            # print(f"원본 이미지 저장: {original_img_path}")

            # try:
            #     original_img_path = os.path.join(original_folder, os.path.basename(img_file))
            #     success = cv2.imwrite(original_img_path, image_batch[i])
            #     if success:
            #         print(f"원본 이미지 저장 완료: {original_img_path}")
            #     else:
            #         print(f"원본 이미지 저장 실패: {original_img_path}")
            # except Exception as e:
            #     print(f"원본 이미지 저장 중 오류 발생: {e}")

            # 검출된 결과 그리기
            result_img = result.plot()
            result_img_path = os.path.join(output_folder, os.path.basename(img_file))

            # 결과 이미지 저장
            cv2.imwrite(result_img_path, result_img)
            # print(f"검출 결과 저장: {result_img_path}")
            yolo_img_queue.put(result_img_path)

            # 라벨 파일 저장 (YOLO 형식)
            label_file_path = os.path.join(label_folder, f"{os.path.splitext(os.path.basename(img_file))[0]}.txt")
            with open(label_file_path, 'w') as label_file:
                for box in result.boxes:
                    # 박스 정보 가져오기
                    class_id = int(box.cls[0])                  # 클래스 ID
                    x_center = box.xywh[0][0] / img_width       # x 중심
                    y_center = box.xywh[0][1] / img_height      # y 중심
                    width = box.xywh[0][2] / img_width          # 너비
                    height = box.xywh[0][3] / img_height        # 높이

                    # 라벨을 YOLO 형식으로 저장: 클래스 ID, x_center, y_center, width, height
                    label_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

            # print(f"라벨 저장: {label_file_path}")

        # 객체가 검출되지 않으면 결과 저장 안 함
        if not objects_detected:
            print(f"검출된 객체 없음: {img_file}")
