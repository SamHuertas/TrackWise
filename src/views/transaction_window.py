from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from src.ui.transaction_dialog_ui import Ui_TransactionWindow
from src.models.expense_model import ExpenseModel
from src.models.monthly_budget_model import MonthlyBudgetModel

class TransactionWindow(QDialog):
    expense_added = pyqtSignal(int)  # Signal to emit budget_id when expense is added
    
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_TransactionWindow()
        self.setWindowTitle("New Transaction")
        self.setModal(True)
        self.ui.setupUi(self)
        self.ui.DateInput.setDate(QDate.currentDate())
        self.expense_model = ExpenseModel()
        self.budget_model = MonthlyBudgetModel()
        self.main_window = main_window  # Store reference to main window
        self.transaction_controller = main_window.transaction_controller  # Get reference to transaction controller
        self.setup_categories()
        self.setup_connections()
        
    def setup_connections(self):
        self.ui.SaveButton.clicked.connect(self.add_expense)
        self.ui.CancelButton.clicked.connect(self.reject)
        
    def add_expense(self):
        try:
            amount = float(self.ui.AmountInput.text())
            if amount <= 0:
                QMessageBox.warning(self, "Invalid Input", "Amount must be greater than 0")
                return
                
            category = self.ui.CategoryInput.currentText()
            date = self.ui.DateInput.date()
            description = self.ui.DescriptionInput.text()
            
            # Validate inputs
            if not category or not description:
                QMessageBox.warning(self, "Invalid Input", "Please fill in all fields")
                return
                
            # Get month and year from the date
            month = date.month()
            year = date.year()
            print(f"Adding expense for month: {month}, year: {year}")
            
            # Check if budget exists for this month
            budget = self.main_window.budget_model.get_budget_for_month(month, year)
            if not budget:
                QMessageBox.warning(self, "No Budget", f"No budget exists for {self.main_window.budget_model.get_month_name(month)} {year}")
                return
                
            print(f"Found budget with ID: {budget['BudgetID']}")
            
            # Add the expense with the correct budget ID
            self.expense_model.add_expense(
                budget_id=budget['BudgetID'],
                amount=amount,
                category=category,
                description=description,
                date=date.toString(Qt.DateFormat.ISODate)
            )
            # Ensure database changes are committed
            self.expense_model.db.connection.commit()
            print("Expense added successfully")         
            # Emit signal to update the dashboard and refresh transaction table
            self.clear_form()
            self.expense_added.emit(budget['BudgetID'])
            print("Form cleared")
            
            # Close the window and refresh transaction list
            self.transaction_controller.load_transactions()
            
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Amount must be a valid number")

    def clear_form(self):
        # Clears all input fields
        self.ui.AmountInput.clear()
        self.ui.CategoryInput.setCurrentIndex(-1)  # Reset to show placeholder
        self.ui.DateInput.setDate(self.ui.DateInput.date())
        self.ui.DescriptionInput.clear() 
    
    def setup_categories(self):
        # Sets up the categories in the combo box
        categories = ["Entertainment", "Food", "Groceries", "Healthcare", "Housing", "Shopping", "Transportation", "Utilities", "Other"]
        self.ui.CategoryInput.clear()
        self.ui.CategoryInput.setPlaceholderText("Select a Category")
        self.ui.CategoryInput.addItems(categories)
        self.ui.CategoryInput.setCurrentIndex(-1)  # Set to show placeholder