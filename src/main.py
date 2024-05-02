import sys
import signal

from typing import Optional, Any, Union
from pathlib import Path
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import uic

import tools

from env import ENV
from db import db, Timetable
from generator import GenerateTimetable

class MainWindow(QMainWindow):
    MainTable: QTableWidget

    SQL_Add_Row: QPushButton
    SQL_Current_Row: QLabel
    SQL_Delete_Row: QPushButton
    SQL_Refresh: QPushButton
    SQL_Save: QPushButton

    YearDropdown: QComboBox
    TermDropdown: QComboBox

    Import_Add: QPushButton
    Import_Info: QToolButton
    Import_Username: QLineEdit
    Import_Password: QLineEdit
    Generator_Generate: QPushButton

    checkBoxDarkMode: QCheckBox

    listTimetable: list[Timetable]
    listTimetableMapId: list[Optional[int]]
    listTimetableRemove: list[int]
    currentSelect: Optional[int]

    unsave: bool

    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi(Path(__file__).resolve().parents[1].joinpath("obj", "main-window.ui"), self)

        ############ Ui Settings #############
        self.setFixedSize(self.size())
        self.MainTable.setColumnWidth(0, 50)
        self.MainTable.setColumnWidth(1, 50)
        self.MainTable.setColumnWidth(2, 150)
        self.MainTable.setColumnWidth(3, 200)
        self.MainTable.setColumnWidth(4, 100)
        self.MainTable.setColumnWidth(5, 200)
        self.MainTable.setColumnWidth(6, 100)
        self.MainTable.setColumnWidth(7, 100)
        self.MainTable.setColumnWidth(8, 100)
        self.MainTable.setColumnWidth(9, 240)

        self.MainTable.verticalHeader().setVisible(True)
        self.MainTable.horizontalHeader().setStyleSheet("QHeaderView::section { color: black; }")
        self.MainTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.MainTable.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.MainTable.itemChanged.connect(lambda: setattr(self, "unsave", True))
        self.MainTable.cellClicked.connect(lambda: self.SQL_Current_Row.setText(f"Row currently selected : {self.MainTable.currentRow()}"))

        self.YearDropdown.addItems(tools.getYearList())
        self.YearDropdown.setCurrentIndex(14)

        ############ Ui Setup callback #############
        self.SQL_Add_Row.clicked.connect(self.addRow)
        self.SQL_Delete_Row.clicked.connect(self.deleteRow)
        self.SQL_Refresh.clicked.connect(self.refreshTable)
        self.SQL_Save.clicked.connect(self.sendToDatabase)
        self.Import_Info.clicked.connect(self.sendInfo)
        self.checkBoxDarkMode.stateChanged.connect(self.switchDarkMode)
        self.Import_Add.clicked.connect(self.import_from_reg_ubru)
        self.Generator_Generate.clicked.connect(self.generateTimetable)
        ############ First Init #############

        self.listTimetable = []
        self.listTimetableMapId = []
        self.listTimetableRemove = []
        self.currentSelect = None
        self.unsave = False

        self.checkBoxDarkMode.setChecked(ENV["DARKMODE"] == 1)

        self.refreshTable()

    ############ callback function #############
    def addRow(self):
        self.listTimetableMapId.append(None)
        row = self.MainTable.rowCount()
        self.MainTable.insertRow(row)
        for col in range(self.MainTable.columnCount()):
            self.MainTable.setItem(row, col, self.toTableWidgetItem("", center=True))

        self.unsave = True

    def deleteRow(self):
        if self.MainTable.selectedIndexes():
            row = self.MainTable.currentIndex().row()
        else:
            row = self.MainTable.rowCount() - 1

        if row >= 0:
            self.MainTable.removeRow(row)
            self.listTimetableMapId.pop(row)

        self.unsave = True

    def refreshTable(self):
        if self.unsave:
            reply = QMessageBox.question(
                self, "Unsaved changes", "Your changes have not been save, Yes to cancel edit",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        result = db.get()

        self.listTimetable.clear()
        self.listTimetableMapId.clear()
        self.listTimetableRemove.clear()
        self.currentSelect = None
        self.MainTable.clearSelection()

        if result[0] is True:
            self.MainTable.setRowCount(len(result[1]))
            for row, record in enumerate(result[1]):
                self.listTimetable.append(record)
                it = iter(record)
                self.listTimetableMapId.append(next(it))
                for col, data in enumerate(it):
                    self.MainTable.setItem(row, col, self.toTableWidgetItem(data, center=True))
        else:
            QMessageBox.warning(self, "Error", "Failed to query data from database\n\n" + result[1])

        self.unsave = False

    def sendToDatabase(self):
        currentData = []
        for row in range(self.MainTable.rowCount()):
            tmp = []
            tmp.append(self.listTimetableMapId[row])
            for col in range(self.MainTable.columnCount()):
                text = self.MainTable.item(row, col).text().strip()
                if text == "":
                    QMessageBox.warning(self, "Error", "The data in the table should not be empty.")
                    return
                tmp.append(text)
            tt = Timetable(*tmp)
            try:
                tt.year = int(tt.year)
                tt.term = int(tt.term)
                tt.classSection = int(tt.classSection)
            except:
                QMessageBox.warning(self, "Warning", "column Year, Term, Section is only number !")
                return

            currentData.append(tt)

        result = db.update(currentData, self.listTimetable)

        if result[0] is True:
            if result[1] is True:
                QMessageBox.information(self, "Information", "Saved successfully")
            else:
                QMessageBox.information(self, "Information", "No update")
        else:
            QMessageBox.warning(self, "Error", "Failed to query data from database\n\n" + result[1])

        self.unsave = False
        self.refreshTable()

    def sendInfo(self):
        QMessageBox.information(self, "Info", "import data from https://reg.ubru.ac.th/")

    def switchDarkMode(self) -> None:
        if self.checkBoxDarkMode.isChecked():
            self.setStyleSheet("background-color: rgb(41, 41, 41)")
            self.MainTable.setStyleSheet("background-color: rgb(30, 31, 40); border-color: rgb(255, 255, 255);")
        else:
            self.setStyleSheet("")
            self.MainTable.setStyleSheet("")

    def import_from_reg_ubru(self) -> None:
        QMessageBox.warning(self, "Error", "Nah, i don't want to release this feature yet.")
    @staticmethod
    def toTableWidgetItem(text: Any, center: bool = False) -> QTableWidgetItem:
        item = QTableWidgetItem(str(text if text is not None else ""))
        if center:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    def generateTimetable(self):
        year = self.YearDropdown.currentText()
        term = self.TermDropdown.currentText()
        datalist = []
        for row in range(self.MainTable.rowCount()):
            foundYear = self.MainTable.item(row, 0)
            foundTerm = self.MainTable.item(row, 1)
            if foundYear is not None and foundTerm is not None and foundYear.text() == year and foundTerm.text() == term:
                datalist.append({
                    "Year": self.MainTable.item(row, 0).text(),
                    "Term": self.MainTable.item(row, 1).text(),
                    "Weekday": self.MainTable.item(row, 2).text(),
                    "Time": self.MainTable.item(row, 3).text(),
                    "Subject_Id": self.MainTable.item(row, 4).text(),
                    "Subject_Name": self.MainTable.item(row, 5).text(),
                    "Credit": self.MainTable.item(row, 6).text(),
                    "Classroom": self.MainTable.item(row, 7).text(),
                    "Section": self.MainTable.item(row, 8).text(),
                    "Instructor_Name": self.MainTable.item(row, 9).text()
                })
        GenerateTimetable(datalist)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    windows = MainWindow()
    windows.show()
    sys.exit(app.exec())
