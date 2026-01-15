from django.contrib import admin

# Register your models here.
from users.models.user_management import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User