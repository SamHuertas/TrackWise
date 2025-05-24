from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt, QDate
from src.ui.transaction_dialog_ui import Ui_TransactionWindow

CATEGORIES = ["Entertainment", "Food", "Groceries", "Healthcare", "Housing", "Shopping", "Transportation", "Utilities", "Other"]

class TransactionWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_TransactionWindow()
        self.setWindowTitle("New Transaction")
        self.setModal(True)
        self.ui.setupUi(self)
        
        self.expense_model = main_window.expense_model
        self.budget_model = main_window.budget_model
        self.main_window = main_window
        
        self.ui.DateInput.setDate(QDate.currentDate())
        self.ui.CategoryInput.addItems(CATEGORIES)
        self.ui.CategoryInput.setCurrentIndex(-1)
        self.ui.CategoryInput.setPlaceholderText("Select a Category")
        
        self.ui.SaveButton.clicked.connect(self.add_expense)
        self.ui.CancelButton.clicked.connect(self.reject)
        
    def add_expense(self):
        amount_text = self.ui.AmountInput.text()
        category = self.ui.CategoryInput.currentText()
        description = self.ui.DescriptionInput.text()
        
        if not category or not description:
            QMessageBox.warning(self, "Invalid Input", "Please fill in all fields")
            return
            
        try:
            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self, "Invalid Input", "Amount must be greater than 0")
                return
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Amount must be a valid number")
            return
            
        date = self.ui.DateInput.date()
        month = date.month()
        year = date.year()
        
        # Get budget info
        budget = self.budget_model.get_budget_for_month(month, year)
        if not budget:
            QMessageBox.warning(self, "No Budget", f"No budget exists for {self.budget_model.get_month_name(month)} {year}")
            return

        # Add expense
        self.expense_model.add_expense(
            budget_id=budget['BudgetID'],
            amount=amount,
            category=category,
            description=description,
            date=date.toString(Qt.DateFormat.ISODate)
        )
        
        # Update transaction list first and close window
        self.main_window.transaction_controller.load_transactions()
        self.main_window.dashboard_controller.refresh_dashboard()
        self.accept()
        self.main_window.budget_controller.load_budget_data()

    def clear_form(self):
        self.ui.AmountInput.clear()
        self.ui.CategoryInput.setCurrentIndex(-1)
        self.ui.DateInput.setDate(QDate.currentDate())
        self.ui.DescriptionInput.clear()