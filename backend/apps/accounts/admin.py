from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Permission, Role, RolePermission, User, UserProfile


class UserProfileInline(admin.StackedInline):
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


class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1
    autocomplete_fields = ["permission"]
    readonly_fields = ["granted_by"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
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
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Role & Permissions",
            {"fields": ("role", "is_active", "is_staff", "is_superuser")},
        ),
    )
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
    filter_horizontal = ()


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
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
        return obj.permissions.count()

    @admin.display(description="Users")
    def user_count(self, obj: Role) -> int:
        return obj.users.count()


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("codename", "name", "category")
    list_filter = ("category",)
    search_fields = ("codename", "name")
    ordering = ("category", "codename")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "employee_id", "timezone")
    list_filter = ("timezone",)
    search_fields = ("user__email", "employee_id", "department")
    readonly_fields = ("user",)
