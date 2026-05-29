from uuid import uuid4
from django.contrib.auth.models import (

    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,

)

from django.db import models

class UserManager(BaseUserManager):

    """
    Custom manager responsible for creating
    regular users and superusers.
    """
    def create_user(
        self,
        email,
        name,
        date_of_birth,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError(
                "An email address is required."
            )
        normalized_email = self.normalize_email(email)
        user = self.model(
            email=normalized_email,
            name=name,
            date_of_birth=date_of_birth,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(
        self,
        email,
        name,
        date_of_birth,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )
        return self.create_user(
            email,
            name,
            date_of_birth,
            password,
            **extra_fields,
        )

class User(AbstractBaseUser, PermissionsMixin):

    """
    Custom user model that uses email instead
    of username for authentication.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(
        unique=True
    )
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(

        auto_now=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
        "date_of_birth",
    ]
    
    def __str__(self):
        return self.email