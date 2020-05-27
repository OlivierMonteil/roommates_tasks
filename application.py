from PySide2 import QtWidgets, QtCore
from qmodel import QTableModel
from tablemodel import Model
from view import TableView
import calendar


class RoommatesTaskListApp:
    def __init__(self, args, parent = None):

        DAYS = list(calendar.day_name)
        ROOMMATES = ['Toto', 'Naf-faf', 'Le grand mechant Loup']

        self.app = QtWidgets.QApplication(args)

        self.table_view = TableView()
        self.table_model = Model(DAYS, ROOMMATES)
        self.qmodel = QTableModel(self)

        self.table_view.setModel(self.qmodel)

    def run(self):
        self.table_view.show()
        return self.app.exec_()