from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from functools import partial
from uuid import uuid4
from common.models.basemodel import BaseModel
from django.utils.crypto import get_random_string
from django.utils import timezone


class UserManager(BaseUserManager["User"]):
    def create_user(
        self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )
        group, _ = Group.objects.get_or_create(name="Full Access")
        group.user_set.add(user)
        return user

    def staff(self):
        return self.get_queryset().filter(is_staff=True)
    

class User(
    PermissionsMixin, BaseModel, AbstractBaseUser
):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=True)
    last_confirm_email_request = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    last_password_reset_request = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to="user-avatars", blank=True, null=True)
    jwt_token_key = models.CharField(
        max_length=12, default=partial(get_random_string, length=12)
    )
    search_document = models.TextField(blank=True, default="")
    uuid = models.UUIDField(default=uuid4, unique=True)

    # Denormalized number of orders placed by the user
    number_of_orders = models.PositiveIntegerField(default=0, db_default=0)

    USERNAME_FIELD = "email"
    NEWLY_CREATED_USER = False

    objects = UserManager()

    class Meta:
        ordering = ("email",)
        indexes = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        # Override the default __str__ of AbstractUser that returns username, which may
        # lead to leaking sensitive data in logs.
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        return str(self.email) if self.email else "User"