# -*- coding: utf-8 -*-
"""
Only edit dataframe values.  No new rows or columns.
"""
from pandasqt.compat import QtCore, QtGui, Qt, Slot, Signal

from DataTableView import DataTableWidget
from DataTableView import DragTable

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    
class DataTableWidgetEditData(DataTableWidget):
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

        #self.tableView = QtGui.QTableView(self)
        self.tableView = DragTable(self)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)
        self.buttons = []

    @Slot(bool)
    def enableEditing(self, enabled):
        """Enable the editing buttons to add/remove rows/columns and to edit
        the data.

        This method is also a slot.
        In addition, the data of model will be made editable,
        if the `enabled` parameter is true.

        Args:
            enabled (bool): This flag indicates, if the buttons
                shall be activated.

        """
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

