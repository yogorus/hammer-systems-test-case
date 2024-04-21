# Generated by Django 5.0.4 on 2024-04-21 17:11

import api.utils
import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('code', models.CharField(default=api.utils.generate_unique_code, max_length=6, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('is_activated', models.BooleanField()),
                ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invited_users', to='api.referral')),
            ],
        ),
        migrations.AddField(
            model_name='referral',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='referral', to='api.user'),
        ),
    ]