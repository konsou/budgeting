namespace ExpenseTracker.Services
{
    public class ExpenseService
    {
        private System.Collections.Generic.List<ExpenseTracker.Models.Expense> _expenses;
        public ExpenseService()
        {
            _expenses = [];
        }

        public void AddExpense(ExpenseTracker.Models.Expense expense)
        {
            _expenses.Add(expense);
        }

        public System.Collections.Generic.List<ExpenseTracker.Models.Expense> GetExpenses()
        {
            return _expenses;
        }
    }
}