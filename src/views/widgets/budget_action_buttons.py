from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtGui, QtCore
from pathlib import Path

class BudgetActionButtons(QWidget):
    delete_budget_requested = pyqtSignal(int)

    def __init__(self, budget_id: int):
        super().__init__()
        self.budget_id = budget_id
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.DepositButton = QPushButton("")
        self.DepositButton.setObjectName("DepositButton")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("src/assets/plus.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.DepositButton.setIcon(icon1)
        self.DepositButton.setIconSize(QtCore.QSize(17, 17))
        self.DepositButton.setFixedSize(20, 20)
        self.DepositButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.DepositButton.setStyleSheet(Path("src/styles/BudgetActionStyle.qss").read_text())
        leftspacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(leftspacer)
        layout.addWidget(self.DepositButton)

        self.DeleteButton = QPushButton("")
        self.DeleteButton.setObjectName("DeleteButton")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("src/assets/trash.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.DeleteButton.setIcon(icon2)
        self.DeleteButton.setIconSize(QtCore.QSize(20, 20))
        self.DeleteButton.setFixedSize(20, 20)
        self.DeleteButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.DeleteButton.setStyleSheet(Path("src/styles/BudgetActionStyle.qss").read_text())
        self.DeleteButton.clicked.connect(self.on_delete_clicked)
        layout.addWidget(self.DeleteButton)
        rightspacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(rightspacer)

        

        self.setLayout(layout)

    def on_delete_clicked(self):
        self.delete_budget_requested.emit(self.budget_id)