from PySide2 import QtWidgets, QtGui, QtCore

import re


class CellEditor(QtWidgets.QTextEdit):
    """
    Custom cell editor :
      - add a new task line, starting with "- " on "Enter"
      - emits "editing_finished" signal on "Ctrl +Enter" (TableDelegate will end
        the cell editing on that signal)
    """

    editing_finished = QtCore.Signal(QtWidgets.QTextEdit)

    def __init__(self, parent=None):
        super(CellEditor, self).__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            # go to a new "- " line
            if not event.modifiers():
                text = self.toPlainText()
                self.setText(text +'\n- ')
                self.move_cursor_at_the_end()
                return

            # ask for editing's ending
            elif event.modifiers() == QtCore.Qt.ControlModifier:
                self.editing_finished.emit(self)
                return

        super(CellEditor, self).keyPressEvent(event)

    def move_cursor_at_the_end(self):
        cursor = self.textCursor()
        cursor.movePosition(cursor.End, cursor.MoveAnchor)
        self.setTextCursor(cursor)


class TableDelegate(QtWidgets.QStyledItemDelegate):
    """
    Custom item delegate for TableView. Will allow :
      - using custom cell editors
      - perhaps some custom painting for tasks states?
    """

    def __init__(self, parent=None):
        super(TableDelegate, self).__init__(parent)

        self.parent = parent

    def createEditor(self, parent, option, index):
        editor = CellEditor(parent)
        editor.editing_finished.connect(lambda :self.on_editing_finished(editor, index))
        return editor

    def on_editing_finished(self, editor, index):
        # edit cell's data and close editor
        self.setModelData(editor, self.parent.model(), index)
        self.closeEditor.emit(editor)

    def setEditorData(self, editor, index):
        # add a new "- " line to editor and set cursor at the end of it
        value = index.model().data(index, QtCore.Qt.EditRole)
        text = value +'\n- ' if value else '- '

        editor.setText(text)
        editor.move_cursor_at_the_end()

    def setModelData(self, editor, model, index):
        value = editor.toPlainText()

        # remove empty "- " ending lines before setting cell's data
        while True:
            empty_end = re.search('(\s*-\s*)$', value)
            if not empty_end:
                break

            value = value[:-len(empty_end.group(1))]

        model.setData(index, value, QtCore.Qt.EditRole)


class TableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super(TableView, self).__init__(parent)

        self.setAlternatingRowColors(True)

        self.verticalHeader().setFixedWidth(100)
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.horizontalHeader().setMinimumSectionSize(150)

        delegate = TableDelegate(self)
        self.setItemDelegate(delegate)

        self.setMinimumSize(600, 250)
