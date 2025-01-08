# Generated by Django 5.1.3 on 2025-01-07 14:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farming', '0004_alter_order_estimated_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]