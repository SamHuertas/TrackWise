from PyQt6.QtCore import QDate
from datetime import datetime

class DashboardController:
    def __init__(self, main_window, budget_model, savings_model):
        self.main_window = main_window
        self.budget_model = budget_model
        self.savings_model = savings_model
        self.setup_month_combobox()
        self.setup_connections()

    def setup_month_combobox(self):
        # Initialize the month combobox with months that have budgets.
        print("Setting up month combobox...")
        current_text = self.main_window.Month.currentText() if self.main_window.Month.count() > 0 else None
        budgets = self.budget_model.get_all_budget_summary()
        print(f"Found {len(budgets) if budgets else 0} budgets")
        
        self.main_window.Month.clear()
        
        for budget in budgets:
            month_num = int(budget['Month'])
            year = int(budget['Year'])
            month_name = QDate.fromString(str(month_num), 'M').toString('MMMM')
            self.main_window.Month.addItem(f"{month_name} {year}", budget['BudgetID'])
        
        # Try to restore previous selection
        if current_text:
            index = self.main_window.Month.findText(current_text)
            if index >= 0:
                self.main_window.Month.setCurrentIndex(index)
                print(f"Restored previous selection: {current_text}")
                return
        
        # If no previous selection or it wasn't found, set to current month
        current_date = datetime.now()
        current_month_year = f"{current_date.strftime('%B')} {current_date.year}"
        
        # Find index of current month/year in combobox
        index = self.main_window.Month.findText(current_month_year)
        if index >= 0:
            self.main_window.Month.setCurrentIndex(index)
            print(f"Set to current month: {current_month_year}")
        elif self.main_window.Month.count() > 0:
            self.main_window.Month.setCurrentIndex(0)
            print("Set to first available month")
        
        # Update display
        if self.main_window.Month.count() > 0:
            self.update_dashboard(self.main_window.Month.currentData())
            print("Updated dashboard display")

    def setup_connections(self):
        self.main_window.Month.currentIndexChanged.connect(self.on_month_changed)

    def on_month_changed(self, index):
        if index >= 0:
            budget_id = self.main_window.Month.itemData(index)
            self.update_dashboard(budget_id)

    def update_dashboard(self, budget_id):
        self.budget_model.db.connection.commit()
        budget_summary = self.budget_model.get_budget_summary(budget_id)
        total_savings = self.savings_model.sum_of_all_deposits()
        total_amount = total_savings['total'] if total_savings else 0
        self.main_window.Money3.setText(f"₱{total_amount:.2f}")

        if budget_summary:
            self.main_window.Money.setText(f"₱{budget_summary['BudgetAmount']:.2f}")
            self.main_window.Money2.setText(f"₱{budget_summary['TotalExpenses']:.2f}")
            
            percentage = (budget_summary['TotalExpenses'] / budget_summary['BudgetAmount']) * 100
            self.main_window.progressBar.setValue(int(percentage))
            self.main_window.PercentageUsed.setText(f"{percentage:.0f}% of monthly budget")
            
            savings = budget_summary['TotalDeposits']

            if savings > 0:
                self.main_window.Tally.setText(f"+₱{savings:.2f} this month")
            else:
                self.main_window.Tally.setText("No deposits this month")
        else:
            self.main_window.Money.setText("₱0.00")
            self.main_window.Money2.setText("₱0.00")
            self.main_window.progressBar.setValue(0)
            self.main_window.PercentageUsed.setText("0% of monthly budget")
            self.main_window.Tally.setText("₱0.00")
        
    def refresh_dashboard(self):
        if self.main_window.Month.count() > 0:
            current_budget_id = self.main_window.Month.currentData()
            self.update_dashboard(current_budget_id)
    