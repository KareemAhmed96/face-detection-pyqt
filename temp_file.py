from PyQt5.QtWidgets import *
from main_view import Ui_MainWindow
import qdarkstyle

class CustomApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.submitBtn.clicked.connect(self.logToSystem)
        self.show()

    def logToSystem(self):
        user_name = self.userName.text()
        password  = self.userPass.text()
        if user_name == 'admin' and password == 'admin':
            self.stackedPages.setCurrentIndex(1)
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Login Error")
            msg_box.setText("The username or password maybe incorrect")
            msg_box.exec_()

dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()

app = QApplication([])
app.setStyleSheet(dark_stylesheet)
window = CustomApp()
app.exec_()