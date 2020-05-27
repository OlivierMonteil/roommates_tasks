from PySide2 import QtCore

class QTableModel(QtCore.QAbstractTableModel):
    def __init__(self, application, parent=None):
        super(QTableModel, self).__init__(parent)

        self.application = application
        self._data = self.application.table_model

    def headerData(self, i, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Vertical:
                return self._data.DAYS[i]
            else:
                return self._data.ROOMMATES[i]
        else:
            return None

    def rowCount(self, parent = None):
        return self._data.rowCount()

    def columnCount(self, parent = None):
        return self._data.columnCount()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        if role == QtCore.Qt.EditRole:
            return self._data[index.row()][index.column()]

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled |QtCore.Qt.ItemIsSelectable