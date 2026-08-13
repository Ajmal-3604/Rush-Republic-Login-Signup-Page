import re

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models


def validate_contact_number(value):
    """Simple validator: 10-15 digits, optional leading +."""
    if not re.match(r'^\+?\d{10,15}$', value):
        raise ValidationError('Enter a valid contact number (10-15 digits, optional leading +).')


class CustomUserManager(BaseUserManager):
    """Manager for CustomUser where email is the unique login identifier."""

    def create_user(self, username, email, department, contact, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field is required')
        if not username:
            raise ValueError('The Username field is required')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            department=department,
            contact=contact,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, contact, password=None, **extra_fields):
        extra_fields.setdefault('department', CustomUser.Department.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, extra_fields.pop('department'), contact, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model for the Rush Republic Employee Management Portal."""

    class Department(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        SOCIAL_MEDIA = 'SOCIAL_MEDIA', 'Social Media'
        PRODUCTION_COORDINATOR = 'PRODUCTION_COORDINATOR', 'Production Co-Ordinator'
        CLIENT_SERVICING = 'CLIENT_SERVICING', 'Client-Servicing'

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15, validators=[validate_contact_number])
    department = models.CharField(max_length=30, choices=Department.choices)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'contact', 'department']

    def __str__(self):
        return f'{self.username} ({self.get_department_display()})'

    @property
    def is_admin(self):
        return self.department == self.Department.ADMIN
