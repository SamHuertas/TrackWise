from src.database.db_manager import DBManager
from datetime import date

class ExpenseModel:
    def __init__(self):
        self.db = DBManager()

    def add_expense(self, budget_id: int, amount: float, category: str, description: str, date: date):
        # Add a new expense entry to the database

        self.db.execute( "INSERT INTO Expenses (BudgetID, Amount, Category, Description, Date) VALUES (%s, %s, %s, %s, %s)",(budget_id, amount, category, description, date))

    def delete_expense(self, expense_id: int):
        # Delete an expense entry from the database
        self.db.execute("DELETE FROM Expenses WHERE ExpensesID = %s", (expense_id,))

    def get_expense(self, expense_id: int):
        # Retrieve an expense entry from the database
        return self.db.fetchone("SELECT * FROM Expenses WHERE ExpensesID = %s", (expense_id,))

    def get_expenses_by_budgetid(self, budget_id: int):
        # Retrieve all expenses for a specific budget
        return self.db.fetchall("SELECT * FROM Expenses WHERE BudgetID = %s", (budget_id,))

    def get_expenses_by_month(self, month: int, year: int):
        # Retrieve all expenses for a specific month and year
        return self.db.fetchall("SELECT * FROM Expenses WHERE MONTH(Date) = %s AND YEAR(Date) = %s", (month, year))

    def get_expenses_by_current_week(self):
        # Get all expenses for the current week
        return self.db.fetchall("SELECT * FROM Expenses WHERE YEARWEEK(Date, 1) = YEARWEEK(CURDATE(), 1)")

    def get_all_expenses(self, budget_id: int):
        # Get all expenses for a specific budget
        return self.db.fetchall("SELECT * FROM Expenses WHERE BudgetID = %s", (budget_id,))

    def get_expenses_by_date_range(self, start_date, end_date, budget_id: int):
        # Get expenses within a date range for a specific budget
        return self.db.fetchall("SELECT * FROM Expenses WHERE Date BETWEEN %s AND %s AND BudgetID = %s", (start_date, end_date, budget_id))

    def get_expenses_by_category(self, category: str, budget_id: int):
        # Get expenses by category for a specific budget
        return self.db.fetchall("SELECT * FROM Expenses WHERE Category = %s AND BudgetID = %s", (category, budget_id))

    def get_total_expenses(self, budget_id: int):
        # Get total expenses for a specific budget
        result = self.db.fetchone("SELECT SUM(Amount) as total FROM Expenses WHERE BudgetID = %s", (budget_id,))
        return result['total'] if result and result['total'] is not None else 0

    def get_all_transactions(self):
        # Get all transactions ordered by date (most recent first)
        return self.db.fetchall("SELECT ExpensesID, Date, Category, Description, Amount FROM Expenses ORDER BY Date DESC")
     
    def update_expense(self, expense_id: int, amount: float, category: str, description: str):
        # Update an existing expense entry
        self.db.execute("UPDATE Expenses SET Amount = %s, Category = %s, Description = %s WHERE ExpensesID = %s", (amount, category, description, expense_id))

    def get_top5_expenses(self):
        # Get the top 5 most recently added expenses by ordering by ExpensesID
        return self.db.fetchall("SELECT * FROM Expenses ORDER BY ExpensesID DESC LIMIT 5")
    
    def get_expenses_by_budget(self, budget_id: int):
        """Get all expenses for a specific budget grouped by category"""
        return self.db.fetchall("""
            SELECT Category, SUM(Amount) as Amount 
            FROM Expenses 
            WHERE BudgetID = %s
            GROUP BY Category
            ORDER BY Amount DESC
        """, (budget_id,))
    
    def get_expenses_by_budget_this_week(self, budget_id: int):
        """Get expenses for current week grouped by category for a specific budget"""
        return self.db.fetchall("""
            SELECT Category, SUM(Amount) as Amount 
            FROM Expenses 
            WHERE BudgetID = %s AND YEARWEEK(Date, 1) = YEARWEEK(CURDATE(), 1)
            GROUP BY Category
            ORDER BY Amount DESC
        """, (budget_id,))

    def get_expenses_by_budget_today(self, budget_id: int):
        """Get expenses for current day grouped by category for a specific budget"""
        return self.db.fetchall("""
            SELECT Category, SUM(Amount) as Amount 
            FROM Expenses 
            WHERE BudgetID = %s AND DATE(Date) = CURDATE()
            GROUP BY Category
            ORDER BY Amount DESC
        """, (budget_id,))