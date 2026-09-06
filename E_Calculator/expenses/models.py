from django.conf import settings
from django.db import models

from common.models.basemodel import BaseModel


class Category(BaseModel):
    CATEGORY_TYPE_CHOICES = [
        ("expense", "Expense"),
        ("income", "Income"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, default="expense")
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "name", "type")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.type})"


class Expense(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="expenses")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    expense_date = models.DateField()

    class Meta:
        ordering = ["-expense_date", "-created_at"]

    def __str__(self):
        return f"{self.title} - {self.amount}"


class RecurringExpense(BaseModel):
    FREQUENCY_CHOICES = [
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recurring_expenses")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="recurring_expenses")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["start_date", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.frequency})"


class Income(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="incomes")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="incomes")
    source = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    income_date = models.DateField()

    class Meta:
        ordering = ["-income_date", "-created_at"]

    def __str__(self):
        return f"{self.source} - {self.amount}"


class Budget(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="budgets")
    month = models.DateField()
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ("user", "category", "month")
        ordering = ["-month"]

    def __str__(self):
        return f"{self.category.name} - {self.limit_amount} for {self.month}"
