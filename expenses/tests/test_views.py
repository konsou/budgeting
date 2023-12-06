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
            "/api/v1/expenses", self.expense_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Expense.objects.filter(recipient=self.expense_data["recipient"]).exists()
        )

    def test_create_expense_returns_correct_data(self):
        response = self.client.post(
            "/api/v1/expenses", self.expense_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        returned_expense = response.json()
        self.assertEqual(returned_expense["date"], self.expense_data["date"])
        self.assertEqual(
            Decimal(returned_expense["amount"]), Decimal(self.expense_data["amount"])
        )
        self.assertEqual(returned_expense["account"], self.expense_data["account"])
        self.assertEqual(returned_expense["category"], self.expense_data["category"])
        self.assertEqual(returned_expense["recipient"], self.expense_data["recipient"])
        self.assertEqual(
            returned_expense["description"], self.expense_data["description"]
        )

    def test_create_expense_returns_valid_id(self):
        response = self.client.post(
            "/api/v1/expenses", self.expense_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        returned_expense = response.json()
        self.assertIsNotNone(returned_expense["id"])
        self.assertIsInstance(returned_expense["id"], int)
        self.assertTrue(Expense.objects.filter(id=returned_expense["id"]).exists())
