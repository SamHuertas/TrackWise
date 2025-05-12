from PyQt6.QtWidgets import QMainWindow
from src.ui.main_window_ui import Ui_MainWindow as MainWindowUI
from src.utils.sidebar_utils import SidebarManager
from src.controllers.monthly_budget_controller import MonthlyBudgetController
from src.controllers.dashboard_controller import DashboardController
from src.controllers.transaction_management_controller import TransactionManagementController
from src.models.monthly_budget_model import MonthlyBudgetModel
from src.models.expense_model import ExpenseModel
from src.views.transaction_window import TransactionWindow

class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.budget_model = MonthlyBudgetModel()
        self.expense_model = ExpenseModel()
        self.budget_controller = MonthlyBudgetController(self, self.budget_model)
        self.dashboard_controller = DashboardController(self, self.budget_model)
        self.transaction_controller = TransactionManagementController(self, self.budget_model, self.expense_model)
        self.setup_sidebar()
        self.setup_connections()
        self.center_window()

    def setup_sidebar(self):
        buttons = [self.HomeButton, self.MonthlyBudgetsButton, self.TransactionButton, self.SavingButton]
        self.sidebar_manager = SidebarManager(buttons, self.stackedWidget)

    def setup_connections(self):
        self.AddBudgetButton.clicked.connect(self.budget_controller.input_budget)
        self.budget_controller.budget_added.connect(self.dashboard_controller.setup_month_combobox)
        self.budget_controller.budget_deleted.connect(self.dashboard_controller.setup_month_combobox)
        self.NewTransaction.clicked.connect(self.open_transaction_window)
        self.AddTransaction.clicked.connect(self.open_transaction_window)

    def open_transaction_window(self):
        self.transaction_window = TransactionWindow(self)
        self.transaction_window.expense_added.connect(self.handle_expense_added)
        self.transaction_window.show()
        

    def handle_expense_added(self, budget_id):
        # Force immediate refresh of all components
        self.dashboard_controller.refresh_dashboard()
        self.budget_controller.load_budget_data()
        self.transaction_controller.load_transactions()

    def center_window(self):
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    
    



   