from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QWidget, QListWidget, QLabel, QDialog
import sys
import csv

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('정보 입력')

        self.age_line_edit = QLineEdit()
        self.gender_line_edit = QLineEdit()
        self.country_line_edit = QLineEdit()
        self.view_button = QPushButton('보기')

        layout = QVBoxLayout()
        layout.addWidget(QLabel('나이:'))
        layout.addWidget(self.age_line_edit)
        layout.addWidget(QLabel('성별:'))
        layout.addWidget(self.gender_line_edit)
        layout.addWidget(QLabel('국가:'))
        layout.addWidget(self.country_line_edit)
        layout.addWidget(self.view_button)

        self.setLayout(layout)

        self.view_button.clicked.connect(self.show_info)

    def show_info(self):
        age = self.age_line_edit.text()
        gender = self.gender_line_edit.text()
        country = self.country_line_edit.text()

        info_window = InfoWindow(age, gender, country)
        info_window.setModal(True) 
        info_window.exec()


class InfoWindow(QDialog):
    def __init__(self, age, gender, country):
        super().__init__()
        self.setWindowTitle('정보 확인')

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f'나이: {age}'))
        layout.addWidget(QLabel(f'성별: {gender}'))
        layout.addWidget(QLabel(f'국가: {country}'))

        save_button = QPushButton('저장')
        close_button = QPushButton('닫기')
        load_button = QPushButton('불러오기')

        layout.addWidget(save_button)
        layout.addWidget(close_button)
        layout.addWidget(load_button)

        self.setLayout(layout)

        save_button.clicked.connect(lambda: self.save_info(age, gender, country))
        close_button.clicked.connect(self.close)
        load_button.clicked.connect(self.load_info)

    def save_info(self, age, gender, country):
        data = [generate_id(), age, gender, country]
        try:
            with open('info.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)
            QMessageBox.information(self, '저장완료', '정보가 성공적으로 저장되었습니다')
        except Exception as e:
            QMessageBox.critical(self, '저장실패', f'저장중 에러가 발생했습니다:\n {str(e)}')

    def load_info(self):
        try:
            with open('info.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                lines = [line for line in reader]

            if len(lines) > 0:
                list_window = ListWindow(lines)
                list_window.exec()
            else:
                QMessageBox.information(self, '정보 불러오기', '저장된 정보가 없습니다')

        except Exception as e:
            QMessageBox.critical(self, '정보 불러오기 실패', f'불러오기중 에러가 발생했습니다:\n {str(e)}')


class ListWindow(QDialog):
    def __init__(self,lines):
        super().__init__()
        self.setWindowTitle('저장된 정보')

        list_widget = QListWidget()
        for line in lines:
            item = f'ID: {line[0]}, 나이: {line[1]}, 성별: {line[2]}, 국가: {line[3]}'
            list_widget.addItem(item)

        layout = QVBoxLayout()
        layout.addWidget(list_widget)

        self.setLayout(layout)


def generate_id():
    # ID를 생성하기 위해 현재 시간을 받아와 사용
    import time
    return int(time.time())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    input_window = InputWindow()
    input_window.show()
    sys.exit(app.exec())