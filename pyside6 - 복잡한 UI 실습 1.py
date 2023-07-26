from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QVBoxLayout, QGroupBox, QLabel, QLineEdit, QHBoxLayout 
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('복잡한 UI예시')

        # 그룹 상자 1
        group_box1 = QGroupBox('그룹 상자 1')
        label1 = QLabel('이름:')
        line_edit1 = QLineEdit()
        button1 = QPushButton('저장')

        layout1 = QVBoxLayout()
        layout1.addWidget(label1)
        layout1.addWidget(line_edit1)
        layout1.addWidget(button1)
        group_box1.setLayout(layout1)

        # 그룹 상자 2
        group_box2 = QGroupBox('그룹 상자 2')
        label2 = QLabel('나이:')
        line_edit2 = QLineEdit()
        button2 = QPushButton('취소')

        layout2 = QHBoxLayout()
        layout2.addWidget(label2)
        layout2.addWidget(line_edit2)
        layout2.addWidget(button2)
        group_box2.setLayout(layout2)

        # 전체 레이아웃
        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box1)
        main_layout.addWidget(group_box2)

        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())