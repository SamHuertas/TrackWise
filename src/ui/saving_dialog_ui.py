# Form implementation generated from reading ui file 'saving.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from pathlib import Path


class Ui_SavingWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(444, 300)
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        Dialog.setStyleSheet(Path("src/styles/SavingDialogStyle.qss").read_text())
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.NewSavingGoal = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.NewSavingGoal.setFont(font)
        self.NewSavingGoal.setObjectName("NewSavingGoal")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.NewSavingGoal)
        self.line_2 = QtWidgets.QFrame(parent=Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.line_2)
        self.GoalName = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.GoalName.setFont(font)
        self.GoalName.setObjectName("GoalName")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.GoalName)
        self.GoalNameInput = QtWidgets.QLineEdit(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.GoalNameInput.setFont(font)
        self.GoalNameInput.setObjectName("GoalNameInput")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.GoalNameInput)
        self.GoalAmount = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.GoalAmount.setFont(font)
        self.GoalAmount.setObjectName("GoalAmount")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.GoalAmount)
        self.GoalAmountInput = QtWidgets.QLineEdit(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.GoalAmountInput.setFont(font)
        self.GoalAmountInput.setText("")
        self.GoalAmountInput.setObjectName("GoalAmountInput")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.GoalAmountInput)
        self.line = QtWidgets.QFrame(parent=Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.line)
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
        self.SaveGoal = QtWidgets.QPushButton(parent=self.Buttons)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.SaveGoal.setFont(font)
        self.SaveGoal.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.SaveGoal.setObjectName("SaveGoal")
        self.horizontalLayout.addWidget(self.SaveGoal)
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.ItemRole.FieldRole, self.Buttons)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.NewSavingGoal.setText(_translate("Dialog", "New Saving Goal"))
        self.GoalName.setText(_translate("Dialog", "Goal Name"))
        self.GoalNameInput.setPlaceholderText(_translate("Dialog", "What are you saving for?"))
        self.GoalAmount.setText(_translate("Dialog", "Goal Amount"))
        self.GoalAmountInput.setPlaceholderText(_translate("Dialog", "0.00"))
        self.CancelButton.setText(_translate("Dialog", "Cancel"))
        self.SaveGoal.setText(_translate("Dialog", "Save Goal"))
