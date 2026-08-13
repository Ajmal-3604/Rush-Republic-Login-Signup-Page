from rest_framework.permissions import BasePermission

from .models import CustomUser


class IsAdmin(BasePermission):
    """Allows access only to users in the Admin department."""

    message = 'Only Admin department users can access this resource.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.department == CustomUser.Department.ADMIN
        )


class IsSocialMedia(BasePermission):
    """Allows access to Social Media users (Admin also has full access)."""

    message = 'Only Social Media department users can access this resource.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.department in (
                CustomUser.Department.SOCIAL_MEDIA,
                CustomUser.Department.ADMIN,
            )
        )


class IsProductionCoordinator(BasePermission):
    """Allows access to Production Co-Ordinator users (Admin also has full access)."""

    message = 'Only Production Co-Ordinator department users can access this resource.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.department in (
                CustomUser.Department.PRODUCTION_COORDINATOR,
                CustomUser.Department.ADMIN,
            )
        )


class IsClientServicing(BasePermission):
    """Allows access to Client-Servicing users (Admin also has full access)."""

    message = 'Only Client-Servicing department users can access this resource.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.department in (
                CustomUser.Department.CLIENT_SERVICING,
                CustomUser.Department.ADMIN,
            )
        )
