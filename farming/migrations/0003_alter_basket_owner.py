# Generated by Django 5.1.3 on 2024-12-28 05:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farming', '0002_product_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL),
        ),
    ]