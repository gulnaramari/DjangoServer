from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        permission_can_unpublish = Permission.objects.get(codename="can_unpublish_product")
        permission_delete_product = Permission.objects.get(codename="delete_product")

        group.permissions.add(permission_can_unpublish)
        group.permissions.add(permission_delete_product)

        self.stdout.write(self.style.SUCCESS("Группа успешно создана и настроена."))
