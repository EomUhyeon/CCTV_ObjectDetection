import sys
import threading
import multiprocessing
from PySide6.QtWidgets import QApplication
from gui_package import MainWindow
from cctv_save import cctv_save
from object_detection_241001_003 import yolo_process

class CCTVObjectDetection:
    def __init__(self):
        # 학성 중학교 hagseong junghaggyo
        self.video_url_01 = 'http://211.34.248.240:1935/live/T065.stream/playlist.m3u8'
        self.video_name_01 = 'hagseong_junghaggyo'
        self.save_interval_01 = 10
        self.save_quality_01 = 90
        self.cctv_to_yolo_queue_01 = multiprocessing.Queue()

        self.cctv_img_queue_01 = multiprocessing.Queue()
        cctv_process_01 = multiprocessing.Process(
            target=cctv_save,
            args=(self.video_url_01, self.video_name_01, self.save_interval_01, self.save_quality_01,
                  self.cctv_img_queue_01, self.cctv_to_yolo_queue_01))
        cctv_process_01.start()

        # 서부역 입구 삼거리 seobuyeog ibgu samgeoli
        self.video_url_02 = 'https://wowza.cheonan.go.kr/live/cctv002.stream/playlist.m3u8'
        self.video_name_02 = 'seobuyeog_ibgu_samgeoli'
        self.save_interval_02 = 15
        self.save_quality_02 = 90
        self.cctv_to_yolo_queue_02 = multiprocessing.Queue()

        self.cctv_img_queue_02 = multiprocessing.Queue()
        cctv_process_02 = multiprocessing.Process(
            target=cctv_save,
            args=(self.video_url_02, self.video_name_02, self.save_interval_02, self.save_quality_02,
                  self.cctv_img_queue_02, self.cctv_to_yolo_queue_02))
        cctv_process_02.start()

        self.yolo_img_queue_01 = multiprocessing.Queue()
        self.yolo_img_queue_02 = multiprocessing.Queue()
        yolo = multiprocessing.Process(
            target=yolo_process,
            args=(32,
                  self.video_name_01, self.yolo_img_queue_01, self.cctv_to_yolo_queue_01,
                  self.video_name_02, self.yolo_img_queue_02, self.cctv_to_yolo_queue_02))
        yolo.start()

        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.window.show()

    def gui_controller(self):
        while True:
            if not self.cctv_img_queue_01.empty():
                img_path = self.cctv_img_queue_01.get()
                self.window.update_label_image(img_path, 0)
            if not self.yolo_img_queue_01.empty():
                img_path = self.yolo_img_queue_01.get()
                self.window.update_label_image(img_path, 1)

            if not self.cctv_img_queue_02.empty():
                img_path = self.cctv_img_queue_02.get()
                self.window.update_label_image(img_path, 2)
            if not self.yolo_img_queue_02.empty():
                img_path = self.yolo_img_queue_02.get()
                self.window.update_label_image(img_path, 3)

    def run(self):
        thread = threading.Thread(target=self.gui_controller)
        thread.start()

        sys.exit(self.app.exec())


if __name__ == "__main__":
    cctv_object_detection = CCTVObjectDetection()
    cctv_object_detection.run()
