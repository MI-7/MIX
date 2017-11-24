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
from ui.infodialog import *

class MixMainWindow(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'MIX Interpreter'
        self.left = 10
        self.top = 10
        self.width = 1280
        self.height = 960
        self.current_line = 0
        self.total_line = 0
        self.code_to_execute = ""
        self.code_text = ""
        self.code_text_in_list = []
        self.memory = MemoryState()
        self.initUI()

    @pyqtSlot()
    def on_click_debug(self):
        pass

    @pyqtSlot()
    def on_click_stop(self):
        pass

    @pyqtSlot()
    def on_click_resume(self):
        pass

    @pyqtSlot()
    def on_click_info(self):
        dialog = InfoDialog()
        sG = QApplication.desktop().screenGeometry()
        x = (sG.width()-dialog.width()) / 2
        y = (sG.height()-dialog.height()) / 2
        
        dialog.move(x,y)
        dialog.exec_()

    @pyqtSlot()
    def on_click_step(self):
        (self.code_to_execute, self.current_line) = self.next_stmt_sm.step(undef)
        
        #print("code_to_execute:"+self.code_to_execute+"..total:"+str(self.total_line)+"..current:"+str(self.current_line))
        #print("code_to_execute:" + self.code_to_execute)
        
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
        mapp = MixALPreProcessor(self.code_text_in_list)
        mapp.preprocessall()
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
    
    def initUI(self):
        # window layout
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon("res/ico/openfile.ico"))
        
        self.textbox_code = CodeEditor("", self)
        self.textbox_code.move(QPoint(10, 55))
        self.textbox_code.resize(QSize(300, 720))
        self.textbox_code.setPlainText("abc"+os.linesep+"cde"+os.linesep+"fgh")

        # initiate menu
        self.action_open_file = QAction(QIcon("res/ico/openfile.ico"), "&Open File", self, triggered=self.on_click_open)
        self.action_debug = QAction(QIcon("res/ico/debug.ico"), "&Debug", self, triggered=self.on_click_debug)
        self.action_step = QAction(QIcon("res/ico/debug_step.ico"), "&Step", self, triggered=self.on_click_step)
        self.action_resume = QAction(QIcon("res/ico/debug_resume.ico"), "&Resume", self, triggered=self.on_click_resume)
        self.action_stop = QAction(QIcon("res/ico/debug_stop.ico"), "S&top", self, triggered=self.on_click_stop)
        self.action_run = QAction(QIcon("res/ico/run.ico"), "&Go", self, triggered=self.on_click_go)
        self.action_info = QAction(QIcon("res/ico/alien.ico"), "&Info", self, triggered=self.on_click_info)
        
        self.openMenu = self.menuBar().addMenu("&文件")
        self.openMenu.addAction(self.action_open_file)
        self.debugMenu = self.menuBar().addMenu("&调试")
        self.debugMenu.addAction(self.action_debug)
        self.debugMenu.addAction(self.action_step)
        self.debugMenu.addAction(self.action_resume)
        self.debugMenu.addAction(self.action_stop)
        self.debugMenu.addAction(self.action_run)
        self.infoMenu = self.menuBar().addMenu("&信息")
        self.infoMenu.addAction(self.action_info)

        self.toolbar = self.addToolBar('Open')
        self.toolbar.addAction(self.action_open_file)
        self.toolbar = self.addToolBar('Debug')
        self.toolbar.addAction(self.action_debug)
        self.toolbar = self.addToolBar('Step')
        self.toolbar.addAction(self.action_step)
        self.toolbar = self.addToolBar('Resume')
        self.toolbar.addAction(self.action_resume)
        self.toolbar = self.addToolBar('Stop')
        self.toolbar.addAction(self.action_stop)
        self.toolbar = self.addToolBar('Run')
        self.toolbar.addAction(self.action_run)
        self.toolbar = self.addToolBar('Info')
        self.toolbar.addAction(self.action_info)

        self.show()