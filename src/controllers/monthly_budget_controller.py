import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from src.database.db_manager import DBManager
from src.models.monthly_budget_model import MonthlyBudgetModel

class MonthlyBudgetController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = DBManager()
        self.model = MonthlyBudgetModel()
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

    def add_budget(self):
        month = self.main_window.BudgetDateEdit.date().month()
        year = self.main_window.BudgetDateEdit.date().year()
        amount = self.main_window.BudgetInput.text()

        if not amount or not amount.isdigit() or int(amount) <= 0:
            QMessageBox.warning(self.main_window, "Invalid Input", "Please enter a valid budget amount.")
            return

        amount = float(amount)

        if self.model.budget_exists(month, year):
            QMessageBox.warning(self.main_window, "Budget Exists", "A budget for this month already exists.")
            return

        self.model.add_budget(amount, month, year)
        print(f"Budget added for {month}/{year}: {amount}")
        
        