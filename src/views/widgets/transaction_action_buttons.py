from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtGui, QtCore
from pathlib import Path

class TransactionActionButtons(QWidget):
    delete_transaction_requested = pyqtSignal(int)
    edit_transaction_requested = pyqtSignal(int)

    def __init__(self, transaction_id):
        super().__init__()
        self.transaction_id = transaction_id
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.EditButton = QPushButton("")
        self.EditButton.setObjectName("EditButton")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("src/assets/Edit.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.EditButton.setIcon(icon1)
        self.EditButton.setIconSize(QtCore.QSize(17, 17))
        self.EditButton.setFixedSize(20, 20)
        self.EditButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.EditButton.setStyleSheet(Path("src/styles/ButtonActionStyle.qss").read_text())
        self.EditButton.clicked.connect(self.on_edit_clicked)
        leftspacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(leftspacer)
        layout.addWidget(self.EditButton)

        # Delete button
        self.DeleteButton = QPushButton("")
        self.DeleteButton.setObjectName("DeleteButton")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("src/assets/trash.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.DeleteButton.setIcon(icon2)
        self.DeleteButton.setIconSize(QtCore.QSize(20, 20))
        self.DeleteButton.setFixedSize(20, 20)
        self.DeleteButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.DeleteButton.setStyleSheet(Path("src/styles/ButtonActionStyle.qss").read_text())
        self.DeleteButton.clicked.connect(self.on_delete_clicked)
        layout.addWidget(self.DeleteButton)

        # Add spacer to push buttons to the left
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer)

        self.setLayout(layout)

    def on_delete_clicked(self):
        self.delete_transaction_requested.emit(self.transaction_id) 

    def on_edit_clicked(self):
        self.edit_transaction_requested.emit(self.transaction_id)