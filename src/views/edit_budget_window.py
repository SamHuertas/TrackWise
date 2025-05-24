from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QDate
from src.ui.edit_budget_dialog_ui import Ui_EditBudgetWindow

class EditBudgetWindow(QDialog):
    def __init__(self, main_window, budget):
        super().__init__()
        self.ui = Ui_EditBudgetWindow()
        self.setWindowTitle("Edit Monthly Budget")
        self.setModal(True)
        self.ui.setupUi(self)
        
        self.budget_model = main_window.budget_model
        self.main_window = main_window
        self.budget = budget
        
        self.ui.EditBudgetInput.setText(f"{budget['Amount']:.2f}")
        month = int(budget['Month'])
        year = int(budget['Year'])
        month_str = QDate.fromString(str(month), 'M').toString('MMMM')
        self.ui.EditAmount.setText(f"For the Month of: {month_str} {year}")
        
        self.ui.SaveButton.clicked.connect(self.update_budget)
        self.ui.CancelButton.clicked.connect(self.close)

    def update_budget(self):
        try:
            new_amount = float(self.ui.EditBudgetInput.text())
            if new_amount <= 0:
                QMessageBox.warning(self, "Input Error", "Amount must be greater than zero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid amount.")
            return
            
        # Get the current expenses and deposits for this budget
        budget_summary = self.budget_model.get_budget_summary(self.budget['BudgetID'])
        total_expenses = float(budget_summary['TotalExpenses'])
        total_deposits = float(budget_summary['TotalDeposits'])
        min_required = total_expenses + total_deposits
        if new_amount < min_required:
            QMessageBox.warning(
                self,
                "Invalid Amount",
                f"Budget cannot be less than the sum of expenses and deposits (₱{min_required:.2f})."
            )
            return
                
        self.budget_model.update_budget(self.budget['BudgetID'], new_amount)
        self.accept()


