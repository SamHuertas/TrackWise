from PyQt6.QtWidgets import QMessageBox, QWidget
from src.views.widgets.savings_card import SavingsGoalWidget
from src.views.deposit_window import DepositWindow

class SavingsController(QWidget):
    def __init__(self, main_window, savings_model):
        super().__init__()
        self.main_window = main_window
        self.savings_model = savings_model
        self.load_savings_goals()
        self.update_total_savings()

    def sort_savings_by_progress(self, savings_goals):
        def get_progress(goal):
            goal_amount = goal['Goal Amount']
            total_deposits = goal['TotalDeposits']
            return (total_deposits / goal_amount) if goal_amount > 0 else 0
        return sorted(savings_goals, key=get_progress, reverse=True)

    def load_savings_goals(self):
        # Get all savings goals
        savings_goals = self.savings_model.get_all_savings_summaries()
        savings_goals = self.sort_savings_by_progress(savings_goals)
        
        layout = self.main_window.SavingsItems.layout()
        
        # Clear existing widgets 
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create and add savings cards
        for goal in savings_goals:
            savings_card = SavingsGoalWidget()
            savings_card.update_data(goal)
            savings_card.deposit_requested.connect(self.show_deposit_window)
            savings_card.delete_requested.connect(self.delete_savings)
            layout.addWidget(savings_card)
            
        # Add stretch at the end
        layout.addStretch()
        self.update_total_savings()

    def show_deposit_window(self, savings_id):
        deposit_window = DepositWindow(self.main_window, savings_id)
        deposit_window.exec()

    def update_total_savings(self):
        total_savings = self.savings_model.sum_of_all_deposits()
        amount = total_savings['total'] if total_savings else 0
        self.main_window.AccumSavings.setText(f"₱{amount:.2f}")

    def delete_savings(self, savings_id):
        reply = QMessageBox.question(self, 'Delete Savings Goal', 'Are you sure you want to delete this savings goal?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.savings_model.delete_savings_goal(savings_id)
            self.load_savings_goals()  
            self.main_window.dashboard_controller.refresh_dashboard()
            self.main_window.budget_controller.load_budget_data()  