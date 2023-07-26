from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QWidget
import sys
import os

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('탐색기')
        self.resize(500,400)

        self.folder_button = QPushButton('폴더 열기')
        self.folder_button.clicked.connect(self.open_folder_dialog)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(['파일'])

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.folder_button)
        main_layout.addWidget(self.tree_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.folder_path=''

    def open_folder_dialog(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.Directory)   # 대화 상자 폴더 선택모드
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)   # 파일 대화상자가 디렉토리만 표시
        folder_dialog.directoryEntered.connect(self.set_folder_path)   # set_folder_path 함수를 실행시켜 선택한 폴더를 경로로 설정
        folder_dialog.accepted.connect(self.display_files)   # 파일 표시 역할을 하는 함수 
        folder_dialog.exec_()

    def set_folder_path(self, folder_path):
        self.folder_path = folder_path

    def display_files(self):
        if self.folder_path:
            self.tree_widget.clear()

            root_item = QTreeWidgetItem(self.tree_widget, [self.folder_path])  # 최상위 디랙토리 설정
            self.tree_widget.addTopLevelItem(root_item)

            for dir_path, _, file_names in os.walk(self.folder_path):  # for 문으로 folder path의 아이탬 찾기
                dir_item = QTreeWidgetItem(root_item, [os.path.basename(dir_path)])
                root_item.addChild(dir_item)

                for file_name in file_names:
                    file_item = QTreeWidgetItem(dir_item, [file_name])
                    dir_item.addChild(file_item)

                root_item.setExpanded(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileExplorer()
    window.show()
    sys.exit(app.exec())