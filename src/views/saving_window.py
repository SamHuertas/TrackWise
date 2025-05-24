from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QDate
from src.ui.saving_dialog_ui import Ui_SavingWindow



class SavingWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_SavingWindow()
        self.setWindowTitle("New Savings Goal")
        self.setModal(True)
        self.ui.setupUi(self)
        
        self.savings_model = main_window.savings_model
        self.main_window = main_window
        
        self.setup_connections()
        
    def setup_connections(self):
        self.ui.SaveGoal.clicked.connect(self.add_savings_goal)
        self.ui.CancelButton.clicked.connect(self.reject)

    def add_savings_goal(self):
        try:
            amount = float(self.ui.GoalAmountInput.text())
            name = self.ui.GoalNameInput.text().strip()
            
            if not name:
                QMessageBox.warning(self, "Invalid Input", "Name cannot be empty")
                return

            if amount <= 0:
                QMessageBox.warning(self, "Invalid Input", "Amount must be greater than 0")
                return

            date = QDate.currentDate()
            date_str = date.toString("yyyy-MM-dd")
            self.savings_model.add_savings_goal(date_str, name, amount)
            
            self.main_window.savings_controller.load_savings_goals()
            self.main_window.dashboard_controller.load_top_savings_goals()
            self.accept()
            
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount")


        
            
            
                