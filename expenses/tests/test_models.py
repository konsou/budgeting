from django.test import TestCase
from expenses.models import Account
from expenses.models import Category


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
