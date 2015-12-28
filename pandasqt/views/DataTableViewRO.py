"""
Read Only Data table view.  This has no buttons for editing.
"""
from pandasqt.compat import QtCore, QtGui, Qt, Slot, Signal

from pandasqt.models.DataFrameModel import DataFrameModel
from pandasqt.views.EditDialogs import AddAttributesDialog, RemoveAttributesDialog

from DataTableView import DataTableWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class DataTableWidgetRO(DataTableWidget):
    """A Custom widget with a TableView and a toolbar.

    This widget shall display all `DataFrameModels` and
    enable the editing of this (edit data, adding/removing,
    rows/columns).

    """
    def initUi(self):
        """Initalizes the User Interface with all sub widgets.

        """
        self.gridLayout = QtGui.QGridLayout(self)

        self.tableView = QtGui.QTableView(self)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)

    def setViewModel(self, model):
        """Sets the model for the enclosed TableView in this widget.

        Args:
            model (DataFrameModel): The model to be displayed by
                the Table View.

        """
        if isinstance(model, DataFrameModel):
            selectionModel = self.tableView.selectionModel()
            self.tableView.setModel(model)
            del selectionModel

