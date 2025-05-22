from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QWidget
from src.models.savings_model import SavingsModel
from src.views.widgets.savings_card import SavingsGoalWidget
from src.views.deposit_window import DepositWindow
from datetime import date

class SavingsController(QWidget):
    savings_updated = pyqtSignal()
    deposit_added = pyqtSignal(int)  # Emits savings_id when deposit is added
    savings_deleted = pyqtSignal(int)  # Emits savings_id when deleted

    def __init__(self, main_window, savings_model):
        super().__init__()
        self.main_window = main_window
        self.savings_model = savings_model
        self.load_savings_goals()
        self.update_total_savings()
    
    def load_savings_goals(self):
        self.savings_model.db.connection.commit()
        # Clear existing widgets
        layout = self.main_window.SavingsItems.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get all savings goals
        savings_goals = self.savings_model.get_all_savings_summaries()
        
        # Create and add savings cards
        for goal in savings_goals:
            savings_card = SavingsGoalWidget()
            savings_card.update_data(goal)
            savings_card.deposit_requested.connect(self.show_deposit_window)
            layout.addWidget(savings_card)
        layout.addStretch()
        self.update_total_savings()

    def show_deposit_window(self, savings_id):
        deposit_window = DepositWindow(self.main_window, savings_id)
        deposit_window.deposit_added.connect(self.load_savings_goals)
        deposit_window.deposit_added.connect(self.main_window.handle_deposit_added)  # Connect to refresh handler
        deposit_window.exec()

    def on_deposit_added(self):
        self.load_savings_goals()
        self.main_window.dashboard_controller.refresh_dashboard()
        self.update_total_savings()

    def update_total_savings(self):
        total_savings = self.savings_model.sum_of_all_deposits()
        amount = total_savings['total'] if total_savings else 0
        self.main_window.AccumSavings.setText(f"₱{amount:.2f}")

