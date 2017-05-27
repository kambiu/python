import sys

from PyQt5.QtWidgets import QApplication, QWidget



app = QApplication(sys.argv)



window = QWidget()

window.setGeometry(1000, 500, 500, 300)

window.setWindowTitle('This is the Windows Title')



window.show()

sys.exit(app.exec_())