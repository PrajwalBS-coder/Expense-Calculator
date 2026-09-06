from decimal import Decimal
from django.db.models import Sum

from .models import Budget, Expense, Income


def get_monthly_summary_for_user(user, month):
    expense_total = Expense.objects.filter(user=user, expense_date__month=month.month, expense_date__year=month.year).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    income_total = Income.objects.filter(user=user, income_date__month=month.month, income_date__year=month.year).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    return {
        "month": month.strftime("%Y-%m"),
        "total_expenses": str(expense_total),
        "total_income": str(income_total),
        "net_balance": str(income_total - expense_total),
    }


def get_category_breakdown_for_user(user, month):
    items = Expense.objects.filter(user=user, expense_date__month=month.month, expense_date__year=month.year).values("category__name").annotate(total_expense=Sum("amount")).order_by("-total_expense")

    return [
        {
            "category_name": item["category__name"],
            "total_expense": str(item["total_expense"]),
        }
        for item in items
    ]


def get_budget_vs_spent_for_user(user, month):
    budget_rows = []
    budgets = Budget.objects.filter(user=user, month__month=month.month, month__year=month.year).select_related("category")

    for budget in budgets:
        spent = Expense.objects.filter(
            user=user,
            category=budget.category,
            expense_date__month=month.month,
            expense_date__year=month.year,
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        budget_rows.append(
            {
                "category_name": budget.category.name,
                "budget_limit": str(budget.limit_amount),
                "total_spent": str(spent),
                "remaining": str(budget.limit_amount - spent),
                "percent_used": str((spent / budget.limit_amount * Decimal("100")) if budget.limit_amount else Decimal("0.00")),
            }
        )

    return budget_rows
