import sys

from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow



class window(QMainWindow):



    def __init__(self):

        super(window, self).__init__()

        self.setGeometry(50, 50, 500, 300)

        self.setWindowTitle('Lesson 2 pyqt5 Tut')

        self.setWindowIcon(QIcon('chrome.png'))

        self.show()



app = QApplication(sys.argv)

Gui = window()

sys.exit(app.exec_())