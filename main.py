import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from memorystate import *
import numpy as np
from utility import *
from codeeditor import CodeEditor
from mixaltomachinecode import *
from mixalpreprocessor import *
from mixexecutor import *

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window'
        self.left = 10
        self.top = 10
        self.width = 1024
        self.height = 768
        self.current_line = 0
        self.total_line = 0
        self.code_to_execute = ""
        self.code_text = ""
        self.code_text_in_list = []
        self.memory = MemoryState()
        self.initUI()
 
    @pyqtSlot()
    def on_click_step(self):
        (self.code_to_execute, self.current_line) = self.next_stmt_sm.step(undef)
        
        #print("code_to_execute:"+self.code_to_execute+"..total:"+str(self.total_line)+"..current:"+str(self.current_line))
        print("code_to_execute:" + self.code_to_execute)
        
        extraSelections = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(Qt.yellow).lighter(160)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        
        # self.textbox_code.moveCursor(QTextCursor.End)
        
        #cur = self.textbox_code.textCursor()
        cur = QTextCursor(self.textbox_code.document().findBlockByLineNumber(self.current_line))
        self.textbox_code.setTextCursor(cur)
        
        selection.cursor = cur
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        #self.textbox_code.setExtraSelections(extraSelections)
            
    @pyqtSlot()
    def on_click_start(self):
        self.current_line = 0
        self.total_line = self.textbox_code.document().lineCount()

        cur = QTextCursor(self.textbox_code.document().findBlockByLineNumber(self.current_line))
        self.textbox_code.setTextCursor(cur)
        
        self.memory = MemoryState()
        
        print("total:"+str(self.total_line)+"current:"+str(self.current_line))
    
    @pyqtSlot()
    def on_click_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '~/',"Program Files (*.*)")
        if (fname[0]!=''):
            f = open(fname[0], 'r')
            with f:
                self.code_text = f.read()

                self.code_text_in_list = self.code_text.splitlines()
                #print(self.code_text_in_list)
                
                self.textbox_code.setPlainText(self.code_text)
                
                self.current_line = 0
                self.total_line = self.textbox_code.document().lineCount()
                
                print("total:"+str(self.total_line)+"current:"+str(self.current_line))
            f.close()

    @pyqtSlot()
    def on_click_go(self):
        mapp = MixALPreProcessor(self.code_text_in_list, self.memory)
        mapp.preprocessall()
        processed_code = mapp.processed_code
        processed_code_dict = mapp.processed_code_dict
        orig = mapp.orig
        end = mapp.end
        
        mixlog(MDEBUG, "finished preprocessing")
        
        # load everything into memory
        for line in processed_code_dict.keys():
            sm = MixToMachineCodeTranslatorSM()
            sm.transduce([x for x in processed_code_dict[line]], False)
            (sym, aa, i, f, op, c) = sm.output
            aa = dectobin(my_int(aa), 2)
            self.memory.setMemory(line, [sym] + aa + [i, f, c])
    
        me = MixExecutor(processed_code_dict, orig, end, self.memory)
        me.go(True)
        mixlog(MDEBUG, "finished executing")
        #for n in range (3000, 3050):
            #print("M:", ms.getMemory(n))
        print("M:", self.memory.getMemory(2000))
        print("A:", self.memory.getA())
        print("X:", self.memory.getX())
        print("i1", self.memory.geti1())
        print("i2", self.memory.geti2())
        print("i3", self.memory.geti3())
        print("i4", self.memory.geti4())
        print("i5", self.memory.geti5())
        print("i6", self.memory.geti6())
        print("cmp", self.memory.getcomparisonindicator())
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.textbox_code = CodeEditor("", self)
        self.textbox_code.move(QPoint(10, 10))
        self.textbox_code.resize(QSize(500, 720))
        self.textbox_code.setPlainText("abc"+os.linesep+"cde"+os.linesep+"fgh")
 
        # Create a button in the window
        self.button_open = QPushButton('Open', self)
        self.button_open.move(510,350)
        
        self.button_start = QPushButton('Reset', self)
        self.button_start.move(510,380)
        
        self.button_step = QPushButton('Step', self)
        self.button_step.move(610,380)
        
        self.button_go = QPushButton('Go', self)
        self.button_go.move(710,380)
 
        # connect button to function on_click
        self.button_start.clicked.connect(self.on_click_start)
        self.button_step.clicked.connect(self.on_click_step)
        self.button_open.clicked.connect(self.on_click_open)
        self.button_go.clicked.connect(self.on_click_go)
        
        self.show()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
