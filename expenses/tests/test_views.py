from django.test import TestCase, Client
from expenses.models import Account, Category, Expense
from datetime import date
from decimal import Decimal


class ExpenseAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(name="Test Account")
        self.category = Category.objects.create(name="Test Category")
        self.expense_data = {
            "date": date.today().isoformat(),
            "amount": str(Decimal("100.00")),
            "account": self.account.id,
            "category": self.category.id,
            "recipient": "Test Recipient",
            "description": "Test Description",
        }

    def test_create_expense(self):
        response = self.client.post(
            "/expenses", self.expense_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Expense.objects.filter(recipient=self.expense_data["recipient"]).exists()
        )
