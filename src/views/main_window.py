from PyQt6.QtWidgets import QMainWindow
from src.ui.main_window_ui import Ui_MainWindow as MainWindowUI
from src.utils.sidebar_utils import SidebarManager
from src.controllers.monthly_budget_controller import MonthlyBudgetController
from src.controllers.dashboard_controller import DashboardController
from src.controllers.transaction_management_controller import TransactionManagementController
from src.models.monthly_budget_model import MonthlyBudgetModel
from src.models.expense_model import ExpenseModel
from src.views.transaction_window import TransactionWindow
from src.views.saving_window import SavingWindow
from src.views.widgets.savings_card import SavingsGoalWidget
from src.controllers.savings_controller import SavingsController
from src.models.savings_model import SavingsModel

class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.budget_model = MonthlyBudgetModel()
        self.expense_model = ExpenseModel()
        self.savings_model = SavingsModel()
        self.budget_controller = MonthlyBudgetController(self, self.budget_model)
        self.dashboard_controller = DashboardController(self, self.budget_model)
        self.transaction_controller = TransactionManagementController(self, self.expense_model)
        self.savings_controller = SavingsController(self, self.savings_model)
        self.setup_sidebar()
        self.setup_connections()
        self.center_window()
        
        # Add a test savings card
        test_account = {
            "id": 1,
            "name": "New Car",
            "amount": 5000.00,
            "target": 25000.00,
            "progress": 20.0
        }
        test_account2 = {
            "id": 1,
            "name": "New Car",
            "amount": 5000.00,
            "target": 25000.00,
            "progress": 20.0
        }
        savings_card = SavingsGoalWidget(test_account)
        savings_card2 = SavingsGoalWidget(test_account2)
        self.SavingsItems.layout().addWidget(savings_card)
        self.SavingsItems.layout().addWidget(savings_card2)
        self.SavingsItems.layout().addStretch()  # Keeps cards at the top

    def setup_sidebar(self):
        buttons = [self.HomeButton, self.MonthlyBudgetsButton, self.TransactionButton, self.SavingButton]
        self.sidebar_manager = SidebarManager(buttons, self.stackedWidget)

    def setup_connections(self):
        self.AddBudgetButton.clicked.connect(self.budget_controller.input_budget)
        self.budget_controller.budget_added.connect(self.dashboard_controller.setup_month_combobox)
        self.budget_controller.budget_deleted.connect(self.dashboard_controller.setup_month_combobox)
        self.NewTransaction.clicked.connect(self.open_transaction_window)
        self.AddTransaction.clicked.connect(self.open_transaction_window)
        self.NewGoalButton.clicked.connect(self.open_saving_window)
        self.ViewAll.clicked.connect(self.sidebar_manager.show_transactions_page)
        self.transaction_controller.transaction_deleted.connect(self.handle_transaction_deleted)
        self.PrevPage.clicked.connect(self.transaction_controller.previous_page)
        self.NextPage.clicked.connect(self.transaction_controller.next_page)
        self.CategoriesSelect.currentTextChanged.connect(self.on_category_changed)
        self.TransactionDate.dateChanged.connect(self.transaction_controller.on_date_changed)
        self.FilterButton.clicked.connect(self.transaction_controller.on_filter_clicked)

    def open_transaction_window(self):
        self.transaction_window = TransactionWindow(self)
        self.transaction_window.expense_added.connect(self.handle_expense_added)
        self.transaction_window.show()

    def open_saving_window(self):
        self.saving_window = SavingWindow(self)
        self.saving_window.show()

    def handle_transaction_deleted(self, budget_id):
        # Force immediate refresh of all components
        self.dashboard_controller.refresh_dashboard()
        self.budget_controller.load_budget_data()
        self.transaction_controller.load_transactions()

    def handle_expense_added(self, budget_id):
        # Force immediate refresh of all components
        self.dashboard_controller.refresh_dashboard()
        self.budget_controller.load_budget_data()
        self.transaction_controller.load_transactions()

    def on_category_changed(self, category):
        self.transaction_controller.current_page = 1  # Reset to first page when filter changes
        self.transaction_controller.load_transactions()

    def center_window(self):
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    
    



   