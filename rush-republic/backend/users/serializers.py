import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for returning user/profile data to the client."""

    department_display = serializers.CharField(source='get_department_display', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'contact',
            'department', 'department_display',
            'created_at', 'updated_at',
        ]
        read_only_fields = fields


class SignupSerializer(serializers.ModelSerializer):
    """Handles new employee registration with full validation."""

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'contact', 'password',
            'confirm_password', 'department',
        ]

    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate_contact(self, value):
        if not re.match(r'^\+?\d{10,15}$', value):
            raise serializers.ValidationError(
                'Enter a valid contact number (10-15 digits, optional leading +).'
            )
        return value

    def validate_password(self, value):
        # Enforces: 8+ chars, one upper, one lower, one digit, one special char.
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', value):
            raise serializers.ValidationError('Password must contain at least one number.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-\[\];\'\\/`~+=]', value):
            raise serializers.ValidationError('Password must contain at least one special character.')
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password': "Passwords don't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Login serializer using email + password instead of username + password,
    and embeds department/user info directly in the JWT + response payload.
    """

    username_field = CustomUser.USERNAME_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['department'] = user.department
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
