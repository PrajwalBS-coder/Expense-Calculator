from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from expenses.models import Category, Expense, RecurringExpense
from users.models.user_management import User


class ExpenseApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="securepass123",
            first_name="Test",
            last_name="User",
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(
            user=self.user,
            name="Food",
            type="expense",
        )

    def test_create_expense(self):
        url = reverse("expense-list-create")
        payload = {
            "category": self.category.id,
            "title": "Lunch",
            "description": "Office lunch",
            "amount": "50.00",
            "expense_date": "2026-09-01",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        expense = Expense.objects.get()
        self.assertEqual(expense.title, "Lunch")
        self.assertEqual(expense.category, self.category)
        self.assertEqual(response.data["category"], self.category.id)
        self.assertEqual(response.data["category_name"], "Food")

    def test_expense_cannot_use_another_users_category(self):
        other_user = User.objects.create_user(
            email="other@example.com",
            password="securepass123",
            first_name="Other",
            last_name="User",
        )
        other_category = Category.objects.create(
            user=other_user,
            name="Travel",
            type="expense",
        )

        response = self.client.post(
            reverse("expense-list-create"),
            {
                "category": str(other_category.id),
                "title": "Flight",
                "amount": "300.00",
                "expense_date": "2026-09-02",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Expense.objects.count(), 0)

    def test_categories_can_be_filtered_by_type(self):
        Category.objects.create(user=self.user, name="Salary", type="income")

        response = self.client.get(reverse("category-list-create"), {"type": "expense"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([category["name"] for category in response.data], ["Food"])

    def test_list_expenses_for_authenticated_user(self):
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Groceries",
            amount="120.50",
            expense_date=date(2026, 9, 3),
        )

        response = self.client.get(reverse("expense-list-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Groceries")

    def test_user_sees_only_own_expenses(self):
        other_user = User.objects.create_user(
            email="other@example.com",
            password="securepass123",
            first_name="Other",
            last_name="User",
        )
        other_category = Category.objects.create(
            user=other_user,
            name="Travel",
            type="expense",
        )
        Expense.objects.create(
            user=other_user,
            category=other_category,
            title="Flight",
            amount="300.00",
            expense_date=date(2026, 9, 2),
        )

        response = self.client.get(reverse("expense-list-create"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_expense_list_filters_by_category_and_date_range(self):
        other_category = Category.objects.create(
            user=self.user,
            name="Travel",
            type="expense",
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Lunch",
            amount="50.00",
            expense_date=date(2026, 9, 1),
        )
        Expense.objects.create(
            user=self.user,
            category=other_category,
            title="Train ticket",
            amount="80.00",
            expense_date=date(2026, 9, 15),
        )

        response = self.client.get(
            reverse("expense-list-create"),
            {
                "category": str(self.category.id),
                "start_date": "2026-09-01",
                "end_date": "2026-09-10",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Lunch")

    def test_expense_list_supports_search_and_sort(self):
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Office lunch",
            amount="50.00",
            expense_date=date(2026, 9, 1),
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Groceries",
            amount="100.00",
            expense_date=date(2026, 9, 12),
        )

        response = self.client.get(
            reverse("expense-list-create"),
            {"search": "lunch", "sort": "amount_desc"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Office lunch")

        response = self.client.get(reverse("expense-list-create"), {"sort": "amount_desc"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Groceries")
        self.assertEqual(response.data[1]["title"], "Office lunch")

    def test_recurring_expense_can_be_created_and_validates_dates(self):
        response = self.client.post(
            reverse("recurring-expense-list-create"),
            {
                "category": str(self.category.id),
                "title": "Rent",
                "amount": "1200.00",
                "frequency": "monthly",
                "start_date": "2026-09-01",
                "end_date": "2027-08-31",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["frequency"], "monthly")
        self.assertTrue(RecurringExpense.objects.filter(user=self.user, title="Rent").exists())

        response = self.client.post(
            reverse("recurring-expense-list-create"),
            {
                "title": "Invalid schedule",
                "amount": "10.00",
                "frequency": "weekly",
                "start_date": "2026-09-10",
                "end_date": "2026-09-01",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_monthly_summary_uses_authenticated_user_only(self):
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Lunch",
            amount="50.00",
            expense_date=date(2026, 9, 1),
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Dinner",
            amount="25.00",
            expense_date=date(2026, 9, 10),
        )

        response = self.client.get(reverse("monthly-summary"), {"month": "2026-09"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_expenses"], "75.00")
        self.assertEqual(response.data["total_income"], "0.00")
        self.assertEqual(response.data["net_balance"], "-75.00")

    def test_category_breakdown_returns_user_data(self):
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Lunch",
            amount="50.00",
            expense_date=date(2026, 9, 1),
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Dinner",
            amount="25.00",
            expense_date=date(2026, 9, 10),
        )

        response = self.client.get(reverse("category-breakdown"), {"month": "2026-09"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["category_name"], "Food")
        self.assertEqual(response.data[0]["total_expense"], "75.00")
