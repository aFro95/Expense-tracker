import pandas as pd
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Sum
from django.urls import reverse
from django.http import HttpResponse
from .models import Expense, Category, BudgetLimit
from .forms import ExpenseForm, BudgetLimitForm, CategoryForm
from collections import defaultdict
from datetime import datetime


@login_required
def index(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]
    
    total_expenses_by_category = defaultdict(lambda: {'amount': 0, 'limit': None, 'currency': 'RON'})
    for expense in Expense.objects.filter(user=request.user):
        category_name = expense.category.name if expense.category else 'Uncategorized'
        total_expenses_by_category[category_name]['amount'] += expense.amount
        total_expenses_by_category[category_name]['currency'] = expense.currency

    for budget in BudgetLimit.objects.filter(user=request.user):
        category_name = budget.category.name
        if category_name in total_expenses_by_category:
            total_expenses_by_category[category_name]['limit'] = budget.limit

    context = {
        'expenses': expenses,
        'total_expenses_by_category': dict(total_expenses_by_category),
    }

    return render(request, 'expenses/index.html', context)


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('index')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def set_budget_limit(request):
    if request.method == 'POST':
        form = BudgetLimitForm(request.POST)
        if form.is_valid():
            budget_limit = form.save(commit=False)
            budget_limit.user = request.user
            budget_limit.save()
            messages.success(request, "Budget limit set successfully!")
            return redirect('index')
    else:
        form = BudgetLimitForm()
    return render(request, 'expenses/set_budget_limit.html', {'form': form})

@login_required
def all_expenses(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category', 'all')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    sort_by = request.GET.get('sort_by', 'date_desc')

    expenses = Expense.objects.filter(user=request.user)

    if selected_category != 'all':
        expenses = expenses.filter(category_id=selected_category)
    
    if from_date:
        expenses = expenses.filter(date__gte=datetime.strptime(from_date, '%d-%m-%Y'))
    
    if to_date:
        expenses = expenses.filter(date__lte=datetime.strptime(to_date, '%d-%m-%Y'))
    
    if sort_by == 'date_asc':
        expenses = expenses.order_by('date')
    elif sort_by == 'date_desc':
        expenses = expenses.order_by('-date')
    elif sort_by == 'amount_asc':
        expenses = expenses.order_by('amount')
    elif sort_by == 'amount_desc':
        expenses = expenses.order_by('-amount')
    
    return render(request, 'expenses/all_expenses.html', {
        'categories': categories,
        'expenses': expenses,
        'selected_category': selected_category,
        'from_date': from_date,
        'to_date': to_date,
        'sort_by': sort_by
    })

@login_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'expenses/manage_categories.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'expenses/add_category.html', {'form': form})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('manage_categories')
    return render(request, 'expenses/delete_category.html', {'category': category})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    return render(request, 'expenses/delete_expense.html', {'expense': expense})

@login_required
def export_expenses(request, file_format):
    expenses = Expense.objects.filter(user=request.user)
    df = pd.DataFrame(list(expenses.values('description', 'amount', 'date', 'currency', 'category__name')))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="expenses.xlsx"'
    df.to_excel(response, index=False)
    return response

@login_required
def import_expenses(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            data = pd.read_excel(file, engine='openpyxl')
        else:
            return render(request, 'expenses/all_expenses.html', {'error': 'File format not supported'})

        for _, row in data.iterrows():
            category, _ = Category.objects.get_or_create(name=row['Category'])
            Expense.objects.create(
                user=request.user,
                description=row['Description'],
                amount=row['Amount'],
                date=row['Date'],
                currency=row['Currency'],
                category=category
            )
        return redirect(reverse('all_expenses'))
    return render(request, 'expenses/all_expenses.html')

@login_required
def report(request):
    expenses_by_category = Expense.objects.filter(user=request.user).values('category__name').annotate(total_amount=Sum('amount'))
    categories = [expense['category__name'] for expense in expenses_by_category]
    amounts = [float(expense['total_amount']) for expense in expenses_by_category]
    return render(request, 'expenses/report.html', {
        'categories': json.dumps(categories),
        'amounts': json.dumps(amounts),
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def delete_all_expenses(request):
    if request.method == 'POST':
        Expense.objects.filter(user=request.user).delete()
        return redirect('index')
