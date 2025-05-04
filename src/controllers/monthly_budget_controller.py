import sys
from datetime import datetime
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QTableWidgetItem
from src.database.db_manager import DBManager

class MonthlyBudgetController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = DBManager()
        self.setup_ui_connections()
        self.setup_table()

    def setup_ui_connections(self):
        self.main_window.AddBudgetButton.clicked.connect(self.add_budget)
        self.main_window.BudgetDateEdit.setDisplayFormat("MMMM yyyy")
        current_date = QtCore.QDate.currentDate()
        self.main_window.BudgetDateEdit.setDate(current_date)
        self.main_window.BudgetDateEdit.setCalendarPopup(True)


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

    def add_budget(self):
        budget_amount_text = self.main_window.BudgetInput.text()

        if not budget_amount_text:
            QtWidgets.QMessageBox.warning(self.main_window, "Input Error", "Please enter a budget amount.")
            return
        try:
            budget_amount = float(budget_amount_text)
            if budget_amount <= 0:
                raise ValueError("Budget amount must be greater than zero.")
        except ValueError:
            QtWidgets.QMessageBox.warning(self.main_window, "Input Error", "Please enter a valid budget amount.")
            return
        
        date = self.main_window.BudgetDateEdit.date()
        month = date.month()
        day = date.day()
        year = date.year()  

