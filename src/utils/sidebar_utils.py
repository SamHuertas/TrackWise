from src.ui.main_window_ui import Ui_MainWindow
from PyQt6.QtWidgets import QPushButton, QStackedWidget

class SidebarManager(Ui_MainWindow):
    def __init__(self, buttons: list[QPushButton], stacked_widget: QStackedWidget):
        self.buttons = buttons
        self.stackedWidget = stacked_widget
        self.setup_page_connections()


    def setup_page_connections(self):
        for button in self.buttons:
            button.setCheckable(True)

        self.buttons[0].clicked.connect(self.show_home_page)
        self.buttons[1].clicked.connect(self.show_budgets_page)
        self.buttons[2].clicked.connect(self.show_transactions_page)
        self.buttons[3].clicked.connect(self.show_savings_page)

        self.show_home_page()

    def show_home_page(self):
        self.stackedWidget.setCurrentIndex(0)
        self.update_button_states(self.buttons[0])

    def show_budgets_page(self):
        self.stackedWidget.setCurrentIndex(1)
        self.update_button_states(self.buttons[1])

    def show_transactions_page(self):
        self.stackedWidget.setCurrentIndex(2)
        self.update_button_states(self.buttons[2])

    def show_savings_page(self):
        self.stackedWidget.setCurrentIndex(3)
        self.update_button_states(self.buttons[3])

    def update_button_states(self, active_button):
        for button in self.buttons:
            button.setChecked(button is active_button)