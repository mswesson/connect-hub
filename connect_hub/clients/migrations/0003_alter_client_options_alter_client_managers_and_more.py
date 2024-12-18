# Generated by Django 5.1.3 on 2024-11-30 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_client_groups_alter_client_user_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={},
        ),
        migrations.AlterModelManagers(
            name='client',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='client',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='client',
            name='email',
        ),
        migrations.RemoveField(
            model_name='client',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='client',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='client',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='client',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='client',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='client',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='password',
        ),
        migrations.RemoveField(
            model_name='client',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='client',
            name='username',
        ),
    ]
