from PyQt6.QtCore import QDate
from datetime import datetime
from src.views.widgets.transaction_card import TransactionCard
from src.views.widgets.dashboard_savings_card import DashboardSavingsCard
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


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
        self.refresh_pie_chart()  

    def setup_month_combobox(self):
        budgets = list(self.budget_model.get_all_budget_summary())
        self.main_window.Month.clear()
        
        if not budgets:
            self.main_window.Month.addItem("No Budget Available")
            self.update_dashboard(None)
            return
            
        for budget in budgets:
            month_num = int(budget['Month'])
            year = int(budget['Year'])
            month_name = QDate.fromString(str(month_num), 'M').toString('MMMM')
            self.main_window.Month.addItem(f"{month_name} {year}", budget['BudgetID'])
        
        # Set to current month if available, otherwise first item
        current_date = datetime.now()
        current_month_year = f"{current_date.strftime('%B')} {current_date.year}"
        
        index = self.main_window.Month.findText(current_month_year)
        self.main_window.Month.setCurrentIndex(index if index >= 0 else 0)
        self.update_dashboard(self.main_window.Month.currentData())

    def setup_connections(self):
        self.main_window.Month.currentIndexChanged.connect(self.on_month_changed)
        self.main_window.MonthSelect.currentIndexChanged.connect(self.handle_month_select)

    def on_month_changed(self, index):
        budget_id = self.main_window.Month.itemData(index)
        self.update_dashboard(budget_id)

    def update_dashboard(self, budget_id):
        # Get total savings regardless of budget
        total_savings = self.savings_model.sum_of_all_deposits()
        total_amount = total_savings['total'] if total_savings else 0
        self.main_window.Money3.setText(f"₱{total_amount:.2f}")

        if not budget_id:
            self.reset_dashboard_display()
            return
            
        budget_summary = self.budget_model.get_budget_summary(budget_id)
        if budget_summary:
            self.main_window.Money.setText(f"₱{budget_summary['BudgetAmount']:.2f}")
            self.main_window.Money2.setText(f"₱{budget_summary['TotalExpenses']:.2f}")
            
            percentage = (budget_summary['TotalExpenses'] / budget_summary['BudgetAmount']) * 100
            self.main_window.progressBar.setValue(int(percentage))
            self.main_window.PercentageUsed.setText(f"{percentage:.0f}% of monthly budget")
            
            savings = budget_summary['TotalDeposits']
            self.main_window.Tally.setText(f"+₱{savings:.2f} this month" if savings > 0 else "No deposits this month")
        else:
            self.reset_dashboard_display()

    def reset_dashboard_display(self):
        self.main_window.Money.setText("₱0.00")
        self.main_window.Money2.setText("₱0.00")
        self.main_window.progressBar.setValue(0)
        self.main_window.PercentageUsed.setText("0% of monthly budget")
        self.main_window.Tally.setText("No budget available")
        
    def refresh_dashboard(self):
        if self.main_window.Month.count() > 0:
            current_budget_id = self.main_window.Month.currentData()
            if current_budget_id:
                budget_summary = self.budget_model.get_budget_summary(current_budget_id)
                if budget_summary:
                    # Update budget info
                    self.main_window.Money.setText(f"₱{budget_summary['BudgetAmount']:.2f}")
                    self.main_window.Money2.setText(f"₱{budget_summary['TotalExpenses']:.2f}")
                    
                    # Update progress
                    percentage = (budget_summary['TotalExpenses'] / budget_summary['BudgetAmount']) * 100
                    self.main_window.progressBar.setValue(int(percentage))
                    self.main_window.PercentageUsed.setText(f"{percentage:.0f}% of monthly budget")
                    
                    # Update savings
                    savings = budget_summary['TotalDeposits']
                    self.main_window.Tally.setText(f"+₱{savings:.2f} this month" if savings > 0 else "No deposits this month")
                    
                    # Update total savings
                    total_savings = self.savings_model.sum_of_all_deposits()
                    total_amount = total_savings['total'] if total_savings else 0
                    self.main_window.Money3.setText(f"₱{total_amount:.2f}")
                    
                    # Update recent transactions
                    self.load_recent_transactions()
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
        
        if not top5:
            message = QLabel("No recent transactions")
            message.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(message)
            return

        for transaction in top5:
            transaction_card = TransactionCard()
            transaction_card.update_data(transaction) 
            layout.addWidget(transaction_card)
        layout.addStretch(1)

    def load_top_savings_goals(self):
        # Clear existing widgets
        layout = self.main_window.SavingsContents.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get all savings goals
        savings_goals = self.savings_model.get_all_savings_summaries()
        if not savings_goals:
            message = QLabel("No savings")
            message.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(message)
            return

        # Sort savings goals by completion percentage
        def get_progress(goal):
            goal_amount = goal['Goal Amount']
            total_deposits = goal['TotalDeposits']
            return (total_deposits / goal_amount) if goal_amount > 0 else 0

        sorted_goals = sorted(savings_goals, key=get_progress, reverse=True)

        # Get the top 3 goals
        top_3_goals = sorted_goals[:3]

        for goal in top_3_goals:
            savings_card = DashboardSavingsCard()
            savings_card.update_data(goal)
            layout.addWidget(savings_card)
    
    def handle_month_select(self, index):
        # Handle MonthSelect combobox selection
        current_budget_id = self.main_window.Month.currentData()
        if not current_budget_id:
            return
        
        selected_period = self.main_window.MonthSelect.currentText().strip()
        self.show_pie_chart(current_budget_id, selected_period)

    def show_pie_chart(self, budget_id, period):
        # Display pie chart data for the given budget and period
        if not budget_id:
            return
            
        # Get expenses based on period
        if period == "This Week":
            expenses = self.expense_model.get_expenses_by_budget_this_week(budget_id)
        elif period == "This Day":
            expenses = self.expense_model.get_expenses_by_budget_today(budget_id)
        else:  # This Month
            expenses = self.expense_model.get_expenses_by_budget(budget_id)
            
        # Calculate category totals
        category_totals = {}
        for expense in expenses:
            category = expense['Category']
            amount = expense['Amount']
            category_totals[category] = category_totals.get(category, 0) + amount
            
        # Update the donut chart
        self.main_window.donut_chart.set_data(category_totals)

    def refresh_pie_chart(self):
        # Refresh the pie chart with current budget and period 
        current_budget_id = self.main_window.Month.currentData()
        if not current_budget_id:
            return
            
        selected_period = self.main_window.MonthSelect.currentText().strip()
        self.show_pie_chart(current_budget_id, selected_period)
