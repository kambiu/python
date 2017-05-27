import sys

from PyQt5.QtCore import QCoreApplication

# from PyQt5.QtGui import *

from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox

from PyQt5.uic.properties import QtGui





class window(QMainWindow):



    def __init__(self):

        super(window, self).__init__()

        self.setGeometry(50, 50, 500, 300)

        self.setWindowTitle('pyqt5 Tut')

        extractAction = QAction('&Get to the choppah', self)

        extractAction.setShortcut('Ctrl+Q')

        extractAction.setStatusTip('leave the app')

        extractAction.triggered.connect(self.close_application)



        self.statusBar()



        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&File')

        fileMenu.addAction(extractAction)



        extractAction = QAction(QIcon('chrome.png'), 'flee the scene', self)

        extractAction.triggered.connect(self.close_application)



        self.toolBar = self.addToolBar('extraction')

        self.toolBar.addAction(extractAction)



        self.home()



    def home(self):

        btn = QPushButton('quit', self)

        btn.clicked.connect(self.close_application)

        btn.resize(btn.sizeHint())

        btn.move(0, 100)



        self.show()



    def close_application(self):


		# ch7
        choice = QMessageBox.question(self, 'Message',

                                     "Are you sure to quit?", QMessageBox.Yes |

                                     QMessageBox.No, QMessageBox.No)



        if choice == QMessageBox.Yes:

            print('quit application')

            sys.exit()

        else:

            pass



if __name__ == "__main__":  # had to add this otherwise app crashed



    def run():

        app = QApplication(sys.argv)

        Gui = window()

        sys.exit(app.exec_())



run()