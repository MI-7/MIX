import traceback
from mixinterpreter.mixexecutor import *
from ui.codeeditor import CodeEditor
from ui.infodialog import *
from utility import *
import os


class MixMainWindow(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        self.title = 'MIX Interpreter'
        self.left = 10
        self.top = 10
        self.width = 1280
        self.height = 960
        self.current_line = 0
        self.total_line = 0
        self.profile_start = 4000
        self.code_to_execute = ""
        self.code_text = ""
        self.code_text_in_list = []
        self.memory = MemoryState()
        self.me = None
        self.initUI()
        self.load_memory_into_display()

    # 4001 -> 5000 holds profiling records
    def load_profiling_results(self):
        i = self.profile_start

        self.tableWidget.setItem(i, 0, QTableWidgetItem('Line'))
        self.tableWidget.setItem(i, 1, QTableWidgetItem('Code'))
        self.tableWidget.setItem(i, 2, QTableWidgetItem('Times'))
        self.tableWidget.setItem(i, 3, QTableWidgetItem('Unit'))
        self.tableWidget.setItem(i, 4, QTableWidgetItem('Total'))
        i = i + 1

        total_total_time = 0
        dict_line_result = {}
        for key in self.me.profilingresult.keys():
            code, times, unit_time, total_time = self.me.profilingresult[key]
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(key)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(code))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(times)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(unit_time)))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(total_time)))
            dict_line_result[i] = total_time
            i = i + 1
            total_total_time = total_total_time + total_time
            # self.profilingresult[current_line] = (self.processed_code_dict[current_line], 1, unit, unit)

        self.tableWidget.setItem(i, 4, QTableWidgetItem(str(total_total_time)))
        for key in dict_line_result.keys():
            self.tableWidget.setItem(key, 5,
                                     QTableWidgetItem(str(100 * dict_line_result[key] / total_total_time)[0:6] + '%'))
        self.tableWidget.selectRow(i)

    def load_memory_into_display(self):
        num_mode = NUM_MODE_DEC
        if self.dec_radio.isChecked():
            num_mode = NUM_MODE_DEC
        elif self.bin_radio.isChecked():
            num_mode = NUM_MODE_BIN
        elif self.ch_radio.isChecked():
            num_mode = NUM_MODE_CH

        self.a1_label.setText(format_num(self.memory.a1, num_mode))
        self.a2_label.setText(format_num(self.memory.a2, num_mode))
        self.a3_label.setText(format_num(self.memory.a3, num_mode))
        self.a4_label.setText(format_num(self.memory.a4, num_mode))
        self.a5_label.setText(format_num(self.memory.a5, num_mode))
        self.asym_label.setText(self.memory.asym)
        self.anum_label.setText(str(partstodec_withsign(self.memory.getA())))

        self.x1_label.setText(format_num(self.memory.x1, num_mode))
        self.x2_label.setText(format_num(self.memory.x2, num_mode))
        self.x3_label.setText(format_num(self.memory.x3, num_mode))
        self.x4_label.setText(format_num(self.memory.x4, num_mode))
        self.x5_label.setText(format_num(self.memory.x5, num_mode))
        self.xsym_label.setText(self.memory.xsym)
        self.xnum_label.setText(str(partstodec_withsign(self.memory.getX())))

        self.i14_label.setText(format_num(self.memory.i14, num_mode))
        self.i15_label.setText(format_num(self.memory.i15, num_mode))
        self.i1sym_label.setText(self.memory.i1sym)
        self.i1num_label.setText(str(partstodec_withsign(self.memory.geti1())))

        self.i24_label.setText(format_num(self.memory.i24, num_mode))
        self.i25_label.setText(format_num(self.memory.i25, num_mode))
        self.i2sym_label.setText(self.memory.i2sym)
        self.i2num_label.setText(str(partstodec_withsign(self.memory.geti2())))

        self.i34_label.setText(format_num(self.memory.i34, num_mode))
        self.i35_label.setText(format_num(self.memory.i35, num_mode))
        self.i3sym_label.setText(self.memory.i3sym)
        self.i3num_label.setText(str(partstodec_withsign(self.memory.geti3())))

        self.i44_label.setText(format_num(self.memory.i44, num_mode))
        self.i45_label.setText(format_num(self.memory.i45, num_mode))
        self.i4sym_label.setText(self.memory.i4sym)
        self.i4num_label.setText(str(partstodec_withsign(self.memory.geti4())))

        self.i54_label.setText(format_num(self.memory.i54, num_mode))
        self.i55_label.setText(format_num(self.memory.i55, num_mode))
        self.i5sym_label.setText(self.memory.i5sym)
        self.i5num_label.setText(str(partstodec_withsign(self.memory.geti5())))

        self.i64_label.setText(format_num(self.memory.i64, num_mode))
        self.i65_label.setText(format_num(self.memory.i65, num_mode))
        self.i6sym_label.setText(self.memory.i6sym)
        self.i6num_label.setText(str(partstodec_withsign(self.memory.geti6())))

        self.j4_label.setText(format_num(self.memory.j4, num_mode))
        self.j5_label.setText(format_num(self.memory.j5, num_mode))
        self.jsym_label.setText(self.memory.jsym)
        self.jnum_label.setText(str(partstodec_withsign(self.memory.getj())))

        self.overload_switch_label.setText(str(self.memory.overload_switch))
        self.comparison_indicator_label.setText(self.memory.comparison_indicator)

        for i in range(4000):
            m = self.memory.getMemory(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(m[0])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(m[1])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(m[2])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(m[3])))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(m[4])))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(m[5])))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(partstodec_withsign(m))))

    def initUI(self):
        # window layout
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon("res/ico/openfile.ico"))

        self.a_label = QLabel('a')
        self.a1_label = QLabel()
        self.a2_label = QLabel()
        self.a3_label = QLabel()
        self.a4_label = QLabel()
        self.a5_label = QLabel()
        self.asym_label = QLabel()
        self.anum_label = QLabel()

        self.x_label = QLabel('x')
        self.x1_label = QLabel()
        self.x2_label = QLabel()
        self.x3_label = QLabel()
        self.x4_label = QLabel()
        self.x5_label = QLabel()
        self.xsym_label = QLabel()
        self.xnum_label = QLabel()

        self.i1_label = QLabel('i1')
        self.i14_label = QLabel()
        self.i15_label = QLabel()
        self.i1sym_label = QLabel()
        self.i1num_label = QLabel()

        self.i2_label = QLabel('i2')
        self.i24_label = QLabel()
        self.i25_label = QLabel()
        self.i2sym_label = QLabel()
        self.i2num_label = QLabel()

        self.i3_label = QLabel('i3')
        self.i34_label = QLabel()
        self.i35_label = QLabel()
        self.i3sym_label = QLabel()
        self.i3num_label = QLabel()

        self.i4_label = QLabel('i4')
        self.i44_label = QLabel()
        self.i45_label = QLabel()
        self.i4sym_label = QLabel()
        self.i4num_label = QLabel()

        self.i5_label = QLabel('i5')
        self.i54_label = QLabel()
        self.i55_label = QLabel()
        self.i5sym_label = QLabel()
        self.i5num_label = QLabel()

        self.i6_label = QLabel('i6')
        self.i64_label = QLabel()
        self.i65_label = QLabel()
        self.i6sym_label = QLabel()
        self.i6num_label = QLabel()

        self.j_label = QLabel('j')
        self.j4_label = QLabel()
        self.j5_label = QLabel()
        self.jsym_label = QLabel()
        self.jnum_label = QLabel()

        self.overload_switch_label = QLabel()  # 1=overload / 0=not-overload
        self.comparison_indicator_label = QLabel()  # L / E / G

        self.textbox_code = CodeEditor("", self)
        # self.textbox_code.move(QPoint(10, 55))
        # self.textbox_code.resize(QSize(300, 720))
        # self.textbox_code.setPlainText("abc"+os.linesep+"cde"+os.linesep+"fgh")

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(5000)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Cell (1,2)"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Cell (2,1)"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Cell (4,2)"))
        # self.tableWidget.resizeColumnsToContents()
        # self.tableWidget.setColumnWidth(10, 10)
        self.tableWidget.resizeRowsToContents()

        self.dec_radio = QRadioButton()
        self.dec_radio.setChecked(True)
        self.dec_radio.setText("Dec")
        self.dec_radio.toggled.connect(lambda: self.load_memory_into_display())

        self.bin_radio = QRadioButton()
        self.bin_radio.setChecked(False)
        self.bin_radio.setText("Bin")
        self.bin_radio.toggled.connect(lambda: self.load_memory_into_display())

        self.ch_radio = QRadioButton()
        self.ch_radio.setChecked(False)
        self.ch_radio.setText("Chr")
        self.ch_radio.toggled.connect(lambda: self.load_memory_into_display())

        self.space_label = QLabel('         ')

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.textbox_code, 0, 0, 11, 1)

        grid.addWidget(self.dec_radio, 0, 1)
        grid.addWidget(self.bin_radio, 0, 2)
        grid.addWidget(self.ch_radio, 0, 3)
        grid.addWidget(self.space_label, 0, 4)
        grid.addWidget(self.space_label, 0, 5)
        grid.addWidget(self.space_label, 0, 6)
        grid.addWidget(self.space_label, 0, 7)
        grid.addWidget(self.space_label, 0, 8)
        grid.addWidget(self.space_label, 0, 9)
        grid.addWidget(self.space_label, 0, 10)
        grid.addWidget(self.space_label, 0, 11)
        grid.addWidget(self.space_label, 0, 12)
        grid.addWidget(self.space_label, 0, 13)
        grid.addWidget(self.space_label, 0, 14)
        grid.addWidget(self.space_label, 0, 15)
        grid.addWidget(self.space_label, 0, 16)
        grid.addWidget(self.space_label, 0, 17)
        grid.addWidget(self.space_label, 0, 18)

        grid.addWidget(self.a_label, 1, 1)
        grid.addWidget(self.asym_label, 1, 2)
        grid.addWidget(self.a1_label, 1, 3)
        grid.addWidget(self.a2_label, 1, 4)
        grid.addWidget(self.a3_label, 1, 5)
        grid.addWidget(self.a4_label, 1, 6)
        grid.addWidget(self.a5_label, 1, 7)
        grid.addWidget(self.anum_label, 1, 8)

        grid.addWidget(self.x_label, 2, 1)
        grid.addWidget(self.xsym_label, 2, 2)
        grid.addWidget(self.x1_label, 2, 3)
        grid.addWidget(self.x2_label, 2, 4)
        grid.addWidget(self.x3_label, 2, 5)
        grid.addWidget(self.x4_label, 2, 6)
        grid.addWidget(self.x5_label, 2, 7)
        grid.addWidget(self.xnum_label, 2, 8)

        grid.addWidget(self.i1_label, 3, 1)
        grid.addWidget(self.i1sym_label, 3, 2)
        grid.addWidget(self.i14_label, 3, 3)
        grid.addWidget(self.i15_label, 3, 4)
        grid.addWidget(self.i1num_label, 3, 5)

        grid.addWidget(self.i2_label, 4, 1)
        grid.addWidget(self.i2sym_label, 4, 2)
        grid.addWidget(self.i24_label, 4, 3)
        grid.addWidget(self.i25_label, 4, 4)
        grid.addWidget(self.i2num_label, 4, 5)

        grid.addWidget(self.i3_label, 5, 1)
        grid.addWidget(self.i3sym_label, 5, 2)
        grid.addWidget(self.i34_label, 5, 3)
        grid.addWidget(self.i35_label, 5, 4)
        grid.addWidget(self.i3num_label, 5, 5)

        grid.addWidget(self.i4_label, 6, 1)
        grid.addWidget(self.i4sym_label, 6, 2)
        grid.addWidget(self.i44_label, 6, 3)
        grid.addWidget(self.i45_label, 6, 4)
        grid.addWidget(self.i4num_label, 6, 5)

        grid.addWidget(self.i5_label, 7, 1)
        grid.addWidget(self.i5sym_label, 7, 2)
        grid.addWidget(self.i54_label, 7, 3)
        grid.addWidget(self.i55_label, 7, 4)
        grid.addWidget(self.i5num_label, 7, 5)

        grid.addWidget(self.i6_label, 8, 1)
        grid.addWidget(self.i6sym_label, 8, 2)
        grid.addWidget(self.i64_label, 8, 3)
        grid.addWidget(self.i65_label, 8, 4)
        grid.addWidget(self.i6num_label, 8, 5)

        grid.addWidget(self.j_label, 9, 1)
        grid.addWidget(self.jsym_label, 9, 2)
        grid.addWidget(self.j4_label, 9, 3)
        grid.addWidget(self.j5_label, 9, 4)
        grid.addWidget(self.jnum_label, 9, 5)
        grid.addWidget(self.overload_switch_label, 9, 6)
        grid.addWidget(self.comparison_indicator_label, 9, 7)

        grid.addWidget(self.tableWidget, 10, 1, 1, 18)

        # self.memory = [['+', 0, 0, 0, 0, 0] for i in range(0, memory_space)]

        displaywidget = QWidget()
        displaywidget.setLayout(grid)
        # self.setCentralWidget(displaywidget)
        self.setWidget(displaywidget)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MixMainWindow()

    sG = QApplication.desktop().screenGeometry()
    x = (sG.width() - ex.width) / 2
    y = (sG.height() - ex.height) / 2
    ex.move(x, y)

    sys.exit(app.exec_())
