import logging
from django.core.management.base import BaseCommand
from apps.accounts.constants import (
    DEFAULT_PERMISSIONS,
    PERMISSION_DEFINITIONS,
    SYSTEM_ROLES,
)
from apps.accounts.models import Permission, Role, RolePermission

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seeds the database with system roles and their default permissions."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Seeding TeamFlow RBAC data...\n"))
        self._seed_permissions()
        self._seed_roles()
        self._assign_default_permissions()
        self.stdout.write(self.style.SUCCESS("\n✓ RBAC seeding complete."))

    def _seed_permissions(self):
        self.stdout.write("  Creating permissions...")
        created_count = 0
        skipped_count = 0
        for perm_def in PERMISSION_DEFINITIONS:
            _, created = Permission.objects.get_or_create(
                codename=perm_def["codename"],
                defaults={"name": perm_def["name"], "category": perm_def["category"]},
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1
        self.stdout.write(
            f"    Permissions: {created_count} created, {skipped_count} already existed."
        )

    def _seed_roles(self):
        self.stdout.write("  Creating roles...")
        created_count = 0
        skipped_count = 0
        for slug, role_data in SYSTEM_ROLES.items():
            _, created = Role.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": role_data["name"],
                    "description": role_data["description"],
                    "hierarchy_level": role_data["hierarchy_level"],
                    "is_system_role": True,
                },
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1
        self.stdout.write(
            f"    Roles: {created_count} created, {skipped_count} already existed."
        )

    def _assign_default_permissions(self):
        self.stdout.write("  Assigning default permissions...")
        assigned_count = 0
        skipped_count = 0
        for role_slug, permission_codenames in DEFAULT_PERMISSIONS.items():
            try:
                role = Role.objects.get(slug=role_slug)
            except Role.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"    ⚠ Role '{role_slug}' not found, skipping.")
                )
                continue
            for codename in permission_codenames:
                try:
                    permission = Permission.objects.get(codename=codename)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"    ⚠ Permission '{codename}' not found, skipping."
                        )
                    )
                    continue
                _, created = RolePermission.objects.get_or_create(
                    role=role, permission=permission
                )
                if created:
                    assigned_count += 1
                else:
                    skipped_count += 1
        self.stdout.write(
            f"    Assignments: {assigned_count} created, {skipped_count} already existed."
        )
