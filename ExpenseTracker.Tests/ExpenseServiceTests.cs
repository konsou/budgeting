using Xunit;
using ExpenseTracker.Services;
using ExpenseTracker.Models;

public class ExpenseServiceTests
{
    [Fact]
    public void AddExpense_ShouldAddExpense_WhenValidData()
    {
        var expenseService = new ExpenseService();
        var expense = new Expense
        {
            Description = "Groceries",
            Amount = 50.00,
            Category = "Food"
        };

        expenseService.AddExpense(expense);

        Assert.Contains(expense, expenseService.GetExpenses());
    }
}