from PyQt6.QtWidgets import QMainWindow
from src.ui.main_window_ui import Ui_MainWindow as MainWindowUI

class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_page_connections()


    def setup_page_connections(self):
        self.HomeButton.clicked.connect(self.show_home_page)
        self.MonthlyBudgetsButton.clicked.connect(self.show_budgets_page)
        self.TransactionButton.clicked.connect(self.show_transactions_page)
        self.SavingButton.clicked.connect(self.show_savings_page)

    def show_home_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_budgets_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def show_transactions_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def show_savings_page(self):
        self.stackedWidget.setCurrentIndex(3)