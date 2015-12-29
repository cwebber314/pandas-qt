# -*- coding: utf-8 -*-
from pandasqt.compat import QtCore, QtGui, Qt, Slot, Signal

from DataTableView import DataTableWidget
from DataTableView import DragTable

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    
class DataTableWidgetEditRows(DataTableWidget):
    """A Custom widget with a TableView and a toolbar.

    This widget shall display all `DataFrameModels` and
    enable the editing of this (edit data, adding/removing,
    rows/columns).

    """
    def initUi(self):
        """Initalizes the Uuser Interface with all sub widgets.

        """
        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.buttonFrame = QtGui.QFrame(self)
        #self.buttonFrame.setMinimumSize(QtCore.QSize(250, 50))
        #self.buttonFrame.setMaximumSize(QtCore.QSize(250, 50))
        self.buttonFrame.setFrameShape(QtGui.QFrame.NoFrame)
        spacerItemButton = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.buttonFrameLayout = QtGui.QGridLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(0, 0, 0, 0)

        self.addRowButton = QtGui.QToolButton(self.buttonFrame)
        self.addRowButton.setObjectName('addrowbutton')
        self.addRowButton.setText(self.tr(u'+row'))
        self.addRowButton.setToolTip(self.tr(u'add new row'))
        icon = QtGui.QIcon(QtGui.QPixmap(_fromUtf8(':/icons/edit-table-insert-row-below.png')))

        self.addRowButton.setIcon(icon)

        self.removeRowButton = QtGui.QToolButton(self.buttonFrame)
        self.removeRowButton.setObjectName('removerowbutton')
        self.removeRowButton.setText(self.tr(u'-row'))
        self.removeRowButton.setToolTip(self.tr(u'remove selected rows'))
        icon = QtGui.QIcon(QtGui.QPixmap(_fromUtf8(':/icons/edit-table-delete-row.png')))

        self.removeRowButton.setIcon(icon)

        self.buttons = [self.addRowButton, self.removeRowButton]

        for index, button in enumerate(self.buttons):
            button.setMinimumSize(self._iconSize)
            button.setMaximumSize(self._iconSize)
            button.setIconSize(self._iconSize)
            button.setCheckable(True)
            self.buttonFrameLayout.addWidget(button, 0, index, 1, 1)
        self.buttonFrameLayout.addItem(spacerItemButton, 0, index+1, 1, 1)

        for button in self.buttons:
            button.setEnabled(False)

        #self.tableView = QtGui.QTableView(self)
        self.tableView = DragTable(self)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)
        
        self.gridLayout.addWidget(self.buttonFrame, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)

        self.addRowButton.toggled.connect(self.addRow)
        self.removeRowButton.toggled.connect(self.removeRow)

    @Slot(bool)
    def enableEditing(self, enabled):
        """Enable the editing buttons to add/remove rows/columns and to edit the data.

        This method is also a slot.
        In addition, the data of model will be made editable,
        if the `enabled` parameter is true.

        Args:
            enabled (bool): This flag indicates, if the buttons
                shall be activated.

        """
        for button in self.buttons:
            button.setEnabled(enabled)
            if button.isChecked():
                button.setChecked(False)

        model = self.tableView.model()

        if model is not None:
            model.enableEditing(enabled)

    def updateDelegates(self):
        """reset all delegates.  We have to wait for the delegates to get
        updated before we enable editing"""
        for index, column in enumerate(self.tableView.model().dataFrame().columns):
            dtype = self.tableView.model().dataFrame()[column].dtype
            self.updateDelegate(index, dtype)

        self.enableEditing(True)

