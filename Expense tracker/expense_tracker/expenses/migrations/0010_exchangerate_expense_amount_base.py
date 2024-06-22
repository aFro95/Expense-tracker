# Generated by Django 5.0.6 on 2024-06-21 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0009_alter_expense_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExchangeRate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("base_currency", models.CharField(max_length=3)),
                ("target_currency", models.CharField(max_length=3)),
                ("rate", models.DecimalField(decimal_places=4, max_digits=10)),
                ("date", models.DateField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name="expense",
            name="amount_base",
            field=models.DecimalField(
                blank=True, decimal_places=2, editable=False, max_digits=10, null=True
            ),
        ),
    ]
