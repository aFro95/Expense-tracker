# Generated by Django 5.0.6 on 2024-06-19 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0005_alter_expense_user_budgetlimit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="expense",
            name="currency",
            field=models.CharField(max_length=3),
        ),
    ]