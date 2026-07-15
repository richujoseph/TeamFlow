"""
TeamFlow EPMS — Custom User Manager.

Provides email-based user creation methods. Django requires a custom
manager when using a custom User model with a non-default USERNAME_FIELD.
"""

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.

    Uses email as the unique identifier instead of username.
    """

    def create_user(
        self,
        email: str,
        password: str | None = None,
        first_name: str = "",
        last_name: str = "",
        **extra_fields,
    ):
        """
        Create and return a regular user with the given email and password.

        Args:
            email: The user's email address (will be normalized).
            password: The user's password (will be hashed).
            first_name: The user's first name.
            last_name: The user's last name.
            **extra_fields: Additional fields to set on the User model.

        Returns:
            The created User instance.

        Raises:
            ValueError: If email is not provided.
        """
        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        first_name: str = "",
        last_name: str = "",
        **extra_fields,
    ):
        """
        Create and return a superuser with full admin privileges.

        Superusers have is_staff=True and is_superuser=True, granting
        access to Django admin and bypassing all custom RBAC checks.

        Args:
            email: The superuser's email address.
            password: The superuser's password.
            first_name: The superuser's first name.
            last_name: The superuser's last name.
            **extra_fields: Additional fields.

        Returns:
            The created superuser User instance.

        Raises:
            ValueError: If is_staff or is_superuser is not True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
