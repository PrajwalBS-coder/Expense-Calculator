from django.urls import path

from .views import (
    BudgetDetailView,
    BudgetListCreateView,
    BudgetVsSpentView,
    CategoryBreakdownView,
    CategoryDetailView,
    CategoryListCreateView,
    ExpenseDetailView,
    ExpenseListCreateView,
    IncomeDetailView,
    IncomeListCreateView,
    MonthlySummaryView,
    RecurringExpenseDetailView,
    RecurringExpenseListCreateView,
)

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<uuid:id>/", CategoryDetailView.as_view(), name="category-detail"),
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list-create"),
    path("expenses/<uuid:id>/", ExpenseDetailView.as_view(), name="expense-detail"),
    path("recurring-expenses/", RecurringExpenseListCreateView.as_view(), name="recurring-expense-list-create"),
    path("recurring-expenses/<uuid:id>/", RecurringExpenseDetailView.as_view(), name="recurring-expense-detail"),
    path("income/", IncomeListCreateView.as_view(), name="income-list-create"),
    path("income/<uuid:id>/", IncomeDetailView.as_view(), name="income-detail"),
    path("budgets/", BudgetListCreateView.as_view(), name="budget-list-create"),
    path("budgets/<uuid:id>/", BudgetDetailView.as_view(), name="budget-detail"),
    path("reports/monthly-summary/", MonthlySummaryView.as_view(), name="monthly-summary"),
    path("reports/category-breakdown/", CategoryBreakdownView.as_view(), name="category-breakdown"),
    path("reports/budget-vs-spent/", BudgetVsSpentView.as_view(), name="budget-vs-spent"),
]
