from PySide6.QtWidgets import QApplication, QPushButton
 
def handle_button_click():
    print('버튼이 클릭되었습니다')

app = QApplication([])
button = QPushButton('클릭하세요')

button.clicked.connect(handle_button_click)

button.show()
app.exec()