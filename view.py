from PySide2 import QtWidgets, QtGui, QtCore


class TableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super(TableView, self).__init__(parent)
