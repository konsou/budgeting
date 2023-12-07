from typing import Union

from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker

from expenses.models import Account, Category, Expense
from datetime import date
from decimal import Decimal


class BaseExpenseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(name="Test Account")
        self.category = Category.objects.create(name="Test Category")
        self.url = reverse("expenses")
        self.expense_json_data: dict[str, Union[str, int]] = {
            "date": date.today().isoformat(),
            "amount": "100.00",
            "account": self.account.id,
            "category": self.category.id,
            "recipient": "Test Recipient",
            "description": "Test Description",
        }

    def create_expense(self):
        return baker.make(
            Expense,
            date=self.expense_json_data["date"],
            amount=self.expense_json_data["amount"],
            account=self.account,
            category=self.category,
            recipient=self.expense_json_data["recipient"],
            description=self.expense_json_data["description"],
        )


class ExpenseCreateAPITests(BaseExpenseTestCase):
    def test_create_expense(self):
        response = self.client.post(
            self.url, self.expense_json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Expense.objects.filter(
                recipient=self.expense_json_data["recipient"]
            ).exists()
        )

    def test_create_expense_returns_correct_data(self):
        response = self.client.post(
            self.url, self.expense_json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        returned_expense = response.json()
        self.assertEqual(returned_expense["date"], self.expense_json_data["date"])
        self.assertEqual(
            Decimal(returned_expense["amount"]),
            Decimal(self.expense_json_data["amount"]),
        )
        self.assertEqual(returned_expense["account"], self.expense_json_data["account"])
        self.assertEqual(
            returned_expense["category"], self.expense_json_data["category"]
        )
        self.assertEqual(
            returned_expense["recipient"], self.expense_json_data["recipient"]
        )
        self.assertEqual(
            returned_expense["description"], self.expense_json_data["description"]
        )

    def test_create_expense_returns_valid_id(self):
        response = self.client.post(
            self.url, self.expense_json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        returned_expense = response.json()
        self.assertIsNotNone(returned_expense["id"])
        self.assertIsInstance(returned_expense["id"], int)
        self.assertTrue(Expense.objects.filter(id=returned_expense["id"]).exists())


class ExpenseListAPITests(BaseExpenseTestCase):
    def setUp(self):
        super().setUp()
        self.expenses = [self.create_expense() for _ in range(5)]

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
