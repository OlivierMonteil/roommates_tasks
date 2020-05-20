from PySide2 import QtWidgets, QtGui, QtCore

import calendar
import re

DAYS = list(calendar.day_name)
ROOMMATES = ['Toto', 'NafNaf', 'Paf le iench']


class CellEditor(QtWidgets.QTextEdit):

    editing_finished = QtCore.Signal(QtWidgets.QTextEdit)

    def __init__(self, parent=None):
        super(CellEditor, self).__init__(parent)

    def keyPressEvent(self, event):
        modifs = event.modifiers()
        if event.key() == QtCore.Qt.Key_Return:
            if not event.modifiers():
                text = self.toPlainText()
                self.setText(text +'\n- ')
                self.move_cursor_at_the_end()
                return

            elif event.modifiers() == QtCore.Qt.ControlModifier:
                self.editing_finished.emit(self)
                return

        super(CellEditor, self).keyPressEvent(event)

    def move_cursor_at_the_end(self):
        cursor = self.textCursor()
        cursor.movePosition(cursor.End, cursor.MoveAnchor)
        self.setTextCursor(cursor)


class TableDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TableDelegate, self).__init__(parent)

        self.parent = parent

    def createEditor(self, parent, option, index):
        editor = CellEditor(parent)
        editor.editing_finished.connect(lambda :self.on_editing_finished(editor, index))
        return editor

    def on_editing_finished(self, editor, index):
        self.setModelData(editor, self.parent.model(), index)
        self.closeEditor.emit(editor)

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.clear()
        text = value +'\n- ' if value else '- '
        editor.setText(text)

        editor.move_cursor_at_the_end()

    def setModelData(self, editor, model, index):
        value = editor.toPlainText()

        while True:
            empty_end = re.search('(\s*-\s*)$', value)
            if not empty_end:
                break

            value = value[:-len(empty_end.group(1))]

        model.setData(index, value, QtCore.Qt.EditRole)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        super(TableModel, self).__init__(parent)

        self._data = data

    def headerData(self, i, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Vertical:
                return DAYS[i]
            else:
                return ROOMMATES[i]
        else:
            return None

    def rowCount(self, parent=None):
        return len(DAYS)

    def columnCount(self, parent=None):
        return len(ROOMMATES)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        if role == QtCore.Qt.EditRole:
            return self._data[index.row()][index.column()]

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            return True

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled


class TableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super(TableView, self).__init__(parent)

        self.setAlternatingRowColors(True)
        self.verticalHeader().setAlternatingRowColors(True)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    table = TableView()
    delegate = TableDelegate(table)
    table.setItemDelegate(delegate)

    bullshit_model = []
    for i, _ in enumerate(DAYS):
        bullshit_model.append([])
        for x in ROOMMATES:
            bullshit_model[i].append('')

    model = TableModel(bullshit_model)
    table.setModel(model)

    table.show()

    sys.exit(app.exec_())
