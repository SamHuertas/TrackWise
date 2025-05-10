from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from src.models.expense_model import ExpenseModel
from src.views.widgets.transaction_action_buttons import TransactionActionButtons

class TransactionManagementController(QWidget):
    transaction_deleted = pyqtSignal(int)  # Signal emitted when a transaction is deleted

    def __init__(self, main_window, budget_model):
        super().__init__()
        self.main_window = main_window
        self.budget_model = budget_model
        self.expense_model = ExpenseModel()
        self.current_page = 1
        self.items_per_page = 10
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

    def filter_transactions(self, transactions):
        # Get filter parameters
        filter_date = self.main_window.TransactionDate.date()
        category = self.main_window.CategoriesSelect.currentText()
        search_text = self.main_window.SearchTransac.text().lower()
        
        # Apply filters
        filtered_transactions = []
        for transaction in transactions:
            transaction_date = QDate.fromString(str(transaction['Date']), Qt.DateFormat.ISODate)
            if (category == "All Categories" or transaction['Category'] == category) and \
               (not search_text or search_text in transaction['Description'].lower()):
                filtered_transactions.append(transaction)
        
        # Sort transactions by date (most recent first)
        filtered_transactions.sort(key=self.sort_by_date, reverse=True)
        return filtered_transactions

    def load_transactions(self):
        table = self.main_window.TransactionTable
        table.setRowCount(0)
        transactions = self.expense_model.get_all_transactions()
        transactions.sort(key=self.sort_by_date)
        
        # Calculate pagination
        total_items = len(transactions)
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, total_items)
        
        # Update page indicator
        self.main_window.ItemIndic.setText(f"Showing {start_idx + 1}-{end_idx} of {total_items} transactions")
        self.main_window.Page.setText(f"Page {self.current_page}")
        
        # Enable/disable pagination buttons
        self.main_window.PrevPage.setEnabled(self.current_page > 1)
        self.main_window.NextPage.setEnabled(self.current_page < total_pages)
        
        # Display transactions for current page
        for row, transaction in enumerate(transactions[start_idx:end_idx]):
            table.insertRow(row)
            
            # Date
            transaction_date = QDate.fromString(str(transaction['Date']), Qt.DateFormat.ISODate)
            date_str = transaction_date.toString("MMM dd, yyyy")
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setForeground(QtGui.QColor("#333333"))
            table.setItem(row, 0, date_item)
            
            # Category
            category_item = QTableWidgetItem(transaction['Category'])
            category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            category_color = self.category_color_mapping().get(transaction['Category'], "#9E9E9E")
            category_item.setForeground(QtGui.QColor(category_color))
            table.setItem(row, 1, category_item)
            
            # Description
            description_item = QTableWidgetItem(transaction['Description'])
            description_item.setForeground(QtGui.QColor("#333333"))
            table.setItem(row, 2, description_item)
            
            # Amount
            amount_item = QTableWidgetItem(f"-₱{transaction['Amount']:.2f}")
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            amount_item.setForeground(QtGui.QColor("#f44336"))  # Red color for expenses
            table.setItem(row, 3, amount_item)
            
            # Actions
            action_buttons = TransactionActionButtons(transaction['ExpensesID'])
            action_buttons.delete_transaction_requested.connect(self.delete_transaction)
            table.setCellWidget(row, 4, action_buttons)

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_transactions()

    def next_page(self):
        total_items = len(self.expense_model.get_all_transactions())
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_transactions()

    def handle_expense_added(self, budget_id):
        self.load_transactions()
        self.transaction_deleted.emit(budget_id)

    def delete_transaction(self, transaction_id):
        reply = QMessageBox.question(
            self.main_window,
            "Delete Transaction",
            "Are you sure you want to delete this transaction?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.expense_model.delete_expense(transaction_id)
            self.load_transactions()
            self.transaction_deleted.emit(transaction_id) 