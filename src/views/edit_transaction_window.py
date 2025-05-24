from PyQt6.QtWidgets import QDialog, QMessageBox
from src.ui.edit_transaction_dialog_ui import Ui_EditTransactionWindow

CATEGORIES = ["Entertainment", "Food", "Groceries", "Healthcare", "Housing", "Shopping", "Transportation", "Utilities", "Other"]

class EditTransactionWindow(QDialog):
    def __init__(self, main_window, transaction):
        super().__init__()
        self.ui = Ui_EditTransactionWindow()
        self.setWindowTitle("Edit Transaction")
        self.setModal(True)
        self.ui.setupUi(self)
        
        self.expense_model = main_window.expense_model
        self.budget_model = main_window.budget_model
        self.main_window = main_window
        self.transaction = transaction
        
        self.ui.EditCategoryInput.addItems(CATEGORIES)
        self.ui.EditCategoryInput.setCurrentText(transaction['Category'])
        self.ui.EditDescriptionInput.setText(transaction['Description'])
        self.ui.EditAmountInput.setText(f"{transaction['Amount']:.2f}")
        
        self.ui.SaveButton.clicked.connect(self.update_transaction)
        self.ui.CancelButton.clicked.connect(self.close)

    def update_transaction(self):
        # Get input values
        category = self.ui.EditCategoryInput.currentText()
        description = self.ui.EditDescriptionInput.text()
        
        try:
            amount = float(self.ui.EditAmountInput.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Amount must be a valid number.")
            return
            
        if not description:
            QMessageBox.warning(self, "Input Error", "Description cannot be empty.")
            return
        if amount <= 0:
            QMessageBox.warning(self, "Input Error", "Amount must be greater than zero.")
            return
        
        # Only check budget if amount changed
        if amount != float(self.transaction['Amount']):
            budget_summary = self.budget_model.get_budget_summary(self.transaction['BudgetID'])
            if budget_summary:
                remaining = float(budget_summary['Remaining'])
                original_amount = float(self.transaction['Amount'])
                new_remaining = remaining + original_amount - amount
                if new_remaining < 0:
                    QMessageBox.warning(
                        self,
                        "Budget Exceeded",
                        f"Amount exceeds remaining budget (₱{remaining:.2f})"
                    )
                    return
        
        # Update transaction
        self.expense_model.update_expense(self.transaction['ExpensesID'], amount, category, description)
        self.accept()

