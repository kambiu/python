import sys

from PyQt5.QtCore import QCoreApplication, Qt

from PyQt5.QtGui import QIcon, QColor

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox

from PyQt5.QtWidgets import QCalendarWidget, QFontDialog, QColorDialog, QTextEdit, QFileDialog

from PyQt5.QtWidgets import QCheckBox, QProgressBar, QComboBox, QLabel, QStyleFactory, QLineEdit, QInputDialog







class window(QMainWindow):



    def __init__(self):

        super(window, self).__init__()

        self.setGeometry(50, 50, 800, 500)

        self.setWindowTitle('pyqt5 Tut')

        self.setWindowIcon(QIcon('pic.png'))



        extractAction = QAction('&Get to the choppah', self)

        extractAction.setShortcut('Ctrl+Q')

        extractAction.setStatusTip('leave the app')

        extractAction.triggered.connect(self.close_application)



        openEditor = QAction('&Editor', self)

        openEditor.setShortcut('Ctrl+E')

        openEditor.setStatusTip('Open Editor')

        openEditor.triggered.connect(self.editor)



        openFile = QAction('&Open File', self)

        openFile.setShortcut('Ctrl+O')

        openFile.setStatusTip('Open File')

        openFile.triggered.connect(self.file_open)


		# ch15
        saveFile = QAction('&Save File', self)

        saveFile.setShortcut('Ctrl+S')

        saveFile.setStatusTip('Save File')

        saveFile.triggered.connect(self.file_save)





        self.statusBar()



        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&File')

        fileMenu.addAction(extractAction)



        fileMenu.addAction(openFile)
		# ch15
        fileMenu.addAction(saveFile)





        editorMenu = mainMenu.addMenu('&Editor')

        editorMenu.addAction(openEditor)



        extractAction = QAction(QIcon('pic.png'), 'flee the scene', self)

        extractAction.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar('extraction')

        self.toolBar.addAction(extractAction)



        fontChoice = QAction('Font', self)

        fontChoice.triggered.connect(self.font_choice)

        # self.toolBar = self.addToolBar('Font')

        self.toolBar.addAction(fontChoice)



        cal = QCalendarWidget(self)

        cal.move(500, 200)

        cal.resize(200, 200)



        self.home()



    def editor(self):

        self.textEdit = QTextEdit()

        self.setCentralWidget(self.textEdit)



    def file_open(self):

        # need to make name an tupple otherwise i had an error and app crashed

        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)

        print('tot na dialog gelukt')  # for debugging

        file = open(name, 'r')

        print('na het inlezen gelukt') # for debugging

        self.editor()



        with file:

            text = file.read()

            self.textEdit.setText(text)


	# ch15
    def file_save(self):

        name, _ = QFileDialog.getSaveFileName(self,'Save File', options=QFileDialog.DontUseNativeDialog)

        file = open(name, 'w')

        text = self.textEdit.toPlainText()

        file.write(text)

        file.close()



    def color_picker(self):

        color = QColorDialog.getColor()

        self.styleChoice.setStyleSheet('QWidget{background-color: %s}' % color.name())



    def font_choice(self):

        font, valid = QFontDialog.getFont()

        if valid:

            self.styleChoice.setFont(font)



    def home(self):

        btn = QPushButton('quit', self)

        btn.clicked.connect(self.close_application)

        btn.resize(btn.sizeHint())

        btn.move(0, 100)



        checkBox = QCheckBox('Enlarge window', self)

        # checkBox.toggle()  # if you want to be checked in in the begin

        checkBox.move(0, 50)

        checkBox.stateChanged.connect(self.enlarge_window)



        self.progress = QProgressBar(self)

        self.progress.setGeometry(200, 80, 250, 20)



        self.btn = QPushButton('download', self)

        self.btn.move(200, 120)

        self.btn.clicked.connect(self.download)



        self.styleChoice = QLabel('Windows', self)

        comboBox = QComboBox(self)

        comboBox.addItem('motif')

        comboBox.addItem('Windows')

        comboBox.addItem('cde')

        comboBox.addItem('Plastique')

        comboBox.addItem('Cleanlooks')

        comboBox.addItem('windowsvista')



        comboBox.move(25, 250)

        self.styleChoice.move(25, 150)

        comboBox.activated[str].connect(self.style_choice)



        color = QColor(0,0,0)

        fontColer = QAction('font bg color', self)

        fontColer.triggered.connect(self.color_picker)

        self.toolBar.addAction(fontColer)



        self.show()



    def style_choice(self, text):

        self.styleChoice.setText(text)

        QApplication.setStyle(QStyleFactory.create(text))



    def download(self):

        self.completed = 0



        while self.completed < 100:

            self.completed += 0.0001

            self.progress.setValue(self.completed)



    def enlarge_window(self, state):

        if state == Qt.Checked:

            self.setGeometry(50, 50, 1000, 600)

        else:

            self.setGeometry(50, 50 , 500, 300)



    def close_application(self):



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