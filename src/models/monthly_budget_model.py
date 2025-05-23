from src.database.db_manager import DBManager

class MonthlyBudgetModel:
    def __init__(self):
        self.db = DBManager()

    def add_budget(self, amount: float, month: int, year: int):
        # Add a new budget entry to the database
        if amount <= 0 or month < 1 or month > 12:
            return False
        self.db.execute("INSERT INTO MonthlyBudget (amount, month, year) VALUES (%s, %s, %s)", (amount, month, year))

    def get_budget_by_id(self, budget_id: int):
        # Retrieve a budget entry by its ID
        result = self.db.fetchone("SELECT * FROM MonthlyBudget WHERE BudgetID = %s", (budget_id,))
        return result if result else None

    def get_budget_for_month(self, month: int, year: int):
        # Retrieve the budget for a specific month and year
        result = self.db.fetchone("SELECT * FROM MonthlyBudget WHERE month = %s AND year = %s", (month, year))
        return result if result else None
    
    def delete_budget(self, budget_id: int):
        # Delete a budget entry for a specific id
        expenses_count = len(self.db.fetchall("SELECT * FROM Expenses WHERE BudgetID = %s", (budget_id,)))
        deposits_count = len(self.db.fetchall("SELECT * FROM Deposits WHERE BudgetID = %s", (budget_id,)))

        if expenses_count > 0 or deposits_count > 0:
            print("Cannot delete budget entry with associated expenses or deposits.")
            return False

        self.db.execute("DELETE FROM MonthlyBudget WHERE BudgetID = %s", (budget_id,))
        print(f"Budget entry with ID {budget_id} deleted.")
        return True

    def budget_exists(self, month, year):
        # Check if a budget entry exists for a specific month and year
        result = self.db.fetchall("SELECT * FROM MonthlyBudget WHERE month = %s AND year = %s", (month, year))
        if result:
            return True
        return False
    
    def get_budget_summary(self, budget_id: int):
        # Retrieve a summary of a budget entry by its ID
        result = self.db.fetchone("""
            SELECT 
                mb.BudgetID, 
                mb.Month, 
                mb.Year, 
                mb.Amount AS BudgetAmount,
                (SELECT COALESCE(SUM(Amount), 0) FROM Expenses WHERE BudgetID = mb.BudgetID) AS TotalExpenses,
                (SELECT COALESCE(SUM(Amount), 0) FROM Deposits WHERE BudgetID = mb.BudgetID) AS TotalDeposits,
                mb.Amount - 
                (SELECT COALESCE(SUM(Amount), 0) FROM Expenses WHERE BudgetID = mb.BudgetID) -
                (SELECT COALESCE(SUM(Amount), 0) FROM Deposits WHERE BudgetID = mb.BudgetID) AS Remaining
            FROM MonthlyBudget mb
            WHERE mb.BudgetID = %s
        """, (budget_id,))
        return result if result else None
    
    def get_all_budget_summary(self):
        return self.db.fetchall("""
            SELECT 
                mb.BudgetID, 
                mb.Month, 
                mb.Year, 
                mb.Amount AS BudgetAmount,
                (SELECT COALESCE(SUM(Amount), 0) FROM Expenses WHERE BudgetID = mb.BudgetID) AS TotalExpenses,
                (SELECT COALESCE(SUM(Amount), 0) FROM Deposits WHERE BudgetID = mb.BudgetID) AS TotalDeposits,
                mb.Amount - 
                (SELECT COALESCE(SUM(Amount), 0) FROM Expenses WHERE BudgetID = mb.BudgetID) -
                (SELECT COALESCE(SUM(Amount), 0) FROM Deposits WHERE BudgetID = mb.BudgetID) AS Remaining
            FROM MonthlyBudget mb
            ORDER BY mb.Year DESC, mb.Month DESC
        """)

    def get_month_name(self, month: int):
        # Retrieve the name of a month by its number
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return month_names[month - 1] if 1 <= month <= 12 else None
    
    def get_budget_id_by_month_year(self, month: int, year: int):
        # Retrieve the budget ID for a specific month and year
        result = self.db.fetchone("SELECT BudgetID FROM MonthlyBudget WHERE Month = %s AND Year = %s", (month, year))
        return result['BudgetID'] if result else None
    
    def update_budget(self, budget_id: int, amount: float):
        # Update the budget amount for a specific budget ID
        self.db.execute("UPDATE MonthlyBudget SET Amount = %s WHERE BudgetID = %s", (amount, budget_id))
        return True