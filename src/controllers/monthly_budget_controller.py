import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QWidget
from src.database.db_manager import DBManager
from src.models.monthly_budget_model import MonthlyBudgetModel
from src.views.widgets.budget_action_buttons import BudgetActionButtons
from src.views.edit_budget_window import EditBudgetWindow

class MonthlyBudgetController(QWidget):
    budget_added = pyqtSignal()  # Signal emitted when a new budget is added
    budget_deleted = pyqtSignal()  # Signal emitted when a budget is deleted
    budget_edited = pyqtSignal()  # Signal emitted when a budget is edited

    def __init__(self, main_window, budget_model):
        super().__init__()
        self.main_window = main_window
        self.budgetmodel = budget_model
        self.setup_table()
        self.load_budget_data()
        self.setup_calendar()

    def setup_table(self):
        table = self.main_window.MonthlyBudgetList
        table.setColumnCount(0)
        table.setColumnCount(6)
        
        headers = ["Month", "Budget Amount", "Expenses", "Deposits", "Remaining", "Actions"]
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setHighlightSections(False)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setFixedHeight(40)
        table.verticalHeader().setDefaultSectionSize(40)
        table.setShowGrid(False)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
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
        self.budgetmodel.db.connection.commit()
        budgets = self.budgetmodel.get_all_budget_summary()
        budgets.sort(key=self.sort_by_date)
        
        for row,budget in enumerate(budgets):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(f"{QDate.fromString(str(budget['Month']), 'M').toString('MMMM')} {budget['Year']}"))

            budget_amount = QTableWidgetItem(f"₱{budget['BudgetAmount']:.2f}")
            budget_amount.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            budget_amount.setForeground(QtGui.QColor("#333333"))
            table.setItem(row, 1, budget_amount)

            expenses = QTableWidgetItem(f"-₱{budget['TotalExpenses']:.2f}")
            expenses.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            expenses.setForeground(QtGui.QColor("#f44336"))  # Red color for expenses
            table.setItem(row, 2, expenses)

            deposits = QTableWidgetItem(f"+₱{budget['TotalDeposits']:.2f}")
            deposits.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            deposits.setForeground(QtGui.QColor("#4a86e8"))  # Blue color for deposits
            table.setItem(row, 3, deposits)

            remaining = QTableWidgetItem(f"₱{budget['Remaining']:.2f}")
            remaining.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            remaining.setForeground(QtGui.QColor("#4CAF50"))  # Green color for remaining
            table.setItem(row, 4, remaining)
            
            action_buttons = BudgetActionButtons(budget['BudgetID'])
            action_buttons.delete_budget_requested.connect(self.delete_budget)
            action_buttons.edit_budget_requested.connect(self.edit_budget)
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
        self.budget_added.emit()
    
    def delete_budget(self, budget_id):
        reply = QMessageBox.question(
            self.main_window, 
            "Delete Budget", 
            "Are you sure you want to delete this budget?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            print(f"Attempting to delete budget {budget_id}...")  # Debug print
            success = self.budgetmodel.delete_budget(budget_id)
            if not success:
                QMessageBox.warning(
                    self.main_window,
                    "Cannot Delete",
                    "This budget cannot be deleted because it has associated expenses or deposits."
                )
            else:
                print("Budget deleted successfully")  # Debug print
                self.load_budget_data()
                self.budget_deleted.emit()

    def edit_budget(self, budget_id):
        budget = self.budgetmodel.get_budget_by_id(budget_id)
        edit_budget_window = EditBudgetWindow(self.main_window, budget)
        edit_budget_window.budget = budget
        edit_budget_window.exec()
        if edit_budget_window.result() == QtWidgets.QDialog.DialogCode.Accepted:
            self.load_budget_data()
            self.budget_edited.emit()