from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('메시지 박스 예제')
        self.resize(500,400)

        layout = QVBoxLayout()

        info_button = QPushButton('정보 메시지')
        info_button.clicked.connect(self.show_info_message)
        layout.addWidget(info_button)

        warning_button = QPushButton('경고 메시지')
        warning_button.clicked.connect(self.show_warning_message)
        layout.addWidget(warning_button)

        question_button = QPushButton('질문 메시지')
        question_button.clicked.connect(self.show_question_message)
        layout.addWidget(question_button)

        self.setLayout(layout)

    def show_info_message(self):
        QMessageBox.information(self, '정보', '이것은 정보메시지 입니다', QMessageBox.Ok)

    def show_warning_message(self):
        QMessageBox.warning(self, '경고', '이것은 경고메시지 입니다', QMessageBox.Ok)

    def show_question_message(self):
        result = QMessageBox.question(self, '질문', '계속 진행하시겠습니까?', QMessageBox.Yes, QMessageBox.No)
        if result == QMessageBox.Yes:
            QMessageBox.information(self, '응답', '예를 클릭했습니다.', QMessageBox.Ok)
        else:
            QMessageBox.information(self, '응답', '아니오를 클릭했습니다.', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
        