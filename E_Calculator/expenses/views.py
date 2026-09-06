from datetime import datetime

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Budget, Category, Expense, Income, RecurringExpense
from .reporting import get_budget_vs_spent_for_user, get_category_breakdown_for_user, get_monthly_summary_for_user
from .serializers import BudgetSerializer, CategorySerializer, ExpenseSerializer, IncomeSerializer, RecurringExpenseSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)

        category_id = self.request.query_params.get("category")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        search = self.request.query_params.get("search")
        sort = self.request.query_params.get("sort", "date_desc")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if start_date:
            queryset = queryset.filter(expense_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(expense_date__lte=end_date)

        if search:
            queryset = queryset.filter(title__icontains=search)

        if sort == "amount_asc":
            return queryset.order_by("amount", "-expense_date")
        if sort == "amount_desc":
            return queryset.order_by("-amount", "-expense_date")
        if sort == "date_asc":
            return queryset.order_by("expense_date", "-created_at")
        return queryset.order_by("-expense_date", "-created_at")


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class RecurringExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = RecurringExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)


class RecurringExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecurringExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)


class IncomeListCreateView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


class BudgetListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class MonthlySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        month_value = request.query_params.get("month")
        if not month_value:
            return Response({"detail": "month query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = datetime.strptime(month_value, "%Y-%m")
        except ValueError:
            return Response({"detail": "month must be in YYYY-MM format"}, status=status.HTTP_400_BAD_REQUEST)

        summary = get_monthly_summary_for_user(request.user, month)
        return Response(summary)


class CategoryBreakdownView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        month_value = request.query_params.get("month")
        if not month_value:
            return Response({"detail": "month query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = datetime.strptime(month_value, "%Y-%m")
        except ValueError:
            return Response({"detail": "month must be in YYYY-MM format"}, status=status.HTTP_400_BAD_REQUEST)

        breakdown = get_category_breakdown_for_user(request.user, month)
        return Response(breakdown)


class BudgetVsSpentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        month_value = request.query_params.get("month")
        if not month_value:
            return Response({"detail": "month query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = datetime.strptime(month_value, "%Y-%m")
        except ValueError:
            return Response({"detail": "month must be in YYYY-MM format"}, status=status.HTTP_400_BAD_REQUEST)

        data = get_budget_vs_spent_for_user(request.user, month)
        return Response(data)
