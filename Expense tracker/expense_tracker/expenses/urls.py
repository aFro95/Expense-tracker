from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_expense, name='add_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('all/', views.all_expenses, name='all_expenses'),
    path('signup/', views.signup, name='signup'),
    path('report/', views.report, name='report'),
    path('add_category/', views.add_category, name='add_category'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('export/<str:file_format>/', views.export_expenses, name='export_expenses'),
    path('import/', views.import_expenses, name='import_expenses'),
    path('set_budget_limit/', views.set_budget_limit, name='set_budget_limit'),
    path('delete_all_expenses/', views.delete_all_expenses, name='delete_all_expenses'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
