from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QWidget
from src.views.widgets.budget_action_buttons import BudgetActionButtons
from src.views.edit_budget_window import EditBudgetWindow

class MonthlyBudgetController(QWidget):
    def __init__(self, main_window, budget_model):
        super().__init__()
        self.main_window = main_window
        self.budgetmodel = budget_model
        
        self.setup_table()
        self.setup_calendar()
        self.load_budget_data()

    def setup_table(self):
        table = self.main_window.MonthlyBudgetList
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
        return (int(budget['Year']), int(budget['Month']))

    def load_budget_data(self):
        table = self.main_window.MonthlyBudgetList
        table.setRowCount(0)
        
        budgets = list(self.budgetmodel.get_all_budget_summary())
        if not budgets:
            table.insertRow(0)
            message_item = QTableWidgetItem("No budget data available")
            message_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(0, 0, message_item)
            table.setSpan(0, 0, 1, 6)
            return
            
        budgets.sort(key=self.sort_by_date)
        table.setRowCount(len(budgets))
        
        for row, budget in enumerate(budgets):
            # Month and Year
            month_str = QDate.fromString(str(budget['Month']), 'M').toString('MMMM')
            month_item = QTableWidgetItem(f"{month_str} {budget['Year']}")
            month_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            month_item.setForeground(QtGui.QColor("#333333"))
            table.setItem(row, 0, month_item)
            
            # Budget Amount
            budget_amount = QTableWidgetItem(f"₱{budget['BudgetAmount']:.2f}")
            budget_amount.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            budget_amount.setForeground(QtGui.QColor("#333333"))
            table.setItem(row, 1, budget_amount)
            
            # Expenses
            expenses = QTableWidgetItem(f"-₱{budget['TotalExpenses']:.2f}")
            expenses.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            expenses.setForeground(QtGui.QColor("#f44336"))
            table.setItem(row, 2, expenses)
            
            # Deposits
            deposits = QTableWidgetItem(f"+₱{budget['TotalDeposits']:.2f}")
            deposits.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            deposits.setForeground(QtGui.QColor("#4a86e8"))
            table.setItem(row, 3, deposits)
            
            # Remaining
            remaining = QTableWidgetItem(f"₱{budget['Remaining']:.2f}")
            remaining.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            remaining.setForeground(QtGui.QColor("#4CAF50"))
            table.setItem(row, 4, remaining)
            
            # Actions
            action_buttons = BudgetActionButtons(budget['BudgetID'])
            action_buttons.delete_budget_requested.connect(self.delete_budget)
            action_buttons.edit_budget_requested.connect(self.edit_budget)
            table.setCellWidget(row, 5, action_buttons)

    def input_budget(self):
        month = self.main_window.BudgetDateEdit.date().month()
        year = self.main_window.BudgetDateEdit.date().year()
        amount = self.main_window.BudgetInput.text()

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self.main_window, "Invalid Input", "Please enter a valid budget amount.")
            return

        if self.budgetmodel.budget_exists(month, year):
            QMessageBox.warning(self.main_window, "Budget Exists", "A budget for this month already exists.")
            return

        # Add the budget
        self.budgetmodel.add_budget(amount, month, year)
        self.load_budget_data()
    
    def delete_budget(self, budget_id):
        reply = QMessageBox.question(
            self.main_window, 
            "Delete Budget", 
            "Are you sure you want to delete this budget?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.budgetmodel.delete_budget(budget_id):
                self.load_budget_data()
                self.main_window.dashboard_controller.setup_month_combobox()
            else:
                QMessageBox.warning(
                    self.main_window,
                    "Cannot Delete",
                    "This budget cannot be deleted because it has associated expenses or deposits."
                )

    def edit_budget(self, budget_id):
        budget = self.budgetmodel.get_budget_by_id(budget_id)        
        edit_budget_window = EditBudgetWindow(self.main_window, budget)
        if edit_budget_window.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.load_budget_data()
            self.main_window.dashboard_controller.refresh_dashboard()