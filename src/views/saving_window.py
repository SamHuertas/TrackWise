from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from src.ui.saving_dialog_ui import Ui_SavingWindow
from src.models.savings_model import SavingsModel

class SavingWindow(QDialog):
    saving_added = pyqtSignal(int)  # Signal to emit budget_id when expense is added
    
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_SavingWindow()
        self.setWindowTitle("New Savings Goal")
        self.setModal(True)
        self.ui.setupUi(self)
        