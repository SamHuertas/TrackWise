from PyQt6 import QtCore, QtGui, QtWidgets
from pathlib import Path


class Ui_DepositWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(462, 310)
        Dialog.setStyleSheet(Path("src/styles/DepositDialogStyle.qss").read_text())
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.NewDeposit = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.NewDeposit.setFont(font)
        self.NewDeposit.setObjectName("NewDeposit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.NewDeposit)
        self.line_2 = QtWidgets.QFrame(parent=Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.line_2)
        self.MonthlyBudget = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.MonthlyBudget.setFont(font)
        self.MonthlyBudget.setObjectName("MonthlyBudget")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.MonthlyBudget)
        self.MonthlyBudgetInput = QtWidgets.QComboBox(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.MonthlyBudgetInput.setFont(font)
        self.MonthlyBudgetInput.setEditable(False)
        self.MonthlyBudgetInput.setObjectName("MonthlyBudgetInput")
        self.MonthlyBudgetInput.addItem("")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.MonthlyBudgetInput)
        self.RemainingBalance = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.RemainingBalance.setFont(font)
        self.RemainingBalance.setObjectName("RemainingBalance")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.RemainingBalance)
        self.RemainingBalanceValidator = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.RemainingBalanceValidator.setFont(font)
        self.RemainingBalanceValidator.setObjectName("RemainingBalanceValidator")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.RemainingBalanceValidator)
        self.DepositAmount = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.DepositAmount.setFont(font)
        self.DepositAmount.setObjectName("DepositAmount")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.DepositAmount)
        self.DepositAmountInput = QtWidgets.QLineEdit(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.DepositAmountInput.setFont(font)
        self.DepositAmountInput.setObjectName("DepositAmountInput")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.DepositAmountInput)
        self.line = QtWidgets.QFrame(parent=Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.line)
        self.Buttons = QtWidgets.QWidget(parent=Dialog)
        self.Buttons.setObjectName("Buttons")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Buttons)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.CancelButton = QtWidgets.QPushButton(parent=self.Buttons)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.CancelButton.setFont(font)
        self.CancelButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout.addWidget(self.CancelButton)
        self.DepositButton = QtWidgets.QPushButton(parent=self.Buttons)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.DepositButton.setFont(font)
        self.DepositButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.DepositButton.setObjectName("DepositButton")
        self.horizontalLayout.addWidget(self.DepositButton)
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.ItemRole.FieldRole, self.Buttons)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.NewDeposit.setText(_translate("Dialog", "Deposit to"))
        self.MonthlyBudget.setText(_translate("Dialog", "Monthly Budget"))
        self.MonthlyBudgetInput.setCurrentText(_translate("Dialog", "New Item"))
        self.MonthlyBudgetInput.setItemText(0, _translate("Dialog", "New Item"))
        self.RemainingBalance.setText(_translate("Dialog", "Remaining Balance"))
        self.RemainingBalanceValidator.setText(_translate("Dialog", "₱0.00"))
        self.DepositAmount.setText(_translate("Dialog", "Deposit Amount"))
        self.DepositAmountInput.setPlaceholderText(_translate("Dialog", "How much are you going to deposit?"))
        self.CancelButton.setText(_translate("Dialog", "Cancel"))
        self.DepositButton.setText(_translate("Dialog", "Deposit Savings"))
