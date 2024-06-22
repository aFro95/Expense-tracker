from django import forms
from .models import Expense, Category, BudgetLimit

class ExpenseForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'text', 'class': 'form-control', 'id': 'datepicker', 'autocomplete': 'off'}),
        input_formats=['%d-%m-%Y']
    )
    currency = forms.ChoiceField(
        choices=[('RON', 'RON'), ('EUR', 'EUR'), ('USD', 'USD')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date', 'currency', 'category']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ImportFileForm(forms.Form):
    file = forms.FileField()

class BudgetLimitForm(forms.ModelForm):
    class Meta:
        model = BudgetLimit
        fields = ['category', 'limit']