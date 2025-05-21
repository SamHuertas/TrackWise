from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from src.ui.saving_dialog_ui import Ui_SavingWindow
from src.models.savings_model import SavingsModel


class SavingWindow(QDialog):
    saving_added = pyqtSignal()  # Signal to notify when a savings goal is added
    
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_SavingWindow()
        self.setWindowTitle("New Savings Goal")
        self.setModal(True)
        self.ui.setupUi(self)
        self.savings_model = SavingsModel()
        self.main_window = main_window
        self.setup_connections()
        
    def setup_connections(self):
        self.ui.SaveGoal.clicked.connect(self.add_savings_goal)
        self.ui.CancelButton.clicked.connect(self.reject)

    def add_savings_goal(self):
        try:
            amount = float(self.ui.GoalAmountInput.text())
            name = self.ui.GoalNameInput.text()
            
            if not name or not amount:
                QMessageBox.warning(self, "Invalid Input", "Please fill in all fields")
                return

            if amount <= 0:
                QMessageBox.warning(self, "Invalid Input", "Amount must be greater than 0")
                return
            
            if not name:
                QMessageBox.warning(self, "Invalid Input", "Name cannot be empty")
                return

            
            date = QDate.currentDate()
            date_str = date.toString("yyyy-MM-dd")
            self.savings_model.add_savings_goal(date_str, name, amount)
            self.clear_form()
            self.saving_added.emit()  # Emit signal to notify that a savings goal was added


        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Amount must be a valid number")
                
    def clear_form(self):
        self.ui.GoalAmountInput.clear()
        self.ui.GoalNameInput.clear()

        
            
            
                