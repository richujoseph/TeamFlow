"""
TeamFlow EPMS — Accounts Admin Configuration.

Registers User, Role, Permission, and UserProfile with the Django admin
interface using custom fieldsets and display configurations.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Permission, Role, RolePermission, User, UserProfile


# ---------------------------------------------------------------------------
# Inline: UserProfile shown on User edit page
# ---------------------------------------------------------------------------
class UserProfileInline(admin.StackedInline):
    """Display UserProfile fields inline on the User admin page."""

    model = UserProfile
    can_delete = False
    verbose_name = "Profile"
    verbose_name_plural = "Profile"
    fields = (
        "avatar",
        "phone",
        "bio",
        "department",
        "employee_id",
        "timezone",
        "notification_preferences",
    )


# ---------------------------------------------------------------------------
# Inline: RolePermission shown on Role edit page
# ---------------------------------------------------------------------------
class RolePermissionInline(admin.TabularInline):
    """Display assigned permissions inline on the Role admin page."""

    model = RolePermission
    extra = 1
    autocomplete_fields = ["permission"]
    readonly_fields = ["granted_by"]


# ---------------------------------------------------------------------------
# User Admin
# ---------------------------------------------------------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin configured for email-based authentication.

    Replaces the default username-based fieldsets with email-based ones.
    Shows UserProfile inline for convenient editing.
    """

    inlines = [UserProfileInline]

    # List display
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "role")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)

    # Edit form fieldsets
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Role & Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
    )

    # Add form fieldsets (creating a new user)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    # Remove filter_horizontal since we don't use Django's groups/permissions
    filter_horizontal = ()


# ---------------------------------------------------------------------------
# Role Admin
# ---------------------------------------------------------------------------
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin configuration for Role management."""

    inlines = [RolePermissionInline]

    list_display = (
        "name",
        "slug",
        "hierarchy_level",
        "is_system_role",
        "permission_count",
        "user_count",
    )
    list_filter = ("is_system_role", "hierarchy_level")
    search_fields = ("name", "slug")
    readonly_fields = ("slug",)
    ordering = ("hierarchy_level",)

    @admin.display(description="Permissions")
    def permission_count(self, obj: Role) -> int:
        """Show the number of permissions assigned to this role."""
        return obj.permissions.count()

    @admin.display(description="Users")
    def user_count(self, obj: Role) -> int:
        """Show the number of users assigned to this role."""
        return obj.users.count()


# ---------------------------------------------------------------------------
# Permission Admin
# ---------------------------------------------------------------------------
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Admin configuration for Permission management."""

    list_display = ("codename", "name", "category")
    list_filter = ("category",)
    search_fields = ("codename", "name")
    ordering = ("category", "codename")


# ---------------------------------------------------------------------------
# UserProfile Admin (standalone access)
# ---------------------------------------------------------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Standalone admin for UserProfile (also available inline on User)."""

    list_display = ("user", "department", "employee_id", "timezone")
    list_filter = ("timezone",)
    search_fields = ("user__email", "employee_id", "department")
    readonly_fields = ("user",)
