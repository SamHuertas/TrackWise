from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from src.views.widgets.transaction_action_buttons import TransactionActionButtons
from src.views.edit_transaction_window import EditTransactionWindow
import math

class TransactionManagementController(QWidget):
    def __init__(self, main_window, expense_model):
        super().__init__()
        self.main_window = main_window
        self.expense_model = expense_model
        self.current_page = 1
        self.items_per_page = 10
        self.main_window.TransactionDate.setMinimumDate(QDate(2025, 1, 1))
        self.main_window.TransactionDate.setSpecialValueText("Select a Date")
        self.main_window.TransactionDate.setDate(self.main_window.TransactionDate.minimumDate())
        self.main_window.TransactionDate.dateChanged.connect(self.on_date_changed)
        self.setup_table()
        self.setup_categories()
        self.load_transactions()

    def setup_table(self):
        table = self.main_window.TransactionTable
        table.setColumnCount(5)
        
        headers = ["Date", "Category", "Description", "Amount", "Actions"]
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setHighlightSections(False)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setFixedHeight(40)
        table.verticalHeader().setDefaultSectionSize(40)
        table.setShowGrid(False)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)

    def setup_categories(self):
        categories = ["All Categories", "Entertainment", "Food", "Groceries", "Healthcare", "Housing", "Shopping", "Transportation", "Utilities", "Other"]
        self.main_window.CategoriesSelect.clear()
        self.main_window.CategoriesSelect.setPlaceholderText("Select a Category")
        self.main_window.CategoriesSelect.addItems(categories)
        self.main_window.CategoriesSelect.setCurrentIndex(-1)

    def category_color_mapping(self):
        return {
            "Entertainment": "#f44336",
            "Food": "#4a86e8",
            "Groceries": "#4CAF50",
            "Healthcare": "#9C27B0",
            "Housing": "#FF9800",   
            "Shopping": "#FFEB3B",
            "Transportation": "#FF5722",
            "Utilities": "#00BCD4",
            "Other": "#9E9E9E"
        }

    def sort_by_date(self, transaction):
        # Parse the date string from the database (format: YYYY-MM-DD)
        date_str = str(transaction['Date'])
        year, month, day = map(int, date_str.split('-'))
        return (year, month, day)

    def filter_by_category(self, transactions):
        category = self.main_window.CategoriesSelect.currentText()

        if not category:
            category = "All Categories"

        filtered_transactions = []
        for transaction in transactions:
            if category == "All Categories" or category == transaction['Category']:
                filtered_transactions.append(transaction)
        
        return filtered_transactions

    def filter_by_date(self, transactions):
        selected_date = self.main_window.TransactionDate.date()
        # If date is minimum date (placeholder), show all transactions
        if selected_date == self.main_window.TransactionDate.minimumDate():
            return transactions
            
        filtered_transactions = []
        for transaction in transactions:
            # Convert transaction date string to QDate
            transaction_date = QDate.fromString(str(transaction['Date']), Qt.DateFormat.ISODate)
            # Compare year, month, and day separately to ensure exact date match
            if (transaction_date.year() == selected_date.year() and 
                transaction_date.month() == selected_date.month() and 
                transaction_date.day() == selected_date.day()):
                filtered_transactions.append(transaction)
                
        return filtered_transactions

    def load_transactions(self):
        table = self.main_window.TransactionTable
        table.clearContents()
        table.setRowCount(0)

        # Get transactions and apply filters
        transactions = self.expense_model.get_all_transactions()
        if not transactions:
            return
        
        # Apply filters and sort
        filtered_transactions = self.filter_by_date(self.filter_by_category(transactions))
        filtered_transactions.sort(key=self.sort_by_date)
        
        # Calculate pagination
        total_items = len(filtered_transactions)
        total_pages = math.ceil(total_items / self.items_per_page)
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, total_items)
        
        # Update page info
        self.main_window.ItemIndic.setText(f"Showing {start_idx + 1}-{end_idx} of {total_items} transactions")
        self.main_window.Page.setText(f"Page {self.current_page}")
        self.main_window.PrevPage.setEnabled(self.current_page > 1)
        self.main_window.NextPage.setEnabled(self.current_page < total_pages)
        
        # Display current page
        table.setRowCount(end_idx - start_idx)
        for row, transaction in enumerate(filtered_transactions[start_idx:end_idx]):
            # Date
            date_str = QDate.fromString(str(transaction['Date']), Qt.DateFormat.ISODate).toString("MMM dd, yyyy")
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setForeground(QtGui.QColor("#333333"))
            table.setItem(row, 0, date_item)
            
            # Category
            category_item = QTableWidgetItem(transaction['Category'])
            category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            category_item.setForeground(QtGui.QColor(self.category_color_mapping().get(transaction['Category'], "#9E9E9E")))
            table.setItem(row, 1, category_item)
            
            # Description
            description_item = QTableWidgetItem(transaction['Description'])
            description_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            description_item.setForeground(QtGui.QColor("#333333"))
            table.setItem(row, 2, description_item)
            
            # Amount
            amount_item = QTableWidgetItem(f"-₱{transaction['Amount']:.2f}")
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            amount_item.setForeground(QtGui.QColor("#f44336"))
            table.setItem(row, 3, amount_item)
            
            # Actions
            action_buttons = TransactionActionButtons(transaction['ExpensesID'])
            action_buttons.delete_transaction_requested.connect(self.delete_transaction)
            action_buttons.edit_transaction_requested.connect(self.edit_transaction)
            table.setCellWidget(row, 4, action_buttons)

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_transactions()

    def next_page(self):
        total_items = len(self.expense_model.get_all_transactions())
        total_pages = math.ceil(total_items / self.items_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_transactions()

    def delete_transaction(self, transaction_id):
        reply = QMessageBox.question(
            self.main_window,
            "Delete Transaction",
            "Are you sure you want to delete this transaction?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Get the transaction to find its budget ID before deleting
            transaction = self.expense_model.get_expense(transaction_id)
            if transaction:
                budget_id = transaction['BudgetID']
                self.expense_model.delete_expense(transaction_id)
                
                self.load_transactions()
                
                self.main_window.dashboard_controller.refresh_dashboard()
                self.main_window.budget_controller.load_budget_data()
                self.main_window.dashboard_controller.load_recent_transactions()

    def edit_transaction(self, transaction_id):
        transaction = self.expense_model.get_expense(transaction_id)
        edit_window = EditTransactionWindow(self.main_window, transaction)
        edit_window.exec()
        if edit_window.result() == QtWidgets.QDialog.DialogCode.Accepted:
            self.load_transactions()
            
            # Update dashboard and budget data
            self.main_window.dashboard_controller.refresh_dashboard()
            self.main_window.budget_controller.load_budget_data()
            self.main_window.dashboard_controller.load_recent_transactions()

    def on_date_changed(self, date):
        self.current_page = 1  
        self.load_transactions()

    def on_filter_clicked(self):
        self.current_page = 1  
        self.load_transactions()
        self.main_window.CategoriesSelect.setCurrentIndex(-1)
        self.main_window.TransactionDate.setDate(self.main_window.TransactionDate.minimumDate())



            
            

