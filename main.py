from ui.app import *
from PyQt5.QtWidgets import QApplication
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MixMainWindow()
    
    sG = QApplication.desktop().screenGeometry()
    x = (sG.width()-ex.width) / 2
    y = (sG.height()-ex.height) / 2
    ex.move(x, y)
    
    sys.exit(app.exec_())