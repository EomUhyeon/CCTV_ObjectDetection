from PySide6.QtWidgets import QMainWindow, QLabel, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from gui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # UI 설정
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # QScrollArea 설정
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # 기존 centralwidget에 QScrollArea 추가
        self.scroll_area.setWidget(self.ui.centralwidget)
        self.setCentralWidget(self.scroll_area)

        # 라벨 리스트 생성
        self.labels = []
        self.add_labels_to_grid(4)

    def add_labels_to_grid(self, count):
        for i in range(count):
            row = i // 2
            col = i % 2
            label = QLabel(f"Waiting for image {i + 1}", self)
            label.setAlignment(Qt.AlignCenter)
            self.ui.gridLayout.addWidget(label, row, col)
            self.labels.append(label)

    def update_label_image(self, image_path, label_num):
        pixmap = QPixmap(image_path).scaled(400, 400, Qt.KeepAspectRatio)
        self.labels[label_num].setPixmap(pixmap)
