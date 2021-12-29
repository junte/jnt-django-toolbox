from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from test_proj.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("email",)

    USERNAME_FIELD = "email"

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()  # noqa: WPS110

    def __str__(self):
        """Text representation."""
        return self.email
