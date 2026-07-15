"""
TeamFlow EPMS — Accounts Models.

Implements the custom RBAC authentication system:
- Permission: Granular permission definitions (e.g., "project.create")
- Role: System roles with M2M to Permission via RolePermission
- User: Custom user model with email auth (no Django PermissionsMixin)
- UserProfile: Extended user information (avatar, bio, preferences)

Architecture:
- User extends AbstractBaseUser only (not PermissionsMixin)
- is_staff / is_superuser are manual fields for Django admin access
- All app-level authorization uses Role → Permission M2M
- has_perm() / has_module_perms() are implemented manually for admin compat
"""

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.text import slugify

from core.models import BaseModel, TimeStampedModel

from .managers import UserManager


# ---------------------------------------------------------------------------
# Permission Model
# ---------------------------------------------------------------------------
class Permission(BaseModel):
    """
    A granular permission that can be assigned to roles.

    Permissions use dot-notation codenames (e.g., "project.create") and are
    grouped by category for organizational purposes in the admin UI.
    """

    codename = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text='Dot-notation identifier (e.g., "project.create").',
    )
    name = models.CharField(
        max_length=255,
        help_text='Human-readable name (e.g., "Create Projects").',
    )
    category = models.CharField(
        max_length=50,
        db_index=True,
        help_text='Permission group (e.g., "project", "task", "report").',
    )
    description = models.TextField(
        blank=True,
        help_text="Optional detailed description of what this permission allows.",
    )

    class Meta:
        ordering = ["category", "codename"]
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self) -> str:
        return f"{self.codename} ({self.name})"


# ---------------------------------------------------------------------------
# Role Model
# ---------------------------------------------------------------------------
class Role(BaseModel):
    """
    A system role that groups permissions together.

    Roles are assigned to users and determine what actions they can perform.
    System roles (is_system_role=True) are protected from deletion and
    are seeded via the seed_roles management command.

    The hierarchy_level determines role precedence:
    - 0 = Administrator (highest)
    - 7 = Viewer (lowest)
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        help_text='Display name (e.g., "Project Manager").',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        help_text='URL-safe identifier (e.g., "project_manager"). Auto-generated from name.',
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of this role's responsibilities.",
    )
    is_system_role = models.BooleanField(
        default=False,
        help_text="System roles cannot be deleted. Set True for built-in roles.",
    )
    hierarchy_level = models.IntegerField(
        default=0,
        db_index=True,
        help_text="Role precedence: 0 = highest (Admin), 7 = lowest (Viewer).",
    )
    permissions = models.ManyToManyField(
        Permission,
        through="RolePermission",
        blank=True,
        related_name="roles",
        help_text="Permissions assigned to this role.",
    )

    class Meta:
        ordering = ["hierarchy_level", "name"]
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not set."""
        if not self.slug:
            self.slug = slugify(self.name).replace("-", "_")
        super().save(*args, **kwargs)

    def has_permission(self, codename: str) -> bool:
        """
        Check if this role has a specific permission.

        Args:
            codename: The permission codename to check (e.g., "project.create").

        Returns:
            True if the role has the permission, False otherwise.
        """
        return self.permissions.filter(codename=codename).exists()

    def get_all_permission_codenames(self) -> set[str]:
        """Return all permission codenames assigned to this role."""
        return set(self.permissions.values_list("codename", flat=True))


# ---------------------------------------------------------------------------
# RolePermission (Through Table)
# ---------------------------------------------------------------------------
class RolePermission(TimeStampedModel):
    """
    Through table linking Role ↔ Permission with audit metadata.

    Records which user granted the permission (for audit trail purposes).
    """

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_permissions",
        help_text="The role receiving this permission.",
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name="role_permissions",
        help_text="The permission being granted.",
    )
    granted_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="granted_permissions",
        help_text="The user who granted this permission (audit trail).",
    )

    class Meta:
        unique_together = ("role", "permission")
        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"

    def __str__(self) -> str:
        return f"{self.role.name} → {self.permission.codename}"


# ---------------------------------------------------------------------------
# User Model
# ---------------------------------------------------------------------------
class User(AbstractBaseUser, BaseModel):
    """
    Custom User model using email as the primary identifier.

    Does NOT extend PermissionsMixin. Instead:
    - is_staff / is_superuser are manual BooleanFields for Django admin
    - has_perm() / has_module_perms() are implemented for admin compatibility
    - All app-level authorization uses the Role → Permission M2M system

    This avoids mixing Django's auth.Permission/Group tables with our
    custom RBAC, keeping authorization in one clean system.
    """

    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Primary identifier. Used for login.",
    )
    first_name = models.CharField(
        max_length=150,
        help_text="User's first name.",
    )
    last_name = models.CharField(
        max_length=150,
        help_text="User's last name.",
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Grants access to the Django admin interface.",
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text="Grants all permissions without explicit assignment.",
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Active users can log in. Deactivate instead of deleting.",
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the user account was created.",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text="The user's assigned role (determines permissions).",
    )

    # Django auth configuration
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    # --- Properties ---

    @property
    def full_name(self) -> str:
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def role_name(self) -> str:
        """Return the name of the user's assigned role, or 'Unassigned'."""
        return self.role.name if self.role else "Unassigned"

    # --- Django Admin Compatibility ---
    # These methods are required by Django admin even without PermissionsMixin.

    def has_perm(self, perm: str, obj=None) -> bool:
        """
        Check if the user has a specific permission.

        For Django admin: superusers have all permissions.
        For app-level: delegates to the custom RBAC system.

        Args:
            perm: Permission string. For admin, this is "app_label.codename".
                  For RBAC, this is our custom codename (e.g., "project.create").
            obj: Optional object for object-level permissions (unused).

        Returns:
            True if the user has the permission.
        """
        if self.is_superuser:
            return True
        if not self.is_active:
            return False
        # Check custom RBAC
        if self.role:
            return self.role.has_permission(perm)
        return False

    def has_module_perms(self, app_label: str) -> bool:
        """
        Check if the user has permissions to access a Django admin module.

        Superusers and staff can access admin modules.

        Args:
            app_label: The Django app label (e.g., "accounts").

        Returns:
            True if the user can access the module.
        """
        if self.is_superuser:
            return True
        return self.is_staff

    # --- Custom RBAC Methods ---

    def has_permission(self, codename: str) -> bool:
        """
        Check if the user has a custom RBAC permission.

        Superusers bypass all checks. Users without a role are denied.

        Args:
            codename: Permission codename (e.g., "project.create").

        Returns:
            True if the user has the permission.
        """
        if self.is_superuser:
            return True
        if not self.role:
            return False
        return self.role.has_permission(codename)

    def get_all_permissions(self) -> set[str]:
        """Return all permission codenames the user has via their role."""
        if self.is_superuser:
            return set(Permission.objects.values_list("codename", flat=True))
        if not self.role:
            return set()
        return self.role.get_all_permission_codenames()


# ---------------------------------------------------------------------------
# UserProfile Model
# ---------------------------------------------------------------------------
class UserProfile(BaseModel):
    """
    Extended user profile information.

    Separated from User to keep the auth model lean. Contains optional
    fields like avatar, bio, department, and notification preferences.

    A UserProfile is auto-created when a User is created (via signal).
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="The user this profile belongs to.",
    )
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/",
        blank=True,
        null=True,
        help_text="Profile picture. Uploaded to media/avatars/.",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Phone number (optional).",
    )
    bio = models.TextField(
        blank=True,
        help_text="Short biography or description.",
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        help_text="Department or team name.",
    )
    employee_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        help_text="Employee or student ID (must be unique if provided).",
    )
    timezone = models.CharField(
        max_length=50,
        default="UTC",
        help_text="User's preferred timezone (IANA format, e.g., 'Asia/Kolkata').",
    )
    notification_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON object storing notification channel preferences.",
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self) -> str:
        return f"Profile: {self.user.email}"
