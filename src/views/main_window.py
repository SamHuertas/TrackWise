from PyQt6.QtWidgets import QMainWindow
from PyQt6 import QtWidgets
from src.ui.main_window_ui import Ui_MainWindow as MainWindowUI
from src.utils.sidebar_utils import SidebarManager
from src.views.widgets.donut_chart import DonutChart
from datetime import datetime

from src.controllers.monthly_budget_controller import MonthlyBudgetController
from src.controllers.dashboard_controller import DashboardController
from src.controllers.transaction_management_controller import TransactionManagementController
from src.controllers.savings_controller import SavingsController

from src.models.monthly_budget_model import MonthlyBudgetModel
from src.models.expense_model import ExpenseModel
from src.models.savings_model import SavingsModel

from src.views.transaction_window import TransactionWindow
from src.views.saving_window import SavingWindow

class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.budget_model = MonthlyBudgetModel()
        self.expense_model = ExpenseModel()
        self.savings_model = SavingsModel()
        self.budget_controller = MonthlyBudgetController(self, self.budget_model)
        self.dashboard_controller = DashboardController(self, self.budget_model, self.savings_model, self.expense_model)
        self.transaction_controller = TransactionManagementController(self, self.expense_model)
        self.savings_controller = SavingsController(self, self.savings_model)
        current_date = datetime.now()
        formatted_date = current_date.strftime("%A, %B %d, %Y")
        self.Date.setText(formatted_date)
        self.setup_sidebar()
        self.setup_connections()
        self.center_window()

    def setup_sidebar(self):
        buttons = [self.HomeButton, self.MonthlyBudgetsButton, self.TransactionButton, self.SavingButton]
        self.sidebar_manager = SidebarManager(buttons, self.stackedWidget)

    def setup_connections(self):
        self.AddBudgetButton.clicked.connect(self.budget_controller.input_budget)

        self.NewTransaction.clicked.connect(self.open_transaction_window)
        self.AddTransaction.clicked.connect(self.open_transaction_window)
        
        self.NewGoalButton.clicked.connect(self.open_saving_window)
        
        self.ViewAll.clicked.connect(self.sidebar_manager.show_transactions_page)
        self.ViewAllSavings.clicked.connect(self.sidebar_manager.show_savings_page)

        self.PrevPage.clicked.connect(self.transaction_controller.previous_page)
        self.NextPage.clicked.connect(self.transaction_controller.next_page)

        self.CategoriesSelect.currentTextChanged.connect(self.on_category_changed)
        self.TransactionDate.dateChanged.connect(self.transaction_controller.on_date_changed)
        self.FilterButton.clicked.connect(self.transaction_controller.on_filter_clicked)

    def open_transaction_window(self):
        self.transaction_window = TransactionWindow(self)
        self.transaction_window.exec()

    def open_saving_window(self):
        self.saving_window = SavingWindow(self)
        self.saving_window.exec()

    def on_category_changed(self, category):
        self.transaction_controller.current_page = 1  
        self.transaction_controller.load_transactions()

    def center_window(self):
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)




