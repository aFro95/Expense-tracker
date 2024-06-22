from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from forex_python.converter import CurrencyRates

def validate_currency(value):
    valid_currencies = ['RON', 'EUR', 'USD', 'GBP']
    if value not in valid_currencies:
        raise ValidationError(
            _('%(value)s is not a valid currency'),
            params={'value': value},
        )

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_base = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True, blank=True)
    date = models.DateField()
    currency = models.CharField(max_length=3, validators=[validate_currency])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.currency != 'RON':
            c = CurrencyRates()
            self.amount_base = c.convert(self.currency, 'RON', self.amount)
        else:
            self.amount_base = self.amount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.description} - {self.amount} {self.currency}"

class BudgetLimit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.category.name}: {self.limit}"