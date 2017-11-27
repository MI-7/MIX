from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class InfoDialog(QDialog): 
    def __init__(self, txt, parent=None): 
        super(InfoDialog, self).__init__(parent)
        self.txt = txt
        self.initUI() 
        self.setWindowIcon(QIcon("res/ico/alien.ico"))
        self.setWindowTitle("INFO") 
        self.resize(240, 100)

    def initUI(self):
        self.label = QLabel(self)
        self.label.setFixedWidth(200)
        self.label.setFixedHeight(40)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(self.txt)

        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.red)
        self.label.setAutoFillBackground(True)
        #pe.setColor(QPalette.Window,Qt.green)  
        #pe.setColor(QPalette.Background,Qt.blue)  
        self.label.setPalette(pe)

        self.label.setFont(QFont("Roman times", 10, QFont.Bold))  
          
        self.label.move(10,10)

#    def changePath(self): 
#        open = QFileDialog() 
#        self.path = open.getExistingDirectory() 
#        self.pathLineEdit.setText(self.path) 
#        print(self.path)