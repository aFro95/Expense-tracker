import csv
from datetime import datetime
from django.contrib.auth.models import User
from expenses.models import Expense, Category

def run():
    default_user = User.objects.get(username='ge0')

    with open('expenses_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category, created = Category.objects.get_or_create(name=row['Category'])
            date = datetime.strptime(row['Date'], '%Y-%m-%d')
            Expense.objects.create(
                description=row['Description'],
                amount=row['Amount'],
                date=date,
                currency=row['Currency'],
                category=category,
                user=default_user
            )
