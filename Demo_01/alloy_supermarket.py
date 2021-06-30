import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


class AlloySupermarket(QTabWidget):
    def __init__(self):
        super(AlloySupermarket, self).__init__()
        self.initUI()
        self.tab1UI()
        self.tab2UI()

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('AlloySupermarket/res/AsDB.db')

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle('Alloy Supermarket')
        self.setWindowIcon(QIcon('AlloySupermarket/res/as.ico'))
        self.font = QFont('Arial', 16)
        self.font_s = QFont('Arial', 12)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.addTab(self.tab1, 'Concentrations --> Performance')
        self.addTab(self.tab2, 'Performance --> Concentrations')

    def tab1UI(self):
        # 设置整体布局
        layout = QGridLayout()
        self.tab1.setLayout(layout)
        gb1 = QGroupBox('Concentrations (wt.%)')
        gb2 = QGroupBox('Performance')
        reset_btn = QPushButton('Reset')
        predict_btn = QPushButton('Predict')
        layout.addWidget(gb1, 0, 0, 2, 5)
        layout.addWidget(reset_btn, 2, 1, 1, 1)
        layout.addWidget(predict_btn, 2, 3, 1, 1)
        layout.addWidget(gb2, 3, 0, 3, 5)

        # 设置Concentrations
        grid1 = QGridLayout()
        gb1.setLayout(grid1)
        la_Si = QLabel('   Si:')
        la_Mg = QLabel('   Mg:')
        la_Al = QLabel('   Al:')
        la_Sc = QLabel('   Sc:')
        la_Si.setToolTip('4.0 ~ 13.0 wt.%')
        la_Mg.setToolTip('0.0 ~ 0.7 wt.%')
        self.input_Si = QDoubleSpinBox()
        self.input_Si.setMinimum(4.0)
        self.input_Si.setMaximum(13.0)
        self.input_Si.setSingleStep(0.01)
        self.input_Si.setAccelerated(True)
        self.input_Mg = QDoubleSpinBox()
        self.input_Mg.setMinimum(0.0)
        self.input_Mg.setMaximum(0.7)
        self.input_Mg.setSingleStep(0.1)
        self.input_Mg.setAccelerated(True)
        self.data_Al = QLabel('Default')
        self.data_Sc = QLabel('Default')
        grid1.addWidget(la_Si, 0, 0, 1, 1)
        grid1.addWidget(self.input_Si, 0, 1, 1, 2)
        grid1.addWidget(la_Mg, 1, 0, 1, 1)
        grid1.addWidget(self.input_Mg, 1, 1, 1, 2)
        grid1.addWidget(la_Al, 0, 3, 1, 1)
        grid1.addWidget(self.data_Al, 0, 4, 1, 2)
        grid1.addWidget(la_Sc, 1, 3, 1, 1)
        grid1.addWidget(self.data_Sc, 1, 4, 1, 2)

        # 设置 Performance
        grid2 = QGridLayout()
        gb2.setLayout(grid2)
        la_UTS = QLabel('   UTS(MPa):')
        la_YS = QLabel('   YS (MPa):')
        la_EL = QLabel('   EL (%):')
        self.data_UTS = QLabel('Default')
        self.data_YS = QLabel('Default')
        self.data_EL = QLabel('Default')
        grid2.addWidget(la_UTS, 0, 0, 1, 1)
        grid2.addWidget(la_YS, 1, 0, 1, 1)
        grid2.addWidget(la_EL, 2, 0, 1, 1)
        grid2.addWidget(self.data_UTS, 0, 1, 1, 1)
        grid2.addWidget(self.data_YS, 1, 1, 1, 1)
        grid2.addWidget(self.data_EL, 2, 1, 1, 1)

        # 设置字体
        la_Al.setFont(self.font)
        la_Si.setFont(self.font)
        la_Mg.setFont(self.font)
        la_Sc.setFont(self.font)
        la_UTS.setFont(self.font)
        la_YS.setFont(self.font)
        la_EL.setFont(self.font)
        self.data_Al.setFont(self.font_s)
        self.data_Sc.setFont(self.font_s)
        self.data_UTS.setFont(self.font_s)
        self.data_YS.setFont(self.font_s)
        self.data_EL.setFont(self.font_s)

        # 绑定事件和槽
        reset_btn.clicked.connect(self.tab1_reset)
        predict_btn.clicked.connect(self.tab1_predict)

    def tab2UI(self):
        # 设置整体布局
        layout = QGridLayout()
        self.tab2.setLayout(layout)
        gb1 = QGroupBox('Performance')
        gb2 = QGroupBox('Concentrations (wt.%)')
        reset_btn = QPushButton('Reset')
        predict_btn = QPushButton('Predict')
        layout.addWidget(gb1, 0, 0, 1, 5)
        layout.addWidget(reset_btn, 2, 1, 1, 1)
        layout.addWidget(predict_btn, 2, 3, 1, 1)
        layout.addWidget(gb2, 3, 0, 4, 5)

        # 设置 Performance
        hbox = QHBoxLayout()
        gb1.setLayout(hbox)
        la_UTS = QLabel('   UTS(MPa):')
        la_YS = QLabel('   YS(MPa):')
        la_EL = QLabel('   EL(%):')
        la_UTS.setToolTip('195 ~ 260 MPa')
        la_YS.setToolTip('100 ~ 160 MPa')
        la_EL.setToolTip('2.5 ~ 11.0 %')
        la_e1 = QLabel('±')
        la_e2 = QLabel('±')
        la_e3 = QLabel('±')
        self.input_UTS = QLineEdit()
        self.input_UTS.setValidator(QIntValidator(195, 260))
        self.input_UTS.setPlaceholderText('195 - 260')
        self.error_UTS = QSpinBox()
        self.error_UTS.setMinimum(0)
        self.error_UTS.setMaximum(10)
        self.error_UTS.setSingleStep(1)
        self.error_UTS.setAccelerated(True)
        self.error_UTS.setValue(3)
        self.input_YS = QLineEdit()
        self.input_YS.setValidator(QIntValidator(100, 160))
        self.input_YS.setPlaceholderText('100 - 160')
        self.error_YS = QSpinBox()
        self.error_YS.setMinimum(0)
        self.error_YS.setMaximum(10)
        self.error_YS.setSingleStep(1)
        self.error_YS.setAccelerated(True)
        self.error_YS.setValue(3)
        self.input_EL = QLineEdit()
        self.input_EL.setValidator(QDoubleValidator(2.5, 11.0, 1))
        self.input_EL.setPlaceholderText('2.5 - 11.0')
        self.error_EL = QDoubleSpinBox()
        self.error_EL.setMinimum(0.0)
        self.error_EL.setMaximum(3.0)
        self.error_EL.setSingleStep(0.5)
        self.error_EL.setAccelerated(True)
        self.error_EL.setValue(1.0)
        hbox.addWidget(la_UTS)
        hbox.addWidget(self.input_UTS)
        hbox.addWidget(la_e1)
        hbox.addWidget(self.error_UTS)
        hbox.addWidget(la_YS)
        hbox.addWidget(self.input_YS)
        hbox.addWidget(la_e2)
        hbox.addWidget(self.error_YS)
        hbox.addWidget(la_EL)
        hbox.addWidget(self.input_EL)
        hbox.addWidget(la_e3)
        hbox.addWidget(self.error_EL)

        # 设置Concentrations
        vbox = QVBoxLayout()
        gb2.setLayout(vbox)
        self.model = QStandardItemModel(30, 7)
        self.model.setHorizontalHeaderLabels(['Al (wt.%)', 'Si (wt.%)', 'Mg (wt.%)', 'Sc (wt.%)', 'UTS (MPa)', 'YS (MPa)', 'EL (%)'])
        self.view = QTableView()
        self.view.setModel(self.model)
        bar = QScrollBar()
        self.view.setVerticalScrollBar(bar)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        vbox.addWidget(self.view)

        # 设置字体
        la_UTS.setFont(self.font_s)
        la_YS.setFont(self.font_s)
        la_EL.setFont(self.font_s)

        # 绑定事件和槽
        reset_btn.clicked.connect(self.tab2_reset)
        predict_btn.clicked.connect(self.tab2_predict)

    def tab1_reset(self):
        # print('reset1')
        self.input_Si.setValue(4.0)
        self.input_Mg.setValue(0.0)
        self.data_Al.setText('Default')
        self.data_Sc.setText('Default')
        self.data_UTS.setText('Default')
        self.data_YS.setText('Default')
        self.data_EL.setText('Default')

    def tab1_predict(self):
        # print('predict1')
        Si = float(self.input_Si.text())
        Mg = float(self.input_Mg.text())
        # print(Si)
        # print(Mg)
        
        # 数据库操作
        if not self.db.open():
            QMessageBox.critical(self, 'Critical', 'Can Not Open Database', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            # print('not open')
        else:
            query = QSqlQuery()
            sql = 'select Al, Sc, UTS, YS, EL from Al_Si_Mg_Sc where Si = %.2f and Mg = %.2f' % (Si, Mg)
            query.prepare(sql)
            if not query.exec_():
                QMessageBox.critical(self, 'Critical', query.lastError(), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                while query.next():
                    Al = query.value(0)
                    Sc = query.value(1)
                    UTS = query.value(2)
                    YS = query.value(3)
                    EL = query.value(4)
                    # print(Al, Sc, UTS, YS, EL)
            self.db.close()

            self.data_Al.setText('%.2f' % Al)
            self.data_Sc.setText('%.2f' % Sc)
            self.data_UTS.setText('%.2f' % UTS)
            self.data_YS.setText('%.2f' % YS)
            self.data_EL.setText('%.2f' % EL)

    def tab2_reset(self):
        # print('reset2')
        self.input_UTS.clear()
        self.input_YS.clear()
        self.input_EL.clear()
        self.input_UTS.setPlaceholderText('195 - 260')
        self.input_YS.setPlaceholderText('100 - 160')
        self.input_EL.setPlaceholderText('2.5 - 11.0')
        self.error_UTS.setValue(3.0)
        self.error_YS.setValue(3.0)
        self.error_EL.setValue(1.0)
        self.model.clear()
        self.model = QStandardItemModel(30, 7)
        self.model.setHorizontalHeaderLabels(['Al (wt.%)', 'Si (wt.%)', 'Mg (wt.%)', 'Sc (wt.%)', 'UTS (MPa)', 'YS (MPa)', 'EL (%)'])
        self.view.setModel(self.model)

    def tab2_predict(self):
        # print('predict2')
        self.model.clear()
        self.model = QStandardItemModel(30, 7)
        self.model.setHorizontalHeaderLabels(['Al (wt.%)', 'Si (wt.%)', 'Mg (wt.%)', 'Sc (wt.%)', 'UTS (MPa)', 'YS (MPa)', 'EL (%)'])
        self.view.setModel(self.model)

        UTS, YS, EL, UTS_e, YS_e, EL_e = 0, 0, 0, 0, 0, 0
        if (self.input_UTS.text() == '') | (self.input_YS.text() == '') | (self.input_EL.text() == ''):
            QMessageBox.critical(self, 'Critical', 'Please Input Data', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            UTS = float(self.input_UTS.text())
            YS = float(self.input_YS.text())
            EL = float(self.input_EL.text())
            UTS_e = float(self.error_UTS.text())
            YS_e = float(self.error_YS.text())
            EL_e = float(self.error_EL.text())
        # print(UTS)
        # print(YS)
        # print(EL)

        # 数据库操作
        if not self.db.open():
            QMessageBox.critical(self, 'Critical', 'Can Not Open Database', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            # print('not open')
        else:
            query = QSqlQuery()
            sql = 'select Al, Si, Mg, Sc, UTS, YS, EL from Al_Si_Mg_Sc where (UTS between %.2f and %.2f) and (YS between %.2f and %.2f) and (EL between %.2f and %.2f)' % (UTS-UTS_e, UTS+UTS_e, YS-YS_e, YS+YS_e, EL-EL_e, EL+EL_e)
            query.prepare(sql)
            test = False
            if not query.exec_():
                QMessageBox.critical(self, 'Critical', query.lastError(), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                i = 0
                while query.next():
                    test = query.value(0)
                    Al = query.value(0)
                    Si = query.value(1)
                    Mg = query.value(2)
                    Sc = query.value(3)
                    UTS = query.value(4)
                    YS = query.value(5)
                    EL = query.value(6)
                    # print(Al, Si, Mg, Sc)
                    item_Al = QStandardItem('%.2f' % Al)
                    item_Si = QStandardItem('%.2f' % Si)
                    item_Mg = QStandardItem('%.2f' % Mg)
                    item_Sc = QStandardItem('%.2f' % Sc)
                    item_UTS = QStandardItem('%.2f' % UTS)
                    item_YS = QStandardItem('%.2f' % YS)
                    item_EL = QStandardItem('%.2f' % EL)
                    self.model.setItem(i, 0, item_Al)
                    self.model.setItem(i, 1, item_Si)
                    self.model.setItem(i, 2, item_Mg)
                    self.model.setItem(i, 3, item_Sc)
                    self.model.setItem(i, 4, item_UTS)
                    self.model.setItem(i, 5, item_YS)
                    self.model.setItem(i, 6, item_EL)
                    i += 1
            self.db.close()

            if not test:
                print('321')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = AlloySupermarket()
    main.show()
    sys.exit(app.exec_())
