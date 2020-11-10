from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from main_view import Ui_MainWindow
from Face_Recognizer import *
import qdarkstyle

class RecognizerApp(QMainWindow, Ui_MainWindow):
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

        self.addFaceBtn.clicked.connect(lambda:self.addNewUser(self.faceName.text()))
        self.detectFaceBtn.clicked.connect(self.authenticate)

    def addNewUser(self, user_name):
        self.user_name = user_name
        self.image_path = Face_Recognizer().saveFaceImage(self.user_name)
        status = Face_Recognizer().registerFace(self.user_name, self.image_path)
        if status == 'success':
            print('success')
            self.statusDisplay.setText('Your face data was added successfully')
        elif status == 'failed':
            print('failed')
            self.statusDisplay.setText('Couldn\'t detect your face, please try again')

    def authenticate(self):
        self.obj = Face_Recognizer()
        self.obj.im_s.new_image.connect(self.change_image)
        self.obj.compareToDatabase()

    def change_image(self , image_path):
        pix_map = QPixmap(image_path)
        self.cameraWindow.setPixmap(pix_map)


dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()

app = QApplication([])
app.setStyleSheet(dark_stylesheet)
window = RecognizerApp()
app.exec_()


