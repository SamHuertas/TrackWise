from PyQt6.QtCore import QDate
from datetime import datetime
from src.views.widgets.transaction_card import TransactionCard

class DashboardController:
    def __init__(self, main_window, budget_model, savings_model, expense_model):
        self.main_window = main_window
        self.budget_model = budget_model
        self.expense_model = expense_model
        self.savings_model = savings_model
        self.setup_month_combobox()
        self.setup_connections()
        self.load_recent_transactions()
        self.load_top_savings_goals()
        self.current_budget_id = None

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
        self.current_budget_id = budget_id
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
            
            self.update_expense_breakdown(budget_id)
        else:
            self.main_window.Money.setText("₱0.00")
            self.main_window.Money2.setText("₱0.00")
            self.main_window.progressBar.setValue(0)
            self.main_window.PercentageUsed.setText("0% of monthly budget")
            self.main_window.Tally.setText("₱0.00")
    
    def update_expense_breakdown(self, budget_id):
        """Fetch expense breakdown by category and update the donut chart based on current period selection"""
        # Get current selection from MonthSelect dropdown
        current_index = self.main_window.MonthSelect.currentIndex()
        period_map = {
            0: "month",  # This Month
            1: "week",   # This Week  
            2: "day"     # This Day
        }
        
        period = period_map.get(current_index, "month")
        self.update_expense_breakdown_by_period(budget_id, period)

    def update_expense_breakdown_by_period(self, budget_id, period="month"):
        """Update expense breakdown based on selected time period"""
        if period == "week":
            expenses = self.expense_model.get_expenses_by_budget_this_week(budget_id)
        elif period == "day":
            expenses = self.expense_model.get_expenses_by_budget_today(budget_id)
        else:  # Default to month
            expenses = self.expense_model.get_expenses_by_budget(budget_id)
        
        category_totals = {}
        for expense in expenses:
            category = expense['Category']
            amount = expense['Amount']
            category_totals[category] = category_totals.get(category, 0) + amount
            
        self.main_window.donut_chart.set_data(category_totals)

    def on_expense_period_changed(self, index):
        """Handle changes to the expense breakdown period dropdown"""
        if self.current_budget_id is None:
            return
            
        period_map = {
            0: "month",  # This Month
            1: "week",   # This Week  
            2: "day"     # This Day
        }
        
        period = period_map.get(index, "month")
        self.update_expense_breakdown_by_period(self.current_budget_id, period)
        
    def refresh_dashboard(self):
        if self.main_window.Month.count() > 0:
            current_budget_id = self.main_window.Month.currentData()
            self.update_dashboard(current_budget_id)
        self.load_top_savings_goals()
    
    def load_recent_transactions(self):
        # Clear the transaction list layout first
        layout = self.main_window.TransactionContents.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Get the top 5 most recent transactions
        top5 = self.expense_model.get_top5_expenses()

        for transaction in top5:
            transaction_card = TransactionCard()
            transaction_card.update_data(transaction) 
            layout.addWidget(transaction_card)

    def load_top_savings_goals(self):
        # Clear existing widgets
        layout = self.main_window.SavingsContents.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get all savings goals
        savings_goals = self.savings_model.get_all_savings_summaries()

        # Sort savings goals by completion percentage
        def get_progress(goal):
            goal_amount = goal['Goal Amount']
            total_deposits = goal['TotalDeposits']
            return (total_deposits / goal_amount) if goal_amount > 0 else 0

        sorted_goals = sorted(savings_goals, key=get_progress, reverse=True)

        # Get the top 3 goals
        top_3_goals = sorted_goals[:3]

        # Create and add DashboardSavingsCard for top 3 goals
        from src.views.widgets.dashboard_savings_card import DashboardSavingsCard
        for goal in top_3_goals:
            savings_card = DashboardSavingsCard()
            savings_card.update_data(goal)
            layout.addWidget(savings_card)



