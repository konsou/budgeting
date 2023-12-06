from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase
from expenses.models import Account, Category, Expense
from datetime import date


class ExpenseModelTests(TestCase):
    def setUp(self):
        # Set up the related objects and the Expense object for the tests
        self.account = Account.objects.create(name="Savings Account")
        self.category = Category.objects.create(name="Groceries")
        self.expense_date = date.today()
        self.expense_amount = 100.50
        self.expense_recipient = "Supermarket"
        self.expense_description = "Weekly groceries"

        self.expense = Expense.objects.create(
            date=self.expense_date,
            amount=self.expense_amount,
            account=self.account,
            category=self.category,
            recipient=self.expense_recipient,
            description=self.expense_description,
        )

    def test_create_expense(self):
        # Check if the Expense instance exists
        self.assertTrue(Expense.objects.filter(id=self.expense.id).exists())

    def test_delete_account_category(self):
        self.account.delete()
        self.category.delete()
        self.expense.refresh_from_db()
        self.assertIsNone(self.expense.account)
        self.assertIsNone(self.expense.category)

    def test_expense_fields(self):
        # Retrieve the instance to ensure all fields were saved correctly
        saved_expense = Expense.objects.get(id=self.expense.id)
        self.assertEqual(saved_expense.date, self.expense_date)
        self.assertEqual(saved_expense.amount, self.expense_amount)
        self.assertEqual(saved_expense.account, self.account)
        self.assertEqual(saved_expense.category, self.category)
        self.assertEqual(saved_expense.recipient, self.expense_recipient)
        self.assertEqual(saved_expense.description, self.expense_description)

    def test_string_representation(self):
        # The __str__ method could return a string that includes the date and amount, for example
        expected_representation = f"{self.expense_date} - {self.expense_amount}"
        self.assertEqual(str(self.expense), expected_representation)


class AccountModelTests(TestCase):
    def setUp(self):
        self.account_name = "Checking Account"
        self.account = Account.objects.create(name=self.account_name)

    def test_create_account(self):
        self.assertTrue(Account.objects.filter(name=self.account_name).exists())

    def test_account_name(self):
        self.assertEqual(self.account.name, self.account_name)

    def test_string_representation(self):
        self.assertEqual(str(self.account), self.account_name)


class CategoryModelTests(TestCase):
    def setUp(self):
        self.category_name = "Utilities"
        self.category = Category.objects.create(name=self.category_name)

    def test_create_category(self):
        self.assertTrue(Category.objects.filter(name=self.category_name).exists())

    def test_category_name(self):
        self.assertEqual(self.category.name, self.category_name)

    def test_string_representation(self):
        self.assertEqual(str(self.category), self.category_name)
