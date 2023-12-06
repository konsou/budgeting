from django.db import models
from decimal import Decimal
from datetime import date


class Account(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expense(models.Model):
    date = models.DateField(default=date.today)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    account = models.ForeignKey(
        Account, null=True, blank=False, on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        Category, null=True, blank=False, on_delete=models.SET_NULL
    )
    recipient = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} - {self.amount}"
