from django.test import TestCase, Client
from django.urls import reverse

from expenses.models import Account, Category, Expense
from datetime import date
from decimal import Decimal


class ExpenseCreateAPITests(TestCase):
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
        self.url = reverse("expenses")

    def test_create_expense(self):
        response = self.client.post(
            self.url, self.expense_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Expense.objects.filter(recipient=self.expense_data["recipient"]).exists()
        )

    def test_create_expense_returns_correct_data(self):
        response = self.client.post(
            self.url, self.expense_data, content_type="application/json"
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
            self.url, self.expense_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        returned_expense = response.json()
        self.assertIsNotNone(returned_expense["id"])
        self.assertIsInstance(returned_expense["id"], int)
        self.assertTrue(Expense.objects.filter(id=returned_expense["id"]).exists())


class ExpenseListAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(name="Test Account")
        self.category = Category.objects.create(name="Test Category")
        self.expense_data = {
            "date": date.today().isoformat(),
            "amount": str(Decimal("100.00")),
            "account": self.account,
            "category": self.category,
            "recipient": "Test Recipient",
            "description": "Test Description",
        }
        self.expenses = [Expense.objects.create(**self.expense_data) for _ in range(5)]
        self.url = reverse("expenses")

    def test_list_expenses(self):
        response = self.client.get(self.url, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        returned_expenses = response.json()
        self.assertEqual(len(returned_expenses), len(self.expenses))

        for returned_expense in returned_expenses:
            self.assertIn("id", returned_expense)
            self.assertIn("date", returned_expense)
            self.assertIn("amount", returned_expense)
            self.assertIn("account", returned_expense)
            self.assertIn("category", returned_expense)
            self.assertIn("recipient", returned_expense)
            self.assertIn("description", returned_expense)
