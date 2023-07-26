from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

def open_file_dialog():
    file_dialog = QFileDialog()
    file_dialog.setWindowTitle('파일열기')
    file_dialog.setFileMode(QFileDialog.ExistingFile) # 기존 파일 선택 모드
    file_dialog.setViewMode(QFileDialog.Detail) # 상세 보기 모드
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles() # 선택한 파일 처리 로직 작성
        print(selected_files)

app = QApplication([])
main_window = QMainWindow()
button = QPushButton('파일 열기', main_window)
button.clicked.connect(open_file_dialog)
main_window.show()
app.exec()