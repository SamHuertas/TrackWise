from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from src.ui.edit_transaction_dialog_ui import Ui_EditTransactionWindow
from src.models.expense_model import ExpenseModel
from src.models.monthly_budget_model import MonthlyBudgetModel

class EditTransactionWindow(QDialog):


    def __init__(self, main_window, transaction):
        super().__init__()
        self.ui = Ui_EditTransactionWindow()
        self.setWindowTitle("Edit Transaction")
        self.setModal(True)
        self.ui.setupUi(self)
        self.expense_model = ExpenseModel()
        self.budget_model = MonthlyBudgetModel()
        self.main_window = main_window  # Store reference to main window
        self.transaction_controller = main_window.transaction_controller  # Get reference to transaction controller
        self.transaction = transaction  # Store the transaction being edited
        self.setup_categories()
        self.populate_fields()
        self.setup_connections()

    def setup_connections(self):
        # Connect the buttons to their respective functions
        self.ui.SaveButton.clicked.connect(self.update_transaction)
        self.ui.CancelButton.clicked.connect(self.close)

    def populate_fields(self):
        # Set the input fields with the transaction's original data
        # Category
        category = self.transaction['Category']
        self.ui.EditCategoryInput.setCurrentText(category)
        # Description
        self.ui.EditDescriptionInput.setText(self.transaction['Description'])
        # Amount
        self.ui.EditAmountInput.setText(f"{self.transaction['Amount']:.2f}")

    def setup_categories(self):
        # Sets up the categories in the combo box
        categories = ["Entertainment", "Food", "Groceries", "Healthcare", "Housing", "Shopping", "Transportation", "Utilities", "Other"]
        self.ui.EditCategoryInput.clear()
        self.ui.EditCategoryInput.addItems(categories)

    def update_transaction(self):
        category = self.ui.EditCategoryInput.currentText()
        description = self.ui.EditDescriptionInput.text()
        amount = float(self.ui.EditAmountInput.text())

        if not description:
            QMessageBox.warning(self, "Input Error", "Description cannot be empty.")
            return
        if amount <= 0:
            QMessageBox.warning(self, "Input Error", "Amount must be greater than zero.")
            return
        
        # Get the budget ID for this transaction
        expense = self.expense_model.get_expense(self.transaction['ExpensesID'])
        budget_id = expense['BudgetID'] if expense else None
        if budget_id is not None:
            # Get the budget summary (which includes the Remaining column)
            budget_model = MonthlyBudgetModel()
            budget_summary = budget_model.get_budget_summary(budget_id)
            if budget_summary:
                remaining = float(budget_summary['Remaining'])
                original_amount = float(self.transaction['Amount'])
                new_amount = float(amount)
                new_remaining = remaining + original_amount - new_amount
                if new_remaining < 0:
                    QMessageBox.warning(
                        self,
                        "Budget Exceeded",
                        f"Amount exceeds remaining budget (₱{remaining:.2f})"
                    )
                    return
        
        # Update the transaction in the database
        self.expense_model.update_expense(self.transaction['ExpensesID'], amount, category, description)
        self.accept()  # Close the dialog

