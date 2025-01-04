# students/management/commands/setup_permissions.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from account.models import Student  # Adjust the import based on your model location

class Command(BaseCommand):
    help = 'Set up user groups and permissions'

    def handle(self, *args, **kwargs):
        # Create user groups
        groups = ['Principal', 'Vice Principal', 'Supervisor', 'Regional Admin', 'Woreda Admin']
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created'))

        # Get the content type for the Student model
        student_content_type = ContentType.objects.get_for_model(Student)

        # Define permissions
        permissions = [
            ('can_add_student', 'Can add student'),
            ('can_change_student', 'Can change student'),
            ('can_delete_student', 'Can delete student'),
            ('can_view_student', 'Can view student'),
        ]

        for codename, name in permissions:
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=student_content_type  # Correct way to set content type
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Permission "{name}" created'))

        principal_group = Group.objects.get(name='Principal')
        vice_principal_group = Group.objects.get(name='Vice Principal')
        supervisor_group = Group.objects.get(name='Supervisor')
        regional_admin_group = Group.objects.get(name='Regional Admin')
        woreda_admin_group = Group.objects.get(name='Woreda Admin')

        for perm in permissions:
            permission = Permission.objects.get(codename=perm[0])
            principal_group.permissions.add(permission)
            vice_principal_group.permissions.add(permission)
            supervisor_group.permissions.add(permission)
            regional_admin_group.permissions.add(permission)
            woreda_admin_group.permissions.add(permission)
            
        view_permission = Permission.objects.get(codename='can_view_student')
        supervisor_group.permissions.add(view_permission)
        regional_admin_group.permissions.add(view_permission)
        woreda_admin_group.permissions.add(view_permission)

        self.stdout.write(self.style.SUCCESS('Permissions setup completed'))