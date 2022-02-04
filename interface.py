import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd
import sqlite3

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(581, 505)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(180, 10, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 190, 551, 231))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 281, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 100, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(430, 440, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 150, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.connectionString = ':memory:'
        self.lineEdit.setText(':memory:')
        self.con = sqlite3.connect(self.connectionString)
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.run)

    def run(self):
        if self.connectionString != self.lineEdit.text():
            self.con.close()
            self.connectionString = self.lineEdit.text()
            self.con = sqlite3.connect(self.connectionString)
            self.cur = self.con.cursor()
        comand = self.textEdit.toPlainText()
        #print(comand)
        try:
            for i in comand.split(';'):
                if sqlite3.complete_statement(comand):
                    if i.upper().startswith("SELECT"):
                        result = self.cur.execute(i).fetchall()
                        desc = [j[0] for j in self.cur.execute(i).description]
                        self.createTable(desc, result)
                    else:
                        self.cur.execute(i)
                    self.textEdit.setText('')
        except sqlite3.Error as error:
            self.textEdit.setText(' что то пошло не так. Кокретнее : ' + str(error.args[0]))


    def createTable(self, desc, res):
        res = [list(i) for i in res]
        self.table = QtWidgets.QTableView()
        data = pd.DataFrame(res, columns=desc)
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.table.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Работа с SQL"))
        self.label.setText(_translate("MainWindow", "Работа с базой данных"))
        self.pushButton.setText(_translate("MainWindow", "Выполнить"))
        self.label_4.setText(_translate("MainWindow", "Введите запрос"))
        self.label_5.setText(_translate("MainWindow", "Введите ссылку на объект"))
