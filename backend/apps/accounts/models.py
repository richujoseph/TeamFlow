from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.text import slugify
from core.models import BaseModel, TimeStampedModel
from .managers import UserManager


class Permission(BaseModel):
    codename = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text='Dot-notation identifier (e.g., "project.create").',
    )
    name = models.CharField(
        max_length=255, help_text='Human-readable name (e.g., "Create Projects").'
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


class Role(BaseModel):
    name = models.CharField(
        max_length=50, unique=True, help_text='Display name (e.g., "Project Manager").'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        help_text='URL-safe identifier (e.g., "project_manager"). Auto-generated from name.',
    )
    description = models.TextField(
        blank=True, help_text="Detailed description of this role's responsibilities."
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
        if not self.slug:
            self.slug = slugify(self.name).replace("-", "_")
        super().save(*args, **kwargs)

    def has_permission(self, codename: str) -> bool:
        return self.permissions.filter(codename=codename).exists()

    def get_all_permission_codenames(self) -> set[str]:
        return set(self.permissions.values_list("codename", flat=True))


class RolePermission(TimeStampedModel):
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


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Primary identifier. Used for login.",
    )
    first_name = models.CharField(max_length=150, help_text="User's first name.")
    last_name = models.CharField(max_length=150, help_text="User's last name.")
    is_staff = models.BooleanField(
        default=False, help_text="Grants access to the Django admin interface."
    )
    is_superuser = models.BooleanField(
        default=False, help_text="Grants all permissions without explicit assignment."
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Active users can log in. Deactivate instead of deleting.",
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the user account was created."
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text="The user's assigned role (determines permissions).",
    )
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def role_name(self) -> str:
        return self.role.name if self.role else "Unassigned"

    def has_perm(self, perm: str, obj=None) -> bool:
        if self.is_superuser:
            return True
        if not self.is_active:
            return False
        if self.role:
            return self.role.has_permission(perm)
        return False

    def has_module_perms(self, app_label: str) -> bool:
        if self.is_superuser:
            return True
        return self.is_staff

    def has_permission(self, codename: str) -> bool:
        if self.is_superuser:
            return True
        if not self.role:
            return False
        return self.role.has_permission(codename)

    def get_all_permissions(self) -> set[str]:
        if self.is_superuser:
            return set(Permission.objects.values_list("codename", flat=True))
        if not self.role:
            return set()
        return self.role.get_all_permission_codenames()


class UserProfile(BaseModel):
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
        max_length=20, blank=True, help_text="Phone number (optional)."
    )
    bio = models.TextField(blank=True, help_text="Short biography or description.")
    department = models.CharField(
        max_length=100, blank=True, help_text="Department or team name."
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
