import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QWidget
from src.database.db_manager import DBManager
from src.models.monthly_budget_model import MonthlyBudgetModel
from src.views.widgets.budget_action_buttons import BudgetActionButtons

class MonthlyBudgetController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.db = DBManager()
        self.budgetmodel = MonthlyBudgetModel()
        self.setup_ui_connections()
        self.setup_table()
        self.load_budget_data()
        self.setup_calendar()

    def setup_ui_connections(self):
        self.main_window.AddBudgetButton.clicked.connect(self.input_budget)

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

    def sort_by_date(self, budget):
        year = int(budget['Year'])
        month = int(budget['Month'])
        return (year, month)

    def load_budget_data(self):
        table = self.main_window.MonthlyBudgetList
        table.setRowCount(0)
        budgets = self.budgetmodel.get_all_budget_summary()
        budgets.sort(key=self.sort_by_date)
        
        for row,budget in enumerate(budgets):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(f"{QDate.fromString(str(budget['Month']), 'M').toString('MMMM')} {budget['Year']}"))
            table.setItem(row, 1, QTableWidgetItem(f"${budget['BudgetAmount']:.2f}"))
            table.setItem(row, 2, QTableWidgetItem(f"${budget['TotalExpenses']:.2f}"))
            table.setItem(row, 3, QTableWidgetItem(f"${budget['TotalDeposits']:.2f}"))
            table.setItem(row, 4, QTableWidgetItem(f"${budget['Remaining']:.2f}"))
            action_buttons = BudgetActionButtons(budget['BudgetID'])
            table.setCellWidget(row, 5, action_buttons)

    def input_budget(self):
        month = self.main_window.BudgetDateEdit.date().month()
        year = self.main_window.BudgetDateEdit.date().year()
        amount = self.main_window.BudgetInput.text()

        if not amount or not amount.isdigit() or int(amount) <= 0:
            QMessageBox.warning(self.main_window, "Invalid Input", "Please enter a valid budget amount.")
            return

        amount = float(amount)

        if self.budgetmodel.budget_exists(month, year):
            QMessageBox.warning(self.main_window, "Budget Exists", "A budget for this month already exists.")
            return

        self.budgetmodel.add_budget(amount, month, year)
        print(f"Budget added for {month}/{year}: {amount}")
        self.load_budget_data()
        
        