from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt, QDate
from src.ui.deposit_dialog_ui import Ui_DepositWindow
from datetime import datetime


class DepositWindow(QDialog):
    def __init__(self, main_window, savings_id=None):
        super().__init__()
        self.ui = Ui_DepositWindow()
        self.setWindowTitle("Deposit to Savings Goal")
        self.setModal(True)
        self.ui.setupUi(self)
        
        self.savings_model = main_window.savings_model
        self.budget_model = main_window.budget_model
        self.main_window = main_window
        self.savings_id = savings_id
        
        self.setup_connections()
        self.setup_header()
        self.setup_combobox_and_remaining_balance()

    def setup_connections(self):
        self.ui.DepositButton.clicked.connect(self.handle_deposit)
        self.ui.CancelButton.clicked.connect(self.close)

    def setup_header(self):
        self.ui.NewDeposit.setText("Deposit to " + self.savings_model.get_savings_goal(self.savings_id)['Name'].title())

    def setup_combobox_and_remaining_balance(self):
        self.ui.MonthlyBudgetInput.clear()
        self.budgets = self.budget_model.get_all_budget_summary()
        
        # Add items to combobox
        for budget in self.budgets:
            month_num = int(budget['Month'])
            year = int(budget['Year'])
            month_name = QDate.fromString(str(month_num), 'M').toString('MMMM')
            self.ui.MonthlyBudgetInput.addItem(f"{month_name} {year}", budget['BudgetID'])
        
        # Connect the signal to handle selection changes
        self.ui.MonthlyBudgetInput.currentIndexChanged.connect(self.on_monthly_budget_changed)
        
        # Set to current month if available
        current_date = datetime.now()
        current_month_year = f"{current_date.strftime('%B')} {current_date.year}"
        
        # Find and select current month/year in combobox
        index = self.ui.MonthlyBudgetInput.findText(current_month_year)
        if index >= 0:
            self.ui.MonthlyBudgetInput.setCurrentIndex(index)
        elif self.ui.MonthlyBudgetInput.count() > 0:
            self.ui.MonthlyBudgetInput.setCurrentIndex(0)

        # Trigger initial remaining balance update
        if self.ui.MonthlyBudgetInput.count() > 0:
            self.on_monthly_budget_changed(self.ui.MonthlyBudgetInput.currentIndex())

    def on_monthly_budget_changed(self, index):
        if index >= 0 and self.budgets:
            budget = self.budgets[index]
            self.ui.RemainingBalanceValidator.setText(f"₱{budget['Remaining']:.2f}")
        else:
            self.ui.RemainingBalanceValidator.setText("₱0.00")
        
    def handle_deposit(self):
        try:
            amount = float(self.ui.DepositAmountInput.text())
            if amount <= 0:
                QMessageBox.warning(self, "Invalid Input", "Amount must be greater than 0")
                return
                
            budget_id = self.ui.MonthlyBudgetInput.currentData()
            if not budget_id:
                QMessageBox.warning(self, "Error", "Please select a monthly budget")
                return

            current_index = self.ui.MonthlyBudgetInput.currentIndex()
            if current_index >= 0 and self.budgets:
                remaining_balance = self.budgets[current_index]['Remaining']
                if amount > remaining_balance:
                    QMessageBox.warning(
                        self, 
                        "Invalid Amount", 
                        f"Amount exceeds remaining budget (₱{remaining_balance:.2f})"
                    )
                    return

            # --- New savings goal remaining amount check ---
            savings_goal_summary = self.savings_model.get_savings_summary(self.savings_id)
            if savings_goal_summary:
                goal_amount = savings_goal_summary['Goal Amount']
                total_deposits = savings_goal_summary['TotalDeposits']
                remaining_to_goal = goal_amount - total_deposits
                
                if amount > remaining_to_goal:
                     QMessageBox.warning(
                        self, 
                        "Invalid Amount", 
                        f"Amount exceeds remaining amount for goal (₱{remaining_to_goal:.2f})"
                    )
                     return

            # Add deposit to savings with current date
            current_date = QDate.currentDate().toString(Qt.DateFormat.ISODate)
            self.savings_model.add_deposit(budget_id, self.savings_id, current_date, amount)
            self.main_window.savings_controller.load_savings_goals()
            self.main_window.dashboard_controller.refresh_dashboard()
            self.main_window.budget_controller.load_budget_data()
            self.accept()
            
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount")