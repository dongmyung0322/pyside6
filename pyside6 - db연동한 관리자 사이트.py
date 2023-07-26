import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,\
    QStackedWidget, QListWidget
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 데이터 베이스 설정
os.makedirs('./db', exist_ok=True)
engine = create_engine('sqlite:///db/user.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) # db중복 방지용 id
    username = Column(String, unique=True )
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

# 데이터 베이스 세션 설정
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

#회원 가입 페이지
class RegisterPage(QWidget):
    def __init__(self, stacked_widget, main_window):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.main_window = main_window

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.register)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.register_button)
        
        self.setLayout(self.layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please Enter username and password')
            return
        
        # 사용자 생성
        user = User(username, password)
        
        # 데이터베이스에 추가
        session.add(user)
        session.commit()

        QMessageBox.information(self, 'Success', 'Register Successful')
        self.stacked_widget.setCurrentIndex(1) # 현제 페이지를 (1)번 페이지로 지정

        self.main_window.show_login_page() # 로그인 페이지로 넘어감

    
# 로그인 페이지
class LoginPage(QWidget):
    def __init__(self, stacked_widget, main_window):
        super().__init__()
        
        self.stacked_widget = stacked_widget
        self.main_window = main_window

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)
        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.register)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)
        
        self.setLayout(self.layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        user = session.query(User).filter_by(username=username, password=password).first()

        if user:
            QMessageBox.information(self, 'Success', 'Login successful')
            self.stacked_widget.setCurrentIndex(2) # 페이지 인덱스를 2로 지정

            self.main_window.show_admin_page() # admin페이지로 이동

        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')

    def register(self):
        self.main_window.show_register_page()


# 관리자 페이지
class AdminPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.user_list = QListWidget()

        self.show_user_list_button = QPushButton('Show user list')
        self.show_user_list_button.clicked.connect(self.show_user_list)
        self.logout_button = QPushButton('Logout')
        self.logout_button.clicked.connect(self.logout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.show_user_list_button)
        self.layout.addWidget(self.user_list)
        self.layout.addWidget(self.logout_button)

        self.setLayout(self.layout)

    def show_user_list(self):
        self.user_list.clear()

        # 모든 사용자 조회
        users = session.query(User).all()

        for user in users:
            self.user_list.addItem(user.username)

    def logout(self):
        self.main_window.show_login_page()


# 메인 창
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('User Authorization')

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.register_page = RegisterPage(self.stacked_widget, self)
        self.login_page = LoginPage(self.stacked_widget, self)
        self.admin_page = AdminPage(self)

        self.stacked_widget.addWidget(self.login_page)  
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.admin_page)

        self.show_login_page() # 초기 페이지를 로그인 페이지로 보이게 지정

    def show_register_page(self):
        self.stacked_widget.setCurrentIndex(1)  # 회원가입 페이지 인덱스 = 1
        self.register_page.username_input.clear()
        self.register_page.password_input.clear()

    def show_login_page(self):
        self.stacked_widget.setCurrentIndex(0)  # 로그인 페이지 인덱스 = 0
        self.register_page.username_input.clear()
        self.register_page.password_input.clear()

    def show_admin_page(self):
       #self.admin_page.update_user_list()
        self.stacked_widget.setCurrentIndex(2)  # 어드민 페이지 인덱스 = 2



if __name__ == '__main__':
    app = QApplication(sys.argv)
    #window = RegisterPage(stacked_widget= None, main_window= None)
    #window = AdminPage(main_window=None)
    window = MainWindow()
    window.show()
    app.exec_()

