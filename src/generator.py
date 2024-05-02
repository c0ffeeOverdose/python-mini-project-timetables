import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
from pathlib import Path
from typing import Any, Dict

class Generator(QDialog):
    Table: QTableWidget

    Label_Year: QLabel
    Label_Term: QLabel
    Label_Themes: QLabel

    Dropdown_Themes: QComboBox
    Dropdown_Language: QComboBox

    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi(Path(__file__).resolve().parents[1].joinpath("obj", "timetable.ui"), self)
        self.Table.setColumnWidth(0, 525)
        self.Table.setColumnWidth(1, 50)
        self.Table.setColumnWidth(2, 525)
        self.Table.setRowHeight(0, 124)
        self.Table.setRowHeight(1, 124)
        self.Table.setRowHeight(2, 124)
        self.Table.setRowHeight(3, 124)
        self.Table.setRowHeight(4, 137)

        self.Table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.Table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.Table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.Dropdown_Themes.addItems(["Dark", "Light", "Purple", "Cyan", "Lime", "Amber", "Deep-Orange"])
        self.Dropdown_Themes.setCurrentIndex(0)
        self.Dropdown_Themes.currentIndexChanged.connect(self.changeTheme)

        self.Dropdown_Language.addItems(["English", "ไทย", "Greek"])
        self.Dropdown_Language.setCurrentIndex(0)
        self.Dropdown_Language.currentIndexChanged.connect(self.changeLanguage)
    def addSubTable(self, row: int, col: int, data:list[str]) -> None:
        inner_table = QTableWidget()
        inner_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        inner_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        inner_table.setRowCount(4)
        inner_table.setColumnCount(3)
        inner_table.setSpan(0, 0, 1, 3)
        inner_table.setSpan(1, 0, 1, 3)

        for i in data:
            for j in i:
                item = QTableWidgetItem(str(j))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                inner_table.setItem(data.index(i), i.index(j), item)

        inner_table.setRowHeight(0, 30)
        inner_table.setRowHeight(1, 30)
        inner_table.setRowHeight(2, 30)
        inner_table.setRowHeight(3, 30)
        inner_table.setColumnWidth(0, 120)
        inner_table.setColumnWidth(1, 120)
        inner_table.setColumnWidth(2, 282)

        inner_table.horizontalHeader().setVisible(False)
        inner_table.verticalHeader().setVisible(False)

        inner_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        inner_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.Table.setCellWidget(row, col, inner_table)
        return None
    def changeTheme(self, index: int) -> None:
        if index == 0:
            self.setStyleSheet("background-color: #2C2F33; color: #FFFFFF;")
        elif index == 1:
            self.setStyleSheet("background-color: #FFFFFF; color: #000000;")
        elif index == 2:
            self.setStyleSheet("background-color:#5d34a4; color:#fff;")
        elif index == 3:
            self.setStyleSheet("background-color:#00bcd4; color:#fff;")
        elif index == 4:
            self.setStyleSheet("background-color:#8bc34a; color:#fff;")
        elif index == 5:
            self.setStyleSheet("background-color:#ffc107; color:#fff;")
        elif index == 6:
            self.setStyleSheet("background-color:#ff5722; color:#fff;")

        return None

    def changeLanguage(self, index: int) -> None:
        languagelist = [["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ["วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์", "วันอาทิตย์"], ["Δευτέρα", "Τρίτη", "Τετάρτη", "Πέμπτη", "Παρασκευή", "Σάββατο", "Κυριακή"]]
        titlelist = [["Morning", "", "Afternoon"], ["เช้า", "", "บ่าย"], ["Πρωί", "", "Απόγευμα"]]

        self.Table.setVerticalHeaderLabels(languagelist[index])
        self.Table.setHorizontalHeaderLabels(titlelist[index])
        # for i in range(7):
            # self.Table.horizontalHeaderItem(i).setText(languagelist[index][i])

        return None

daylist = ["วันจันทร์ Monday", "วันอังคาร Tuesday", "วันพุธ Wednesday", "วันพฤหัสบดี Thursday", "วันศุกร์ Friday", "วันเสาร์ Saturday", "วันอาทิตย์ Sunday"]

def matchDay(day: str) -> int:
    index = 0
    for i in daylist:
        if day in i:
            return index
        index += 1
    return -1

def GenerateTimetable(datalist: list[Dict]) -> bool:
    dlg = Generator()
    dlg.setWindowTitle("Timetable")

    for data in datalist:
        Year = data["Year"] or ""
        Term = data["Term"] or ""
        Weekday = data["Weekday"] or ""
        Time = data["Time"] or ""
        Subject_Id = data["Subject_Id"] or ""
        Subject_Name = data["Subject_Name"] or ""
        Credit = data["Credit"] or ""
        Classroom = data["Classroom"] or ""
        Section = data["Section"] or ""
        Instructor_Name = data["Instructor_Name"] or ""

        StartTime: str
        Columns_Number: int
        try:
            StartTime = Time.split("-")[0]
            StartTime = StartTime.split(".")[0]
            if StartTime.isdigit() is False:
                continue
            StartTime = int(StartTime)
            if StartTime < 12:
                Columns_Number = 0
            else:
                Columns_Number = 2
            variables_to_check = [Year, Term, Weekday, Time, Subject_Id, Subject_Name, Credit, Classroom, Section, Instructor_Name]
            if "" in variables_to_check:
                continue
        except:
            pass
        dlg.addSubTable(matchDay(Weekday), Columns_Number, [[Time], [Subject_Name], [Subject_Id, Credit, Instructor_Name], [Classroom, Section, ""]])
        dlg.Label_Year.setText("Year : " + Year)
        dlg.Label_Term.setText("Term : " + Term + "st")
    dlg.exec()
    return True

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     windows = Generator()
#     windows.show()
#     sys.exit(app.exec())
