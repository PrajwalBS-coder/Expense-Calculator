from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api.create_user import UserCreateView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
