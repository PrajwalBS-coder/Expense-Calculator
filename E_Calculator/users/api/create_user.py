from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from ..serializers import UserCreateSerializer
from ..models.user_management import User

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Create a new user.",
        responses={201: UserCreateSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
