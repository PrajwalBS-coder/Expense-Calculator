from django.urls import path
from .api.create_user import UserCreateView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user-create'),
]
