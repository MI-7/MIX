from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class InfoDialog(QDialog): 
    def __init__(self, parent=None): 
        super(InfoDialog, self).__init__(parent)
        self.initUI() 
        self.setWindowIcon(QIcon("res/ico/alien.ico"))
        self.setWindowTitle("信息") 
        self.resize(240, 100)

    def initUI(self):
        self.label = QLabel(self)
        self.label.setFixedWidth(200)
        self.label.setFixedHeight(40)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(u"MUHAHAHAHAHAHAHAHAHA")

        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.red)
        self.label.setAutoFillBackground(True)
        #pe.setColor(QPalette.Window,Qt.green)  
        #pe.setColor(QPalette.Background,Qt.blue)  
        self.label.setPalette(pe)

        self.label.setFont(QFont("Roman times",10,QFont.Bold))  
          
        self.label.move(10,10)
        #grid = QGridLayout() 
        #grid.addWidget(QLabel("路径："), 0, 0) 
        #self.pathLineEdit = QLineEdit() 
        #self.pathLineEdit.setFixedWidth(200) 
        #grid.addWidget(self.pathLineEdit, 0, 1) 
        #button = QPushButton("更改") 
        #button.clicked.connect(self.changePath) 
        #grid.addWidget(button, 0, 2) 
        #grid.addWidget(QLabel("<font color='#ff0000'>包含Keywords.xml、Avatar,AvatarSet,Market.xls的路径</font>"), 1, 0, 1, 3) 
        #buttonBox = QDialogButtonBox() 
        #buttonBox.setOrientation(Qt.Horizontal)  # 设置为水平方向
        #buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel) 
        #buttonBox.accepted.connect(self.accept)  # 确定
        #buttonBox.rejected.connect(self.reject)  # 取消
        #grid.addWidget(buttonBox, 2, 1) 
        #self.setLayout(grid) 

#    def changePath(self): 
#        open = QFileDialog() 
#        self.path = open.getExistingDirectory() 
#        self.pathLineEdit.setText(self.path) 
#        print(self.path)