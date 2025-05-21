from PyQt6.QtCore import QObject, pyqtSignal
from src.models.savings_model import SavingsModel
from datetime import date

class SavingsController(QObject):
    savings_updated = pyqtSignal()
    deposit_added = pyqtSignal(int)  # Emits savings_id when deposit is added
    savings_deleted = pyqtSignal(int)  # Emits savings_id when deleted

    def __init__(self, view, savings_model: SavingsModel):
        super().__init__()
        self.view = view
        self.model = savings_model

