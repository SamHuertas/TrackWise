from src.database.db_manager import DBManager
from datetime import date

class SavingsModel:
    def __init__(self):
        self.db = DBManager()

    def add_savings_goal(self, date: date, name: str, goal_amount: float):
        # Add a new savings goal to the database
        if goal_amount < 0:
            return False
        self.db.execute(
            "INSERT INTO Savings (Date, Name, `Goal Amount`) VALUES (%s, %s, %s)",
            (date, name, goal_amount)
        )

    def add_deposit(self, budget_id: int, savings_id: int, date: date, amount: float):
        # Add a new deposit to the database
        if amount <= 0:
            return False
        self.db.execute(
            "INSERT INTO Deposits (BudgetID, SavingsID, Date, Amount) VALUES (%s, %s, %s, %s)",
            (budget_id, savings_id, date, amount)
        )

    def delete_savings_goal(self, savings_id: int):
        # Delete a savings goal and its associated deposits
        self.db.execute("DELETE FROM Deposits WHERE SavingsID = %s", (savings_id,))
        self.db.execute("DELETE FROM Savings WHERE SavingsID = %s", (savings_id,))

    def get_savings_goal(self, savings_id: int):
        # Retrieve a savings goal by its ID
        return self.db.fetchone("SELECT * FROM Savings WHERE SavingsID = %s", (savings_id,))

    def get_all_savings_goals(self):
        # Retrieve all savings goals
        return self.db.fetchall("SELECT * FROM Savings ORDER BY Date DESC")

    def get_deposits_for_savings(self, savings_id: int):
        # Retrieve all deposits for a specific savings goal
        return self.db.fetchall("SELECT * FROM Deposits WHERE SavingsID = %s", (savings_id,))

    def get_total_deposits_for_savings(self, savings_id: int):
        # Get total amount deposited for a savings goal
        result = self.db.fetchone("SELECT SUM(Amount) FROM Deposits WHERE SavingsID = %s", (savings_id,))
        return result[0] or 0

    def get_savings_summary(self, savings_id: int):
        # Get a summary of a savings goal including total deposits
        result = self.db.fetchone("""
            SELECT 
                s.SavingsID,
                s.Date,
                s.Name,
                s.`Goal Amount`,
                COALESCE(SUM(d.Amount), 0) as TotalDeposits,
                s.`Goal Amount` - COALESCE(SUM(d.Amount), 0) as RemainingAmount
            FROM 
                Savings s
            LEFT JOIN 
                Deposits d ON s.SavingsID = d.SavingsID
            WHERE 
                s.SavingsID = %s
            GROUP BY 
                s.SavingsID, s.Date, s.Name, s.`Goal Amount`
        """, (savings_id,))
        return result if result else None

    def get_all_savings_summaries(self):
        # Get summaries for all savings goals including total deposits
        return self.db.fetchall("""
            SELECT 
                s.SavingsID,
                s.Date,
                s.Name,
                s.`Goal Amount`,
                COALESCE(SUM(d.Amount), 0) as TotalDeposits,
                s.`Goal Amount` - COALESCE(SUM(d.Amount), 0) as RemainingAmount
            FROM 
                Savings s
            LEFT JOIN 
                Deposits d ON s.SavingsID = d.SavingsID
            GROUP BY 
                s.SavingsID, s.Date, s.Name, s.`Goal Amount`
            ORDER BY 
                s.Date DESC
        """)

    def update_savings_goal(self, savings_id: int, name: str = None, goal_amount: float = None, 
                          date: date = None):
        # Update a savings goal's details
        updates = []
        params = []
        
        if name is not None:
            updates.append("Name = %s")
            params.append(name)
        if goal_amount is not None:
            updates.append("`Goal Amount` = %s")
            params.append(goal_amount)
        if date is not None:
            updates.append("Date = %s")
            params.append(date)
            
        if updates:
            query = f"UPDATE Savings SET {', '.join(updates)} WHERE SavingsID = %s"
            params.append(savings_id)
            self.db.execute(query, tuple(params))

    def delete_deposit(self, deposit_id: int):
        # Delete a specific deposit
        self.db.execute("DELETE FROM Deposits WHERE DepositsID = %s", (deposit_id,)) 