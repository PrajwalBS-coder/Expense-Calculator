from rest_framework import serializers

from .models import Budget, Category, Expense, Income, RecurringExpense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "type", "description", "user"]
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ExpenseSerializer(serializers.ModelSerializer):
    category=serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Expense
        fields = ["id", "user", "category", "title", "description", "amount", "expense_date"]
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class RecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = ["id", "user", "category", "title", "description", "amount", "frequency", "start_date", "end_date", "is_active"]
        read_only_fields = ["id", "user"]

    def validate(self, attrs):
        if attrs.get("end_date") and attrs["end_date"] < attrs["start_date"]:
            raise serializers.ValidationError({"end_date": "End date must be on or after start date."})
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["id", "user", "category", "source", "description", "amount", "income_date"]
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "user", "category", "month", "limit_amount"]
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
