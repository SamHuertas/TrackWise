from PyQt6.QtWidgets import QMainWindow
from src.ui.main_window_ui import Ui_MainWindow as MainWindowUI
from src.utils.sidebar_utils import SidebarManager
from src.controllers.monthly_budget_controller import MonthlyBudgetController

class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_sidebar()
        self.setup_budget_table()


    def setup_sidebar(self):
        buttons = [self.HomeButton, self.MonthlyBudgetsButton, self.TransactionButton, self.SavingButton]
        self.sidebar_manager = SidebarManager(buttons, self.stackedWidget)
    
    def setup_budget_table(self):
        self.monthly_budget_controller = MonthlyBudgetController(self)



   