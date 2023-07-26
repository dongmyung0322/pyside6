from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QWidget, QListWidget, QLabel, QDialog, QGroupBox
import sys
import csv

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('복잡한 UI 응용')
        self.resize(500,250)

        # 그룹 상자 설정
        group_box1 = QGroupBox('info')
        group_box2 = QGroupBox('입력 내용 보기')
        group_box3 = QGroupBox('저장 & 불러오기')

        # 라벨 설정
        self.label_id = QLabel('id: ')
        self.label_age = QLabel('나이: ')
        self.label_gender = QLabel('성별: ')
        self.label_country = QLabel('국가: ')

        # input label 설정
        self.id_line_edit = QLineEdit()
        self.age_line_edit = QLineEdit()
        self.gender_line_edit = QLineEdit()
        self.country_line_edit = QLineEdit()

        # push box 설정
        self.view_button = QPushButton('보기')
        self.view_button.clicked.connect(self.show_info)
        self.close_button = QPushButton('닫기')
        self.close_button.clicked.connect(self.close_info)

        self.save_button = QPushButton('저장')
        self.save_button.clicked.connect(self.save_info)
        self.load_button = QPushButton('불러오기')
        self.load_button.clicked.connect(self.load_info)

        # 리스트 박스 설정 
        self.list_widget = QListWidget()

        # 그룹 상자 1
        layout1 = QVBoxLayout()
        layout1.addWidget(self.label_id)
        layout1.addWidget(self.id_line_edit)
        layout1.addWidget(self.label_age)
        layout1.addWidget(self.age_line_edit)
        layout1.addWidget(self.label_gender)
        layout1.addWidget(self.gender_line_edit)
        layout1.addWidget(self.label_country)
        layout1.addWidget(self.country_line_edit)

        group_box1.setLayout(layout1)

        # 그룹 상자 2
        self.info_label = QLabel()
        layout2 = QVBoxLayout()
        layout2.addWidget(self.info_label)
        layout2.addWidget(self.view_button)
        layout2.addWidget(self.close_button)
        layout2.setContentsMargins(10, 10, 10, 10)

        group_box2.setLayout(layout2)

        # 그룹 상자 3
        layout3 = QVBoxLayout()
        layout3.addWidget(self.save_button)
        layout3.addWidget(self.load_button)
        layout3.addWidget(self.list_widget)
        layout3.setContentsMargins(10, 10, 10, 10)

        group_box3.setLayout(layout3)

        # 전체 레이아웃
        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box1)
        main_layout.addWidget(group_box2)
        main_layout.addWidget(group_box3)

        self.setLayout(main_layout)

    def show_info(self):
        id = self.id_line_edit.text()
        age = self.age_line_edit.text()
        gender = self.gender_line_edit.text()
        country = self.country_line_edit.text()

        info_text = f'아이디: {id} \n나이: {age} \n성별: {gender} \n국가: {country} \n'
        self.info_label.setText(info_text)

    def close_info(self):
        self.id_line_edit.clear()
        self.age_line_edit.clear()
        self.gender_line_edit.clear()
        self.country_line_edit.clear()
        self.info_label.clear()

    def save_info(self):
        id = self.id_line_edit.text()
        age = self.age_line_edit.text()
        gender = self.gender_line_edit.text()
        country = self.country_line_edit.text()

        data = [id, age, gender, country]

        try:
            with open('info.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)
            QMessageBox.information(self, '저장완료', '정보가 성공적으로 저장되었습니다')
        except Exception as e:
            QMessageBox.critical(self, '저장실패', f'저장중 에러가 발생했습니다:\n {str(e)}')

    def load_info(self):
        self.list_widget.clear()

        try:
            with open('info.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    data_text = f'id: {row[0]}, 나이: {row[1]}, 성별: {row[2]}, 국가: {row[3]}'
                    self.list_widget.addItem(data_text)

        except Exception as e:
            QMessageBox.critical(self, '정보 불러오기 실패', f'불러오기중 에러가 발생했습니다:\n {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())