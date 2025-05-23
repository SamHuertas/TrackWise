from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from src.ui.edit_budget_dialog_ui import Ui_EditBudgetWindow
from src.models.monthly_budget_model import MonthlyBudgetModel

class EditBudgetWindow(QDialog):
    def __init__(self, main_window, budget):
        super().__init__()
        self.ui = Ui_EditBudgetWindow()
        self.setWindowTitle("Edit Monthly Budget")
        self.setModal(True)
        self.ui.setupUi(self)
        self.budget_model = MonthlyBudgetModel()
        self.main_window = main_window  
        self.budget = budget  # Set the budget to be edited from parameter
        self.setup_connections()
        self.populate_fields()

    def setup_connections(self):
        self.ui.SaveButton.clicked.connect(self.update_budget)
        self.ui.CancelButton.clicked.connect(self.close)

    def populate_fields(self):
        if not self.budget:
            return
        self.ui.EditBudgetInput.setText(f"{self.budget['Amount']:.2f}")
        # Set the label for the month/year using the model's get_month_name
        month = int(self.budget['Month'])
        year = int(self.budget['Year'])
        month_str = self.budget_model.get_month_name(month)
        self.ui.EditAmount.setText(f"For the Month of: {month_str} {year}")

    def update_budget(self):
        if not self.budget:
            return
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
        if budget_summary:
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
        # Update the budget in the database
        self.budget_model.update_budget(self.budget['BudgetID'], new_amount)
        self.accept()  # Close the dialog after saving


