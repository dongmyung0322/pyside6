import sys
import os
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QFileDialog, QTreeWidget, \
      QTreeWidgetItem, QListWidget, QHBoxLayout

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('이미지 뷰어')
        self.resize(800,600)

        self.folder_open = QPushButton('폴더 열기')
        self.folder_open.clicked.connect(self.open_folder_dialog)
        self.back_button = QPushButton('뒤로 가기')
        self.back_button.clicked.connect(self.go_back)
        self.forward_button = QPushButton('앞으로 가기')
        self.forward_button.clicked.connect(self.go_forward)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        self.image_list_widget = QListWidget()
        self.image_list_widget.currentRowChanged.connect(self.display_image)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(['파일'])

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.folder_open)
        left_layout.addWidget(self.image_list_widget)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.image_label)
        right_layout.addWidget(self.back_button)
        right_layout.addWidget(self.forward_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.current_folder= ''
        self.current_images = []
        self.current_idx = -1

    def open_folder_dialog(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        folder_dialog.directoryEntered.connect(self.set_folder_path)
        folder_dialog.accepted.connect(self.load_image)
        folder_dialog.exec()

    def set_folder_path(self, folder_path):
        self.current_folder = folder_path

    def load_image(self):
        self.image_list_widget.clear()
        self.tree_widget.clear()

        if self.current_folder:
            self.current_images = []
            self.current_idx = -1

            image_extentions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

            root_item = QTreeWidgetItem(self.tree_widget, [self.current_folder])
            self.tree_widget.addTopLevelItem(root_item)

            for dir_path, _, file_names in os.walk(self.current_folder):
                dir_item = QTreeWidgetItem(root_item, [os.path.basename(dir_path)])
                root_item.addChild(dir_item)

                for file_name in file_names:
                    if file_name.lower().endswith(image_extentions):
                        file_item = QTreeWidgetItem(dir_item, [file_name])
                        dir_item.addChild(file_item)
                        file_path = os.path.join(dir_path, file_name)
                        self.current_images.append(file_path)
                        self.image_list_widget.addItem(file_name)

            if self.current_images:
                self.image_list_widget.setCurrentRow(0)

    def display_image(self, idx):
        if 0 <= idx < len(self.current_images):
            self.current_idx = idx
            image_path = self.current_images[self.current_idx]
            pixmap = QtGui.QPixmap(image_path)
            scale_pixmap = pixmap.scaled(self.image_label.size() * 0.5, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scale_pixmap)

    def go_back(self):
        if self.current_idx > 0:
            self.image_list_widget.setCurrentRow(self.current_idx - 1)

    def go_forward(self):
        if self.current_idx < len(self.current_images) - 1:
            self.image_list_widget.setCurrentRow(self.current_idx +1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec())


