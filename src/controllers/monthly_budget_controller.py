import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from src.database.db_manager import DBManager
from src.models.monthly_budget_model import MonthlyBudgetModel

class MonthlyBudgetController:
    def __init__(self, main_window, model: MonthlyBudgetModel):
        self.main_window = main_window
        self.model = model
        self.db = DBManager()
        self.setup_ui_connections()
        self.setup_table()
        self.setup_calendar()

    def setup_ui_connections(self):
        self.main_window.AddBudgetButton.clicked.connect(self.add_budget)


    def setup_table(self):
        table = self.main_window.MonthlyBudgetList
        table.setColumnCount(0)
        table.setColumnCount(6)
        
        headers = ["Month", "Budget Amount", "Expenses", "Deposits", "Remaining", "Actions"]
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setHighlightSections(False)

        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)

    def setup_calendar(self):
        self.main_window.BudgetDateEdit.setCalendarPopup(False)
        self.main_window.BudgetDateEdit.setDate(QtCore.QDate.currentDate())
        self.main_window.BudgetDateEdit.setDisplayFormat("MMMM yyyy")
        
        