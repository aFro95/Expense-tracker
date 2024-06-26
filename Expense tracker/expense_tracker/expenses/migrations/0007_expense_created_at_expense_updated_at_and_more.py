# Generated by Django 5.0.6 on 2024-06-20 20:12

import django.utils.timezone
import expenses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0006_alter_category_name_alter_expense_currency"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="expense",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="expense",
            name="currency",
            field=models.CharField(
                max_length=3, validators=[expenses.models.validate_currency]
            ),
        ),
    ]
