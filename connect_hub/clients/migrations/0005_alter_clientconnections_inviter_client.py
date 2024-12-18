# Generated by Django 5.1.3 on 2024-12-02 01:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_clientconnections_invited_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientconnections',
            name='inviter_client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections_invited_clients', to='clients.client'),
        ),
    ]
