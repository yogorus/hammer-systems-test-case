# Generated by Django 5.0.4 on 2024-04-21 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='invited_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='invited_users', to='api.referral'),
        ),
    ]
