from ui.mixmainwindow import *
from PyQt5.QtWidgets import QApplication
from ui.mixmemoryneon import *


class MainWindow(QMainWindow):
    count = 0

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        bar = self.menuBar()

        file = bar.addMenu("File")
        file.addAction("New")
        file.addAction("cascade")
        file.addAction("Tiled")
        file.triggered[QAction].connect(self.windowaction)
        self.setWindowTitle("MDI demo")

        self.initUI()

    @pyqtSlot()
    def on_click_debug(self):
        mapp_debug = MixALPreProcessor(self.executorwindow.code_text_in_list)
        try:
            mapp_debug.preprocessall()
        except Exception as err:
            mixlog(MERROR, str(err))
            traceback.print_exc()
            return

        processed_code_dict = mapp_debug.processed_code_dict
        processed_code = mapp_debug.processed_code
        orig = mapp_debug.orig
        end = mapp_debug.end

        mixlog(MDEBUG, "finished preprocessing")

        # clear memory
        self.executorwindow.memory = MemoryState()

        # load everything into memory
        for line in processed_code_dict.keys():
            sm = MixToMachineCodeTranslatorSM()
            sm.transduce([x for x in processed_code_dict[line]], False)
            (sym, aa, i, f, op, c) = sm.output
            aa = dectobin(my_int(aa), 2)
            self.executorwindow.memory.setMemory(line, [sym] + aa + [i, f, c])

        self.executorwindow.me = MixExecutor(processed_code_dict, orig, end, self.executorwindow.memory)
        self.executorwindow.me.start()
        mixlog(MDEBUG, "finished executing")
        self.executorwindow.tableWidget.clearContents()
        self.executorwindow.load_memory_into_display()

        self.action_debug.setEnabled(False)
        self.action_step.setEnabled(True)
        self.action_resume.setEnabled(True)
        self.action_stop.setEnabled(True)
        self.action_run.setEnabled(False)

        self.executorwindow.textbox_code.setPlainText(os.linesep.join(processed_code))

    @pyqtSlot()
    def on_click_stop(self):
        self.action_debug.setEnabled(True)
        self.action_step.setEnabled(False)
        self.action_resume.setEnabled(False)
        self.action_stop.setEnabled(False)
        self.action_run.setEnabled(True)

    @pyqtSlot()
    def on_click_resume(self):
        self.executorwindow.me.resume()
        self.executorwindow.load_memory_into_display()

        self.action_debug.setEnabled(True)
        self.action_step.setEnabled(False)
        self.action_resume.setEnabled(False)
        self.action_stop.setEnabled(False)
        self.action_run.setEnabled(True)

    @pyqtSlot()
    def on_click_info(self):
        dialog = InfoDialog("MUHAHAHAHAHAHA")
        sG = QApplication.desktop().screenGeometry()
        x = (sG.width() - dialog.width()) / 2
        y = (sG.height() - dialog.height()) / 2

        dialog.move(x, y)
        dialog.exec_()

    @pyqtSlot()
    def on_click_step(self):
        try:
            next_line = self.executorwindow.me.step(undef)
        except Exception as err:
            mixlog(MERROR, err)
            traceback.print_exc()
            return

        self.executorwindow.tableWidget.selectRow(next_line)

        self.executorwindow.current_line = next_line - self.executorwindow.me.orig

        extraSelections = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(Qt.yellow).lighter(160)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)

        # self.textbox_code.moveCursor(QTextCursor.End)

        # cur = self.textbox_code.textCursor()
        cur = QTextCursor(
            self.executorwindow.textbox_code.document().findBlockByLineNumber(self.executorwindow.current_line))
        self.executorwindow.textbox_code.setTextCursor(cur)

        selection.cursor = cur
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        # self.textbox_code.setExtraSelections(extraSelections)

        self.executorwindow.load_memory_into_display()

        if next_line == self.executorwindow.me.end:
            self.on_click_stop()
            self.executorwindow.load_profiling_results()

    @pyqtSlot()
    def on_click_open(self):
        opened_file_name = QFileDialog.getOpenFileName(self, 'Open file', 'test_programs/', "Program Files (*.*)")
        if opened_file_name[0] != '':
            f_opened = open(opened_file_name[0], 'r')
            with f_opened:
                self.executorwindow.code_text = f_opened.read()

                self.executorwindow.code_text_in_list = self.executorwindow.code_text.splitlines()
                # print(self.code_text_in_list)

                self.executorwindow.textbox_code.setPlainText(self.executorwindow.code_text)

                self.executorwindow.current_line = 0
                self.executorwindow.total_line = self.executorwindow.textbox_code.document().lineCount()

                # print("total:" + str(self.total_line) + "current:" + str(self.current_line))
            f_opened.close()

            self.action_debug.setEnabled(True)
            self.action_step.setEnabled(False)
            self.action_resume.setEnabled(False)
            self.action_stop.setEnabled(False)
            self.action_run.setEnabled(True)

    @pyqtSlot()
    def on_click_go(self):
        mapp_inner = MixALPreProcessor(self.executorwindow.code_text_in_list)
        mapp_inner.preprocessall()
        processed_code_dict = mapp_inner.processed_code_dict
        orig = mapp_inner.orig
        end = mapp_inner.end

        mixlog(MDEBUG, "finished preprocessing")

        # load everything into memory
        for line in processed_code_dict.keys():
            sm = MixToMachineCodeTranslatorSM()
            sm.transduce([x for x in processed_code_dict[line]], False)
            (sym, aa, i, f, op, c) = sm.output
            aa = dectobin(my_int(aa), 2)
            self.executorwindow.memory.setMemory(line, [sym] + aa + [i, f, c])

        self.executorwindow.me = MixExecutor(processed_code_dict, orig, end, self.executorwindow.memory)
        try:
            self.executorwindow.me.go(True)
        except Exception as err:
            mixlog(MERROR, str(err))
            traceback.print_exc()
            return

        mixlog(MDEBUG, "finished executing")
        self.executorwindow.tableWidget.clearContents()
        self.executorwindow.load_memory_into_display()
        self.executorwindow.load_profiling_results()

    def windowaction(self, q):
        print("triggered")

        if q.text() == "New":
            MainWindow.count = MainWindow.count + 1
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle("subwindow" + str(MainWindow.count))
            self.mdi.addSubWindow(sub)
            sub.show()
        if q.text() == "cascade":
            self.mdi.cascadeSubWindows()
        if q.text() == "Tiled":
            self.mdi.tileSubWindows()

    def initUI(self):
        # initiate menu
        self.action_open_file = QAction(QIcon("res/ico/openfile.ico"), "&Open File", self, triggered=self.on_click_open)
        self.action_debug = QAction(QIcon("res/ico/debug.ico"), "&Debug", self, triggered=self.on_click_debug)
        self.action_step = QAction(QIcon("res/ico/debug_step.ico"), "&Step", self, triggered=self.on_click_step)
        self.action_resume = QAction(QIcon("res/ico/debug_resume.ico"), "&Resume", self, triggered=self.on_click_resume)
        self.action_stop = QAction(QIcon("res/ico/debug_stop.ico"), "S&top", self, triggered=self.on_click_stop)
        self.action_run = QAction(QIcon("res/ico/run.ico"), "&Go", self, triggered=self.on_click_go)
        self.action_info = QAction(QIcon("res/ico/alien.ico"), "&Info", self, triggered=self.on_click_info)

        self.openMenu = self.menuBar().addMenu("&Open")
        self.openMenu.addAction(self.action_open_file)
        self.debugMenu = self.menuBar().addMenu("&Debug")
        self.debugMenu.addAction(self.action_debug)
        self.debugMenu.addAction(self.action_step)
        self.debugMenu.addAction(self.action_resume)
        self.debugMenu.addAction(self.action_stop)
        self.debugMenu.addAction(self.action_run)
        self.infoMenu = self.menuBar().addMenu("&Info")
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

        self.action_debug.setEnabled(False)
        self.action_step.setEnabled(False)
        self.action_resume.setEnabled(False)
        self.action_stop.setEnabled(False)
        self.action_run.setEnabled(False)

        self.memorywindow = MixMemoryNeon()
        self.memorywindow.setWindowTitle("Memory")
        self.mdi.addSubWindow(self.memorywindow)

        self.memorywindow2 = MixMemoryNeon()
        self.memorywindow2.setWindowTitle("Memory2")
        self.mdi.addSubWindow(self.memorywindow2)

        self.executorwindow = MixMainWindow()
        self.executorwindow.setWindowTitle("Executor")
        self.mdi.addSubWindow(self.executorwindow)

        self.mdi.tileSubWindows()


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# if __name__ == '__main__':
# app = QApplication(sys.argv)
# ex = MixMainWindow()

# sG = QApplication.desktop().screenGeometry()
# x = (sG.width()-ex.width) / 2
# y = (sG.height()-ex.height) / 2
# ex.move(x, y)

# sys.exit(app.exec_())
