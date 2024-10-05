import os
import cv2
from ultralytics import YOLO


def yolo_process(batch_size, video_name_1, yolo_img_queue_1, cctv_to_yolo_queue_1, video_name_2, yolo_img_queue_2, cctv_to_yolo_queue_2):
    # YOLO 모델
    model = YOLO('runs/detect/train/weights/best.pt')

    image_batch = []
    image_paths = []

    while True:
        # CCTV 피드 1에서 이미지 가져오기
        if not cctv_to_yolo_queue_1.empty():
            frame_filename_1 = cctv_to_yolo_queue_1.get()

            img_1 = cv2.imread(frame_filename_1)
            if img_1 is None:
                print(f"이미지를 읽을 수 없습니다: {frame_filename_1}")
                continue

            image_batch.append(img_1)
            image_paths.append((frame_filename_1, yolo_img_queue_1, video_name_1))

        # CCTV 피드 2에서 이미지 가져오기
        if not cctv_to_yolo_queue_2.empty():
            frame_filename_2 = cctv_to_yolo_queue_2.get()

            img_2 = cv2.imread(frame_filename_2)
            if img_2 is None:
                print(f"이미지를 읽을 수 없습니다: {frame_filename_2}")
                continue

            image_batch.append(img_2)
            image_paths.append((frame_filename_2, yolo_img_queue_2, video_name_2))

        # 배치 크기만큼 이미지가 모이면 처리
        if len(image_batch) >= batch_size:
            process_batch(model, image_batch, image_paths)
            image_batch = []
            image_paths = []

def process_batch(model, image_batch, image_paths):
    results = model(image_batch)

    for i, result in enumerate(results):
        img_height, img_width, _ = image_batch[i].shape
        img_file, yolo_img_queue, video_name = image_paths[i]

        output_folder = f'./{video_name}/object_detection/kickboard_img'
        label_folder = f'./{video_name}/object_detection/kickboard_label'
        original_folder = f'./{video_name}/object_detection/CCTV_img'

        # 폴더가 존재하지 않으면 생성
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not os.path.exists(label_folder):
            os.makedirs(label_folder)
        if not os.path.exists(original_folder):
            os.makedirs(original_folder)

        objects_detected = False
        valid_boxes = []  # 조건을 만족하는 박스를 저장할 리스트

        if result.boxes is not None and len(result.boxes) > 0:
            for box in result.boxes:
                # 객체의 높이와 너비 계산
                width = box.xywh[0][2] / img_width  # 너비
                height = box.xywh[0][3] / img_height  # 높이

                # 너비 또는 높이가 0.5보다 작은 경우에만 저장
                if width < 0.5 and height < 0.5:
                    valid_boxes.append(box)
                    objects_detected = True

        if objects_detected and valid_boxes:
            # 원본 이미지 저장
            original_img_path = os.path.join(original_folder, os.path.basename(img_file))
            cv2.imwrite(original_img_path, image_batch[i])

            # 검출 결과 그리기
            result_img = result.plot()
            result_img_path = os.path.join(output_folder, os.path.basename(img_file))

            # 검출 결과 이미지 저장
            cv2.imwrite(result_img_path, result_img)
            yolo_img_queue.put(result_img_path)

            # 유효한 박스들에 대한 라벨 저장 (YOLO 형식)
            label_file_path = os.path.join(label_folder, f"{os.path.splitext(os.path.basename(img_file))[0]}.txt")
            with open(label_file_path, 'w') as label_file:
                for box in valid_boxes:
                    class_id = int(box.cls[0])  # 클래스 ID
                    x_center = box.xywh[0][0] / img_width  # x 중심
                    y_center = box.xywh[0][1] / img_height  # y 중심
                    width = box.xywh[0][2] / img_width  # 너비
                    height = box.xywh[0][3] / img_height  # 높이

                    label_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        # 객체가 검출되지 않으면 결과 저장 안 함
        if not objects_detected:
            print(f"검출된 객체 없음: {img_file}")
