from django.test import TestCase
from expenses.models import Account


class AccountModelTests(TestCase):
    def test_create_account(self):
        account = Account.objects.create(name="Checking Account")
        saved_account = Account.objects.get(id=account.id)
        self.assertEqual(saved_account.name, "Checking Account")

    def test_account_name(self):
        account = Account.objects.create(name="Savings Account")
        self.assertEqual(account.name, "Savings Account")

    def test_string_representation(self):
        account = Account(name="Emergency Fund")
        self.assertEqual(str(account), "Emergency Fund")
