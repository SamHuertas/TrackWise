from PyQt6.QtWidgets import QMainWindow
from src.ui.main_window_ui import Ui_MainWindow as MainWindowUI
from src.utils.sidebar_utils import SidebarManager
from src.controllers.monthly_budget_controller import MonthlyBudgetController
from src.controllers.dashboard_controller import DashboardController
from src.views.widgets.budget_action_buttons import BudgetActionButtons
from src.models.monthly_budget_model import MonthlyBudgetModel

class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.budgetcontroller = MonthlyBudgetController(self)
        self.dashboard_controller = DashboardController(self)
        self.setup_sidebar()
        self.setup_connections()


    def setup_sidebar(self):
        buttons = [self.HomeButton, self.MonthlyBudgetsButton, self.TransactionButton, self.SavingButton]
        self.sidebar_manager = SidebarManager(buttons, self.stackedWidget)

    def setup_connections(self):
        self.AddBudgetButton.clicked.connect(self.budgetcontroller.input_budget)



   